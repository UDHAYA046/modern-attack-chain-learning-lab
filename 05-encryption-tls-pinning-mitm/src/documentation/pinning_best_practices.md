# Certificate Pinning Best Practices

## Purpose

Certificate pinning strengthens HTTPS by ensuring that an application trusts only known certificates or public keys instead of trusting every certificate issued by any trusted Certificate Authority.

---

## Recommended Pinning Type

Use SPKI or public key pinning instead of full certificate pinning.

Public key pinning is more flexible because certificates can be renewed while retaining the same public key.

---

## Use SHA256

Use SHA256 fingerprints.

Avoid:

- MD5
- SHA1

SHA256 provides stronger collision resistance and is widely used in modern security systems.

---

## Use Primary and Backup Pins

Applications should never depend on a single pin.

Use:

- Primary pin
- Backup pin

This supports certificate rotation and prevents application outages.

---

## Support Certificate Rotation

Certificates expire and must be renewed.

A safe rotation model is:

```text
Current:
Primary = A
Backup = B

After Rotation:
Primary = B
Backup = C

This ensures continuity.

Fail Closed

If no pin matches, the connection must be rejected.

Correct:

Pin mismatch
↓
Reject connection

Incorrect:

Pin mismatch
↓
Continue anyway

Continuing after failure defeats certificate pinning.

Do Not Disable TLS Validation

Avoid insecure patterns such as:

Trust all certificates
Ignore SSL errors
Disable hostname verification

These mistakes allow Man-in-the-Middle interception.

Protect Against Runtime Tampering

Certificate pinning should be combined with:

Root detection
Emulator detection
Integrity checks
Debugger detection
Backend validation
Use Defense in Depth

Certificate pinning is one layer.

A secure mobile application should combine:

TLS
Certificate Pinning
Root Detection
Integrity Checks
Authentication
Authorization
Backend Monitoring
Summary

Strong pinning requires:

SHA256 fingerprints
Public key pinning
Primary pins
Backup pins
Rotation support
Fail closed validation
Defense in depth

---

## `src/documentation/attack_vs_defense.md`

```md
# TLS MitM Attack vs Certificate Pinning Defense

## Normal HTTPS Flow

```text
Application
↓
HTTPS
↓
Server

The application validates the server certificate using the operating system trust store.

MitM Proxy Flow
Application
↓
mitmproxy
↓
Server

The proxy creates two TLS sessions:

Application ↔ mitmproxy
mitmproxy ↔ Server

This allows the proxy to decrypt and inspect traffic.

How mitmproxy Intercepts HTTPS

mitmproxy creates a dynamic certificate for the target domain and signs it using the mitmproxy root CA.

If the device trusts the mitmproxy root CA, the application may accept the generated certificate.

What the Proxy Can See

If interception succeeds, the proxy may see:

URLs
Headers
Cookies
Tokens
JSON request bodies
JSON response bodies
Status codes
Certificate Pinning Defense

Certificate pinning changes the trust model.

Instead of trusting every certificate signed by a trusted CA, the application trusts only a specific certificate or public key.

Pinning Validation Flow
Certificate received
↓
Extract public key
↓
Generate SHA256 fingerprint
↓
Compare with primary pin
↓
Compare with backup pin
↓
Accept or reject
Why Pinning Blocks MITM

The mitmproxy certificate does not match the expected pinned certificate or public key.

Result:

Pin mismatch
↓
TLS handshake fails
↓
Traffic is not exposed
Attack Side

The attack demonstrates:

Proxy-based interception
Dynamic certificate generation
HTTPS traffic visibility when trusted
MITRE T1557 Adversary-in-the-Middle
MITRE T1040 Network Sniffing
Defense Side

The defense demonstrates:

SHA256 pin validation
Primary pin
Backup pin
Rotation support
Fail closed behavior
Defense in depth
Final Comparison
Area	MitM Attack	Certificate Pinning Defense
Trust Model	Trusts proxy CA	Trusts only pinned keys
Traffic Visibility	Proxy can inspect	Proxy blocked
Certificate Handling	Dynamic fake certificate	Fingerprint validation
Failure Behavior	Traffic exposed	Connection rejected
Security Goal	Intercept traffic	Prevent interception

---

## `src/sample-data/intercepted_requests.json`

Paste this starter data so reports work even before real mitmproxy capture:

```json
[
    {
        "timestamp": "2026-06-23 10:00:00",
        "method": "GET",
        "url": "https://example.com/api/status",
        "host": "example.com",
        "path": "/api/status",
        "request_headers": {
            "User-Agent": "HTTP Toolkit Demo App",
            "Accept": "application/json"
        },
        "status_code": 200,
        "response_headers": {
            "content-type": "application/json"
        },
        "content_type": "application/json",
        "response_size_bytes": 128
    },
    {
        "timestamp": "2026-06-23 10:00:05",
        "method": "POST",
        "url": "https://example.com/api/login",
        "host": "example.com",
        "path": "/api/login",
        "request_headers": {
            "Content-Type": "application/json"
        },
        "status_code": 200,
        "response_headers": {
            "content-type": "application/json"
        },
        "content_type": "application/json",
        "response_size_bytes": 256
    },
    {
        "timestamp": "2026-06-23 10:00:10",
        "method": "GET",
        "url": "https://pinned.badssl.com/",
        "host": "pinned.badssl.com",
        "path": "/",
        "request_headers": {
            "User-Agent": "Pinned Certificate Demo"
        },
        "status_code": 495,
        "response_headers": {
            "content-type": "text/plain"
        },
        "content_type": "text/plain",
        "response_size_bytes": 64
    }
]

