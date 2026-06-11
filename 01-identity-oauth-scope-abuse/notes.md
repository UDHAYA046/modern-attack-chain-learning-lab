# OAuth 2.0 Token Hijacking & Scope Abuse Detector

# Lab 1 – Learning Notes

---

# Table of Contents

1. Problem Statement Overview
2. Identity and Access Management (IAM)
3. Authentication and Authorization
4. OAuth 2.0 Fundamentals
5. Why OAuth Exists
6. OAuth Actors
7. OAuth Architecture
8. OAuth Workflow
9. SaaS and Third-Party Integrations
10. OAuth Authorization Flows
11. OAuth Permissions and Scopes

---

# 1. Problem Statement Overview

## Hackathon Problem Statement

**OAuth 2.0 Token Hijacking & Scope Abuse Detector**

A SaaS platform uses OAuth 2.0 for third-party app integrations. An attacker is exploiting overly broad consent grants to exfiltrate user data.

The objective is to understand:

* Identity and Access Management (IAM)
* OAuth 2.0
* Access Tokens
* OAuth Scopes
* Scope Abuse
* Token Hijacking
* Consent Phishing
* Data Exfiltration
* OAuth Detection Techniques

The final goal is to build a security analysis tool capable of:

* Enumerating OAuth-connected applications
* Identifying dangerous permissions
* Simulating token abuse scenarios
* Calculating risk scores
* Generating remediation recommendations

---

# 2. Identity and Access Management (IAM)

## What is IAM?

Identity and Access Management (IAM) is a security framework used to manage digital identities and control access to resources.

IAM answers two fundamental security questions:

### Question 1

Who are you?

### Question 2

What are you allowed to do?

---

## Why IAM Exists

Without IAM:

* Anyone could access resources
* Systems could not verify users
* Permissions would not exist
* Security would collapse

IAM provides:

* Identity verification
* Access control
* User management
* Security governance

---

## Resources Protected By IAM

IAM protects:

* User Accounts
* Applications
* APIs
* Databases
* Cloud Resources
* Internal Systems
* Enterprise Infrastructure

---

# 3. Authentication and Authorization

These are the two most important concepts in IAM.

Many beginners confuse them.

They are completely different.

---

## Authentication

Authentication is the process of verifying identity.

Authentication answers:

> "Can you prove who you are?"

Examples:

* Username and Password
* OTP
* Fingerprint
* Face Recognition
* Multi-Factor Authentication (MFA)

Example:

A student logs into a university portal.

The portal verifies:

* Username
* Password

If valid:

Authentication succeeds.

---

## Authorization

Authorization determines what an authenticated user can do.

Authorization answers:

> "What are you allowed to access?"

Example:

A student may:

* View Grades
* View Attendance

A student may not:

* Modify Grades
* Create Accounts
* Access Faculty Records

Authorization occurs after authentication.

---

## Authentication vs Authorization

| Authentication    | Authorization          |
| ----------------- | ---------------------- |
| Verifies Identity | Determines Permissions |
| "Who are you?"    | "What can you do?"     |
| Happens First     | Happens Second         |
| Login Process     | Permission Process     |

---

# 4. OAuth 2.0 Fundamentals

## What is OAuth 2.0?

OAuth stands for:

**Open Authorization**

OAuth 2.0 is an authorization framework that allows third-party applications to access user resources without exposing user credentials.

OAuth is not primarily an authentication protocol.

OAuth is an authorization framework.

---

## Industry Adoption

OAuth 2.0 is used by:

* Google
* Microsoft
* GitHub
* LinkedIn
* Amazon
* Salesforce
* Slack
* Notion
* Zoom

It is considered the industry standard for delegated authorization.

---

## What Problem Does OAuth Solve?

Before OAuth:

Applications often required:

* Username
* Password

Example:

A third-party application asks:

"Enter your Gmail password."

This is dangerous because:

* Passwords may be stolen
* Passwords may be reused
* Applications gain excessive trust

OAuth solves this problem.

---

# 5. Why OAuth Exists

Consider:

You have:

* Google Account

You want to use:

* Canva

Canva wants:

* Name
* Email Address
* Profile Information

Without OAuth:

You give Canva your password.

With OAuth:

1. Google authenticates you.
2. Google asks for consent.
3. You approve.
4. Google issues a token.
5. Canva uses the token.

Your password never leaves Google.

---

## Benefits of OAuth

### Enhanced Security

Passwords are never shared.

---

### Controlled Access

Permissions can be limited.

---

