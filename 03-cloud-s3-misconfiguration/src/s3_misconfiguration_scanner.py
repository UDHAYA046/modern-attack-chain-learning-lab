import csv
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table


console = Console()


SENSITIVE_FILE_PATTERNS = [
    ".env",
    ".pem",
    ".sql",
    ".zip",
    ".csv",
    "password",
    "secret",
    "credential",
    "config"
]


def calculate_severity(score):
    if score <= 4:
        return "Low"
    if score <= 9:
        return "Medium"
    if score <= 19:
        return "High"
    return "Critical"


def detect_sensitive_files(objects):
    sensitive_files = []

    for obj in objects:
        lower_obj = obj.lower()

        for pattern in SENSITIVE_FILE_PATTERNS:
            if pattern in lower_obj:
                sensitive_files.append(obj)
                break

    return sensitive_files


def analyze_bucket(bucket):
    bucket_name = bucket.get("bucket_name", "Unknown Bucket")

    risk_score = 0
    findings = []
    recommendations = []
    dry_run_actions = []

    if bucket.get("public_acl", False):
        risk_score += 10
        findings.append("Public ACL detected.")
        recommendations.append("Enable S3 Block Public Access and remove public ACL grants.")
        dry_run_actions.append("Would remove public ACL permissions and enable Block Public Access.")

    if bucket.get("public_bucket_policy", False):
        risk_score += 10
        findings.append("Public bucket policy detected.")
        recommendations.append("Restrict bucket policy Principal from '*' to trusted identities only.")
        dry_run_actions.append("Would update bucket policy to remove public Principal access.")

    if not bucket.get("bucket_policy_exists", False):
        risk_score += 5
        findings.append("Missing bucket policy.")
        recommendations.append("Create a least-privilege bucket policy.")
        dry_run_actions.append("Would create a least-privilege bucket policy template.")

    if not bucket.get("encryption_enabled", False):
        risk_score += 8
        findings.append("Server-side encryption is not enabled.")
        recommendations.append("Enable SSE-S3 or SSE-KMS encryption.")
        dry_run_actions.append("Would enable AES256 server-side encryption.")

    if not bucket.get("versioning_enabled", False):
        risk_score += 4
        findings.append("Versioning is disabled.")
        recommendations.append("Enable bucket versioning to protect against deletion and ransomware.")
        dry_run_actions.append("Would enable bucket versioning.")

    if bucket.get("website_hosting", False):
        risk_score += 3
        findings.append("Static website hosting is enabled.")
        recommendations.append("Review hosted objects and ensure no sensitive files are publicly accessible.")
        dry_run_actions.append("Would review website hosting configuration.")

    sensitive_files = detect_sensitive_files(bucket.get("objects", []))

    if sensitive_files:
        risk_score += 12
        findings.append(f"Sensitive files detected: {', '.join(sensitive_files)}")
        recommendations.append("Remove, encrypt, or restrict access to sensitive files immediately.")
        dry_run_actions.append("Would quarantine or restrict access to sensitive files.")

    if not findings:
        findings.append("No major S3 misconfiguration detected.")
        recommendations.append("Continue monitoring bucket configuration.")

    return {
        "bucket_name": bucket_name,
        "risk_score": risk_score,
        "severity": calculate_severity(risk_score),
        "public_acl": bucket.get("public_acl", False),
        "public_bucket_policy": bucket.get("public_bucket_policy", False),
        "bucket_policy_exists": bucket.get("bucket_policy_exists", False),
        "encryption_enabled": bucket.get("encryption_enabled", False),
        "versioning_enabled": bucket.get("versioning_enabled", False),
        "website_hosting": bucket.get("website_hosting", False),
        "sensitive_files": sensitive_files,
        "findings": findings,
        "recommendations": recommendations,
        "dry_run_actions": dry_run_actions
    }


def write_json_report(report, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)


