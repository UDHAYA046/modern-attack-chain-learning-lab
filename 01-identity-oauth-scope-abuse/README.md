# Lab 1 – OAuth 2.0 Token Hijacking & Scope Abuse Detector

## Domain

**Identity and Access Management (IAM)**

---

## Problem Statement

A SaaS platform uses OAuth 2.0 for third-party application integrations. An attacker is exploiting overly broad consent grants to exfiltrate user data.

This lab focuses on understanding how excessive OAuth permissions, dangerous scope combinations, and long-lived tokens can increase organizational risk.

The objective is to analyze OAuth-connected applications and identify risky authorization patterns before they can be abused.

---

## Background

Modern SaaS applications frequently integrate with third-party services using OAuth 2.0. While OAuth improves security by eliminating password sharing, excessive permissions and poor authorization practices can introduce significant security risks.

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
* Detecting risky scope combinations
* Identifying long-lived token exposure
* Assigning risk scores
* Classifying applications by risk level
* Simulating malicious OAuth application scenarios
* Generating remediation recommendations
* Producing security assessment reports

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
* Interpret OAuth risk indicators
* Map OAuth abuse techniques to MITRE ATT&CK

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

## Simulated Malicious OAuth Scenario

```text
User
↓
Malicious OAuth Application
↓
Requests Excessive Scopes
↓
User Accepts Consent Screen
↓
Access Token Issued
↓
Persistent Access via offline_access
↓
Unauthorized Data Access
```

This repository does not perform real token theft or attack live OAuth providers.

The scenario above demonstrates how attackers can abuse excessive permissions and persistent tokens when users authorize a malicious application.

---

## Implemented Features

The final version of the OAuth Security Analyzer includes:

* OAuth application enumeration
* Scope risk analysis
* Dangerous scope detection
* Dangerous scope combination detection
* Long-lived token risk detection
* Risk scoring and classification
* Security recommendation engine
* JSON report generation
* CSV summary generation
* HTML dashboard generation
* Simulated trusted OAuth application
* Simulated malicious OAuth application

---

## Project Scope

The analyzer evaluates:

* Application Name
* Granted Scopes
* Redirect URI
* Token Type
* Token Expiry
* Last Usage Information

The analyzer then:

* Calculates a risk score
* Identifies dangerous scopes
* Detects risky scope combinations
* Identifies long-lived token risks
* Classifies application risk
* Generates security recommendations

---

## Example Dangerous Scopes

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

## Dangerous Scope Combinations

The analyzer identifies dangerous permission combinations including:

```text
mail.readwrite + offline_access
```

Email modification combined with persistent access.

```text
contacts.read + offline_access
```

Long-term access to organizational contact information.

```text
files.readwrite + offline_access
```

Persistent modification of cloud-hosted files.

---

## Risk Classification Model

| Risk Level | Description                                   |
| ---------- | --------------------------------------------- |
| Low        | Minimal permissions such as email and profile |
| Medium     | Sensitive read-only permissions               |
| High       | Sensitive data access or persistence          |
| Critical   | Read/write access combined with persistence   |

---

## Architecture

```text
OAuth Application Dataset
            │
            ▼
      Scope Analyzer
            │
            ▼
 Dangerous Scope Detector
            │
            ▼
 Risk Scoring Engine
            │
            ▼
 Recommendation Engine
            │
            ▼
 ┌───────────────────────┐
 │ JSON Report           │
 │ CSV Summary           │
 │ HTML Dashboard        │
 └───────────────────────┘
```

---

## Dataset Components

### Standard OAuth Applications

```text
oauth_apps.json
```

Contains multiple simulated OAuth-connected applications with varying permission levels.

### Trusted OAuth Application

```text
good_app.json
```

Represents a legitimate OAuth integration using limited permissions.

### Malicious OAuth Application

```text
evil_app.json
```

Represents a simulated OAuth application requesting excessive permissions and long-term access.

---

## Generated Outputs

### JSON Security Report

```text
oauth_risk_report.json
```

Detailed application-by-application risk assessment.

### CSV Summary

```text
risk_summary.csv
```

Tabular risk summary for reporting and analysis.

### HTML Dashboard

```text
oauth_risk_dashboard.html
```

Visual dashboard displaying:

* Risk Scores
* Risk Levels
* Dangerous Scopes
* Findings
* Recommendations

---

## Folder Structure

```text
01-identity-oauth-scope-abuse/
│
├── README.md
├── notes.md
│
├── sample-data/
│   ├── oauth_apps.json
│   ├── good_app.json
│   └── evil_app.json
│
├── reports/
│   ├── oauth_risk_report.json
│   ├── risk_summary.csv
│   └── oauth_risk_dashboard.html
│
└── src/
    └── oauth_scope_analyzer.py
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

## Learning Outcome

Upon completion, this lab demonstrates:

* Identification of risky OAuth permissions
* Detection of dangerous scope combinations
* Analysis of long-lived token exposure
* Comparison of trusted and malicious OAuth applications
* Automated generation of security recommendations
* Generation of JSON, CSV, and HTML security reports

---

## References

* OAuth 2.0 Framework
* OAuth 2.0 Security Best Current Practices
* OWASP OAuth Security Guidelines
* JWT (JSON Web Token)
* MITRE ATT&CK