### Revocability

Permissions can be revoked at any time.

---

### Standardization

Works consistently across platforms.

---

# 6. OAuth Actors

OAuth defines four primary actors.

Understanding these is essential.

---

## Resource Owner

The entity that owns the data.

Usually:

* User
* Customer
* Employee

Examples:

* Google User
* GitHub User
* Microsoft User

---

## Client

The application requesting access.

Examples:

* Canva
* Zoom
* Slack
* Notion

The Client wants access to user resources.

---

## Authorization Server

Responsible for:

* Authentication
* Consent Collection
* Token Issuance

Examples:

* Google Login
* Microsoft Login
* GitHub Login

---

## Resource Server

Stores protected resources.

Examples:

* Gmail API
* Microsoft Graph API
* GitHub API

The Resource Server validates tokens before granting access.

---

# 7. OAuth Architecture

## High-Level Architecture

User
↓
Client Application
↓
Authorization Server
↓
Access Token
↓
Resource Server
↓
Protected Data

---

## Simplified Example

User wants to connect Canva to Google.

Actors:

Resource Owner:
User

Client:
Canva

Authorization Server:
Google Login

Resource Server:
Google APIs

---

# 8. OAuth Workflow

## Step 1

Client requests access.

Example:

Canva requests access to Google profile information.

---

## Step 2

User authenticates.

Google verifies identity.

---

## Step 3

User grants consent.

Permissions are displayed.

---

## Step 4

Authorization Server issues token.

---

## Step 5

Client presents token.

---

## Step 6

Resource Server validates token.

---

## Step 7

Access granted.

---

# 9. SaaS and Third-Party Integrations

## What is SaaS?

SaaS means:

Software as a Service

Applications delivered over the internet.

Examples:

* Google Docs
* Slack
* Zoom
* Canva
* Notion

---

## What is a SaaS Platform?

A company providing software through the internet.

Examples:

* Canva
* Notion
* Microsoft 365
* Slack

---

## What are Third-Party Integrations?

External applications connecting to another platform.

Examples:

* Canva using Google Login
* Slack using Google Calendar
* Notion using GitHub
* Zoom using Microsoft 365

OAuth enables these integrations securely.

---

## Security Perspective

At this stage:

Nothing malicious has happened.

This only describes:

* OAuth Environment
* SaaS Platform
* Third-Party Application
* Access Tokens

The attack comes later.

---

# 10. OAuth Authorization Flows

Grant Types define:

> How was the Access Token obtained?

---

## Authorization Code Grant

Most secure.

Most common.

Used by:

* Google
* Microsoft
* GitHub
* LinkedIn

Flow:

User
↓
Authorization Code
↓
Access Token

Advantages:

* Highly Secure
* Password Never Shared
* Recommended Flow

---

## Implicit Grant

Older browser-based flow.

Flow:

User
↓
Access Token Directly

Problems:

* Token Exposure
* Easier Theft

Status:

Deprecated

---

## Client Credentials Grant

Machine-to-machine communication.

No human user involved.

Examples:

* Security Tools
* Monitoring Systems
* Cloud Services

---

## Resource Owner Password Credentials Grant

Legacy flow.

User provides credentials directly.

Problems:

* Password Exposure
* Violates OAuth Principles

Status:

Not Recommended

---

## Device Authorization Flow

Used by:

* Smart TVs
* Gaming Consoles
* IoT Devices

User approves access on another device.

---

# 11. OAuth Permissions and Scopes

## What is a Scope?

A Scope defines:

> What can the token do?

A Grant Type determines:

> How the token was obtained.

A Scope determines:

> What permissions the token has.

---

## Common Scopes

### email

Access email address.

---

### profile

Access profile information.

---

### contacts.read

Read contacts.

---

### mail.read

Read emails.

---

### mail.readwrite

Read, modify, send, and delete emails.

High-Risk Scope.

---

### offline_access

Maintain long-term access without repeated authentication.

High-Risk Scope.

---

## Granular Access Control

OAuth allows specific permissions to be granted.

Instead of:

Full Account Access

Users approve:

* email
* profile
* contacts.read

This is called Granular Access Control.

---

## Principle of Least Privilege

Users and applications should receive only the permissions necessary to perform their task.

Benefits:

* Reduced Attack Surface
* Reduced Data Exposure
* Better Security

---

## Scope Abuse

Scope Abuse occurs when applications receive more permissions than necessary.

Example:

Required:

* email
* profile

Requested:

* email
* profile
* contacts.read
* mail.readwrite
* offline_access

