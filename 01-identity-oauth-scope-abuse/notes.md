# OAuth 2.0 Token Hijacking & Scope Abuse Detector

## Lab 1 – Learning Notes

---

# Problem Statement Overview

This lab is based on the cybersecurity hackathon problem statement:

**OAuth 2.0 Token Hijacking & Scope Abuse Detector**

The objective is to understand how OAuth-based systems work, how attackers abuse excessive permissions, and how stolen tokens can be misused to gain unauthorized access to user data.

The project focuses on:

* Identity & Access Management (IAM)
* OAuth 2.0
* Access Tokens
* OAuth Scopes
* Scope Abuse
* Token Hijacking
* OAuth Security Analysis

---

# Identity and Access Management (IAM)

Identity and Access Management (IAM) is a security framework that manages digital identities and controls access to resources.

IAM answers two important questions:

1. Who are you?
2. What are you allowed to do?

IAM is used to secure:

* User Accounts
* Applications
* APIs
* Databases
* Cloud Resources
* Enterprise Systems

---

# Identity

Identity refers to a unique digital entity within a system.

Examples:

* Student
* Faculty Member
* Administrator
* GitHub User
* Google Account
* AWS Account

Every identity must be uniquely identifiable.

---

# Authentication

Authentication is the process of verifying identity.

Authentication answers:

**"Can you prove who you are?"**

Examples:

* Username and Password
* OTP
* Fingerprint
* Face Recognition
* Multi-Factor Authentication (MFA)

Example:

A student logs into a university portal using their credentials.

The system verifies those credentials before granting access.

---

# Authorization

Authorization determines what an authenticated user can access or perform.

Authorization answers:

**"What are you allowed to do?"**

Example:

A student can:

* View grades
* View attendance

A student cannot:

* Modify grades
* Create user accounts

Authorization occurs after authentication.

---

# Authentication vs Authorization

| Authentication    | Authorization                |
| ----------------- | ---------------------------- |
| Verifies identity | Determines permissions       |
| "Who are you?"    | "What can you do?"           |
| Happens first     | Happens after authentication |

---

# OAuth 2.0

OAuth 2.0 (Open Authorization) is an authorization framework that allows third-party applications to access user resources without exposing the user's credentials.

OAuth is currently the industry-standard authorization framework used by:

* Google
* Microsoft
* GitHub
* LinkedIn
* Amazon
* Numerous SaaS platforms

OAuth enables secure data sharing using tokens instead of passwords.

---

# Why OAuth Exists

Without OAuth:

A third-party application would require the user's password to access resources.

Example:

Canva asks for your Gmail password.

This is insecure because:

* Passwords can be stolen
* Passwords can be reused
* Applications gain excessive trust

OAuth solves this problem.

Instead of sharing passwords:

1. User authenticates with Google.
2. Google asks for permission.
3. User approves access.
4. Google issues an Access Token.
5. Canva accesses approved resources.

The password never leaves Google.

---

# Token-Based Authorization

OAuth 2.0 uses a token-based authorization model.

Instead of sharing usernames and passwords with applications, users grant access through temporary access tokens.

Tokens act as proof that permission has been granted.

Advantages:

* Passwords remain protected
* Permissions can be limited
* Tokens can be revoked
* Third-party applications never see user credentials

---

# OAuth Actors

OAuth defines four primary roles.

---

## Resource Owner

The person who owns the data.

Examples:

* User
* Google Account Holder
* Microsoft Account Holder

---

## Client

The application requesting access.

Examples:

* Canva
* Zoom
* Slack
* Notion

---

## Authorization Server

The system responsible for:

* Authentication
* Consent Management
* Token Issuance

Examples:

* Google Login
* Microsoft Login
* GitHub Login

---

## Resource Server

The server hosting protected resources.

Examples:

* Google APIs
* Microsoft Graph API
* GitHub API

The Resource Server validates tokens before granting access.

---

# OAuth Workflow

OAuth 2.0 enables secure resource sharing using Access Tokens.

Basic Flow:

1. Client requests authorization.
2. Resource Owner authenticates.
3. Resource Owner grants consent.
4. Authorization Server issues Access Token.
5. Client presents Access Token.
6. Resource Server validates the token.
7. Resource Server grants access.

---

# Access Token

An Access Token is a temporary credential issued after successful authorization.

Think of it as a temporary permission ticket.

Properties:

* Temporary
* Revocable
* Permission-Based
* Password-Free

Access Tokens allow applications to act on behalf of users.

---

# Grant Types

Grant Types define how an application obtains an Access Token.

Different application types require different authorization mechanisms.

A Grant Type answers:

**"How was the Access Token obtained?"**

---

## Authorization Code Grant

Most common and most secure OAuth flow.

Used by:

* Google Login
* Microsoft Login
* GitHub Login
* LinkedIn Login

Process:

1. User logs in.
2. User grants permission.
3. Authorization Server issues Authorization Code.
4. Client exchanges code for Access Token.

Advantages:

* Highly secure
* Password never reaches the application
* Recommended for modern applications

---

## Implicit Grant

Older browser-based OAuth flow.

