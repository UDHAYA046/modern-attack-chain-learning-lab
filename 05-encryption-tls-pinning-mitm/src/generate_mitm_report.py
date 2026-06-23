import json
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "sample-data" / "intercepted_requests.json"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(exist_ok=True)


def load_intercepted_requests():
    if not DATA_FILE.exists():
        return []

    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def classify_status(code):
    if 200 <= code < 300:
        return "Success"
    if 300 <= code < 400:
        return "Redirect"
    if 400 <= code < 500:
        return "Client Error"
    if 500 <= code < 600:
        return "Server Error"
    return "Unknown"


def generate_report(requests):
    total_requests = len(requests)
    methods = Counter(item.get("method", "UNKNOWN") for item in requests)
    status_codes = Counter(str(item.get("status_code", "UNKNOWN")) for item in requests)
    hosts = Counter(item.get("host", "UNKNOWN") for item in requests)
    content_types = Counter(item.get("content_type", "unknown") for item in requests)

    analyzed_requests = []

    for item in requests:
        status_code = int(item.get("status_code", 0))

        analyzed_requests.append({
            "timestamp": item.get("timestamp"),
            "method": item.get("method"),
            "url": item.get("url"),
            "host": item.get("host"),
            "path": item.get("path"),
            "status_code": status_code,
            "status_category": classify_status(status_code),
            "content_type": item.get("content_type"),
            "response_size_bytes": item.get("response_size_bytes", 0)
        })

    return {
        "lab": "TLS Certificate Pinning Bypass & MitM Attack",
        "summary": {
            "total_requests": total_requests,
            "methods": dict(methods),
            "status_codes": dict(status_codes),
            "hosts": dict(hosts),
            "content_types": dict(content_types)
        },
        "requests": analyzed_requests
    }


def write_json_report(report):
    output_file = REPORT_DIR / "mitm_report.json"
    output_file.write_text(json.dumps(report, indent=4), encoding="utf-8")
    return output_file


def write_html_dashboard(report):
    rows = ""

    for item in report["requests"]:
        rows += f"""
        <tr>
            <td>{item["timestamp"]}</td>
            <td>{item["method"]}</td>
            <td>{item["host"]}</td>
            <td>{item["path"]}</td>
            <td>{item["status_code"]}</td>
            <td>{item["status_category"]}</td>
            <td>{item["content_type"]}</td>
            <td>{item["response_size_bytes"]}</td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>TLS MitM Traffic Dashboard</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f7f9fc;
        }}
        h1 {{
            color: #111827;
        }}
        .summary {{
            background: white;
            padding: 20px;
            border: 1px solid #ddd;
            margin-bottom: 25px;
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
    <h1>TLS MitM Traffic Dashboard</h1>

    <p>This dashboard summarizes HTTPS traffic captured through mitmproxy in a controlled local lab environment.</p>

    <div class="summary">
        <h2>Summary</h2>
        <p><b>Total Requests:</b> {report["summary"]["total_requests"]}</p>
        <p><b>Methods:</b> {report["summary"]["methods"]}</p>
        <p><b>Status Codes:</b> {report["summary"]["status_codes"]}</p>
        <p><b>Hosts:</b> {report["summary"]["hosts"]}</p>
    </div>

    <table>
        <tr>
            <th>Timestamp</th>
            <th>Method</th>
            <th>Host</th>
            <th>Path</th>
            <th>Status Code</th>
            <th>Status Category</th>
            <th>Content Type</th>
            <th>Size Bytes</th>
        </tr>
        {rows}
    </table>
</body>
</html>
"""

    output_file = REPORT_DIR / "mitm_dashboard.html"
    output_file.write_text(html, encoding="utf-8")
    return output_file


def main():
    requests = load_intercepted_requests()

    if not requests:
        print("No intercepted requests found.")
        print(f"Expected file: {DATA_FILE}")
        return

    report = generate_report(requests)

    json_file = write_json_report(report)
    html_file = write_html_dashboard(report)

    print("MitM report generation complete.")
    print(f"JSON report generated: {json_file}")
    print(f"HTML dashboard generated: {html_file}")


if __name__ == "__main__":
    main()