Result:

Excessive Privileges

Higher Risk

Violation of Least Privilege Principle

---

## Risks of Scope Abuse

Attackers may:

* Read Emails
* Modify Emails
* Download Contacts
* Access Sensitive Data
* Maintain Long-Term Access

This forms the foundation of the hackathon problem statement.

# 12. OAuth Tokens

Tokens are the heart of OAuth.

OAuth does not share passwords.

OAuth shares tokens.

A token is a temporary credential that proves permission has been granted.

---

## Why Tokens Exist

Without tokens:

Every application would need:

* Username
* Password

This creates security risks.

OAuth replaces credentials with tokens.

Benefits:

* Passwords remain protected
* Permissions can be limited
* Access can be revoked
* Applications never see user credentials

---

# 13. Access Tokens

## What is an Access Token?

An Access Token is a temporary credential issued by the Authorization Server after successful authorization.

Think of it as:

> A temporary permission ticket.

---

## Real World Analogy

Airport Boarding Pass

Identity Verification:
Passport

Permission:
Boarding Pass

Similarly:

Identity:
User Account

Permission:
Access Token

---

## Properties of Access Tokens

Access Tokens are:

* Temporary
* Revocable
* Permission-Based
* Time-Limited

---

## Purpose

Access Tokens allow applications to act on behalf of users.

Example:

User approves Canva.

Google issues Access Token.

Canva uses token to access:

* Profile Information
* Email Address

without knowing the user's password.

---

# Access Token Lifecycle

User Login
↓
Consent Granted
↓
Access Token Issued
↓
API Access
↓
Token Expires

---

## Why Access Tokens Expire

If a token is stolen:

Attacker's access is limited.

Short-lived tokens reduce damage.

---

# Risks of Access Tokens

If stolen:

Attacker may:

* Read Data
* Access APIs
* Impersonate User

without needing credentials.

This leads to:

Token Hijacking

---

# 14. Refresh Tokens

## What Problem Do Refresh Tokens Solve?

Imagine:

Access Token Validity:

60 Minutes

After 60 minutes:

Token Expires

User would need to login again.

This creates poor user experience.

---

## What is a Refresh Token?

A Refresh Token is a long-lived credential used to obtain new Access Tokens.

---

## Workflow

User Login
↓
Access Token
+
Refresh Token

---

Later:

Access Token Expires
↓
Refresh Token Used
↓
New Access Token Issued

No login required.

---

## Why Refresh Tokens Are Dangerous

If attacker steals:

Access Token

Temporary access.

---

If attacker steals:

Refresh Token

Potential long-term access.

---

## Security Importance

Refresh Tokens are often more valuable than Access Tokens.

---

# 15. Token Expiration

## What is Token Expiration?

Every Access Token should have a limited lifetime.

Example:

15 Minutes

30 Minutes

1 Hour

---

## Why Expiration Exists

Reduces damage caused by:

* Token Theft
* Session Hijacking
* Credential Abuse

---

## Good Practice

Short-Lived Access Tokens

Example:

15–60 Minutes

---

## Poor Practice

Long-Lived Access Tokens

Example:

30 Days

90 Days

Higher risk.

---

# 16. Token Rotation

## What is Token Rotation?

Replacing old tokens with new ones.

---

## Refresh Token Rotation

Old Refresh Token
↓
Exchange
↓
New Refresh Token

Old Token Invalidated

---

## Why Token Rotation Exists

Without rotation:

Stolen Refresh Token remains useful forever.

---

With rotation:

Compromised token becomes useless after replacement.

---

## Security Benefit

Reduces persistence after compromise.

---

# 17. Consent Screens

## What is a Consent Screen?

The page where users approve permissions requested by an application.

Example:

Canva wants permission to:

✓ View Email

✓ View Profile

Allow?

---

## Purpose

Provides visibility into:

* Requested Scopes
* Application Identity
* Permissions Being Granted

---

## Security Importance

This is where users make security decisions.

---

## Common User Mistake

Blindly clicking:

Allow

without reviewing scopes.

---

## Result

Scope Abuse

Permission Abuse

Potential Data Exposure

---

# Example

Application Needs:

email

profile

---

Application Requests:

email

profile

mail.readwrite

contacts.read

offline_access

---

User Clicks:

Allow

---

Attack Surface Increases.

---

# 18. Redirect URIs

## What is a Redirect URI?

After successful authorization, OAuth needs to return the user to the application.

The destination URL is called:

Redirect URI

