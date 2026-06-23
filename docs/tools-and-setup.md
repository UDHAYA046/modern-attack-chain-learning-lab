# Tools and Setup

This document summarizes the major tools and technologies used throughout the Modern Attack Chain Learning Lab.

---

# Core Environment

- Python 3.9+
- VS Code
- Git
- GitHub

---

# Libraries

## Data Processing

- pandas
- numpy

---

## Web Frameworks

- Flask
- FastAPI

---

## Security Libraries

- PyJWT
- cryptography

---

## Cloud Libraries

- boto3

---

## Reporting

- json
- Jinja2

---

## Network Analysis

- mitmproxy

---

## Certificate Tools

- OpenSSL

---

## Optional Cloud Environment

- LocalStack
- AWS Free Tier

---

# Lab-wise Tools

---

## Lab 1 — OAuth Scope Abuse

### Technologies

- FastAPI
- PyJWT
- JSON

---

## Lab 2 — DNS Tunneling Detection

### Technologies

- pandas
- collections
- Jinja2

---

## Lab 3 — S3 Bucket Misconfiguration

### Technologies

- boto3
- JSON
- HTML Dashboard

---

## Lab 4 — JWT Authentication Bypass

### Technologies

- Flask
- PyJWT
- cryptography

---

## Lab 5 — TLS Pinning & MitM

### Technologies

- mitmproxy
- cryptography
- OpenSSL

---

# Reporting Formats

JSON Reports

Examples:

- dns_tunneling_report.json
- s3_bucket_report.json
- jwt_attack_report.json
- mitm_report.json

---

HTML Dashboards

Examples:

- dns_dashboard.html
- s3_dashboard.html
- jwt_dashboard.html
- mitm_dashboard.html

---

# Operating Systems

Primary Development Environment:

- Windows 10

Secondary Environment:

- Linux / Kali Linux (future)

---

# Version Control

Git workflow:

```bash
git add .
git commit -m "message"
git push
```

---

# Repository Goal

Use lightweight tools to build educational security labs that simulate modern attack techniques and corresponding defenses.