# Lab 3 – S3 Bucket Misconfiguration Scanner & Data Exposure Detector

## Domain

**Cloud Security**

---

## Architecture

**Cloud-Native**

---

## MITRE ATT&CK Mapping

**T1530 – Data from Cloud Storage**

---

# Problem Statement

Organizations often maintain hundreds of S3 buckets created by different teams. Misconfigurations such as public access, disabled encryption, missing bucket policies, and exposed sensitive files can lead to severe data breaches.

This lab focuses on identifying insecure S3 bucket configurations, assessing risk levels, and generating remediation recommendations.

---

# Background

Amazon S3 is one of the most widely used cloud storage services.

Misconfigured buckets have caused numerous real-world incidents involving:

* Customer data exposure
* Backup leaks
* Source code disclosure
* Credential exposure
* Ransomware damage
* Public file access

This project simulates a cloud posture management tool that continuously evaluates bucket configurations and highlights security risks.

---

# Objectives

Build an automated S3 Security Analyzer capable of:

* Enumerating bucket configurations
* Detecting public access exposure
* Detecting missing encryption
* Detecting disabled versioning
* Detecting missing bucket policies
* Detecting static website hosting exposure
* Detecting sensitive files
* Assigning risk scores
* Classifying severity levels
* Generating remediation recommendations
* Producing JSON, CSV and HTML reports
* Simulating remediation actions using dry-run mode

---

# Learning Goals

After completing this lab, I should be able to:

* Understand Amazon S3 architecture
* Understand S3 security mechanisms
* Identify common bucket misconfigurations
* Understand bucket policies and ACLs
* Understand server-side encryption
* Understand bucket versioning
* Identify sensitive object exposure
* Perform cloud risk assessment
* Generate remediation recommendations
* Map cloud storage attacks to MITRE ATT&CK

---

# Core Concepts Covered

## Amazon S3

* Buckets
* Objects
* ACLs
* Bucket Policies
* Versioning
* Server-Side Encryption
* Static Website Hosting

---

## Cloud Security Concepts

* Least Privilege
* Data Exposure
* Public Access
* Encryption
* Backup Protection
* Sensitive File Discovery
* Cloud Security Posture Management (CSPM)

---

## Standards and Frameworks

* AWS S3
* IAM
* MITRE ATT&CK
* Principle of Least Privilege

---

# Attack Chain

```text
Misconfigured Bucket
            ↓
Public Access Enabled
            ↓
Sensitive Files Exposed
            ↓
Unauthorized Access
            ↓
Data Theft
            ↓
Credential Leakage
            ↓
Business Impact
```

---

# Misconfigurations Detected

## Public ACL

Examples:

* READ permissions granted to everyone
* WRITE permissions granted to everyone

Risk:

Unauthorized users may access bucket contents.

---

## Public Bucket Policy

Examples:

```json
"Principal": "*"
```

Risk:

Entire Internet may access bucket resources.

---

## Missing Bucket Policy

Risk:

No fine-grained access controls exist.

---

## Missing Encryption

Risk:

Data stored without server-side encryption.

Supported recommendations:

* SSE-S3
* SSE-KMS

---

## Disabled Versioning

Risk:

Objects can be permanently deleted.

Versioning protects against:

* Accidental deletion
* Ransomware
* Overwrites

---

## Website Hosting Exposure

Risk:

Sensitive files may become publicly accessible.

---

## Sensitive Files

Examples:

```text
database.sql
backup.zip
users.csv
passwords.txt
.env
private.pem
secret.txt
config.json
```

Risk:

Credential leakage and confidential data exposure.

---

# Risk Scoring Engine

| Condition               | Score |
| ----------------------- | ----- |
| Public ACL              | +10   |
| Public Bucket Policy    | +10   |
| Missing Bucket Policy   | +5    |
| Missing Encryption      | +8    |
| Versioning Disabled     | +6    |
| Website Hosting Enabled | +4    |
| Sensitive Files Present | +10   |

---

# Severity Classification

| Risk Score | Severity |
| ---------- | -------- |
| 0–9        | Low      |
| 10–19      | Medium   |
| 20–29      | High     |
| 30+        | Critical |

---

# Architecture

```text
Bucket Dataset
        ↓
Bucket Analyzer
        ↓
Misconfiguration Engine
        ↓
Risk Scoring Engine
        ↓
Recommendation Engine
        ↓
Dry-Run Remediation Engine
        ↓
JSON Report
CSV Summary
HTML Dashboard
```

---

# Features Implemented

### Bucket Analysis

* Public ACL detection
* Public bucket policy detection
* Missing bucket policy detection
* Encryption checks
* Versioning checks
* Website hosting checks
* Sensitive file detection

### Risk Assessment

* Risk score calculation
* Severity classification

### Reporting

* JSON report generation
* CSV summary generation
* HTML dashboard generation

### Remediation Simulation

Dry-run actions simulate:

* Enable Block Public Access
* Remove public ACLs
* Restrict bucket policies
* Enable AES256 encryption
* Enable versioning
* Review website hosting configuration
* Quarantine sensitive files

---

# Folder Structure

```text
03-cloud-s3-misconfiguration
│
├── README.md
├── notes.md
│
├── src
│     └── s3_bucket_scanner.py
│
├── sample-data
│     └── s3_buckets.json
│
├── reports
│     ├── s3_security_report.json
│     ├── s3_risk_summary.csv
│     └── s3_dashboard.html
│
└── terminal_screenshots.docx
```

---

# Example Output

```json
{
  "bucket_name": "customer-data-archive",
  "risk_score": 39,
  "severity": "Critical",
  "findings": [
    "Public ACL detected",
    "Missing bucket policy",
    "Encryption disabled",
    "Versioning disabled",
    "Sensitive files detected"
  ]
}
```

---

# MITRE ATT&CK Mapping

| Technique ID | Technique                      |
| ------------ | ------------------------------ |
| T1530        | Data from Cloud Storage        |
| T1485        | Data Destruction               |
| T1567        | Exfiltration Over Web Services |
| T1078        | Valid Accounts                 |

---

# Security Boundary

This project is intended solely for defensive learning purposes.

The project:

* Does not connect to real AWS accounts
* Does not modify real S3 buckets
* Does not perform unauthorized actions
* Uses simulated bucket metadata
* Performs dry-run remediation only

---

# Expected Outcome

Upon completion, this lab demonstrates how cloud defenders can identify S3 bucket misconfigurations, assess risk, detect sensitive file exposure, simulate remediation actions, and generate security reports similar to Cloud Security Posture Management (CSPM) tools.

---

# References

* AWS S3 Documentation
* AWS Security Best Practices
* MITRE ATT&CK
* OWASP Cloud Security Guidelines
* AWS Well-Architected Framework
