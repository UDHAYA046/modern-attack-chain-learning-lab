import csv
import json
import math
from collections import Counter
from pathlib import Path

SUSPICIOUS_KEYWORDS = {
    "attacker",
    "exfil",
    "secret",
    "chunk",
    "payload",
    "malware",
    "command"
}

KNOWN_LEGITIMATE_DOMAINS = {
    "google.com",
    "mail.google.com",
    "cloudfront.net",
    "ec2-54-100.compute.amazonaws.com"
}

#shanon enthorpy
def calculate_entropy(text):
    probabilities = [n / len(text) for n in Counter(text).values()]
    return -sum(p * math.log2(p) for p in probabilities)

#query length
def query_length(domain):
    return len(domain)

#subdomain depth
def subdomain_depth(domain):
    return max(0, len(domain.split(".")) - 2)

#risk level
def risk_level(score):

    if score <= 4:
        return "Low"

    elif score <= 8:
        return "Medium"

    elif score <= 12:
        return "High"

    else:
        return "Critical"


def analyze_domain(entry):
    domain = entry["domain"]
    timestamp = entry.get("timestamp", "Not Provided")

    length = query_length(domain)
    entropy = round(calculate_entropy(domain), 2)
    depth = subdomain_depth(domain)

    score = 0
    findings = []
    recommendations = []

    if domain in KNOWN_LEGITIMATE_DOMAINS:
        findings.append("Known legitimate domain or cloud service.")
        recommendations.append("No immediate action required, but monitor if frequency increases.")

    if length > 45:
        score += 4
        findings.append("Unusually long DNS query length.")
        recommendations.append("Review whether the query contains encoded or hidden data.")
    elif length > 30:
        score += 2
        findings.append("Moderately long DNS query.")

    if entropy > 4.2:
        score += 4
        findings.append("High entropy detected, indicating random or encoded data.")
        recommendations.append("Inspect query for encoded payload patterns.")
    elif entropy > 3.5:
        score += 2
        findings.append("Moderate entropy detected.")

    if depth >= 4:
        score += 3
        findings.append("High subdomain depth detected.")
        recommendations.append("Check for DNS tunnelling style chunking.")
    elif depth >= 2:
        score += 2
        findings.append("Moderate subdomain depth detected.")

    matched_keywords = [
        keyword for keyword in SUSPICIOUS_KEYWORDS
        if keyword in domain.lower()
    ]

    if matched_keywords:
        score += 4
        findings.append(f"Suspicious keywords detected: {', '.join(matched_keywords)}")
        recommendations.append("Investigate domain for possible exfiltration or attacker-controlled infrastructure.")

    if domain not in KNOWN_LEGITIMATE_DOMAINS and not findings:
        findings.append("No major suspicious DNS indicators detected.")
        recommendations.append("No action required.")

    return {
        "domain": domain,
        "timestamp": timestamp,
        "query_length": length,
        "entropy": entropy,
        "subdomain_depth": depth,
        "risk_score": score,
        "risk_level": risk_level(score),
        "findings": findings,
        "recommendations": recommendations
    }


def write_json_report(report, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)


def write_csv_summary(report, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Domain",
            "Timestamp",
            "Query Length",
            "Entropy",
            "Subdomain Depth",
            "Risk Score",
            "Risk Level",
            "Findings"
        ])

        for item in report:
            writer.writerow([
                item["domain"],
                item["timestamp"],
                item["query_length"],
                item["entropy"],
                item["subdomain_depth"],
                item["risk_score"],
                item["risk_level"],
                " | ".join(item["findings"])
            ])


def write_html_dashboard(report, output_file):
    rows = ""

    for item in report:
        rows += f"""
        <tr>
            <td>{item["domain"]}</td>
            <td>{item["query_length"]}</td>
            <td>{item["entropy"]}</td>
            <td>{item["subdomain_depth"]}</td>
            <td>{item["risk_score"]}</td>
            <td>{item["risk_level"]}</td>
            <td>{"<br>".join(item["findings"])}</td>
            <td>{"<br>".join(item["recommendations"])}</td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>DNS Tunnelling Detection Dashboard</title>
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
    <h1>DNS Tunnelling Detection Dashboard</h1>
    <p>This report analyzes DNS queries for tunnelling indicators such as query length, entropy, subdomain depth, suspicious keywords, and abnormal domain structures.</p>

    <table>
        <tr>
            <th>Domain</th>
            <th>Length</th>
            <th>Entropy</th>
            <th>Depth</th>
            <th>Risk Score</th>
            <th>Risk Level</th>
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
    input_file = base_dir / "sample-data" / "dns_queries.json"
    report_dir = base_dir / "reports"

    report_dir.mkdir(exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as file:
        dns_queries = json.load(file)

    report = [analyze_domain(entry) for entry in dns_queries]

    write_json_report(report, report_dir / "dns_tunnelling_report.json")
    write_csv_summary(report, report_dir / "dns_risk_summary.csv")
    write_html_dashboard(report, report_dir / "dns_tunnelling_dashboard.html")

    print("DNS Tunnelling Detection Complete")
    print(f"JSON report generated: {report_dir / 'dns_tunnelling_report.json'}")
    print(f"CSV summary generated: {report_dir / 'dns_risk_summary.csv'}")
    print(f"HTML dashboard generated: {report_dir / 'dns_tunnelling_dashboard.html'}")


if __name__ == "__main__":
    main()