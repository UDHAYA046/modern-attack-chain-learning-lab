# Learning Journal

This document summarizes the major lessons learned throughout the Modern Attack Chain Learning Lab.

---

# Lab 1 — OAuth Scope Abuse

## Topics Learned

- OAuth 2.0
- Access Tokens
- Refresh Tokens
- Scopes
- JWT
- Least Privilege

## Key Lesson

Excessive permissions increase attack surface.

Always grant the minimum permissions required.

---

# Lab 2 — DNS Tunneling Detection

## Topics Learned

- DNS Protocol
- Entropy
- Base64 Encoding
- Subdomain Analysis
- Detection Rules

## Key Lesson

DNS can become a covert communication channel.

Monitoring and anomaly detection are critical.

---

# Lab 3 — S3 Bucket Misconfiguration

## Topics Learned

- S3 Buckets
- ACLs
- Bucket Policies
- Encryption
- Versioning
- Sensitive Files

## Key Lesson

Most cloud breaches are caused by configuration mistakes rather than software vulnerabilities.

---

# Lab 4 — JWT Authentication Bypass

## Topics Learned

- JWT Structure
- Claims
- HS256
- RS256
- alg:none
- Algorithm Confusion
- Claim Forgery

## Key Lesson

Never trust token-supplied algorithms.

Always perform strict algorithm validation.

---

# Lab 5 — TLS Certificate Pinning & MitM

## Topics Learned

- HTTPS
- TLS Handshake
- PKI
- X.509 Certificates
- Certificate Authorities
- mitmproxy
- Certificate Pinning
- SHA256 Fingerprints
- Primary Pins
- Backup Pins
- Rotation Support
- Fail Closed Validation

## Key Lesson

Certificate pinning protects applications from rogue certificates and Man-in-the-Middle attacks.

---

# Overall Learning

Modern attacks span multiple domains.

```text
Identity
↓
Network
↓
Cloud
↓
Application
↓
Cryptography
```

Understanding the attack chain is essential for designing secure systems.

---

# Long-Term Goal

Develop practical expertise in:

- Security Engineering
- Cloud Security
- Application Security
- Network Security
- Cryptography
- Secure System Design

while maintaining a strong defensive mindset.