def write_csv_summary(report, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Bucket Name",
            "Risk Score",
            "Severity",
            "Public ACL",
            "Public Policy",
            "Encryption",
            "Versioning",
            "Website Hosting",
            "Sensitive Files",
            "Findings"
        ])

        for item in report:
            writer.writerow([
                item["bucket_name"],
                item["risk_score"],
                item["severity"],
                item["public_acl"],
                item["public_bucket_policy"],
                item["encryption_enabled"],
                item["versioning_enabled"],
                item["website_hosting"],
                ", ".join(item["sensitive_files"]),
                " | ".join(item["findings"])
            ])


def write_html_dashboard(report, output_file):
    rows = ""

    for item in report:
        rows += f"""
        <tr>
            <td>{item["bucket_name"]}</td>
            <td>{item["risk_score"]}</td>
            <td>{item["severity"]}</td>
            <td>{str(item["public_acl"])}</td>
            <td>{str(item["public_bucket_policy"])}</td>
            <td>{str(item["encryption_enabled"])}</td>
            <td>{str(item["versioning_enabled"])}</td>
            <td>{str(item["website_hosting"])}</td>
            <td>{"<br>".join(item["sensitive_files"]) or "None"}</td>
            <td>{"<br>".join(item["findings"])}</td>
            <td>{"<br>".join(item["recommendations"])}</td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>S3 Misconfiguration Security Dashboard</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f7f9fc;
        }}
        h1 {{
            color: #111827;
        }}
        p {{
            font-size: 16px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            background-color: white;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
            vertical-align: top;
        }}
        th {{
            background-color: #111827;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>
    <h1>S3 Bucket Misconfiguration Security Dashboard</h1>
    <p>This dashboard analyzes simulated S3 bucket configurations for public access, missing encryption, disabled versioning, website hosting exposure, and sensitive file risks.</p>

    <table>
        <tr>
            <th>Bucket</th>
            <th>Risk Score</th>
            <th>Severity</th>
            <th>Public ACL</th>
            <th>Public Policy</th>
            <th>Encryption</th>
            <th>Versioning</th>
            <th>Website</th>
            <th>Sensitive Files</th>
            <th>Findings</th>
            <th>Recommendations</th>
        </tr>
        {rows}
    </table>
</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html)


def print_cli_table(report):
    table = Table(title="S3 Misconfiguration Scanner Results")

    table.add_column("Bucket", style="cyan")
    table.add_column("Score", justify="right")
    table.add_column("Severity")
    table.add_column("Findings")

    for item in report:
        table.add_row(
            item["bucket_name"],
            str(item["risk_score"]),
            item["severity"],
            "\n".join(item["findings"])
        )

    console.print(table)


def print_dry_run_actions(report):
    console.print("\n[bold yellow]Dry Run Remediation Actions[/bold yellow]\n")

    for item in report:
        console.print(f"[bold]Bucket:[/bold] {item['bucket_name']}")

        for action in item["dry_run_actions"]:
            console.print(f"  - {action}")

        console.print("")


def main():
    base_dir = Path(__file__).resolve().parent.parent
    input_file = base_dir / "sample-data" / "s3_buckets.json"
    report_dir = base_dir / "reports"

    report_dir.mkdir(exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as file:
        buckets = json.load(file)

    report = [analyze_bucket(bucket) for bucket in buckets]

    write_json_report(report, report_dir / "s3_misconfiguration_report.json")
    write_csv_summary(report, report_dir / "s3_risk_summary.csv")
    write_html_dashboard(report, report_dir / "s3_security_dashboard.html")

    print_cli_table(report)
    print_dry_run_actions(report)

    console.print("[bold green]S3 Misconfiguration Scan Complete[/bold green]")
    console.print(f"JSON report generated: {report_dir / 's3_misconfiguration_report.json'}")
    console.print(f"CSV summary generated: {report_dir / 's3_risk_summary.csv'}")
    console.print(f"HTML dashboard generated: {report_dir / 's3_security_dashboard.html'}")


if __name__ == "__main__":
    main()