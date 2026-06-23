# TLS Certificate Pinning Bypass & MitM Attack

A controlled local lab demonstrating HTTPS traffic interception concepts, TLS certificate pinning, defensive validation, and certificate rotation mechanisms. This project explores both attack and defense perspectives in secure mobile communication while emphasizing safe, educational use.

---

## MITRE ATT&CK Mapping

- **T1557 – Adversary-in-the-Middle**
- **T1040 – Network Sniffing**

---

## Objectives

- Understand HTTPS interception architecture.
- Analyze TLS traffic using mitmproxy.
- Study certificate pinning concepts.
- Implement primary and backup pin validation.
- Demonstrate certificate rotation support.
- Enforce fail-closed behavior.
- Generate JSON reports and HTML dashboards.
- Document attack and defense techniques.

---

## Folder Structure

```text
05-encryption-tls-pinning-mitm
│
├── README.md
├── notes.md
│
└── src
    │
    ├── mitm_logger.py
    ├── generate_mitm_report.py
    ├── secure_certificate_pinning.py
    │
    ├── sample-data
    │     intercepted_requests.json
    │
    ├── documentation
    │     attack_vs_defense.md
    │     pinning_best_practices.md
    │
    ├── reports
    │     mitm_report.json
    │     mitm_dashboard.html
    │     pinning_validation_report.json
    │
    └── screenshots
```

---

## Components

### mitm_logger.py

Captures HTTPS traffic passing through mitmproxy and stores:

- Timestamp
- HTTP method
- URL
- Host
- Path
- Headers
- Status code
- Content type
- Response size

Output:

```text
sample-data/intercepted_requests.json
```

---

### generate_mitm_report.py

Processes captured traffic and generates:

#### JSON Report

```text
reports/mitm_report.json
```

#### HTML Dashboard

```text
reports/mitm_dashboard.html
```

The dashboard summarizes:

- Request statistics
- HTTP methods
- Status codes
- Hosts
- Traffic details

---

### secure_certificate_pinning.py

Implements defensive certificate pinning using:

- SHA256 fingerprints
- SPKI public key pinning
- Primary pin
- Backup pin
- Rotation support
- Fail-closed validation

Generates:

```text
reports/pinning_validation_report.json
```

---

## Defensive Pinning Model

```text
Certificate Received
        ↓
Extract Public Key
        ↓
Generate SHA256 Fingerprint
        ↓
Compare With Primary Pin
        ↓
Match ?
   Yes → Allow
        ↓
   No
        ↓
Compare With Backup Pin
        ↓
Match ?
   Yes → Allow
        ↓
   No
        ↓
Reject Connection
```

---

## Certificate Rotation

Current State

```text
Primary = A
Backup = B
```

After Rotation

```text
Primary = B
Backup = C
```

This ensures service continuity without breaking clients.

---

## Defense In Depth

The project demonstrates layered security:

```text
TLS
↓
Certificate Pinning
↓
Primary Pin
↓
Backup Pin
↓
Rotation Support
↓
Fail Closed Validation
↓
Secure Communication
```

---

## Installation

Install dependencies:

```bash
pip install mitmproxy cryptography
```

Verify installation:

```bash
mitmproxy --version
```

---

## Running Traffic Analysis

Generate traffic report:

```bash
python 05-encryption-tls-pinning-mitm/src/generate_mitm_report.py
```

Generated files:

```text
reports/
├── mitm_report.json
└── mitm_dashboard.html
```

---

## Running Certificate Validation

Execute:

```bash
python 05-encryption-tls-pinning-mitm/src/secure_certificate_pinning.py
```

Generated file:

```text
reports/pinning_validation_report.json
```

Example Output:

```text
Production Certificate -> Allowed (Primary Pin)

Backup Rotation Certificate -> Allowed (Backup Pin)

mitmproxy Generated Certificate -> Blocked (No Match)

Unknown Rogue Certificate -> Blocked (No Match)
```

---

## Documentation

### attack_vs_defense.md

Explains:

- MITM interception
- Proxy-based HTTPS inspection
- Certificate pinning defenses
- Trust models

### pinning_best_practices.md

Covers:

- SHA256 fingerprints
- SPKI pinning
- Primary and backup pins
- Rotation mechanisms
- Fail-closed behavior
- Defense in depth

---

## Reports Generated

### mitm_report.json

Traffic analysis report.

### mitm_dashboard.html

Interactive dashboard summarizing captured requests.

### pinning_validation_report.json

Certificate validation and rotation report.

---

## Learning Outcomes

- HTTPS architecture
- TLS handshake fundamentals
- Proxy-based interception concepts
- Certificate pinning
- SHA256 fingerprinting
- Public key pinning
- Primary and backup pins
- Certificate rotation
- Fail-closed security
- Defense in depth

---

## Disclaimer

This project is intended solely for educational purposes and controlled local laboratory environments. It demonstrates secure communication principles and defensive certificate validation techniques. No unauthorized interception or misuse is intended.