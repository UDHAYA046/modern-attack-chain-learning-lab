# Lab 1 – OAuth 2.0 Token Hijacking & Scope Abuse Detector

## Domain

**Identity and Access Management (IAM)**

---

## Problem Statement

A SaaS platform uses OAuth 2.0 for third-party app integrations. An attacker is exploiting overly broad consent grants to exfiltrate user data.

This lab focuses on identifying risky OAuth applications by analyzing granted scopes, token characteristics, and permission abuse patterns.

---

## Background

Modern SaaS applications frequently integrate with third-party services using OAuth 2.0. While OAuth improves security by eliminating password sharing, excessive permissions and poor authorization practices can create significant security risks.

Attackers increasingly abuse OAuth applications through:

* Scope Abuse
* Consent Phishing
* Token Hijacking
* Data Exfiltration
* Over-Privileged OAuth Applications

This project explores how defenders can identify and assess risky OAuth integrations before they lead to compromise.

---

## Objective

Build a defensive OAuth Security Analyzer capable of:

* Enumerating OAuth-connected applications
* Identifying dangerous or excessive permissions
* Assigning risk scores
* Classifying applications by risk level
* Simulating token abuse scenarios
* Generating remediation recommendations

---

## Learning Goals

After completing this lab, I should be able to:

* Explain how OAuth 2.0 works
* Understand OAuth scopes and permissions
* Identify scope abuse scenarios
* Understand token hijacking risks
* Analyze OAuth-connected applications
* Apply the Principle of Least Privilege
* Generate meaningful security recommendations
* Map OAuth abuse to MITRE ATT&CK techniques

---

## Core Concepts Covered

### Identity and Access Management (IAM)

* Identity
* Authentication
* Authorization
* Least Privilege

### OAuth 2.0

* OAuth Actors
* Authorization Flows
* Access Tokens
* Refresh Tokens
* Consent Screens
* Redirect URIs

### Security Concepts

* Scope Abuse
* Consent Phishing
* Token Hijacking
* Data Exfiltration
* Risk Scoring
* OAuth Threat Modeling

### Standards and Frameworks

* OAuth 2.0
* JWT
* MITRE ATT&CK

---

## Attack Chain

```text
User
↓
OAuth Consent Screen
↓
Application Requests Scopes
↓
User Grants Permissions
↓
Access Token Issued
↓
Application Accesses Resources
↓
Excessive Permissions Enable Abuse
↓
Sensitive Data Exfiltration
```

---

## Project Scope

This project analyzes OAuth application metadata and assigned permissions to identify potential security risks.

The analyzer evaluates:

* Application Name
* Granted Scopes
* Token Type
* Token Expiry
* Last Usage Information

The analyzer then:

* Calculates a risk score
* Identifies dangerous scopes
* Classifies application risk
* Provides remediation guidance

---

## Example Dangerous Scopes

The following scopes are considered higher risk because they provide access to sensitive resources or enable long-term access.

### Email Access

```text
mail.read
mail.readwrite
```

### Contact Access

```text
contacts.read
```

### File Access

```text
files.read
files.readwrite
```

### Persistent Access

```text
offline_access
```

---

## Risk Classification Model

| Risk Level | Description                                   |
| ---------- | --------------------------------------------- |
| Low        | Minimal permissions such as email and profile |
| Medium     | Sensitive read-only permissions               |
| High       | Sensitive data access or persistence          |
| Critical   | Read/write access combined with persistence   |

---

## Example Input

```json
{
  "app_name": "Productivity Assistant",
  "scopes": [
    "email",
    "profile",
    "mail.readwrite",
    "offline_access"
  ],
  "token_type": "Bearer",
  "token_expiry": "long-lived",
  "last_used": "2026-06-10"
}
```

---

## Example Output

```json
{
  "app_name": "Productivity Assistant",
  "risk_score": 16,
  "risk_level": "Critical",
  "dangerous_scopes": [
    "mail.readwrite",
    "offline_access"
  ],
  "recommendations": [
    "Revoke unnecessary OAuth permissions",
    "Remove offline_access unless required",
    "Replace mail.readwrite with least-privilege read-only scopes"
  ]
}
```

---

## Planned Architecture

```text
OAuth Application Dataset
            │
            ▼
     Scope Analyzer
            │
            ▼
      Risk Engine
            │
            ▼
 Recommendation Engine
            │
            ▼
      Security Report
```

---

## Planned Features

### Phase 1

* OAuth Application Dataset
* Scope Analysis
* Risk Scoring
* JSON Report Generation

### Phase 2

* Dashboard Visualization
* CSV Import Support
* Risk Trend Analysis
* Additional Scope Rules

### Phase 3

* JWT Inspection
* Advanced Detection Logic
* OAuth Audit Log Analysis

---

## Folder Structure

```text
01-identity-oauth-scope-abuse/
│
├── README.md
├── notes.md
├── src/
│   └── oauth_scope_analyzer.py
│
├── sample-data/
│   └── oauth_apps.json
│
└── screenshots/
```

---

## MITRE ATT&CK Mapping

| Technique ID | Technique                             |
| ------------ | ------------------------------------- |
| T1528        | Steal Application Access Token        |
| T1550        | Use Alternate Authentication Material |
| T1539        | Steal Web Session Cookie              |

---

## Security Boundary

This project is intended for educational and defensive learning purposes only.

The project does not:

* Steal OAuth tokens
* Attack real OAuth providers
* Access real user accounts
* Interact with live APIs
* Perform unauthorized actions

All examples, datasets, and demonstrations are simulated.

---

## Expected Outcome

Upon completion, this lab will demonstrate how defenders can identify risky OAuth applications, detect excessive permissions, understand token abuse scenarios, and apply least-privilege principles to reduce OAuth-related security risks.

---

## References

* OAuth 2.0 Framework
* JWT (JSON Web Token)
* MITRE ATT&CK
* OWASP OAuth Security Guidelines
* OAuth 2.0 Security Best Current Practices
