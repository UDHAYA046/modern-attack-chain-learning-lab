# Modern Attack Chain Learning Lab

## Overview

Modern cyber attacks rarely involve a single technique. Attackers often move across multiple domains, exploiting weaknesses in identity, network infrastructure, cloud environments, applications, and cryptographic implementations.

This repository is organized to study the complete attack chain from both offensive and defensive perspectives.

---

## Attack Chain

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

---

## Labs

| Lab | Domain | Topic | MITRE ATT&CK |
|------|---------|--------|---------------|
| Lab 1 | Identity | OAuth Scope Abuse | T1528 |
| Lab 2 | Network | DNS Tunneling Detection | T1071.004 |
| Lab 3 | Cloud | S3 Bucket Misconfiguration | T1530 |
| Lab 4 | Application | JWT Authentication Bypass | T1550.001 |
| Lab 5 | Cryptography | TLS Pinning & MitM | T1557, T1040 |

---

## Learning Philosophy

```text
Understand Attack
        ↓
Study Weakness
        ↓
Build Detection
        ↓
Implement Defense
        ↓
Design Secure Systems
```

---

## Domains Covered

### Identity Security

- OAuth
- Access tokens
- Refresh tokens
- Scopes
- Least privilege

---

### Network Security

- DNS protocol
- Tunneling
- Covert channels
- Detection techniques

---

### Cloud Security

- S3 bucket policies
- ACLs
- Encryption
- Versioning
- Sensitive data exposure

---

### Application Security

- JWT
- Claims
- HS256
- RS256
- Algorithm confusion

---

### Cryptography & Data Protection

- TLS
- Certificates
- PKI
- Certificate pinning
- MITM attacks
- Secure communication

---

## Goal

Build practical understanding of modern attack techniques and the defensive mechanisms required to secure real-world systems.