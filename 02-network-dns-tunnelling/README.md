# Lab 2 – DNS Tunnelling Detection Engine

## Domain

**Network Security**

---

## Problem Statement

Design a DNS Tunnelling Detection Engine capable of identifying suspicious DNS traffic using query length, entropy, subdomain depth, suspicious patterns, and domain behavior analysis.

This lab focuses on detecting abnormal DNS activity that may indicate DNS tunnelling, data exfiltration, command and control communication, or DGA-like behavior.

---

## Objective

Build a defensive DNS Tunnelling Detection Engine capable of:

* Analyzing DNS query datasets
* Calculating query length
* Calculating Shannon entropy
* Measuring subdomain depth
* Detecting suspicious keywords and repeated patterns
* Handling known legitimate cloud/CDN domains
* Assigning risk scores
* Classifying domains as Low, Medium, High, or Critical risk
* Generating JSON, CSV, and HTML reports

---

## Core Concepts Covered

* DNS Fundamentals
* DNS Resolution
* DNS Record Types
* DNS Tunnelling
* Base64 Encoding
* TXT Record Abuse
* CNAME Abuse
* Query Length Analysis
* Shannon Entropy
* Subdomain Depth
* Query Frequency
* Beaconing
* Command and Control
* Domain Generation Algorithms
* False Positives
* MITRE ATT&CK T1071.004

---

## Detection Pipeline

```text
DNS Query Dataset
        ↓
Feature Extraction
        ↓
Query Length
Entropy
Subdomain Depth
Suspicious Pattern Detection
        ↓
Risk Scoring Engine
        ↓
Risk Classification
        ↓
Recommendations
        ↓
JSON Report
CSV Summary
HTML Dashboard
```

---

## Implemented Features

The final version of this lab includes:

* DNS query dataset analysis
* Shannon entropy calculation
* Query length detection
* Subdomain depth analysis
* Suspicious keyword detection
* Known legitimate domain handling
* Risk scoring and classification
* Security recommendation generation
* JSON report generation
* CSV summary generation
* HTML dashboard generation

---

## Risk Classification

| Risk Level | Score Range | Meaning                                                        |
| ---------- | ----------: | -------------------------------------------------------------- |
| Low        |         0–4 | Normal or known legitimate DNS behavior                        |
| Medium     |         5–8 | Some suspicious indicators present                             |
| High       |        9–12 | Multiple suspicious DNS indicators present                     |
| Critical   |         13+ | Strong indicators of DNS tunnelling or malicious communication |

---

## Example Suspicious Indicators

The detector looks for:

* Extremely long domains
* Random-looking domains
* High entropy values
* Deep subdomain structures
* Repeated chunk-like patterns
* Suspicious terms such as `attacker`, `chunk`, `secret`, `payload`, `malware`, and `command`

---

## Example Input

```json
{
  "domain": "chunk1.chunk2.chunk3.attacker.com",
  "timestamp": "2026-06-18 10:00:05"
}
```

---

## Example Output

```json
{
  "domain": "chunk1.chunk2.chunk3.attacker.com",
  "query_length": 33,
  "entropy": 3.65,
  "subdomain_depth": 3,
  "risk_score": 10,
  "risk_level": "High",
  "findings": [
    "Moderately long DNS query.",
    "Moderate entropy detected.",
    "Moderate subdomain depth detected.",
    "Suspicious keywords detected: attacker, chunk"
  ],
  "recommendations": [
    "Investigate domain for possible exfiltration or attacker-controlled infrastructure."
  ]
}
```

---

## Generated Outputs

### JSON Report

```text
dns_tunnelling_report.json
```

Detailed domain-by-domain detection output.

### CSV Summary

```text
dns_risk_summary.csv
```

Tabular summary for review and reporting.

### HTML Dashboard

```text
dns_tunnelling_dashboard.html
```

Visual dashboard containing:

* Domain names
* Query length
* Entropy
* Subdomain depth
* Risk score
* Risk level
* Findings
* Recommendations

---

## Folder Structure

```text
02-network-dns-tunnelling/
│
├── README.md
├── notes.md
│
├── sample-data/
│   └── dns_queries.json
│
├── reports/
│   ├── dns_tunnelling_report.json
│   ├── dns_risk_summary.csv
│   └── dns_tunnelling_dashboard.html
│
└── src/
    └── dns_tunnelling_detector.py
```

---

## MITRE ATT&CK Mapping

| Technique ID | Technique                       |
| ------------ | ------------------------------- |
| T1071.004    | Application Layer Protocol: DNS |
| T1001        | Data Obfuscation                |
| T1105        | Ingress Tool Transfer           |
| T1095        | Non-Application Layer Protocol  |

---

## Security Boundary

This project is for educational and defensive learning purposes only.

It does not:

* Perform DNS tunnelling
* Exfiltrate real data
* Contact attacker-controlled infrastructure
* Capture live traffic without permission
* Attack any real network

All DNS data used in this lab is simulated and safe.

---

## Learning Outcome

After completing this lab, I should be able to:

* Explain how DNS works
* Understand how DNS tunnelling hides data
* Calculate query length, entropy, and subdomain depth
* Identify suspicious DNS indicators
* Understand beaconing and C2 concepts
* Reduce false positives by considering known legitimate domains
* Generate JSON, CSV, and HTML security reports
* Map DNS abuse to MITRE ATT&CK techniques

---

## References

* DNS Protocol Fundamentals
* MITRE ATT&CK T1071.004
* DNS Tunnelling Detection Concepts
* Shannon Entropy
* Network Traffic Analysis