---

## Example

After Google Login:

User Returns To:

https://canva.com/oauth/callback

---

## Why Redirect URIs Matter

Authorization Codes are sent to Redirect URIs.

If Redirect URI is compromised:

Authorization Codes may be stolen.

---

# Attack Scenario

Legitimate URI:

https://app.com/callback

---

Attacker Changes To:

https://evil.com/callback

---

Authorization Code Sent To:

Attacker

---

Potential Result

Token Theft

Account Compromise

---

## Security Best Practice

Only pre-registered Redirect URIs should be allowed.

---

# 19. JWT Fundamentals

## What is JWT?

JWT stands for:

JSON Web Token

---

## Purpose

JWT is a compact format for securely transmitting information between systems.

Common Uses:

* Authentication
* Authorization
* OAuth Tokens
* API Security

---

# JWT Structure

JWT consists of:

Header.Payload.Signature

Three sections separated by dots.

---

## Header

Contains metadata.

Example:

{
"alg": "HS256",
"typ": "JWT"
}

---

Contains:

* Algorithm
* Token Type

---

## Payload

Contains claims.

Claims are pieces of information.

Example:

{
"sub": "user123",
"email": "[user@gmail.com](mailto:user@gmail.com)"
}

---

Contains:

* User Data
* Permissions
* Timestamps

---

## Signature

Verifies integrity.

Ensures token has not been modified.

---

# JWT Claims

## sub

Subject

Usually User ID.

---

## iss

Issuer

Who issued the token.

Example:

Google

Microsoft

GitHub

---

## aud

Audience

Who should use the token.

---

## exp

Expiration Time

When token becomes invalid.

---

## iat

Issued At

When token was created.

---

## nbf

Not Before

Token cannot be used before specified time.

---

## scope

OAuth Permissions

Example:

email profile

or

mail.readwrite offline_access

---

# Encoding vs Encryption

Important Concept

---

JWT is usually:

Encoded

NOT Encrypted

---

Anyone with the token can decode the payload.

---

Never Store:

* Passwords
* Secrets
* Credit Card Information

inside JWT payloads.

---

# JWT Validation

Before granting access:

Servers should verify:

* Signature
* Expiration
* Issuer
* Audience

---

If validation fails:

Access Denied

---

# JWT Security Risks

## Token Leakage

JWT exposed in:

* Logs
* URLs
* Browser Storage

---

## Weak Secrets

Poor signing keys.

---

## Expired Token Acceptance

Server ignores expiration.

---

## Algorithm Confusion

Incorrect algorithm validation.

Very important in JWT attacks.

---

# OAuth and JWT Relationship

OAuth Issues:

Access Token

---

Access Token May Be:

JWT

---

Therefore:

JWT often contains:

* User Information
* Scopes
* Expiration Details

which our analyzer may inspect.

---

# 20. OAuth Application Registration

## Question

How does an OAuth application come into existence?

Before requesting permissions:

Applications must be registered.

---

## Registration Platforms

Examples:

* Google Cloud Console
* Azure Portal
* GitHub Developer Portal

---

# Information Provided During Registration

Developer supplies:

* Application Name
* Website
* Redirect URI
* Logo
* Contact Information

---

# Client ID

Application Identifier

Think:

Application Username

---

Properties:

* Public
* Not Secret
* Used to identify application

---

# Client Secret

Application Credential

Think:

Application Password

---

Properties:

* Confidential
* Must Be Protected

---

## Why Client Secrets Matter

If stolen:

Attacker may impersonate application.

---

# Authorized Scopes

Developer defines:

What permissions application may request.

Examples:

* email
* profile
* contacts.read

---

# Consent Screen Configuration

Developer configures:

* App Name
* Logo
* Support Email
* Privacy Policy

These details appear during consent.

---

# Security Implications

Users often trust:

Professional Branding

without examining permissions.

This becomes important in:

Consent Phishing

which is covered in the next section.

# 21. OAuth Attack Techniques

OAuth is designed to improve security.

However, attackers often abuse OAuth implementations rather than breaking OAuth itself.

Most OAuth attacks target:

* Users
* Permissions
* Tokens
* Misconfigurations

rather than passwords.

---

# 22. Consent Phishing

## What is Consent Phishing?

Traditional phishing attempts to steal credentials.

Example:

Fake Login Page
↓
User Enters Password
↓
Password Stolen

---

OAuth phishing works differently.

Instead of stealing credentials, attackers trick users into granting permissions.

---

## Consent Phishing Flow