Process:

* Access Token is issued directly to the browser.

Problems:

* Token exposure
* Easier token theft

Status:

Deprecated and no longer recommended.

---

## Client Credentials Grant

Used for machine-to-machine communication.

Examples:

* Monitoring Systems
* Security Tools
* Cloud Services

Characteristics:

* No user involvement
* Application authenticates itself

---

## Resource Owner Password Credentials Grant

Legacy OAuth flow.

Process:

* User provides credentials directly to the application.

Problems:

* Password exposure risk
* Violates OAuth principles

Status:

Rarely used and discouraged.

---

## Device Authorization Flow

Designed for devices with limited input capabilities.

Examples:

* Smart TVs
* Gaming Consoles
* IoT Devices

Process:

1. Device displays a code.
2. User visits a verification URL on another device.
3. User approves access.
4. Device receives Access Token.

---

# Scope

A Scope defines what permissions are granted to an Access Token.

A Grant Type answers:

**"How did the application get the token?"**

A Scope answers:

**"What can the token do?"**

Examples:

* email
* profile
* contacts.read
* mail.read
* mail.readwrite
* offline_access

---

# Common OAuth Scopes

## email

Allows access to the user's email address.

---

## profile

Allows access to profile information.

---

## contacts.read

Allows reading contact information.

---

## mail.read

Allows reading emails.

---

## mail.readwrite

Allows:

* Reading emails
* Writing emails
* Modifying emails
* Deleting emails

High-risk permission.

---

## offline_access

Allows long-term access without requiring repeated authentication.

High-risk permission.

---

# Granular Access Control

OAuth supports granular access control.

Instead of granting full account access, users can approve specific permissions.

Examples:

* email
* profile
* contacts.read

Granular access control supports the Principle of Least Privilege.

---

# Principle of Least Privilege

Users and applications should receive only the permissions necessary to perform their tasks.

Excessive permissions increase risk.

Least Privilege reduces:

* Attack Surface
* Data Exposure
* Unauthorized Access

---

# Scope Abuse

Scope Abuse occurs when an application receives more permissions than necessary.

Example:

An application only requires:

* email
* profile

Instead it requests:

* contacts.read
* mail.read
* mail.readwrite
* offline_access

This results in excessive privileges.

---

# Risks of Scope Abuse

Excessive scopes may allow attackers to:

* Read Emails
* Modify Emails
* Download Contacts
* Access Sensitive Data
* Maintain Long-Term Access

Scope Abuse violates the Principle of Least Privilege.

---

# Permission Revocation

OAuth permissions are not permanent.

Users can revoke previously granted permissions.

Once revoked:

* Tokens become invalid
* Applications lose access

This gives users control over third-party integrations.

---

# Token Hijacking

Token Hijacking occurs when an attacker steals a valid Access Token and uses it to impersonate a legitimate user.

The attacker does not need:

* Username
* Password

The stolen token itself provides access.

---

# Common Sources of Token Theft

* Browser Storage
* Local Storage
* Session Storage
* Malware
* Application Logs
* Browser Extensions
* Insecure APIs

---

# Why Token Hijacking Is Dangerous

A stolen Access Token may allow attackers to:

* Access Protected Resources
* Read Sensitive Data
* Perform Actions as the User
* Maintain Persistence

without knowing the user's credentials.

---

# OAuth Security Best Practices

## Use Short-Lived Access Tokens

Tokens should expire quickly to reduce risk if stolen.

---

## Use Refresh Tokens

Refresh Tokens allow applications to obtain new Access Tokens without requiring users to log in again.

(To be studied later.)

---

## Apply Least Privilege

Request only the permissions that are required.

---

## Protect Tokens

Tokens must be secured during:

* Storage
* Transmission
* Logging

---

## Validate Tokens

Resource Servers should verify:

* Signature
* Expiration Time
* Issuer
* Audience

before granting access.

---

# Key Concepts Summary

| Concept         | Meaning                           |
| --------------- | --------------------------------- |
| Identity        | Who the user is                   |
| Authentication  | Verifying identity                |
| Authorization   | Determining permissions           |
| OAuth 2.0       | Authorization framework           |
| Access Token    | Temporary permission credential   |
| Grant Type      | Method used to obtain a token     |
| Scope           | Permission assigned to a token    |
| Scope Abuse     | Excessive permissions granted     |
| Token Hijacking | Theft and misuse of access tokens |

---

# Current Understanding of the Hackathon Problem

The hackathon problem focuses primarily on:

1. Discovering OAuth-connected applications.
2. Identifying dangerous scopes.
3. Detecting Scope Abuse.
4. Calculating Risk Levels.
5. Understanding Token Theft Scenarios.
6. Helping defenders identify risky OAuth integrations.

The project is therefore focused on OAuth Security Analysis rather than OAuth Authentication Implementation.

---

# Topics Pending

The following concepts will be studied later:

* Refresh Tokens
* Token Expiration
* Token Rotation
* Consent Screens
* Redirect URIs
* JWT Fundamentals
* OAuth Threat Models
* MITRE ATT&CK Mapping
* OAuth Detection Techniques
