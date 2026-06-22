# Lab 4 – JWT Authentication Bypass & Algorithm Confusion Attack

## Domain

**Application Security**

---

## Problem Statement

A REST API uses JWT tokens for authentication. The API server contains misconfigurations that allow attackers to bypass authentication using multiple JWT vulnerabilities.

This lab demonstrates three common JWT attack vectors:

1. None Algorithm Attack (`alg:none`)
2. Weak Secret Claim Forgery (HS256)
3. RS256 → HS256 Algorithm Confusion Attack

An intentionally vulnerable Flask API is deployed locally to demonstrate how attackers can forge tokens and obtain unauthorized administrative access.

---

## MITRE ATT&CK Mapping

| Technique ID | Technique                             |
| ------------ | ------------------------------------- |
| T1550.001    | Use Alternate Authentication Material |

---

## Objective

Build a complete JWT attack laboratory capable of:

* Creating vulnerable JWT-based APIs
* Exploiting insecure JWT implementations
* Demonstrating multiple attack vectors
* Forging arbitrary claims
* Obtaining administrative privileges
* Generating attack reports
* Providing secure validation mechanisms
* Demonstrating defensive best practices

---

## Learning Goals

After completing this lab, I should be able to:

* Understand JWT architecture
* Understand JWT structure and claims
* Explain JWT signing algorithms
* Differentiate HS256 and RS256
* Understand JWT verification workflows
* Exploit None Algorithm vulnerabilities
* Understand Algorithm Confusion attacks
* Forge JWT claims
* Implement secure JWT validation
* Apply JWT hardening practices

---

# JWT Fundamentals

A JSON Web Token consists of three parts:

```text
Header.Payload.Signature
```

Example:

```text
xxxxx.yyyyy.zzzzz
```

---

## Header

Contains metadata:

```json
{
  "alg": "RS256",
  "typ": "JWT"
}
```

---

## Payload

Contains claims:

```json
{
  "username": "alice",
  "role": "user"
}
```

---

## Signature

Ensures integrity and authenticity.

---

# Attack Vectors Demonstrated

## 1. None Algorithm Attack

The server accepts:

```json
{
    "alg":"none"
}
```

Unsigned JWTs are accepted without verification.

### Result

Attacker creates:

```json
{
    "role":"admin"
}
```

Administrative access is obtained.

---

## 2. Weak Secret Claim Forgery

Weak HS256 secrets such as:

```text
secret123
```

allow attackers to forge JWTs.

### Result

Admin claims are inserted:

```json
{
    "role":"admin"
}
```

Administrative access is granted.

---

## 3. RS256 → HS256 Algorithm Confusion

The attacker abuses algorithm switching:

```text
RS256
↓
HS256
↓
Public key used as HMAC secret
↓
Forged token accepted
```

### Result

Administrative privileges are obtained.

---

# Final Architecture

```text
                RSA Key Pair
                       │
                       ▼
              Vulnerable Flask API
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
 None Attack     Weak Secret      Algorithm
                  Forgery          Confusion
       │               │               │
       └───────────────┼───────────────┘
                       ▼
                Admin Access Obtained
                       │
                       ▼
               Attack Report Generator
                       │
                       ▼
          JSON Reports + HTML Dashboard
                       │
                       ▼
                Secure Validator
                       │
                       ▼
                Attack Blocked
```

---

# Folder Structure

```text
04-application-jwt-security
│
├── attacker-tool
│   └── jwt_attack_toolkit.py
│
├── vulnerable-api
│   ├── generate_keys.py
│   └── vulnerable_api.py
│
├── secure-validator
│   └── secure_validator.py
│
├── keys
│   ├── private.pem
│   └── public.pem
│
├── sample-data
│   └── sample_tokens.json
│
├── reports
│   ├── jwt_attack_report.json
│   └── jwt_dashboard.html
│
├── screenshots
│
├── notes.md
└── README.md
```

---

# Components

## Vulnerable Flask API

Provides:

* `/login`
* `/profile`
* `/admin`

Contains intentional JWT validation flaws.

---

## JWT Attack Toolkit

Generates:

* None Algorithm Tokens
* Weak Secret Tokens
* Algorithm Confusion Tokens

Automatically launches attacks against the vulnerable API.

---

## Secure Validator

Demonstrates proper JWT validation.

Blocks:

* None Algorithm Attack
* Weak Secret Forgery
* Algorithm Confusion Attack

---

## Reports Generated

### JSON Report

```text
jwt_attack_report.json
```

Contains:

* Attack name
* Vulnerability
* Status code
* Attack result
* Severity
* Response
* Defense recommendations

---

### HTML Dashboard

```text
jwt_dashboard.html
```

Displays:

* Attack vectors
* Success status
* Severity
* Defensive recommendations

---

# Technologies Used

* Python
* Flask
* PyJWT
* Cryptography
* Requests
* JSON
* HTML

---

# Defensive Recommendations

### Enforce Algorithm Pinning

Always specify:

```python
algorithms=["RS256"]
```

---

### Reject alg:none

Unsigned tokens must never be accepted.

---

### Use Strong Secrets

Avoid weak secrets such as:

```text
secret123
```

---

### Prefer RS256

Use asymmetric signing instead of shared secrets.

---

### Verify Standard Claims

Validate:

* exp
* nbf
* iat
* iss
* aud

---

### Secure Key Management

Protect:

* Private keys
* Public keys
* Signing secrets

---

## Security Boundary

This project is intended exclusively for educational and defensive purposes.

The lab:

* Runs locally
* Uses intentionally vulnerable APIs
* Targets no real systems
* Performs no unauthorized access

---

# Expected Outcome

Upon completion, this lab demonstrates how insecure JWT implementations can lead to authentication bypass and privilege escalation. It also shows how proper validation and algorithm pinning can prevent these attacks.

---

# References

* RFC 7519 – JSON Web Token
* OWASP JWT Cheat Sheet
* PyJWT Documentation
* Flask Documentation
* MITRE ATT&CK T1550.001
