# Lab 1 – OAuth 2.0 Token Hijacking & Scope Abuse Detector

## Domain

Identity and Access Management (IAM)

## Problem Statement

A SaaS platform uses OAuth 2.0 for third-party app integrations. An attacker is exploiting overly broad consent grants to exfiltrate user data.

This lab focuses on identifying risky OAuth applications by analyzing granted scopes, token characteristics, and permission abuse patterns.

---

## Objective

The objective of this lab is to build a safe educational OAuth Security Analyzer that can:

- Analyze OAuth-connected applications
- Identify dangerous or over-privileged scopes
- Assign a risk score
- Classify applications as Low, Medium, High, or Critical risk
- Generate remediation recommendations

---

## What This Lab Does

This lab does **not** attack real OAuth providers or real user accounts.

Instead, it uses simulated OAuth application data to understand how defenders can detect risky OAuth integrations.

---

## Core Concepts

- OAuth 2.0
- Access Tokens
- Refresh Tokens
- OAuth Scopes
- Scope Abuse
- Consent Phishing
- Token Hijacking
- Risk Scoring
- Least Privilege
- MITRE ATT&CK T1528 – Steal Application Access Token

---

## Attack Chain

```text
User
↓
OAuth Consent Screen
↓
Application Receives Scopes
↓
Access Token Issued
↓
Application Accesses APIs
↓
Over-Privileged Scopes Enable Abuse
↓
Sensitive Data Exfiltration

Tool Design

The analyzer takes OAuth application records as input.

Each record may include:

Application Name
Granted Scopes
Token Type
Token Expiry
Last Used Timestamp

The tool checks whether the application has risky scopes such as:

mail.readwrite
mail.read
contacts.read
files.readwrite
offline_access
Risk Levels
Risk Level	Meaning
Low	Minimal permissions such as email and profile
Medium	Sensitive read-only access such as contacts or calendar
High	Sensitive data access or persistent access
Critical	Read/write access combined with persistence
Example

Input:

{
  "app_name": "Productivity Assistant",
  "scopes": ["email", "profile", "mail.readwrite", "offline_access"],
  "token_type": "Bearer",
  "token_expiry": "long-lived",
  "last_used": "2026-06-10"
}

Output:

{
  "app_name": "Productivity Assistant",
  "risk_score": 16,
  "risk_level": "Critical",
  "dangerous_scopes": ["mail.readwrite", "offline_access"],
  "recommendations": [
    "Revoke unnecessary OAuth permissions",
    "Remove offline_access unless required",
    "Replace mail.readwrite with least-privilege read-only scopes"
  ]
}
Planned Implementation

The first version of this lab will include:

A sample OAuth application dataset
A Python-based scope analyzer
Risk scoring logic
JSON report generation
Remediation recommendations
Folder Structure
01-identity-oauth-scope-abuse/
│
├── README.md
├── notes.md
├── src/
│   └── oauth_scope_analyzer.py
└── screenshots/
Security Boundary

This lab is for educational and defensive learning only.

It does not:

Steal tokens
Attack real OAuth applications
Access real user data
Abuse live APIs

All examples are simulated and safe.

Learning Outcome

After completing this lab, I should be able to explain:

How OAuth permissions work
Why excessive scopes are dangerous
How token abuse can lead to data exposure
How defenders can score and detect risky OAuth applications
How least privilege reduces OAuth security risk