Attacker Creates OAuth Application
↓
User Authenticates Normally
↓
Real Consent Screen Appears
↓
User Clicks Allow
↓
Attacker Receives Access

---

## Why It Is Effective

Google Login is real.

Microsoft Login is real.

GitHub Login is real.

Nothing appears suspicious.

The malicious component is:

The OAuth Application

not the login page.

---

## Example

Attacker creates:

"Google Productivity Assistant"

Requests:

* mail.readwrite
* contacts.read
* offline_access

User clicks:

Allow

Attacker gains access.

---

## Indicators of Consent Phishing

### Unknown Application

Application has no reputation.

---

### Excessive Permissions

Requests more permissions than necessary.

---

### Generic Branding

Poor logo.

Suspicious website.

---

### Offline Access Requests

Attempts to maintain long-term access.

---

# 23. Token Hijacking

## What is Token Hijacking?

Token Hijacking occurs when an attacker steals a valid OAuth token and uses it to impersonate a legitimate user.

The attacker does not need:

* Username
* Password
* MFA

The token itself provides access.

---

## Why Tokens Are Valuable

Tokens represent:

Permission

not identity.

Possession of the token often means possession of access.

---

## Common Sources of Token Theft

### Browser Storage

Local Storage

Session Storage

---

### Malware

Steals browser data.

---

### Application Logs

Developers accidentally log tokens.

---

### Browser Extensions

Malicious extensions access tokens.

---

### Insecure APIs

Tokens exposed in responses.

---

## Attack Flow

User Grants Access
↓
Token Issued
↓
Attacker Steals Token
↓
Token Presented
↓
Access Granted

---

# 24. Data Exfiltration

## What is Data Exfiltration?

Data Exfiltration is the unauthorized extraction of information from a system.

Simply put:

Stealing Data

---

## Why OAuth Is Attractive

Traditional Attacks Require:

* Credential Theft
* MFA Bypass
* Persistence

OAuth Abuse Often Requires:

User Clicks Allow

---

## Data Commonly Exfiltrated

### Email Data

Messages

Attachments

Communication Records

---

### Contacts

Names

Email Addresses

Phone Numbers

---

### Calendars

Meetings

Schedules

Internal Events

---

### Cloud Files

Documents

Spreadsheets

Reports

---

### Profile Information

Identity Data

Organization Information

Roles

---

## Exfiltration Flow

OAuth Application
↓
User Grants Consent
↓
Token Issued
↓
API Access
↓
Data Downloaded

---

# 25. OAuth Threat Modeling

## What is Threat Modeling?

Threat Modeling is the process of identifying:

* Assets
* Threats
* Attack Paths
* Defenses

before incidents occur.

---

## OAuth Assets

Assets include:

* User Accounts
* Access Tokens
* Refresh Tokens
* OAuth Applications
* Protected APIs

---

## Common OAuth Threats

### Scope Abuse

Excessive permissions granted.

---

### Consent Phishing

Malicious applications obtain approval.

---

### Token Theft

Access Tokens stolen.

---

### Refresh Token Theft

Long-term persistence.

---

### Redirect URI Abuse

Authorization codes stolen.

---

### Data Exfiltration

Sensitive information extracted.

---

# 26. MITRE ATT&CK Mapping

## What is MITRE ATT&CK?

MITRE ATT&CK is a knowledge base documenting real-world attacker behavior.

It helps defenders:

* Understand attacks
* Classify techniques
* Improve detection

---

## Relevant Techniques

### T1528

Steal Application Access Token

Most directly related.

---

### T1550

Use Alternate Authentication Material

Using tokens instead of credentials.

---

### T1539

Steal Web Session Cookie

Related to web session abuse.

---

## Why MITRE Matters

Provides:

* Standardized terminology
* Threat intelligence alignment
* Detection guidance

---

# 27. Risk Scoring Methodology

## Why Risk Scoring Exists

Not all OAuth applications are equally dangerous.

Risk scoring helps prioritize investigations.

---

## Example

Application A:

* email
* profile

Risk:

Low

---

Application B:

* mail.readwrite
* contacts.read
* offline_access

Risk:

High

---

# Example Scoring Model

| Scope          | Score |
| -------------- | ----- |
| email          | 1     |
| profile        | 1     |
| contacts.read  | 3     |
| calendar.read  | 3     |
| mail.read      | 5     |
| offline_access | 6     |
| mail.readwrite | 8     |

---

# Example Calculation

Scopes:

email

profile

mail.readwrite

offline_access

