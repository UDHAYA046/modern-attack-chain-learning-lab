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
    elif score <= 6:
        return "Medium"
    elif score <= 12:
        return "High"
    return "Critical"


def analyze_application(app):
    scopes = app.get("scopes", [])

    risk_score = sum(SCOPE_RISK_SCORES.get(scope, 0) for scope in scopes)
    dangerous_scopes = [scope for scope in scopes if scope in DANGEROUS_SCOPES]

    recommendations = [
        RECOMMENDATIONS[scope]
        for scope in dangerous_scopes
        if scope in RECOMMENDATIONS
    ]

    return {
        "app_name": app.get("app_name", "Unknown Application"),
        "risk_score": risk_score,
        "risk_level": calculate_risk_level(risk_score),
        "dangerous_scopes": dangerous_scopes,
        "recommendations": recommendations
    }


def main():
    base_dir = Path(__file__).resolve().parent.parent
    input_file = base_dir / "sample-data" / "oauth_apps.json"
    output_file = base_dir / "reports" / "oauth_risk_report.json"

    output_file.parent.mkdir(exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as file:
        applications = json.load(file)

    report = [analyze_application(app) for app in applications]

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("OAuth Scope Analysis Complete")
    print(f"Report generated: {output_file}")


if __name__ == "__main__":
    main()
