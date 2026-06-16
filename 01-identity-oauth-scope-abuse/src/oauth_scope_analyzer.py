import csv
import json
from pathlib import Path


SCOPE_RISK_SCORES = {
    "email": 1,
    "profile": 1,
    "calendar.read": 3,
    "contacts.read": 3,
    "mail.read": 5,
    "files.read": 5,
    "offline_access": 6,
    "mail.readwrite": 8,
    "files.readwrite": 8
}


DANGEROUS_SCOPES = {
    "mail.read",
    "mail.readwrite",
    "contacts.read",
    "files.read",
    "files.readwrite",
    "offline_access"
}


DANGEROUS_COMBINATIONS = [
    {
        "scopes": {"mail.readwrite", "offline_access"},
        "reason": "Application has email write access combined with persistent offline access.",
        "extra_score": 6
    },
    {
        "scopes": {"contacts.read", "offline_access"},
        "reason": "Application can read contacts and maintain long-term access.",
        "extra_score": 4
    },
    {
        "scopes": {"files.readwrite", "offline_access"},
        "reason": "Application has file write access combined with persistent offline access.",
        "extra_score": 6
    }
]


RECOMMENDATIONS = {
    "mail.read": "Review whether email read access is required.",
    "mail.readwrite": "Replace mail.readwrite with least-privilege read-only access or revoke it.",
    "contacts.read": "Limit contact access unless strictly required.",
    "files.read": "Review file access permissions.",
    "files.readwrite": "Avoid write access to files unless absolutely necessary.",
    "offline_access": "Remove offline_access unless long-term access is required."
}


def calculate_risk_level(score):
    if score <= 2:
        return "Low"
    if score <= 6:
        return "Medium"
    if score <= 12:
        return "High"
    return "Critical"


def analyze_scope_combinations(scopes):
    scope_set = set(scopes)
    findings = []
    extra_score = 0

    for combo in DANGEROUS_COMBINATIONS:
        if combo["scopes"].issubset(scope_set):
            findings.append(combo["reason"])
            extra_score += combo["extra_score"]

    return findings, extra_score


def analyze_application(app):
    scopes = app.get("scopes", [])

    base_score = sum(SCOPE_RISK_SCORES.get(scope, 0) for scope in scopes)
    dangerous_scopes = [scope for scope in scopes if scope in DANGEROUS_SCOPES]

    combo_findings, combo_score = analyze_scope_combinations(scopes)

    expiry = app.get("token_expiry", "").lower()
    expiry_score = 0
    expiry_finding = None

    if expiry == "long-lived":
        expiry_score = 3
        expiry_finding = "Application uses long-lived tokens, increasing risk if tokens are stolen."

    total_score = base_score + combo_score + expiry_score

    recommendations = [
        RECOMMENDATIONS[scope]
        for scope in dangerous_scopes
        if scope in RECOMMENDATIONS
    ]

    if combo_findings:
        recommendations.append("Review dangerous scope combinations and apply least privilege.")

    if expiry_finding:
        recommendations.append("Use short-lived access tokens and token rotation.")

    findings = []

    if dangerous_scopes:
        findings.append(f"Dangerous scopes detected: {', '.join(dangerous_scopes)}")

    findings.extend(combo_findings)

    if expiry_finding:
        findings.append(expiry_finding)

    return {
        "app_name": app.get("app_name", "Unknown Application"),
        "redirect_uri": app.get("redirect_uri", "Not Provided"),
        "scopes": scopes,
        "risk_score": total_score,
        "risk_level": calculate_risk_level(total_score),
        "dangerous_scopes": dangerous_scopes,
        "findings": findings,
        "recommendations": recommendations
    }


def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json_report(report, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)


def write_csv_summary(report, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Application Name",
            "Risk Score",
            "Risk Level",
            "Dangerous Scopes",
            "Findings"
        ])

        for item in report:
            writer.writerow([
                item["app_name"],
                item["risk_score"],
                item["risk_level"],
                ", ".join(item["dangerous_scopes"]),
                " | ".join(item["findings"])
            ])


def write_html_dashboard(report, output_file):
    rows = ""

    for item in report:
        rows += f"""
        <tr>
            <td>{item["app_name"]}</td>
            <td>{item["risk_score"]}</td>
            <td>{item["risk_level"]}</td>
            <td>{", ".join(item["dangerous_scopes"]) or "None"}</td>
            <td>{"<br>".join(item["findings"]) or "No major findings"}</td>
            <td>{"<br>".join(item["recommendations"]) or "No action required"}</td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>OAuth Risk Dashboard</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f7f9fc;
        }}
        h1 {{
            color: #1f2937;
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
    <h1>OAuth Scope Abuse Risk Dashboard</h1>
    <p>This report analyzes simulated OAuth-connected applications for risky scopes, dangerous scope combinations, and long-lived token exposure.</p>

    <table>
        <tr>
            <th>Application</th>
            <th>Risk Score</th>
            <th>Risk Level</th>
            <th>Dangerous Scopes</th>
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


def main():
    base_dir = Path(__file__).resolve().parent.parent
    sample_dir = base_dir / "sample-data"
    report_dir = base_dir / "reports"

    report_dir.mkdir(exist_ok=True)

    apps = load_json_file(sample_dir / "oauth_apps.json")

    good_app = load_json_file(sample_dir / "good_app.json")
    evil_app = load_json_file(sample_dir / "evil_app.json")

    apps.extend([good_app, evil_app])

    report = [analyze_application(app) for app in apps]

    write_json_report(report, report_dir / "oauth_risk_report.json")
    write_csv_summary(report, report_dir / "risk_summary.csv")
    write_html_dashboard(report, report_dir / "oauth_risk_dashboard.html")

    print("OAuth Security Analyzer Complete")
    print(f"JSON report generated: {report_dir / 'oauth_risk_report.json'}")
    print(f"CSV summary generated: {report_dir / 'risk_summary.csv'}")
    print(f"HTML dashboard generated: {report_dir / 'oauth_risk_dashboard.html'}")


if __name__ == "__main__":
    main()