---

Score:

1 + 1 + 8 + 6 = 16

---

Result:

Critical Risk

---

## Example Risk Levels

### Low

Minimal permissions.

---

### Medium

Sensitive read permissions.

---

### High

Sensitive data access.

---

### Critical

Read + Write + Persistence.

---

# 28. OAuth Logs and Audit Trails

## What is an Audit Trail?

A record of security-related events.

Answers:

Who?

What?

When?

Where?

---

## Common OAuth Events

### Application Registration

New application created.

---

### Consent Granted

User approves permissions.

---

### Token Issued

Access Token created.

---

### Token Refresh

Refresh Token used.

---

### Permission Revocation

Application access removed.

---

## Useful Log Fields

* User
* Application
* Scopes
* Timestamp
* IP Address
* Device
* Location

---

## Why Logs Matter

Logs provide:

Visibility

---

Visibility enables:

Detection

---

Detection enables:

Response

---

# 29. OAuth Detection Techniques

## Dangerous Scope Detection

Flag:

* mail.readwrite
* contacts.read
* offline_access

---

## Excessive Permission Detection

Application requests more permissions than required.

---

## Unknown Application Detection

Application lacks reputation.

---

## Long-Lived Access Detection

Persistent access identified.

---

## Consent Monitoring

Large numbers of users granting access.

---

## Abnormal API Usage

High-volume resource access.

---

# 30. Real-World OAuth Abuse Cases

## Microsoft 365 Consent Phishing

Attackers created malicious OAuth applications.

Users authenticated normally.

Permissions granted:

* mail.read
* contacts.read
* offline_access

Result:

Email and contact access.

---

## Google Workspace OAuth Abuse

Attackers disguised applications as:

* PDF Tools
* Document Viewers
* Productivity Apps

Users granted permissions.

Result:

Access to files and email data.

---

## GitHub OAuth Abuse

Developers approved malicious integrations.

Permissions exposed:

* Source Code
* Repository Data
* Developer Information

---

## Common Pattern

User
↓
OAuth Application
↓
Consent Granted
↓
Token Issued
↓
Permission Abuse
↓
Data Exfiltration

---

# 31. Problem Statement Analysis

## Statement 1

"A SaaS platform uses OAuth 2.0 for third-party app integrations."

Meaning:

A software platform allows external applications to access user resources using OAuth tokens instead of passwords.

This establishes the environment.

No attack has occurred yet.

---

## Statement 2

"An attacker is exploiting overly broad consent grants to exfiltrate user data."

Meaning:

Applications receive excessive permissions.

Users approve those permissions.

Attackers abuse them to access sensitive data.

This is Scope Abuse.

---

## Statement 3

"Enumerate all OAuth-connected applications."

Meaning:

List all connected applications.

Examples:

* Canva
* Slack
* Zoom
* Notion

---

## Statement 4

"Flag dangerous or over-privileged scopes."

Meaning:

Identify permissions such as:

* mail.readwrite
* contacts.read
* offline_access

and classify risk.

---

## Statement 5

"Demonstrate how a stolen access token could be abused."

Meaning:

Show how attackers may misuse valid tokens.

No password required.

---

## Statement 6

"Generate a risk score and remediation recommendations."

Meaning:

Calculate risk level.

Provide mitigation guidance.

---

# 32. Security Recommendations

Recommended Defenses:

* Apply Least Privilege
* Reduce Scope Exposure
* Use Short-Lived Access Tokens
* Enable Token Rotation
* Monitor Consent Activity
* Audit OAuth Applications
* Revoke Unnecessary Permissions
* Protect Tokens During Storage
* Protect Tokens During Transmission

---

# 33. Final Mental Model

Identity
↓
Authentication
↓
Authorization
↓
OAuth
↓
Consent
↓
Scopes
↓
Access Token
↓
API Access

Potential Risks:

* Scope Abuse
* Consent Phishing
* Token Theft
* Refresh Token Theft
* Redirect URI Abuse
* Data Exfiltration

Defenses:

* Least Privilege
* Risk Scoring
* Audit Logs
* Detection Techniques
* Token Security
* Continuous Monitoring

---

# Lab 1 Conclusion

The OAuth 2.0 Token Hijacking & Scope Abuse Detector focuses on understanding how OAuth-based integrations work, how permissions can be abused, how tokens can be stolen, and how defenders can identify risky applications before sensitive data is exposed.

The project is primarily an OAuth Security Analysis and Detection project rather than an OAuth Authentication implementation project.
