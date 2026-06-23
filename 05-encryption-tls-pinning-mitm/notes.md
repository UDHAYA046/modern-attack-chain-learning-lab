
# Lab 5 – TLS Certificate Pinning Bypass & MitM Attack

# Part 1 – HTTPS, TLS, Certificates and Trust Foundations

## 1. What is HTTP?

HTTP stands for Hypertext Transfer Protocol.

It is the protocol used by web browsers, mobile applications and APIs to communicate with servers.

Example:

```text
Client
↓
HTTP Request
↓
Server
↓
HTTP Response
```

A client may be:

* Browser
* Mobile app
* Python script
* API client
* Postman
* Android application

Example HTTP request:

```text
GET /profile HTTP/1.1
Host: example.com
```

Example HTTP response:

```text
200 OK
{
  "username": "alice"
}
```

---

## 2. Problem with Plain HTTP

HTTP is not encrypted.

Anyone between the client and server can see the traffic.

Example:

```text
Client
↓
HTTP Request
↓
Network
↓
Server
```

If an attacker is on the same network, they may observe:

* URLs
* Headers
* Cookies
* API tokens
* Login details
* Request body
* Response body

This creates a major security risk.

---

## 3. What is HTTPS?

HTTPS stands for Hypertext Transfer Protocol Secure.

HTTPS is HTTP protected using TLS.

```text
HTTPS = HTTP + TLS
```

HTTPS protects communication between client and server.

It provides:

* Confidentiality
* Integrity
* Authentication

---

## 4. Confidentiality

Confidentiality means outsiders cannot read the data.

Without HTTPS:

```text
password=admin123
```

may be visible on the network.

With HTTPS:

```text
Encrypted unreadable data
```

is visible instead.

---

## 5. Integrity

Integrity means the data cannot be modified silently.

Without integrity protection, an attacker could change:

```text
amount=100
```

to:

```text
amount=100000
```

TLS helps detect tampering.

---

## 6. Authentication

Authentication means the client can verify that it is communicating with the correct server.

Example:

When visiting:

```text
https://bank.com
```

the browser must confirm:

```text
This server really belongs to bank.com
```

This is done using digital certificates.

---

## 7. What is TLS?

TLS stands for Transport Layer Security.

TLS is the cryptographic protocol that secures HTTPS.

Older term:

```text
SSL
```

Modern term:

```text
TLS
```

People still say “SSL certificates,” but technically modern systems use TLS.

---

## 8. TLS Goals

TLS provides:

```text
Confidentiality
Integrity
Authentication
```

These three properties protect modern web and mobile communication.

---

## 9. What is a Certificate?

A certificate is a digital identity document for a server.

It proves that a server owns a domain.

Example:

```text
example.com
```

has a certificate that says:

```text
This public key belongs to example.com
```

A certificate usually contains:

* Domain name
* Public key
* Issuer
* Validity period
* Signature
* Serial number
* Certificate fingerprint

---

## 10. Certificate Example Fields

### Subject

The identity the certificate belongs to.

Example:

```text
CN=example.com
```

---

### Issuer

The authority that issued the certificate.

Example:

```text
DigiCert
Let's Encrypt
GlobalSign
```

---

### Validity Period

Certificates are valid only for a specific time.

Example:

```text
Valid From: 2026-01-01
Valid Until: 2026-04-01
```

Expired certificates should not be trusted.

---

### Public Key

The server’s public key.

Used during TLS negotiation.

---

### Signature

The certificate authority signs the certificate.

This proves the certificate was issued by a trusted authority.

---

## 11. What is a Certificate Authority?

A Certificate Authority, or CA, is an organization trusted to issue certificates.

Examples:

* Let’s Encrypt
* DigiCert
* GlobalSign
* Sectigo

Browsers and operating systems maintain a list of trusted CAs.

This list is called a trust store.

---

## 12. What is a Trust Store?

A trust store is a collection of trusted root certificates.

Operating systems and browsers use it to decide whether a certificate should be trusted.

Example:

```text
Android Trust Store
Windows Trust Store
Chrome Trust Store
Firefox Trust Store
```

If a certificate is signed by a trusted CA, the client accepts it.

If not, the client rejects it.

---

## 13. Certificate Chain

A website certificate is usually not signed directly by a root CA.

Instead, certificates form a chain.

```text
Root CA
↓
Intermediate CA
↓
Server Certificate
```

Example:

```text
Trusted Root CA
↓
Let's Encrypt Intermediate
↓
example.com Certificate
```

The client verifies the entire chain.

If the chain leads to a trusted root CA, the certificate is trusted.

---

## 14. TLS Handshake

The TLS handshake is the process where client and server establish a secure connection.

Simplified flow:

```text
Client
↓
Hello Server
↓
Server Sends Certificate
↓
Client Verifies Certificate
↓
Keys Are Exchanged
↓
Encrypted Session Begins
```

---

## 15. TLS Handshake Step by Step

### Step 1 – Client Hello

The client says:

```text
I want to connect securely.
These are the TLS versions and cipher suites I support.
```

---

### Step 2 – Server Hello

The server replies:

```text
I support this TLS version and cipher suite.
Here is my certificate.
```

---

### Step 3 – Certificate Verification

The client checks:

* Is the certificate valid?
* Is it expired?
* Is the domain name correct?
* Is the certificate signed by a trusted CA?
* Does the certificate chain lead to a trusted root?

---

### Step 4 – Key Exchange

Client and server agree on encryption keys.

These keys protect the session.

---

### Step 5 – Secure Communication

After the handshake, HTTP traffic is encrypted.

```text
HTTP Request
↓
Encrypted by TLS
↓
Sent over network
↓
Decrypted by server
```

---

## 16. What HTTPS Protects Against

HTTPS protects against:

* Passive sniffing
* Credential theft on the wire
* Request tampering
* Response tampering
* Fake server impersonation

---

## 17. What HTTPS Does Not Fully Protect Against

HTTPS does not protect against everything.

It does not protect against:

* Malware already inside the device
* Compromised apps
* User-installed malicious certificates
* Vulnerable certificate validation logic
* Insecure backend APIs
* Poor app security

This is why certificate pinning exists.

---

## 18. Why Mobile Apps Need Extra Protection

Browsers show certificate warnings to users.

Mobile apps usually do not show detailed certificate warnings.

Mobile apps also communicate with APIs silently in the background.

If an attacker manages to install a malicious CA certificate on a device, some apps may trust it.

This can allow HTTPS interception.

Certificate pinning helps prevent this.

---

## 19. Basic HTTPS Trust Model

Normal HTTPS trust depends on this:

```text
If certificate is signed by trusted CA
↓
Accept connection
```

This works for most browsing.

But for high-security mobile apps, this may not be strict enough.

---

## 20. Key Problem

An attacker may install their own CA certificate on a test device.

Then a proxy can generate fake certificates dynamically.

If the app trusts the device trust store, it may accept the proxy certificate.

This enables traffic interception.

Certificate pinning prevents this by saying:

```text
Do not trust every valid CA.
Trust only this exact certificate or public key.
```

---

# Part 1 Summary

HTTP is plain and readable.

HTTPS protects HTTP using TLS.

TLS provides:

* Confidentiality
* Integrity
* Authentication

Certificates prove server identity.

Certificate Authorities issue certificates.

Trust stores contain trusted root CAs.

The TLS handshake verifies certificates and establishes encryption.

Normal HTTPS trusts any certificate signed by a trusted CA.

Certificate pinning adds stricter trust by allowing only specific known certificates or public keys.

This foundation is required before understanding Man-in-the-Middle attacks and certificate pinning.

# Lab 5 – TLS Certificate Pinning Bypass & MitM Attack

# Part 2 – Man-in-the-Middle Attacks, Proxies, HTTP Toolkit and mitmproxy

---

# 1. What is a Man-in-the-Middle Attack?

A Man-in-the-Middle (MitM) attack occurs when an attacker secretly places themselves between two communicating parties.

Instead of:

```text
Client
↓
Server
```

Communication becomes:

```text
Client
↓
Attacker
↓
Server
```

The attacker becomes an intermediary.

---

# 2. Goal of a MitM Attack

The attacker wants to:

* Observe traffic
* Modify traffic
* Steal credentials
* Inject malicious content
* Change requests
* Change responses
* Capture session tokens

---

# 3. Normal Communication

Without a MitM:

```text
Mobile App
↓
HTTPS
↓
API Server
```

Example:

```text
POST /login

username=alice
password=secret
```

Only the server sees the request.

---

# 4. Communication During MitM

With a MitM:

```text
Mobile App
↓
Attacker Proxy
↓
Server
```

The proxy becomes the middleman.

Traffic flow:

```text
App
↓
Proxy
↓
Real Server
↓
Proxy
↓
App
```

---

# 5. Passive vs Active MitM

## Passive MitM

Only observes traffic.

Example:

```text
Client
↓
Attacker listens
↓
Server
```

No modification.

---

## Active MitM

Intercepts and modifies traffic.

Example:

Changing:

```text
amount=100
```

to:

```text
amount=10000
```

---

# 6. Why HTTPS Makes MitM Difficult

HTTPS encrypts communication.

Suppose:

```text
Client
↓
Encrypted Data
↓
Server
```

The attacker sees:

```text
A8F2E19C8B...
```

Instead of:

```text
password=admin123
```

Encryption prevents simple sniffing.

---

# 7. Why Proxies Are Needed

To inspect HTTPS traffic, a proxy must decrypt traffic.

Example:

```text
App
↓
Proxy
↓
Server
```

The proxy acts as:

* Server for the client
* Client for the server

Thus:

```text
App ↔ Proxy ↔ Server
```

Two TLS sessions exist.

---

# 8. Forward Proxy

A forward proxy sits between the client and server.

Examples:

* Burp Suite
* mitmproxy
* HTTP Toolkit

Architecture:

```text
Client
↓
Forward Proxy
↓
Internet
```

---

# 9. Reverse Proxy

Reverse proxies sit in front of servers.

Examples:

* Nginx
* HAProxy
* AWS ALB

Architecture:

```text
Clients
↓
Reverse Proxy
↓
Backend Servers
```

---

# 10. How HTTPS Interception Works

Suppose the client connects to:

```text
https://bank.com
```

The proxy creates:

### Session 1

```text
Client
↓
Proxy
```

### Session 2

```text
Proxy
↓
bank.com
```

The proxy decrypts traffic between both sessions.

Thus it can read everything.

---

# 11. Dynamic Certificate Generation

The proxy creates a fake certificate:

Instead of:

```text
bank.com certificate
```

Client receives:

```text
Proxy-generated bank.com certificate
```

Signed by:

```text
Proxy Root CA
```

If the client trusts this CA:

```text
Client
↓
Trusts Proxy
↓
Traffic decrypted
```

---

# 12. Trust Store Problem

Suppose:

Windows trust store contains:

```text
Proxy Root CA
```

Then:

```text
Fake bank.com certificate
↓
Signed by Proxy CA
↓
Trusted
```

Traffic can be intercepted.

---

# 13. Packet Sniffing vs HTTPS Proxying

## Packet Sniffing

Tools:

* Wireshark
* tcpdump

Can observe:

* IP addresses
* DNS packets
* TLS packets

Cannot decrypt HTTPS.

---

## HTTPS Proxy

Tools:

* Burp Suite
* mitmproxy
* HTTP Toolkit

Can decrypt traffic if certificates are trusted.

---

# 14. What is mitmproxy?

mitmproxy is an open-source HTTPS interception framework.

Written in Python.

Capabilities:

* Inspect requests
* Inspect responses
* Modify headers
* Modify payloads
* Save traffic
* Create scripts
* Generate certificates

Architecture:

```text
App
↓
mitmproxy
↓
Internet
```

---

# 15. Features of mitmproxy

### HTTPS interception

Decrypts HTTPS traffic.

---

### Request inspection

Shows:

```text
URL
Headers
Cookies
Body
```

---

### Response inspection

Shows:

```text
Status codes
JSON
Images
Headers
```

---

### Traffic replay

Can resend requests.

---

### Scripting

Python scripts automate modifications.

---

# 16. What is HTTP Toolkit?

HTTP Toolkit is a GUI-based interception tool.

Internally similar to:

* Burp Suite
* mitmproxy

It provides:

* User-friendly interface
* HTTPS interception
* Mobile support
* Android support
* Desktop support
* Request inspection
* Response inspection

---

# 17. HTTP Toolkit Architecture

```text
Application
↓
HTTP Toolkit
↓
Internet
```

HTTP Toolkit dynamically generates certificates and intercepts HTTPS traffic.

---

# 18. HTTP Toolkit Android Demo

HTTP Toolkit provides an Android SSL pinning demo app.

Purpose:

To demonstrate:

* Normal HTTPS interception
* Certificate pinning
* Pinning failures
* Security concepts

The demo app is intentionally designed for learning.

---

# 19. mitmproxy Workflow

Step 1:

Start proxy

```text
mitmproxy
```

↓

Step 2:

Configure device proxy settings

↓

Step 3:

Install proxy CA certificate

↓

Step 4:

Traffic flows through proxy

↓

Step 5:

Proxy decrypts HTTPS

↓

Step 6:

Requests become visible

---

# 20. Example Intercepted Request

Original request:

```http
POST /login

{
  "username":"alice",
  "password":"secret"
}
```

mitmproxy displays:

```http
POST https://api.demo.com/login

username=alice
password=secret
```

---

# 21. Example Intercepted Response

Server:

```json
{
    "token":"abc123"
}
```

Proxy sees:

```json
{
    "token":"abc123"
}
```

Everything becomes visible.

---

# 22. Why Interception Fails Sometimes

Some apps implement certificate pinning.

During connection:

```text
App
↓
Receives Proxy Certificate
↓
Certificate mismatch
↓
Reject connection
```

Thus:

```text
Proxy cannot decrypt traffic
```

This is exactly why certificate pinning exists.

---

# 23. MitM Detection Indicators

Applications may detect:

### Unexpected certificates

Different fingerprint.

---

### Different public keys

Pin mismatch.

---

### New CA

Proxy CA present.

---

### Debugging environment

Emulators.

---

### Instrumentation frameworks

Dynamic analysis tools.

---

# 24. MITRE ATT&CK Mapping

### T1557

Adversary-in-the-Middle

Description:

Attackers position themselves between communicating parties.

---

### T1040

Network Sniffing

Description:

Capture network traffic.

---

# 25. MitM Flow Summary

Without MitM:

```text
Client
↓
Server
```

With Proxy:

```text
Client
↓
Proxy
↓
Server
```

Proxy terminates TLS twice:

```text
Client ↔ Proxy
Proxy ↔ Server
```

If the client trusts the proxy certificate:

```text
HTTPS becomes visible.
```

If certificate pinning exists:

```text
Connection fails.
```

---

# Key Takeaways

A Man-in-the-Middle attack inserts an intermediary between client and server.

HTTPS normally prevents passive interception.

HTTPS proxies like:

* mitmproxy
* Burp Suite
* HTTP Toolkit

can decrypt traffic if the client trusts their certificate.

These proxies generate certificates dynamically and establish two TLS sessions.

If applications use certificate pinning, the proxy certificate does not match the expected certificate and interception fails.

This forms the foundation for understanding certificate pinning.

# Lab 5 – TLS Certificate Pinning Bypass & MitM Attack

# Part 3 – Certificate Pinning Fundamentals

---

# 1. Why Normal HTTPS Trust Is Sometimes Insufficient

In normal HTTPS, applications trust certificates issued by any trusted Certificate Authority (CA).

Normal trust model:

```text
Server Certificate
↓
Intermediate CA
↓
Root CA
↓
Trusted by OS
↓
Connection Accepted
```

This model works well for browsers.

However, mobile applications often require stronger guarantees.

---

# Problem

Suppose an attacker installs their own CA certificate into the device trust store.

Then:

```text
Attacker CA
↓
Fake Server Certificate
↓
Signed by Attacker CA
↓
Application Trusts It
↓
Traffic Interception Possible
```

Even though TLS encryption still exists, the attacker becomes part of the trusted chain.

---

# Why Banking Apps Need More Protection

Applications such as:

* Banking apps
* Payment systems
* Healthcare apps
* Enterprise applications

cannot trust every CA in the operating system.

Instead they trust only specific certificates.

This is called:

```text
Certificate Pinning
```

---

# 2. What Is Certificate Pinning?

Certificate pinning means:

```text
Do not trust every valid certificate.

Trust only this specific certificate
or
Trust only this specific public key.
```

Normal HTTPS:

```text
Trust Any Trusted CA
```

Certificate Pinning:

```text
Trust Only What I Explicitly Expect
```

---

# Normal HTTPS Trust

```text
Server Certificate
↓
Signed by Any Trusted CA
↓
Accept Connection
```

---

# Certificate Pinning Trust

```text
Server Certificate
↓
Fingerprint Matches Expected Value
↓
Accept Connection

Otherwise

Reject Connection
```

---

# Goal Of Pinning

Prevent:

* HTTPS interception
* Malicious CAs
* Rogue certificates
* Proxy certificates
* Man-in-the-Middle attacks

---

# 3. Pinning Principle

Instead of asking:

```text
Is this certificate valid?
```

The application asks:

```text
Is this EXACTLY the certificate I expect?
```

---

# Example

Expected fingerprint:

```text
A1:B2:C3:D4:E5
```

Received fingerprint:

```text
A1:B2:C3:D4:E5
```

Result:

```text
Connection Allowed
```

---

Received fingerprint:

```text
X8:Y9:Z0:AA
```

Result:

```text
Connection Rejected
```

---

# 4. Fingerprints

Certificates have unique fingerprints.

Fingerprint example:

```text
4A:85:2F:7B:11:92:DD...
```

Usually generated using:

* SHA1
* SHA256

Modern applications prefer:

```text
SHA256
```

because SHA1 is considered weak.

---

# Fingerprint Generation

Certificate

↓

Hash Function

↓

SHA256 Digest

↓

Fingerprint

Example:

```text
Certificate
↓
SHA256
↓
AB34C729...
```

---

# Why Fingerprints Work

Changing even one bit in the certificate changes the fingerprint completely.

Example:

Original:

```text
AB34C729...
```

Modified certificate:

```text
91D8F5AB...
```

Thus fingerprints uniquely identify certificates.

---

# 5. Types Of Pinning

There are two major types:

### Certificate Pinning

Pins the entire certificate.

### Public Key Pinning

Pins only the public key.

---

# Certificate Pinning

Application stores:

```text
Expected Certificate
```

During connection:

```text
Received Certificate
↓
Compare Entire Certificate
↓
Match ?
↓
Accept
```

---

Advantages

* Simple

Disadvantages

* Certificate renewal breaks the app
* Requires updates frequently

---

# Public Key Pinning

Application stores:

```text
Expected Public Key
```

During connection:

```text
Extract Public Key
↓
Compare Public Key
↓
Match
↓
Accept
```

---

Advantages

* Certificate can be renewed
* Same key pair can continue working

Disadvantages

* More complex

---

# Why Public Key Pinning Is Preferred

Certificates expire frequently.

Example:

Every 90 days.

Public key may remain unchanged.

Therefore:

```text
Certificate Changes
↓
Public Key Same
↓
Application Still Works
```

---

# 6. Certificate Pinning Flow

Normal HTTPS:

```text
App
↓
Any Trusted CA
↓
Connection Accepted
```

Pinned HTTPS:

```text
App
↓
Certificate Received
↓
Fingerprint Check
↓
Match
↓
Connection Accepted
```

Mismatch:

```text
Certificate Received
↓
Fingerprint Different
↓
Connection Rejected
```

---

# 7. How Pinning Stops MitM

Attacker:

```text
Proxy Certificate
```

Application expects:

```text
Bank Certificate
```

Comparison:

```text
Fingerprint Mismatch
```

Result:

```text
Handshake Failure
```

Traffic interception becomes impossible.

---

# Example

Normal Flow:

```text
App
↓
Bank Server
↓
Certificate Match
↓
Success
```

Attack Flow:

```text
App
↓
Proxy
↓
Fake Certificate
↓
Fingerprint Mismatch
↓
Reject Connection
```

---

# 8. Public Key Pinning Example

Expected Public Key:

```text
SHA256(XYZ)
```

Received Public Key:

```text
SHA256(XYZ)
```

Success.

Proxy Public Key:

```text
SHA256(ABC)
```

Mismatch.

Connection blocked.

---

# 9. HPKP

HPKP means:

```text
HTTP Public Key Pinning
```

Introduced to protect websites.

Browser receives:

```text
Public-Key-Pins
```

header.

Example:

```text
Public-Key-Pins:
pin-sha256="ABC..."
```

Browser stores the pins.

Future connections must use those pins.

---

# Why HPKP Was Deprecated

HPKP introduced risks.

Problems:

### Self-inflicted Denial Of Service

Incorrect pin:

```text
Users permanently locked out
```

---

### Hostile Pinning

Attackers could pin malicious keys.

---

### Recovery Difficulties

Lost keys could make websites inaccessible.

Because of these problems HPKP was removed from browsers.

---

# 10. Backup Pins

Applications should never depend on one pin.

Bad design:

```text
Primary Pin Only
```

If certificate changes:

```text
Application Breaks
```

---

Good design:

```text
Primary Pin
+
Backup Pin
```

Flow:

```text
Received Certificate
↓
Primary Match?
↓
No
↓
Backup Match?
↓
Yes
↓
Accept
```

---

# Example

Stored:

```text
Pin A
Pin B
```

Server rotates to certificate B.

Application still works.

---

# 11. Certificate Rotation

Certificates expire.

Therefore they must be renewed.

Problem:

Old certificate:

```text
Fingerprint A
```

New certificate:

```text
Fingerprint B
```

Application storing only A will fail.

This is called:

```text
Pinning Failure
```

---

# Solution

Maintain:

```text
Current Pin
Future Pin
```

This allows seamless migration.

---

# 12. Real-World Pinning

Common in:

### Banking Apps

Examples:

* HDFC
* SBI
* ICICI

---

### Payment Apps

Examples:

* PayPal
* Stripe

---

### Enterprise Apps

Corporate applications

---

### Healthcare Applications

Sensitive data protection

---

# 13. Android Pinning

Android uses:

```text
network_security_config.xml
```

Pin example:

```xml
<pin-set>
    <pin digest="SHA-256">
    ABC123...
    </pin>
</pin-set>
```

---

# 14. OkHttp Pinning

Popular Android library:

```text
OkHttp CertificatePinner
```

Example:

```java
CertificatePinner pinner =
new CertificatePinner.Builder()
.add("api.example.com",
"sha256/ABC123...")
.build();
```

---

# 15. iOS Pinning

Common frameworks:

* URLSession
* TrustKit

TrustKit simplifies certificate pinning.

---

# 16. Pinning Failures

Common reasons:

### Expired Certificates

Certificate changes.

---

### Wrong Fingerprint

Incorrect pin configured.

---

### Missing Backup Pin

Rotation impossible.

---

### Development Certificates

Different environments cause mismatches.

---

### CDN Changes

Certificate chain changes.

---

# 17. Pinning Errors

Applications often display:

```text
SSLHandshakeException
```

or

```text
Certificate pinning failure
```

or

```text
Trust anchor not found
```

These indicate pin mismatch.

---

# 18. Advantages Of Certificate Pinning

Protects against:

* Malicious CA
* Rogue CA
* HTTPS proxies
* MitM attacks
* User-installed certificates

Provides stronger trust than traditional HTTPS.

---

# 19. Limitations Of Pinning

Pinning cannot protect against:

* Compromised device
* Malware inside device
* Rooted devices
* Vulnerable application code
* Runtime instrumentation attacks

Therefore pinning should be part of a larger defense strategy.

---

# Summary

Normal HTTPS trusts any valid CA.

Certificate pinning trusts only specific certificates or public keys.

Pinning defeats proxy-based interception because proxy certificates do not match expected fingerprints.

Public key pinning is generally preferred over certificate pinning.

Backup pins are essential to support certificate rotation.

Certificate pinning is widely used in banking, payment and enterprise applications.

It is one of the strongest defenses against Man-in-the-Middle attacks.


# Lab 5 – TLS Certificate Pinning Bypass & MitM Attack

# Part 4 – Why Certificate Pinning Can Fail

---

# 1. Certificate Pinning Is Not Absolute Security

Certificate pinning greatly increases security.

However, it does not make an application impossible to attack.

Security is layered.

Pinning protects against:

* Proxy interception
* Malicious CAs
* User-installed certificates
* Traditional MitM attacks

But it does not protect against:

* Compromised devices
* Malware inside the device
* Vulnerable application code
* Runtime manipulation

---

# Defense in Depth

Security should look like:

```text
TLS
↓
Certificate Pinning
↓
Root Detection
↓
Integrity Checks
↓
Runtime Protection
↓
Backend Validation
```

No single layer is enough.

---

# 2. Trust Store

Operating systems maintain a list of trusted Certificate Authorities.

Examples:

```text
Windows Trust Store
Android Trust Store
iOS Trust Store
Chrome Trust Store
```

These contain root certificates.

Normal HTTPS works like:

```text
Certificate
↓
Chain Verification
↓
Trusted Root CA
↓
Accept Connection
```

---

# Problem

If an attacker manages to add another trusted root certificate:

```text
Attacker CA
↓
Fake Certificate
↓
Trusted Root
↓
Connection Accepted
```

This is why applications use certificate pinning.

---

# 3. Why Pinning Exists

Pinning introduces:

```text
Certificate Received
↓
Fingerprint Check
↓
Expected Fingerprint ?
↓
Yes → Accept
No → Reject
```

Thus:

```text
Trust Store Alone Is Not Enough
```

---

# 4. Device Compromise

Certificate pinning assumes:

```text
Application Code
↓
Runs Normally
```

But if the device itself is compromised:

```text
Rooted Device
↓
Malware
↓
Modified Runtime
```

The threat model changes.

---

# 5. Runtime Environment

Applications execute inside a runtime environment.

Examples:

### Android

```text
ART Runtime
```

### Java

```text
JVM
```

### Python

```text
Python Interpreter
```

### .NET

```text
CLR
```

If the runtime is manipulated, security assumptions may break.

---

# 6. Dynamic Instrumentation

Dynamic instrumentation means:

```text
Observe Program During Execution
```

instead of:

```text
Analyze Source Code
```

It allows:

* Monitoring
* Function tracing
* Memory observation
* Debugging

Dynamic instrumentation itself is not malicious.

It is heavily used for:

* Debugging
* Performance analysis
* Security testing

---

# Static Analysis vs Dynamic Analysis

### Static Analysis

```text
Source Code
↓
Review
↓
Understand Logic
```

---

### Dynamic Analysis

```text
Program Running
↓
Observe Behavior
```

---

# 7. Rooted Devices

A rooted Android device gives elevated privileges.

This allows:

* Full filesystem access
* System modification
* Advanced debugging

Applications often detect:

```text
Root
↓
Terminate
```

because rooted devices increase risk.

---

# Root Detection Techniques

Applications may check:

* su binary
* BusyBox
* Magisk traces
* Writable system partitions
* Debuggable flags

---

# 8. Emulator Detection

Applications may detect:

* Android emulator
* Virtual devices
* Development environments

Indicators:

```text
Generic device name
Emulator hardware
Known files
```

Purpose:

Prevent analysis and abuse.

---

# 9. Runtime Integrity

Applications may verify:

```text
Application Hash
↓
Expected Hash
↓
Match ?
```

This detects tampering.

---

# 10. Code Integrity

Applications verify:

```text
APK Signature
```

or

```text
Application Signature
```

If modified:

```text
Application Stops
```

---

# 11. Root Detection Is Not Perfect

Root detection:

```text
Raises Difficulty
```

It does not provide:

```text
Absolute Security
```

No detection mechanism is perfect.

---

# 12. Pinning Alone Is Not Enough

Many developers incorrectly believe:

```text
Pinning = Complete Security
```

Reality:

```text
Pinning
+
Runtime Protection
+
Integrity Checks
+
Backend Validation
```

provide stronger protection.

---

# 13. Backend Validation Is Critical

Servers should never trust clients.

The backend must validate:

* Sessions
* Tokens
* Authorization
* Requests

Client-side protections are additional layers.

---

# 14. Secure Architecture

A secure mobile app may contain:

```text
TLS
↓
Certificate Pinning
↓
Root Detection
↓
Integrity Verification
↓
API Authentication
↓
Backend Authorization
↓
Monitoring
```

---

# 15. Principle Of Layered Security

Security should assume:

```text
Any Single Layer May Fail
```

Therefore:

```text
Multiple Independent Layers
```

should exist.

---

# Example

Layer 1:

```text
TLS
```

Layer 2:

```text
Certificate Pinning
```

Layer 3:

```text
Root Detection
```

Layer 4:

```text
Integrity Checks
```

Layer 5:

```text
Server Validation
```

Breaking one layer should not compromise everything.

---

# 16. Zero Trust Philosophy

Modern applications follow:

```text
Never Trust
Always Verify
```

Even clients should not be fully trusted.

Servers must assume:

```text
Requests Can Be Forged
```

and validate everything.

---

# 17. Secure Mobile Architecture

```text
Mobile App
↓
TLS
↓
Certificate Pinning
↓
Integrity Verification
↓
Authentication
↓
Backend API
↓
Authorization
↓
Database
```

Each layer contributes to overall security.

---

# Key Takeaways

Certificate pinning is extremely valuable.

However:

```text
Pinning ≠ Absolute Security
```

Security is achieved through multiple layers.

Applications should combine:

* TLS
* Certificate Pinning
* Backup Pins
* Root Detection
* Integrity Checks
* Backend Validation
* Monitoring

Defense in depth is more powerful than any single mechanism.

# Lab 5 – TLS Certificate Pinning Bypass & MitM Attack

# Part 5 – Defensive Certificate Pinning and Secure Architecture

---

# 1. Security Philosophy

Certificate pinning should be viewed as a defense mechanism, not as an attack prevention mechanism.

The goal is:

```text
Never trust all certificates.

Trust only known certificates or known public keys.
```

---

# 2. Normal HTTPS Validation

Traditional HTTPS performs:

```text
Server Certificate
↓
Certificate Chain Validation
↓
Trusted Root CA
↓
Accept Connection
```

The application trusts any certificate issued by any trusted CA.

---

# Problem

Suppose:

```text
Attacker CA
↓
Fake Certificate
↓
Trusted By Device
↓
Connection Accepted
```

Traditional HTTPS cannot distinguish between:

* Real certificate
* Malicious certificate

if both are signed by trusted roots.

---

# 3. Certificate Pinning Validation

Pinning introduces another layer:

```text
Certificate Received
↓
Fingerprint Extraction
↓
Compare With Stored Fingerprint
↓
Match ?
↓
Accept
```

Otherwise:

```text
Reject Connection
```

---

# 4. Fingerprints

Certificates have unique identities.

Common fingerprint algorithms:

### MD5

Deprecated.

### SHA1

Weak.

### SHA256

Preferred.

### SHA512

Rarely used.

Modern applications generally use:

```text
SHA256
```

---

# Example SHA256 Fingerprint

```text
2A:91:BE:3D:FA:45:6B:71...
```

This uniquely identifies a certificate.

---

# 5. Why SHA256 Is Preferred

SHA256 provides:

* Collision resistance
* High entropy
* Strong cryptographic properties

Changing one bit produces a completely different hash.

Example:

Original:

```text
ABCDEF123
```

Modified:

```text
9B1F74DAA
```

Thus fake certificates produce different fingerprints.

---

# 6. Certificate Pinning Flow

Application stores:

```text
Expected Fingerprint
```

Connection:

```text
Receive Certificate
↓
Compute SHA256
↓
Compare
↓
Match ?
↓
Accept
```

Else:

```text
Reject
```

---

# 7. SPKI Pinning

SPKI means:

```text
Subject Public Key Info
```

Instead of pinning the entire certificate:

```text
Certificate
```

applications pin:

```text
Public Key
```

---

# Why Public Key Pinning Is Better

Certificates expire frequently.

Public keys may remain unchanged.

Therefore:

```text
Certificate Changes
↓
Public Key Same
↓
Application Continues Working
```

This avoids application failures.

---

# 8. Certificate Pinning vs Public Key Pinning

### Certificate Pinning

Pins:

```text
Entire Certificate
```

Advantages:

* Easy

Disadvantages:

* Renewal problems

---

### Public Key Pinning

Pins:

```text
Public Key
```

Advantages:

* Supports certificate renewal
* More flexible

Disadvantages:

* More complex

---

# 9. Primary Pin

Applications should maintain:

```text
Primary Pin
```

Example:

```text
Pin A
```

Connection:

```text
Fingerprint
↓
Pin A Match
↓
Success
```

---

# Problem

If certificate rotates:

```text
Pin A
```

becomes:

```text
Pin B
```

Application breaks.

---

# 10. Backup Pins

Google strongly recommends backup pins.

Store:

```text
Primary Pin
Backup Pin
```

Validation:

```text
Certificate
↓
Primary Match ?
↓
No
↓
Backup Match ?
↓
Yes
↓
Accept
```

---

# Advantages

Supports:

* Rotation
* Certificate replacement
* Disaster recovery

---

# 11. Certificate Rotation

Certificates expire.

Example:

Current certificate:

```text
Pin A
```

Future certificate:

```text
Pin B
```

Store both:

```text
Pin A
Pin B
```

Transition becomes seamless.

---

# 12. Pin Expiration

Pins themselves should expire.

Because:

* Keys may be compromised
* Infrastructure changes
* Organizations evolve

Applications should support:

```text
Pin Refresh
```

rather than permanent hardcoding.

---

# 13. Fail Closed Principle

Correct behavior:

```text
Pin Match ?
↓
No
↓
Reject Connection
```

Never:

```text
Pin Match ?
↓
No
↓
Ignore Error
↓
Continue
```

Ignoring pin failures defeats the entire purpose.

---

# 14. Common Mistakes

### Disabling Validation

Bad:

```java
return true;
```

inside trust validation.

---

### Trusting All Certificates

Dangerous because:

```text
Any Certificate
↓
Accepted
```

---

### Ignoring SSL Exceptions

Dangerous because:

```text
Handshake Failure
↓
Continue Anyway
```

---

### Using One Pin Only

Breaks after rotation.

---

# 15. Android Network Security Config

Android supports:

```text
network_security_config.xml
```

Example:

```xml
<pin-set>
    <pin digest="SHA-256">
        ABCDEF123
    </pin>
</pin-set>
```

Benefits:

* Easy configuration
* No code changes
* Declarative security

---

# 16. OkHttp CertificatePinner

Popular Android library:

```text
OkHttp
```

Pinning example:

```java
CertificatePinner pinner =
new CertificatePinner.Builder()
.add(
"api.example.com",
"sha256/ABCDEF..."
)
.build();
```

Connection succeeds only if:

```text
Fingerprint Matches
```

---

# 17. iOS TrustKit

iOS applications often use:

```text
TrustKit
```

TrustKit supports:

* Public key pinning
* Backup pins
* Rotation support

---

# 18. Banking App Architecture

Typical architecture:

```text
App
↓
TLS
↓
Certificate Pinning
↓
Root Detection
↓
Integrity Checks
↓
Authentication
↓
Backend API
```

Multiple layers improve security.

---

# 19. Secure Pinning Architecture

Client:

```text
Receive Certificate
↓
Extract Public Key
↓
Compute SHA256
↓
Compare With:
Primary Pin
Backup Pin
↓
Match ?
↓
Accept
```

Else:

```text
Reject Connection
```

---

# 20. Pinning Failure Handling

Good applications:

```text
SSLHandshakeException
↓
Connection Blocked
↓
User Notified
```

Bad applications:

```text
SSLHandshakeException
↓
Ignore
↓
Continue
```

---

# 21. Why Google Recommends Backup Pins

Without backup pins:

```text
Certificate Expired
↓
App Broken
```

With backup pins:

```text
Certificate Changed
↓
Backup Pin Matches
↓
Service Continues
```

---

# 22. Defense In Depth

Certificate pinning should be combined with:

### TLS

Provides encryption.

---

### Root Detection

Detect compromised devices.

---

### Integrity Verification

Detect modified applications.

---

### Authentication

Protect APIs.

---

### Backend Validation

Never trust clients.

---

# 23. Zero Trust Principle

Modern philosophy:

```text
Never Trust
Always Verify
```

Even trusted devices must continuously prove identity.

---

# 24. Secure Architecture For Lab 5

Our implementation will use:

```text
HTTP Toolkit Demo App
↓
HTTPS Connection
↓
Certificate Pinning
↓
SHA256 Fingerprints
↓
Primary Pin
↓
Backup Pin
↓
Rotation Support
↓
Secure Validation Engine
↓
Reports
```

---

# 25. Final Defensive Architecture

```text
Client
↓
TLS Handshake
↓
Certificate Received
↓
Extract Public Key
↓
SHA256 Fingerprint
↓
Primary Pin Match?
↓
Backup Pin Match?
↓
Accept
```

Else:

```text
Reject Connection
```

---

# Key Takeaways

Certificate pinning is strongest when combined with:

* SHA256 fingerprints
* Public key pinning
* Primary pins
* Backup pins
* Certificate rotation support
* Fail closed behavior
* Defense in depth

The most robust systems trust only known keys and reject everything else.

# Lab 5 – TLS Certificate Pinning Bypass & MitM Attack

# Part 6 – Environment Setup and Tool Installation

---

# Objective

Before implementing the attack and defense components, we need to prepare the environment and understand why each tool is required.

The tools used in this lab are:

1. Python 3.9+
2. pip
3. mitmproxy
4. OpenSSL
5. HTTP Toolkit Android SSL Pinning Demo
6. Android Emulator (optional)
7. Frida (optional for advanced bypass)

---

# 1. Python

## What is Python?

Python is a high-level programming language widely used for:

- Automation
- Web applications
- Cybersecurity
- Reverse engineering
- Packet analysis
- Cryptography

In this lab Python will be used for:

- Writing MitM scripts
- Building certificate validation engines
- Generating reports
- Parsing intercepted traffic

---

## Checking Python Installation

Command:

```powershell
python --version
```

Example:

```text
Python 3.9.13
```

---

## Why Python 3.9+?

Modern libraries such as:

- cryptography
- mitmproxy
- requests
- pyOpenSSL

require newer Python versions.

---

# 2. pip

## What is pip?

pip stands for:

```text
Pip Installs Packages
```

It is Python's package manager.

It allows installation of external libraries.

Examples:

```powershell
pip install requests
pip install cryptography
pip install mitmproxy
```

---

## Check pip

```powershell
pip --version
```

Example:

```text
pip 25.1.1
```

---

## Upgrade pip

pip periodically receives:

- Security fixes
- Bug fixes
- Compatibility updates

Upgrade command:

```powershell
python -m pip install --upgrade pip
```

Example message:

```text
25.1.1 → 26.0.1
```

This update is optional.

---

# 3. mitmproxy

---

## What is mitmproxy?

mitmproxy stands for:

```text
Man In The Middle Proxy
```

It is an intercepting HTTPS proxy.

It sits between:

```text
Client
↓
mitmproxy
↓
Server
```

allowing us to:

- Observe requests
- Modify requests
- Modify responses
- Save traffic
- Build custom interception scripts

---

## Installation

Command:

```powershell
pip install mitmproxy
```

---

## Verify Installation

Command:

```powershell
mitmproxy --version
```

Example:

```text
Mitmproxy: 9.0.1
Python: 3.9.13
OpenSSL: OpenSSL 3.0.7
Platform: Windows-10
```

---

# Understanding the Output

## Mitmproxy Version

```text
Mitmproxy: 9.0.1
```

Indicates the installed version.

---

## Python Version

```text
Python: 3.9.13
```

Shows the interpreter used by mitmproxy.

---

## OpenSSL

```text
OpenSSL: 3.0.7
```

OpenSSL performs:

- Certificate generation
- TLS encryption
- Cryptographic operations

---

## Platform

```text
Windows-10
```

Shows the operating system.

---

# Why do we need mitmproxy?

Without a proxy:

```text
App
↓
Server
```

Traffic cannot be observed.

With mitmproxy:

```text
App
↓
mitmproxy
↓
Server
```

Traffic becomes visible.

---

# 4. OpenSSL

---

## What is OpenSSL?

OpenSSL is a cryptographic toolkit.

It provides:

- TLS
- SSL
- Certificate generation
- RSA keys
- SHA algorithms

Most HTTPS systems rely on OpenSSL internally.

---

## Why is OpenSSL Needed?

mitmproxy generates certificates dynamically.

For every HTTPS connection:

```text
Server Certificate
↓
mitmproxy creates a fake certificate
↓
Client receives certificate
```

OpenSSL performs this operation.

---

# 5. HTTP Toolkit Android SSL Pinning Demo

Repository:

```text
https://github.com/httptoolkit/android-ssl-pinning-demo
```

---

## Why are we using it?

Building an Android application from scratch is unnecessary.

The repository already contains:

### Normal HTTPS communication

```text
App
↓
Server
```

---

### Certificate pinning

```text
Fingerprint Validation
↓
Reject fake certificates
```

---

### Pinning bypass demonstrations

Used for attack analysis.

---

## Clone Repository

Command:

```powershell
git clone https://github.com/httptoolkit/android-ssl-pinning-demo.git
```

---

# 6. Android Emulator (Optional)

An Android emulator provides:

```text
Virtual Android Device
```

Examples:

- Android Studio Emulator
- Genymotion

Purpose:

Run mobile applications without requiring a physical phone.

---

# 7. Frida (Advanced)

---

## What is Frida?

Frida is a dynamic instrumentation framework.

It injects JavaScript code into processes while they are running.

It allows:

- Function hooking
- Runtime modification
- SSL pinning bypass
- Reverse engineering

---

## Installation

```powershell
pip install frida-tools
```

---

## Verify

```powershell
frida --version
```

---

# Tool Summary

| Tool | Purpose |
|--------|--------|
| Python | Programming language |
| pip | Package manager |
| mitmproxy | HTTPS interception |
| OpenSSL | Certificate generation and TLS |
| HTTP Toolkit Demo | Test application |
| Emulator | Android testing |
| Frida | Runtime instrumentation |

---

# Current Status

Installed:

```text
Python 3.9.13
✓
```

Installed:

```text
pip
✓
```

Installed:

```text
mitmproxy 9.0.1
✓
```

Detected:

```text
OpenSSL 3.0.7
✓
```

Remaining:

```text
HTTP Toolkit Android SSL Pinning Demo
Android Emulator (optional)
Frida (optional)
```

---

# Environment Ready

Current Lab Architecture

                HTTPS APP
                     ↓
               mitmproxy
                     ↓
            Python MitM Script
                     ↓
        intercepted_requests.json
                     ↓
               HTML Dashboard

                     +

       Secure Certificate Pinning Engine
                     ↓
             Primary Pin
             Backup Pin
             Rotation Support
             Fail Closed Validation

# Lab 5 – TLS Certificate Pinning Bypass & MitM Attack

# Part 7 – Proxies, HTTPS Traffic Flow, and MitM Fundamentals

---

# Objective

Before understanding TLS interception and certificate pinning bypass, we must understand:

- What is a proxy?
- Why proxies exist?
- How HTTPS normally works?
- How a Man-in-the-Middle attack works?
- Why HTTPS traffic cannot normally be read?
- Why mitmproxy needs its own certificates?

---

# 1. What is a Proxy?

A proxy is an intermediate system that sits between a client and a server.

Instead of:

```text
Client
↓
Server
```

we have:

```text
Client
↓
Proxy
↓
Server
```

The proxy receives requests from the client and forwards them to the server.

Likewise, responses from the server travel through the proxy before reaching the client.

---

# Real-Life Analogy

Suppose:

You want to speak to a company CEO.

Instead of speaking directly:

```text
You
↓
CEO
```

you communicate through a secretary:

```text
You
↓
Secretary
↓
CEO
```

The secretary forwards everything.

A proxy behaves similarly.

---

# 2. Why Do Proxies Exist?

Proxies are widely used for:

### Monitoring

Observe traffic.

---

### Caching

Improve speed.

---

### Security

Filter malicious requests.

---

### Content Filtering

Block unwanted websites.

---

### Debugging

Inspect APIs and applications.

---

### Traffic Analysis

Used by cybersecurity engineers.

---

# 3. Types of Proxies

---

## Forward Proxy

Located between:

```text
Client
↓
Proxy
↓
Internet
```

Examples:

- Burp Suite
- mitmproxy
- HTTP Toolkit

---

## Reverse Proxy

Located near the server.

```text
Users
↓
Reverse Proxy
↓
Application Servers
```

Examples:

- NGINX
- HAProxy
- Cloudflare

---

## Transparent Proxy

Users do not know it exists.

Often used by:

- Schools
- ISPs
- Enterprises

---

# 4. HTTP Communication

Without HTTPS:

```text
Browser
↓
Server
```

Request:

```http
GET /login
username=admin
password=1234
```

Everything is plaintext.

Anyone monitoring the network can read:

- Username
- Password
- Cookies

---

# Problem

HTTP provides:

```text
NO CONFIDENTIALITY
```

---

# 5. HTTPS Communication

HTTPS adds:

```text
TLS Encryption
```

Flow:

```text
Client
↓
TLS
↓
Server
```

Now traffic becomes encrypted.

Attackers can see:

```text
Encrypted Bytes
```

but not:

- Passwords
- Tokens
- Cookies

---

# Example

Before HTTPS:

```text
password=admin123
```

After HTTPS:

```text
7F 29 C1 A4 D9 E8 ...
```

Human-readable information disappears.

---

# 6. HTTPS Traffic Flow

Step 1

Client sends:

```text
Hello Server
```

---

Step 2

Server sends certificate.

---

Step 3

Certificate verification.

---

Step 4

Key exchange.

---

Step 5

Encrypted session established.

---

Step 6

Application data exchanged.

```text
GET /login
POST /api
JWT token
Cookies
```

All encrypted.

---

# 7. TLS Handshake Overview

Simplified:

```text
Client Hello
↓
Server Hello
↓
Certificate
↓
Key Exchange
↓
Session Keys Generated
↓
Encrypted Communication Begins
```

After this point:

Everything becomes encrypted.

---

# 8. Why Packet Sniffing Fails

Tools:

- Wireshark
- Tcpdump

can capture packets:

```text
7B A1 F4 92 ...
```

but cannot decrypt them.

Because:

```text
Session Keys
```

are secret.

---

# 9. Where Does mitmproxy Sit?

Instead of:

```text
Client
↓
Server
```

we introduce:

```text
Client
↓
mitmproxy
↓
Server
```

Now mitmproxy acts like:

- Server to the client
- Client to the server

Simultaneously.

---

# 10. Two TLS Connections

Normal HTTPS:

```text
Client
↓
Server
```

One TLS tunnel.

---

With mitmproxy:

```text
Client
↓
TLS #1
↓
mitmproxy
↓
TLS #2
↓
Server
```

Two independent encrypted channels exist.

---

# 11. What Happens Internally

Client thinks:

```text
I'm talking to the server.
```

Server thinks:

```text
I'm talking to the client.
```

But both are actually talking to:

```text
mitmproxy
```

This is why it's called:

```text
Man In The Middle
```

---

# 12. Why Can mitmproxy Read Everything?

Traffic flow:

```text
Client
↓
Encrypted
↓
mitmproxy
```

Inside mitmproxy:

```text
Decrypt
↓
Inspect
↓
Modify
↓
Encrypt Again
```

Then:

```text
Encrypted
↓
Server
```

Thus:

mitmproxy sees:

- Headers
- Tokens
- Cookies
- JSON payloads
- Passwords

in plaintext.

---

# 13. Request Flow

Client sends:

```http
POST /login
```

to:

```text
mitmproxy
```

mitmproxy decrypts:

```json
{
 "username":"admin",
 "password":"1234"
}
```

Then re-encrypts and forwards.

---

# 14. Response Flow

Server sends:

```json
{
 "token":"JWT"
}
```

mitmproxy decrypts:

```text
JWT token visible
```

Then encrypts again.

---

# 15. Why Doesn't This Trigger Errors?

Because the client trusts the certificate presented by mitmproxy.

Without trust:

```text
Certificate Error
```

would occur.

---

# 16. Trust Relationship

Normal:

```text
Client
↓
Google Certificate
↓
Trusted CA
↓
Accept
```

MitM:

```text
Client
↓
Fake Certificate
↓
mitmproxy CA
↓
Accept
```

If the mitmproxy CA is trusted.

---

# 17. Problem Introduced by Certificate Pinning

Normal applications trust:

```text
Any trusted CA
```

Pinned applications trust:

```text
One specific certificate
```

Therefore:

```text
mitmproxy certificate
≠
Expected certificate
```

Result:

```text
Connection blocked
```

---

# 18. Why Banking Apps Resist MITM

Because they perform:

```text
Certificate Fingerprint Check
```

Even if:

```text
mitmproxy CA
```

is installed,

the app compares:

```text
SHA256 fingerprint
```

and rejects mismatches.

---

# 19. Attack Goal

Attackers want:

```text
App
↓
Bypass Pinning
↓
Trust Fake Certificate
↓
Traffic Visible
```

This is where:

- Frida
- Dynamic instrumentation
- Hooking

become important.

---

# Summary

Without Proxy:

```text
Client
↓
Server
```

---

With Proxy:

```text
Client
↓
Proxy
↓
Server
```

---

With HTTPS:

```text
Encrypted Communication
```

---

With mitmproxy:

```text
Client
↓
TLS
↓
mitmproxy
↓
TLS
↓
Server
```

---

With Certificate Pinning:

```text
Fingerprint Mismatch
↓
Connection Blocked
```

---

Next Part:

# TLS Handshake Deep Dive

We will study:

- Client Hello
- Server Hello
- Certificates
- Public Keys
- Session Keys
- Symmetric Encryption
- Asymmetric Encryption
- RSA
- Diffie-Hellman
- Perfect Forward Secrecy

These concepts are the heart of certificate pinning and MitM attacks.

# Lab 5 – TLS Certificate Pinning Bypass & MitM Attack

# Part 8 – TLS Handshake Deep Dive

---

# Objective

To understand:

- How HTTPS establishes trust
- Why attackers cannot simply read HTTPS traffic
- How certificates work
- How session keys are generated
- Why TLS interception works
- Why certificate pinning breaks interception

This section is one of the most important concepts in cybersecurity.

---

# 1. Problem Before TLS

Suppose Alice wants to communicate with a bank server.

Without encryption:

```text
Alice
↓
Internet
↓
Bank Server
```

Anyone listening can read:

- Username
- Password
- Credit card numbers
- Session cookies

This is insecure.

---

# Solution

TLS creates:

```text
Confidentiality
Integrity
Authentication
```

---

# 2. Goals of TLS

TLS provides:

### Confidentiality

Prevent eavesdropping.

---

### Integrity

Prevent modification of data.

---

### Authentication

Verify server identity.

---

# 3. TLS Handshake Overview

Before any encrypted data is exchanged:

```text
Client
↓
Client Hello
↓
Server
↓
Server Hello
↓
Certificate
↓
Key Exchange
↓
Session Key Creation
↓
Encrypted Communication Begins
```

Everything after this is encrypted.

---

# 4. Step 1 – Client Hello

Client initiates communication.

Example:

```text
Browser
↓
Client Hello
```

Contains:

### Supported TLS versions

Example:

```text
TLS 1.2
TLS 1.3
```

---

### Cipher suites

Possible algorithms:

```text
AES
ChaCha20
RSA
ECDHE
```

---

### Random number

Example:

```text
Random_A
```

---

### Extensions

Such as:

- SNI
- ALPN

---

# 5. Step 2 – Server Hello

Server responds.

Contains:

### Chosen TLS version

Example:

```text
TLS 1.3
```

---

### Selected cipher suite

Example:

```text
ECDHE + AES256
```

---

### Server random

Example:

```text
Random_B
```

---

# 6. Step 3 – Certificate Transmission

Server sends:

```text
Certificate
```

Certificate contains:

- Domain name
- Public key
- Expiration date
- Issuer
- Signature

Example:

```text
CN = api.bank.com
Issuer = DigiCert
```

---

# 7. Certificate Chain

Certificates form a hierarchy.

```text
Root CA
↓
Intermediate CA
↓
Server Certificate
```

Example:

```text
DigiCert Root
↓
DigiCert Intermediate
↓
Google Certificate
```

---

# 8. Root Certificate Authority

Root CA is trusted by the operating system.

Examples:

- DigiCert
- GlobalSign
- Let's Encrypt

Windows stores them in:

```text
Trusted Root Store
```

---

# 9. Certificate Validation

Browser checks:

### Is certificate expired?

---

### Is domain correct?

```text
api.bank.com
```

must match:

```text
api.bank.com
```

---

### Is signature valid?

---

### Is issuer trusted?

---

If all succeed:

```text
Certificate Accepted
```

---

# 10. Public Key

Certificate contains:

```text
Public Key
```

Example:

```text
RSA Public Key
```

Public key can be shared openly.

Used for:

- Verification
- Encryption

---

# 11. Private Key

Stored only on server.

Never transmitted.

Used for:

- Signing
- Decryption

Relationship:

```text
Public Key
↑
↓
Private Key
```

---

# 12. Asymmetric Cryptography

Two keys exist.

```text
Public Key
Private Key
```

Algorithms:

### RSA

### ECC

---

Advantages:

Secure key exchange.

Disadvantages:

Slow.

---

# 13. Symmetric Encryption

Only one secret key exists.

Example:

```text
Session Key
```

Algorithms:

### AES

### ChaCha20

---

Advantages:

Fast.

Disadvantages:

Need secure key exchange.

---

# 14. Why TLS Uses Both

Asymmetric:

Used for key exchange.

Symmetric:

Used for bulk encryption.

Because:

```text
RSA
Slow

AES
Fast
```

---

# 15. Session Keys

During handshake:

Client and server generate:

```text
Shared Secret
```

Example:

```text
Session Key
```

Only:

```text
Client
Server
```

know this key.

Attackers do not.

---

# 16. Session Key Usage

After handshake:

Everything uses:

```text
AES256
```

Example:

Before:

```json
{
 "password":"admin123"
}
```

After encryption:

```text
7A2F891CA5...
```

Unreadable.

---

# 17. Cipher Suites

Cipher suite defines:

### Key exchange

Example:

```text
ECDHE
```

---

### Authentication

RSA

---

### Encryption

AES256

---

### Hash function

SHA256

---

Example:

```text
TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
```

---

# 18. RSA Key Exchange

Old method.

Process:

```text
Client
↓
Encrypt secret using public key
↓
Server decrypts using private key
```

Problem:

If private key leaks:

Past traffic can be decrypted.

---

# 19. Diffie-Hellman Key Exchange

Modern TLS uses:

```text
ECDHE
```

Elliptic Curve Diffie-Hellman Ephemeral.

Both sides generate temporary keys.

Shared secret is derived mathematically.

Private keys are never transmitted.

---

# 20. Perfect Forward Secrecy

PFS means:

Even if:

```text
Private key stolen
```

old sessions remain secure.

Because:

Session keys are temporary.

Each connection has:

```text
New Session Key
```

---

# 21. Finished Message

Both sides verify:

```text
Handshake integrity
```

If successful:

```text
Encrypted Session Established
```

---

# 22. Application Data Begins

Now:

```text
POST /login
JWT
Cookies
Passwords
```

all travel encrypted.

---

# Complete TLS Flow

```text
Client
↓
Client Hello
↓
Server Hello
↓
Certificate
↓
Certificate Validation
↓
Key Exchange
↓
Shared Secret
↓
Session Key
↓
Finished Message
↓
Encrypted Data
```

---

# 23. Why Wireshark Cannot Read HTTPS

Wireshark sees:

```text
Encrypted Bytes
```

Example:

```text
A8F9124DBAA29E...
```

It cannot see:

```json
{
 "username":"admin"
}
```

because it lacks:

```text
Session Key
```

---

# 24. Why MITM Works

mitmproxy creates:

Two TLS sessions.

```text
Client
↓ TLS1
mitmproxy
↓ TLS2
Server
```

It decrypts traffic in the middle.

Thus it sees plaintext.

---

# 25. Why Certificate Pinning Breaks MITM

Normal validation:

```text
Trust Any Trusted CA
```

Pinned applications:

```text
Trust One Certificate
```

Therefore:

```text
mitmproxy certificate
≠
Expected certificate
```

Result:

```text
Handshake Failure
```

Connection blocked.

---

# Summary

TLS combines:

### Certificates

Identity

---

### Public Keys

Authentication

---

### Private Keys

Signing

---

### Session Keys

Encryption

---

### AES

Fast encryption

---

### Diffie-Hellman

Secure key exchange

---

### Perfect Forward Secrecy

Protection of past sessions

---

### Certificate Validation

Server authenticity

---

### Certificate Pinning

Protection against MITM

---

Next Part:

# Certificates, CAs, Certificate Chains, and Trust Stores

This is where certificate pinning actually begins.

# Lab 5 – TLS Certificate Pinning Bypass & MitM Attack

# Part 9 – Certificates, Certificate Authorities, Certificate Chains and Trust Stores

---

# Objective

Understand:

- What certificates are
- What information certificates contain
- Why Certificate Authorities exist
- How certificate chains work
- What trust stores are
- Why browsers trust websites
- Why mitmproxy installs its own CA
- Why certificate pinning bypasses normal trust mechanisms

This section forms the foundation of certificate pinning.

---

# 1. What is a Certificate?

A certificate is essentially a digital identity card.

Just like:

```text
Passport → proves identity of a person
```

A certificate proves:

```text
Identity of a server
```

Example:

```text
api.google.com
```

The certificate says:

```text
"I am really Google"
```

---

# Real World Analogy

Passport contains:

- Name
- Date of birth
- Country
- Signature

Certificate contains:

- Domain name
- Public key
- Expiry date
- Issuer
- Digital signature

---

# 2. Why Certificates Are Needed

Without certificates:

```text
Client
↓
???
↓
Server
```

An attacker could impersonate the server.

For example:

```text
Fake Bank Website
```

appearing identical to:

```text
Real Bank Website
```

Users cannot distinguish between them.

Certificates solve this problem.

---

# 3. What Does a Certificate Contain?

A certificate contains:

### Subject

Owner.

Example:

```text
CN = api.google.com
```

CN means Common Name.

---

### Public Key

Used for encryption and verification.

Example:

```text
RSA 2048-bit Public Key
```

---

### Issuer

Who issued the certificate.

Example:

```text
DigiCert
```

---

### Serial Number

Unique identifier.

---

### Validity Period

Example:

```text
Not Before:
1 Jan 2026

Not After:
1 Jan 2027
```

---

### Signature

Digital proof created by the issuer.

---

# Example Certificate

```text
Subject:
api.bank.com

Issuer:
DigiCert

Public Key:
RSA 2048

Valid:
2026-2027

Signature:
Digital Signature
```

---

# 4. Public Key Inside Certificate

Certificate contains:

```text
Public Key
```

Public keys can be shared openly.

Clients use them to:

- Verify signatures
- Establish secure communication

Private keys remain only on the server.

---

# 5. Certificate Authorities (CA)

Question:

How do we know that:

```text
api.google.com
```

really belongs to Google?

Answer:

Certificate Authorities.

---

Certificate Authorities are trusted organizations that verify ownership and issue certificates.

Examples:

### DigiCert

### GlobalSign

### Sectigo

### Let's Encrypt

### Entrust

---

# Real World Analogy

CA is like:

```text
Government Passport Office
```

Government verifies identity and issues passport.

Similarly:

```text
CA verifies domain ownership
↓
Issues certificate
```

---

# 6. Certificate Issuance Process

Google requests certificate.

```text
Google
↓
DigiCert
```

DigiCert verifies ownership.

If verified:

```text
Certificate Generated
```

Signed by DigiCert.

---

Result:

```text
Google Certificate
```

---

# 7. Root Certificate Authority

Root CA sits at the top.

Example:

```text
DigiCert Root CA
```

It signs:

```text
Intermediate CA
```

which signs:

```text
Server Certificate
```

---

Hierarchy:

```text
Root CA
↓
Intermediate CA
↓
Server Certificate
```

---

# Why Use Intermediate CA?

Security.

Root certificates are extremely sensitive.

Therefore:

```text
Root CA
```

is rarely used directly.

Instead:

```text
Root
↓
Intermediate
↓
Server
```

---

# Example Chain

```text
DigiCert Root
↓
DigiCert TLS RSA SHA256 2020 CA1
↓
api.google.com Certificate
```

---

# 8. Certificate Chain Validation

Browser receives:

```text
Server Certificate
```

Then verifies:

```text
Server
↓
Intermediate
↓
Root
```

until it reaches:

```text
Trusted Root CA
```

If every signature is valid:

```text
Connection Accepted
```

---

# Chain Visualization

```text
Google Certificate
↓
Signed By
↓
Intermediate CA
↓
Signed By
↓
Root CA
↓
Trusted By OS
```

---

# 9. Trust Store

Operating systems maintain:

```text
Trusted Root Store
```

Contains hundreds of trusted root certificates.

Examples:

Windows

macOS

Android

Linux

Browsers

---

# Windows Trust Store

Contains:

- DigiCert
- GlobalSign
- Let's Encrypt
- Microsoft Root CA

etc.

---

# Browser Validation

Browser checks:

```text
Certificate Chain
↓
Root CA Found?
↓
YES
↓
Accept
```

---

# 10. If Root Is Unknown

Suppose attacker creates:

```text
Fake Root CA
```

Chain:

```text
Fake Root
↓
Fake Intermediate
↓
Fake Bank Certificate
```

Browser checks:

```text
Root Trusted?
```

No.

Result:

```text
NET::ERR_CERT_AUTHORITY_INVALID
```

Connection blocked.

---

# 11. Self-Signed Certificates

Self-signed certificates are signed by themselves.

Example:

```text
Issuer = Subject
```

Such certificates have no trusted chain.

Browsers display:

```text
Your connection is not private
```

---

# 12. Expired Certificates

Certificate validity:

```text
2025-2026
```

Current date:

```text
2027
```

Result:

```text
Certificate Expired
```

Connection rejected.

---

# 13. Domain Mismatch

Certificate says:

```text
api.google.com
```

But website accessed:

```text
facebook.com
```

Mismatch occurs.

Browser rejects.

---

# 14. Revoked Certificates

Certificates can be revoked when:

- Private key leaked
- Certificate compromised

Browsers consult:

### CRL

Certificate Revocation List

or

### OCSP

Online Certificate Status Protocol

to verify.

---

# 15. How mitmproxy Works

mitmproxy creates its own CA.

Example:

```text
mitmproxy Root CA
```

Installed into device trust store.

Then:

```text
Client
↓
mitmproxy CA
↓
Fake Google Certificate
↓
Accepted
```

Thus interception becomes possible.

---

# 16. Dynamic Certificate Generation

Suppose user visits:

```text
api.google.com
```

mitmproxy generates:

```text
Fake api.google.com Certificate
```

signed by:

```text
mitmproxy Root CA
```

Client trusts it because:

```text
mitmproxy Root CA
```

was installed earlier.

---

# 17. Why Certificate Pinning Defeats This

Normal trust:

```text
Any Trusted CA
```

Certificate pinning:

```text
Only THIS certificate
```

Therefore:

```text
Google Certificate
≠
mitmproxy Fake Certificate
```

Result:

```text
SSL Handshake Failure
```

MITM blocked.

---

# 18. Summary

Certificates contain:

- Identity
- Public key
- Expiry
- Issuer
- Signature

---

Certificate Authorities:

Verify ownership and issue certificates.

---

Certificate Chain:

```text
Root
↓
Intermediate
↓
Server
```

---

Trust Store:

Contains trusted root certificates.

---

mitmproxy:

Creates fake certificates signed by its own CA.

---

Certificate Pinning:

Ignores trust store and trusts only specific certificates or public keys.

---

# Next Part

Part 10

## Certificate Fingerprints

## SHA256 Hashes

## SPKI

## Public Key Pinning

## Primary Pins

## Backup Pins

## Rotation Support

This is where the actual defensive mechanism behind certificate pinning begins.

# Lab 5 – TLS Certificate Pinning Bypass & MitM Attack

# Part 10 – Certificate Fingerprints, Public Key Pinning, Backup Pins and Rotation

---

# Objective

Understand:

- Certificate fingerprints
- Hash functions
- SHA256 fingerprints
- SPKI
- Certificate pinning
- Public key pinning
- Primary pins
- Backup pins
- Certificate rotation
- Why Google recommends backup pins

These concepts are at the core of defensive certificate pinning.

---

# 1. Why Certificates Need Unique Identification

Certificates contain:

- Domain name
- Public key
- Issuer
- Signature

But applications need a reliable way to recognize a specific certificate.

This is achieved using:

```text
Fingerprint
```

---

# Real World Analogy

Human:

```text
Fingerprint
↓
Unique Identity
```

Certificate:

```text
Certificate
↓
SHA256 Fingerprint
↓
Unique Identity
```

No two certificates should have the same fingerprint.

---

# 2. What Is A Fingerprint?

A fingerprint is a hash generated from a certificate.

Example:

```text
Certificate
↓
SHA256
↓
A4:B9:F1:92:8D:...
```

This hash becomes the certificate's identity.

---

# Properties Of Fingerprints

### Deterministic

Same certificate produces same fingerprint.

---

### One-way

Cannot reconstruct certificate from hash.

---

### Collision Resistant

Two certificates should not produce the same fingerprint.

---

### Sensitive

Changing one bit changes the fingerprint completely.

---

# Example

Certificate A:

```text
Fingerprint

ABCD1234
```

Certificate B:

```text
Fingerprint

D98E72A9
```

Completely different.

---

# 3. Hash Functions

A hash function converts arbitrary input into fixed-length output.

Example:

```text
Hello
↓
SHA256
↓
185F8DB322...
```

Output length remains constant.

---

# Common Hash Algorithms

### MD5

Broken.

Not recommended.

---

### SHA1

Weak.

Deprecated.

---

### SHA256

Strong.

Industry standard.

---

### SHA512

Very secure.

Less commonly used.

---

Modern pinning generally uses:

```text
SHA256
```

---

# 4. SHA256 Fingerprints

Certificate

↓

Binary Data

↓

SHA256

↓

256-bit digest

↓

Fingerprint

Example:

```text
6F:A3:81:BB:...
```

Applications compare this fingerprint against a stored value.

---

# 5. Certificate Pinning

Traditional HTTPS:

```text
Trust Any Valid Certificate
```

Certificate pinning:

```text
Trust One Specific Certificate
```

Flow:

```text
Receive Certificate
↓
Generate SHA256
↓
Compare Fingerprint
↓
Match?
↓
Accept
```

Otherwise:

```text
Reject Connection
```

---

# Problem With Certificate Pinning

Certificates expire.

Suppose:

Current certificate:

```text
Certificate A
```

Fingerprint:

```text
SHA256(A)
```

After renewal:

```text
Certificate B
```

Fingerprint becomes:

```text
SHA256(B)
```

Pin mismatch occurs.

Application breaks.

---

# 6. Public Key Pinning

Instead of pinning the entire certificate, applications pin:

```text
Public Key
```

This is called:

```text
SPKI Pinning
```

SPKI means:

```text
Subject Public Key Info
```

---

# SPKI Structure

Certificate contains:

```text
Subject
Public Key
Issuer
Signature
Validity
```

SPKI extracts:

```text
Public Key
```

only.

---

# Why SPKI Pinning Is Better

Certificates may change:

```text
Certificate A
↓
Certificate B
```

But public key can remain:

```text
Public Key X
```

Therefore:

```text
SPKI Fingerprint
```

remains unchanged.

Connection continues working.

---

# 7. SPKI Pinning Flow

Receive Certificate

↓

Extract Public Key

↓

Generate SHA256

↓

Compare Stored Pin

↓

Match?

↓

Accept

---

This is more flexible than certificate pinning.

---

# 8. Primary Pin

Applications maintain:

```text
Primary Pin
```

Example:

```text
Pin A
```

Validation:

```text
Fingerprint
↓
Pin A Match?
↓
Accept
```

---

# Problem

Certificate rotation causes:

```text
Pin A
≠
Pin B
```

Application stops working.

---

# 9. Backup Pin

Applications should store:

```text
Primary Pin
Backup Pin
```

Example:

```text
Pin A
Pin B
```

Validation:

```text
Certificate
↓
Primary Match?
↓
No
↓
Backup Match?
↓
Yes
↓
Accept
```

---

# Advantages

Supports:

- Certificate renewal
- Disaster recovery
- Migration
- High availability

---

# 10. Certificate Rotation

Certificates expire.

Example:

Current:

```text
Pin A
```

Future:

```text
Pin B
```

Both are stored:

```text
Primary Pin = A

Backup Pin = B
```

When certificate changes:

```text
Pin B becomes Primary
```

and a new backup pin is added.

---

# Rotation Flow

Current

```text
Primary = A
Backup = B
```

Certificate updated

```text
Primary = B
Backup = C
```

Application never breaks.

---

# 11. Pin Expiration

Pins should not be permanent.

Reasons:

### Key compromise

### Infrastructure changes

### Certificate replacement

### Algorithm upgrades

Applications should support:

```text
Pin Refresh
```

rather than hardcoding forever.

---

# 12. Fail Closed Principle

Correct behavior:

```text
Fingerprint Match?
↓
No
↓
Reject Connection
```

Incorrect behavior:

```text
Fingerprint Match?
↓
No
↓
Continue Anyway
```

This defeats pinning entirely.

---

# 13. Google Recommendations

Google recommends:

### SHA256

### Public Key Pinning

### Backup Pins

### Rotation Support

### Fail Closed Validation

because these provide resilience without sacrificing security.

---

# Example Architecture

Application stores:

```text
Primary Pin
Backup Pin
```

Connection:

```text
Receive Certificate
↓
Extract SPKI
↓
Generate SHA256
↓
Compare
↓
Primary Match?
↓
Yes → Accept

No
↓
Backup Match?
↓
Yes → Accept

No
↓
Reject
```

---

# Benefits

Protects against:

- Rogue CAs
- MITM proxies
- Fake certificates
- User-installed certificates

while still supporting:

- Certificate rotation
- High availability
- Disaster recovery

---

# Summary

Certificate fingerprints uniquely identify certificates.

SHA256 is the preferred fingerprint algorithm.

Certificate pinning trusts a specific certificate.

Public key pinning (SPKI) trusts the public key instead of the certificate.

Primary pins alone are dangerous.

Backup pins are essential.

Certificate rotation requires multiple pins.

Secure implementations fail closed and reject mismatches.

# Lab 5 – TLS Certificate Pinning Bypass & MitM Attack

# Part 11 – HTTP Toolkit, mitmproxy and HTTPS Interception Internals

---

# Objective

Understand:

- How HTTPS interception works
- Why a proxy certificate is needed
- How mitmproxy generates fake certificates
- How HTTP Toolkit works internally
- Why certificate pinning blocks interception
- Why banking applications resist proxy inspection

---

# 1. Why HTTPS Traffic Cannot Normally Be Read

Suppose:

```text
Mobile App
↓
HTTPS
↓
Server
```

During TLS handshake:

- Session keys are established.
- Data becomes encrypted.

Anyone monitoring the network sees:

```text
A7F9D3E4...
```

instead of:

```json
{
    "username":"alice",
    "password":"secret"
}
```

This protects confidentiality.

---

# 2. Problem For Developers

Developers often need to inspect:

- API requests
- JSON responses
- Headers
- Cookies
- Tokens

But HTTPS encryption hides everything.

Therefore developers use:

```text
HTTPS Proxy
```

Examples:

- Burp Suite
- mitmproxy
- HTTP Toolkit

---

# 3. Position Of The Proxy

Normal communication:

```text
Client
↓
Server
```

With proxy:

```text
Client
↓
Proxy
↓
Server
```

The proxy becomes an intermediary.

---

# 4. TLS Session Splitting

Normal HTTPS:

```text
Client
↓
TLS
↓
Server
```

One encrypted tunnel exists.

With mitmproxy:

```text
Client
↓
TLS Session 1
↓
mitmproxy
↓
TLS Session 2
↓
Server
```

Two independent encrypted sessions exist.

---

# 5. Why mitmproxy Can Read Traffic

Traffic arrives:

```text
Encrypted
↓
mitmproxy
↓
Decrypted
↓
Visible Internally
↓
Encrypted Again
↓
Server
```

Thus mitmproxy sees:

- URLs
- Headers
- Cookies
- Tokens
- JSON payloads

in plaintext.

---

# 6. Dynamic Certificate Generation

Suppose the app connects to:

```text
api.bank.com
```

mitmproxy creates:

```text
Fake api.bank.com Certificate
```

and signs it using:

```text
mitmproxy Root CA
```

The app receives:

```text
api.bank.com
Certificate
```

although it was generated by mitmproxy.

---

# 7. mitmproxy Root CA

During installation, mitmproxy creates:

```text
mitmproxy Root Certificate Authority
```

Example:

```text
~/.mitmproxy
```

contains:

```text
mitmproxy-ca-cert.pem
mitmproxy-ca.p12
mitmproxy-ca-cert.cer
```

These are used to sign fake certificates.

---

# 8. Why Browsers Accept These Certificates

If the mitmproxy CA certificate is installed into:

```text
Windows Trust Store
Android Trust Store
Browser Trust Store
```

then:

```text
Fake Google Certificate
↓
Signed By mitmproxy CA
↓
Trusted
↓
Connection Succeeds
```

---

# 9. HTTP Toolkit Internals

HTTP Toolkit internally behaves similarly.

Architecture:

```text
Application
↓
HTTP Toolkit Proxy
↓
Internet
```

HTTP Toolkit:

- Generates certificates dynamically
- Intercepts requests
- Decrypts responses
- Displays traffic graphically

---

# 10. HTTP Toolkit Features

Displays:

### URL

Example:

```text
https://api.demo.com/login
```

---

### Headers

```text
Authorization
Content-Type
User-Agent
```

---

### Request Body

```json
{
    "username":"alice"
}
```

---

### Response Body

```json
{
    "token":"JWT"
}
```

---

### Timing Information

Shows:

- Request duration
- Response latency

---

### Status Codes

Example:

```text
200 OK
404 Not Found
500 Internal Server Error
```

---

# 11. Flow Inside HTTP Toolkit

Step 1

App sends request.

↓

Step 2

HTTP Toolkit receives traffic.

↓

Step 3

Traffic decrypted.

↓

Step 4

Visible to user.

↓

Step 5

Request forwarded to server.

↓

Step 6

Response returned.

↓

Step 7

Displayed graphically.

---

# 12. Example Intercepted Request

Application sends:

```http
POST /login
```

Body:

```json
{
    "username":"alice",
    "password":"secret"
}
```

HTTP Toolkit shows:

```json
{
    "username":"alice",
    "password":"secret"
}
```

Everything becomes visible.

---

# 13. Example Intercepted Response

Server returns:

```json
{
    "token":"eyJ..."
}
```

Proxy sees:

```json
{
    "token":"eyJ..."
}
```

---

# 14. Why This Is Called Man-In-The-Middle

Because communication becomes:

```text
App
↓
Proxy
↓
Server
```

instead of:

```text
App
↓
Server
```

The proxy stands in the middle.

---

# 15. Why Certificate Pinning Blocks This

The app expects:

```text
Google Certificate
```

But receives:

```text
mitmproxy Generated Certificate
```

Comparison:

```text
Expected Fingerprint
≠
Proxy Fingerprint
```

Result:

```text
TLS Handshake Failure
```

Connection blocked.

---

# 16. Why Banking Apps Resist MITM

Banking applications usually perform:

### SHA256 Fingerprint Validation

### Public Key Pinning

### Backup Pins

### Root Detection

### Integrity Checks

Thus even if:

```text
mitmproxy Root CA
```

is installed,

the app still rejects the connection.

---

# 17. Common Errors

When pinning fails:

Applications throw:

### SSLHandshakeException

Example:

```text
Certificate pinning failure
```

---

### Trust Anchor Not Found

Meaning:

```text
Certificate mismatch
```

---

### Handshake Failure

Connection terminated.

---

# 18. HTTP Toolkit Android Demo

HTTP Toolkit provides:

```text
android-ssl-pinning-demo
```

Purpose:

Demonstrate:

- Normal HTTPS interception
- Certificate pinning
- Pinning failures
- Security concepts

The application is intentionally designed for learning.

---

# 19. Educational Use

These tools are widely used for:

### API debugging

### Penetration testing

### Mobile application testing

### Malware analysis

### Reverse engineering

### Security research

They are not inherently malicious.

---

# Summary

mitmproxy and HTTP Toolkit work by creating two TLS sessions:

```text
Client
↓
TLS Session 1
↓
Proxy
↓
TLS Session 2
↓
Server
```

The proxy decrypts traffic in the middle.

To do this, it dynamically generates certificates signed by its own CA.

If the client trusts that CA, HTTPS becomes visible.

Certificate pinning defeats this process because the proxy certificate does not match the expected certificate.

Therefore the TLS handshake fails and interception becomes impossible.

# Lab 5 – TLS Certificate Pinning Bypass & MitM Attack

# Part 12 – Android Certificate Pinning Internals and Real-World Implementations

---

# Objective

Understand how Android applications actually implement certificate pinning.

Study:

- Android Network Security Config
- OkHttp CertificatePinner
- TrustKit
- iOS pinning
- Pin validation flow
- Primary and backup pins
- Real-world banking applications

---

# 1. Why Browsers and Mobile Apps Are Different

Browsers rely on:

```text
OS Trust Store
↓
Any Trusted CA
↓
Accept Connection
```

Mobile applications often require stronger security.

Instead of:

```text
Trust Any CA
```

they implement:

```text
Trust Only Specific Certificates
```

This is certificate pinning.

---

# 2. Android Certificate Validation

Without pinning:

```text
App
↓
TLS Handshake
↓
Certificate Chain Validation
↓
Trusted Root CA
↓
Connection Accepted
```

With pinning:

```text
App
↓
Certificate Validation
↓
Fingerprint Validation
↓
Pin Match?
↓
Accept
```

Otherwise:

```text
Reject Connection
```

---

# 3. Android Network Security Configuration

Introduced in:

```text
Android 7+
```

Provides:

- Certificate pinning
- Custom trust anchors
- Cleartext restrictions

Configuration file:

```text
network_security_config.xml
```

Location:

```text
res/xml/network_security_config.xml
```

---

# Example Structure

```xml
<network-security-config>

    <domain-config>

        <domain>api.example.com</domain>

        <pin-set>

            <pin digest="SHA-256">

                ABC123...

            </pin>

        </pin-set>

    </domain-config>

</network-security-config>
```

---

# Flow

Application

↓

Receives certificate

↓

Generate SHA256

↓

Compare against XML pin

↓

Match?

↓

Accept

Else

↓

Reject

---

# Advantages

Simple.

No code required.

Built into Android.

---

# 4. Cleartext Traffic Policy

Applications may forbid HTTP.

Example:

```xml
<base-config cleartextTrafficPermitted="false"/>
```

This ensures:

```text
HTTPS Only
```

No plaintext traffic.

---

# 5. OkHttp

One of the most popular Android networking libraries.

Used by:

- Retrofit
- Android applications
- Banking apps
- Enterprise apps

---

# Architecture

```text
Application
↓
Retrofit
↓
OkHttp
↓
HTTPS
↓
Server
```

---

# 6. CertificatePinner

OkHttp provides:

```text
CertificatePinner
```

Purpose:

Validate fingerprints before accepting connections.

---

# Example

```java
CertificatePinner pinner =
new CertificatePinner.Builder()
.add(
"api.example.com",
"sha256/ABC123..."
)
.build();
```

---

# Validation Flow

Connection

↓

Receive Certificate

↓

Generate SHA256

↓

Compare

↓

Match?

↓

Success

Else

↓

SSLHandshakeException

---

# 7. Multiple Pins

OkHttp supports:

```java
.add("api.example.com","PinA")
.add("api.example.com","PinB")
```

Benefits:

- Rotation support
- Backup pins
- High availability

---

# 8. Why Multiple Pins Matter

Suppose:

Current certificate:

```text
Pin A
```

Future certificate:

```text
Pin B
```

Both are stored:

```text
Pin A
Pin B
```

When rotation occurs:

```text
Pin B
```

becomes active.

Application continues working.

---

# 9. iOS Pinning

Common frameworks:

### URLSession

Built-in networking.

---

### TrustKit

Popular certificate pinning framework.

---

# TrustKit Features

Supports:

- Public key pinning
- Backup pins
- Reporting
- Rotation

---

# Validation Flow

```text
Receive Certificate
↓
Extract Public Key
↓
Generate SHA256
↓
Compare
↓
Match?
↓
Accept
```

Else:

```text
Reject Connection
```

---

# 10. Public Key Pinning

Preferred by:

- Google
- Apple
- Banking apps

Reason:

Certificates change frequently.

Public keys change less frequently.

Thus:

```text
Certificate A
↓
Certificate B
```

may still contain:

```text
Public Key X
```

No pinning failures occur.

---

# 11. Primary Pin

Application stores:

```text
Primary Pin
```

Example:

```text
Pin A
```

Validation:

```text
Pin A Match?
↓
Accept
```

---

# 12. Backup Pin

Application stores:

```text
Primary Pin
Backup Pin
```

Validation:

```text
Primary Match?
↓
No
↓
Backup Match?
↓
Yes
↓
Accept
```

This prevents service disruption.

---

# 13. Certificate Rotation

Certificates expire.

Current:

```text
Pin A
```

Future:

```text
Pin B
```

Stored:

```text
Primary = A
Backup = B
```

Later:

```text
Primary = B
Backup = C
```

Application never breaks.

---

# 14. Real Banking Applications

Banks often implement:

```text
TLS
↓
Certificate Pinning
↓
Root Detection
↓
Integrity Checks
↓
Authentication
↓
Backend Validation
```

Multiple layers provide defense.

---

# Examples

Commonly found in:

- HDFC
- SBI
- ICICI
- PayPal
- Stripe

---

# 15. Additional Protection

Applications may implement:

### Root Detection

Detect rooted devices.

---

### Emulator Detection

Detect virtual environments.

---

### Integrity Verification

Detect modified APKs.

---

### Debugger Detection

Detect analysis tools.

---

### Runtime Protection

Detect tampering.

---

# 16. Why Pinning Alone Is Not Enough

Pinning protects against:

- Rogue CAs
- HTTPS proxies
- MITM attacks

But not against:

- Rooted devices
- Runtime modifications
- Malware
- Compromised applications

Therefore modern applications combine:

```text
TLS
+
Pinning
+
Integrity Checks
+
Backend Validation
```

---

# 17. Pinning Errors

Common exceptions:

### SSLHandshakeException

Example:

```text
Certificate pinning failure!
```

---

### Trust Anchor Not Found

Meaning:

Certificate mismatch.

---

### Connection Refused

TLS handshake terminated.

---

# 18. Complete Android Pinning Architecture

```text
Application
↓
OkHttp
↓
CertificatePinner
↓
Receive Certificate
↓
Generate SHA256
↓
Primary Pin Match?
↓
Yes
↓
Accept

No
↓
Backup Pin Match?
↓
Yes
↓
Accept

No
↓
SSLHandshakeException
↓
Connection Terminated
```

---

# Summary

Android applications commonly implement certificate pinning using:

### network_security_config.xml

XML-based configuration.

---

### OkHttp CertificatePinner

Programmatic validation.

---

### TrustKit

Popular iOS framework.

---

Modern applications rely on:

- SHA256 fingerprints
- Public key pinning
- Primary pins
- Backup pins
- Rotation support

to defend against Man-in-the-Middle attacks while maintaining availability.

# Lab 5 – TLS Certificate Pinning Bypass & MitM Attack

# Part 13 – Runtime Instrumentation, Frida, Root Detection and Defense in Depth

---

# Objective

Understand:

- Why certificate pinning is not absolute security
- Runtime instrumentation
- Frida fundamentals
- Root detection
- Emulator detection
- Integrity checks
- Defense in depth
- Secure mobile application architecture

---

# 1. Why Certificate Pinning Is Not Perfect

Certificate pinning protects against:

- Rogue Certificate Authorities
- Malicious proxies
- HTTPS interception
- MITM attacks

However, certificate pinning assumes:

```text
Application
↓
Runs Normally
```

If the execution environment itself is compromised, stronger protections are required.

---

# 2. Security Assumptions

Certificate pinning assumes:

### Trusted Application

Code is unmodified.

### Trusted Runtime

No tampering.

### Trusted Device

No root access.

### Trusted Libraries

No modifications.

If these assumptions fail, security weakens.

---

# 3. Runtime Environment

Applications do not execute directly on hardware.

Android applications execute inside:

```text
ART Runtime
```

Java applications execute inside:

```text
JVM
```

Python applications execute inside:

```text
Python Interpreter
```

.NET applications execute inside:

```text
CLR
```

All application behavior passes through the runtime.

---

# 4. Static Analysis vs Dynamic Analysis

## Static Analysis

Examines code without executing it.

```text
APK
↓
Source Code
↓
Review
```

Tools:

- JADX
- apktool
- IDA
- Ghidra

---

## Dynamic Analysis

Observes the application while running.

```text
Running App
↓
Observe Behavior
```

Dynamic analysis allows:

- Function tracing
- API monitoring
- Memory inspection
- Performance debugging

---

# 5. Runtime Instrumentation

Instrumentation means:

```text
Observe Program Behavior During Execution
```

Examples:

- Debuggers
- Profilers
- Monitoring tools

Instrumentation itself is not malicious.

It is used for:

- Software testing
- Performance analysis
- Security research

---

# 6. Frida

Frida is a dynamic instrumentation framework.

Purpose:

Interact with running processes.

Capabilities include:

- Function tracing
- API observation
- Runtime analysis
- Reverse engineering
- Security testing

---

# Installation

```bash
pip install frida-tools
```

Verify:

```bash
frida --version
```

---

# Architecture

```text
Application
↓
Runtime
↓
Frida
↓
Observation Layer
```

---

# 7. Why Security Engineers Use Frida

Common uses:

### Malware analysis

Understand behavior.

---

### Reverse engineering

Study applications.

---

### Debugging

Observe function execution.

---

### API monitoring

Inspect calls.

---

### Security research

Understand protections.

---

# 8. Rooted Devices

Rooting grants elevated privileges.

Provides:

- System access
- Full filesystem access
- Kernel modifications

This increases attack surface.

---

# Normal Device

```text
App
↓
Restricted Environment
```

---

# Rooted Device

```text
App
↓
Elevated Privileges
↓
More Risk
```

---

# 9. Root Detection

Applications attempt to detect:

### su binary

Example:

```text
/system/bin/su
```

---

### BusyBox

---

### Magisk

---

### Writable partitions

---

### Debuggable flags

---

If detected:

```text
Root Found
↓
Terminate
```

---

# 10. Emulator Detection

Applications may detect:

### Android Emulator

### Virtual devices

### Generic hardware

### Known emulator files

Purpose:

Prevent analysis.

---

# Example Checks

Manufacturer:

```text
Genymotion
```

Hardware:

```text
goldfish
```

Device:

```text
generic
```

---

# 11. Debugger Detection

Applications detect:

### JDWP

### ptrace

### Debug flags

If debugger detected:

```text
Terminate
```

---

# 12. Integrity Checks

Applications verify:

```text
APK Signature
```

or

```text
Application Hash
```

Example:

Expected:

```text
ABC123
```

Current:

```text
ABC123
```

Success.

Modified application:

```text
XYZ999
```

Mismatch detected.

---

# 13. Runtime Integrity

Applications verify:

```text
Code Integrity
↓
Match?
↓
Continue
```

Else:

```text
Terminate
```

---

# 14. Why Root Detection Is Not Enough

Root detection:

```text
Raises Difficulty
```

but does not provide:

```text
Absolute Security
```

Security should never rely on one mechanism.

---

# 15. Defense In Depth

Modern applications combine:

```text
TLS
↓
Certificate Pinning
↓
Root Detection
↓
Integrity Checks
↓
Debugger Detection
↓
Authentication
↓
Authorization
↓
Backend Validation
```

Multiple layers increase resilience.

---

# 16. Zero Trust Philosophy

Modern security assumes:

```text
Nothing Is Trusted
```

Every request must be verified.

Principle:

```text
Never Trust
Always Verify
```

Even authenticated clients should be validated continuously.

---

# 17. Backend Validation

Servers should never trust:

- Clients
- Mobile applications
- Tokens without verification

Server must validate:

### Authentication

### Authorization

### Sessions

### Roles

### Inputs

---

# 18. Secure Mobile Architecture

```text
Mobile App
↓
TLS
↓
Certificate Pinning
↓
Root Detection
↓
Integrity Verification
↓
Authentication
↓
Authorization
↓
Backend APIs
↓
Database
```

Each layer contributes independently.

---

# 19. Failure Of One Layer

Suppose:

Certificate pinning fails.

Still protected by:

```text
Root Detection
↓
Integrity Checks
↓
Backend Validation
```

This is the principle of:

```text
Defense In Depth
```

---

# 20. Layered Security

Layer 1:

```text
TLS
```

Layer 2:

```text
Certificate Pinning
```

Layer 3:

```text
Root Detection
```

Layer 4:

```text
Integrity Verification
```

Layer 5:

```text
Authentication
```

Layer 6:

```text
Authorization
```

Layer 7:

```text
Monitoring
```

No single layer should be considered sufficient.

---

# Final Architecture For Lab 5

```text
HTTP Toolkit Demo App
↓
HTTPS
↓
Certificate Pinning
↓
Primary Pin
↓
Backup Pin
↓
Root Detection
↓
Integrity Checks
↓
Backend Validation
↓
Secure Communication
```

---

# Summary

Certificate pinning is a powerful protection mechanism, but security should not depend solely on it.

Modern applications combine:

- TLS
- Certificate Pinning
- Primary Pins
- Backup Pins
- Root Detection
- Emulator Detection
- Integrity Verification
- Backend Validation

to achieve defense in depth.

Security is strongest when multiple independent protections work together.

# Lab 5 – TLS Certificate Pinning Bypass & MitM Attack

# Part 14 – Final Architecture and Mapping to Problem Statement

---

# Objective

Bring together everything studied so far and design a complete architecture that satisfies the Lab 5 problem statement.

The lab combines:

- TLS interception
- HTTPS proxies
- Certificate pinning
- Defensive design
- Primary and backup pins
- Rotation support
- Reporting
- Documentation

---

# High-Level Architecture

```text
HTTP Toolkit Demo App
            ↓
HTTPS Requests
            ↓
mitmproxy
            ↓
mitm_logger.py
            ↓
intercepted_requests.json
            ↓
mitm_report.json
            ↓
mitm_dashboard.html


Defensive Side

secure_certificate_pinning.py

Primary Pin
Backup Pin
Rotation Support
Fail Closed Validation


Documentation

pinning_best_practices.md

attack_vs_defense.md
```

---

# Lab Folder Structure

```text
05-encryption-tls-pinning-mitm

│
├── mitm-demo
│     mitm_logger.py
│
├── defensive-pinning
│     secure_certificate_pinning.py
│
├── sample-data
│     intercepted_requests.json
│
├── reports
│     mitm_report.json
│     mitm_dashboard.html
│
├── documentation
│     pinning_best_practices.md
│     attack_vs_defense.md
│
├── screenshots
│
├── notes.md
│
└── README.md
```

---

# Component 1 – HTTP Toolkit Demo Application

Purpose:

Generate realistic HTTPS traffic.

Provides:

### Normal HTTPS communication

```text
App
↓
Server
```

---

### Certificate pinning

```text
Fingerprint Validation
↓
Accept or Reject
```

---

### Demonstration environment

Safe and intentionally designed for learning.

---

# Component 2 – mitmproxy

Purpose:

Intercept HTTPS traffic.

Architecture:

```text
App
↓
TLS Session 1
↓
mitmproxy
↓
TLS Session 2
↓
Server
```

Capabilities:

- Request inspection
- Response inspection
- Header analysis
- Traffic logging

---

# Component 3 – mitm_logger.py

Purpose:

Collect intercepted traffic.

Stores:

- URL
- Method
- Headers
- Status code
- Timestamp

Output:

```text
intercepted_requests.json
```

---

# Example

```json
{
  "url":"https://api.demo.com/login",
  "method":"POST",
  "status_code":200
}
```

---

# Component 4 – intercepted_requests.json

Purpose:

Persistent traffic storage.

Contains:

- Request information
- Response information
- Metadata

Used by:

```text
mitm_report.json
mitm_dashboard.html
```

---

# Component 5 – Report Generator

Produces:

```text
mitm_report.json
```

Contains:

### URLs

### Status codes

### Request counts

### Timing

### Headers

---

# Component 6 – HTML Dashboard

Produces:

```text
mitm_dashboard.html
```

Visual presentation:

- Tables
- Statistics
- Traffic summaries

---

# Component 7 – Defensive Pinning Engine

File:

```text
secure_certificate_pinning.py
```

Purpose:

Demonstrate secure certificate validation.

---

# Validation Flow

```text
Certificate
↓
Extract Public Key
↓
Generate SHA256
↓
Compare Primary Pin
↓
Match?
↓
Accept

No
↓
Compare Backup Pin
↓
Match?
↓
Accept

No
↓
Reject Connection
```

---

# Component 8 – Primary Pin

Current production certificate.

Example:

```text
Pin A
```

---

# Component 9 – Backup Pin

Future certificate.

Example:

```text
Pin B
```

Supports:

- Rotation
- Disaster recovery
- High availability

---

# Component 10 – Rotation Support

Current state:

```text
Primary = A
Backup = B
```

Future state:

```text
Primary = B
Backup = C
```

Application continues functioning.

---

# Component 11 – Fail Closed Behavior

Correct design:

```text
Pin Match?
↓
No
↓
Reject
```

Never:

```text
Pin Match?
↓
No
↓
Continue
```

---

# Component 12 – Documentation

## pinning_best_practices.md

Contains:

- SHA256
- SPKI
- Backup pins
- Rotation
- Fail closed design

---

## attack_vs_defense.md

Compares:

### MITM Attack

versus

### Certificate Pinning Defense

---

# Complete Data Flow

```text
HTTP Toolkit Demo App
↓
HTTPS Request
↓
mitmproxy
↓
mitm_logger.py
↓
intercepted_requests.json
↓
Report Generator
↓
mitm_report.json
↓
mitm_dashboard.html
```

---

# Defensive Flow

```text
Certificate Received
↓
Extract Public Key
↓
Generate SHA256
↓
Primary Pin Match?
↓
Accept

No
↓
Backup Pin Match?
↓
Accept

No
↓
Reject Connection
```

---

# Mapping to Problem Statement

### TLS interception

✔

Implemented using:

```text
mitmproxy
```

---

### HTTPS traffic analysis

✔

Using:

```text
mitm_logger.py
```

---

### Certificate pinning concepts

✔

Covered extensively.

---

### Defensive implementation

✔

Using:

```text
secure_certificate_pinning.py
```

---

### SHA256 fingerprints

✔

---

### Primary pins

✔

---

### Backup pins

✔

---

### Rotation support

✔

---

### Fail closed validation

✔

---

### JSON reporting

✔

```text
mitm_report.json
```

---

### HTML dashboard

✔

```text
mitm_dashboard.html
```

---

### Documentation

✔

```text
pinning_best_practices.md

attack_vs_defense.md
```

---

### Educational value

✔

---

### Interview value

✔

---

# Final Architecture

```text
                HTTP Toolkit Demo App
                          ↓
                     HTTPS Traffic
                          ↓
                      mitmproxy
                          ↓
                   mitm_logger.py
                          ↓
             intercepted_requests.json
                          ↓
                mitm_report.json
                          ↓
               mitm_dashboard.html

────────────────────────────────

               secure_certificate_pinning.py

                     SHA256 Pins
                    Primary Pin
                    Backup Pin
                   Rotation Support
                  Fail Closed Validation

────────────────────────────────

                 Documentation Layer

            pinning_best_practices.md
                 attack_vs_defense.md
```

---

# Conclusion

This architecture is fully aligned with the Lab 5 objectives.

It combines:

- TLS concepts
- HTTPS interception
- Certificate pinning
- Secure design principles
- Rotation support
- Reporting
- Documentation

while remaining safe, educational, and highly suitable for interviews and portfolio demonstrations.

# Lab 5 – TLS Certificate Pinning Bypass & MitM Attack

# Part 15 – Final Implementation Design and Execution Flow

---

# Objective

Transform the architecture into a practical implementation.

Understand:

- What each Python file will do.
- Data flow between components.
- Input and output formats.
- Reports and dashboards.
- Defensive pinning engine design.

---

# Complete System Overview

```text
HTTP Toolkit Demo App
        ↓
HTTPS Traffic
        ↓
mitmproxy
        ↓
mitm_logger.py
        ↓
intercepted_requests.json
        ↓
Report Generator
        ↓
mitm_report.json
        ↓
mitm_dashboard.html


Defensive Side

secure_certificate_pinning.py
        ↓
Primary Pin
Backup Pin
Rotation Support
Fail Closed Validation
```

---

# 1. mitm_logger.py

Purpose:

Capture HTTPS traffic flowing through mitmproxy.

---

## Input

Traffic intercepted by mitmproxy.

Examples:

```http
POST /login
GET /profile
POST /payment
```

---

## Information Extracted

### Timestamp

Example:

```text
2026-07-01 12:35:22
```

---

### HTTP Method

```text
GET
POST
PUT
DELETE
```

---

### URL

Example:

```text
https://api.demo.com/login
```

---

### Status Code

Example:

```text
200
404
500
```

---

### Headers

Example:

```json
{
 "Content-Type":"application/json"
}
```

---

## Output

```text
intercepted_requests.json
```

---

# Example

```json
[
 {
   "timestamp":"2026-07-01 12:00",
   "method":"POST",
   "url":"https://api.demo.com/login",
   "status_code":200
 }
]
```

---

# 2. intercepted_requests.json

Purpose:

Store captured traffic.

Acts as:

```text
Raw Dataset
```

for report generation.

---

Contains:

- Requests
- Responses
- Metadata

---

# 3. Report Generator

Reads:

```text
intercepted_requests.json
```

Produces:

```text
mitm_report.json
```

---

# Information Included

### Total Requests

Example:

```text
145
```

---

### Status Code Statistics

Example:

```text
200 → 120

404 → 15

500 → 10
```

---

### Unique URLs

Example:

```text
/login
/profile
/payments
```

---

### Methods

Example:

```text
GET
POST
```

---

# Example Report

```json
{
 "total_requests":145,
 "success":120,
 "errors":25
}
```

---

# 4. HTML Dashboard

Purpose:

Visual representation.

Generated file:

```text
mitm_dashboard.html
```

---

Displays:

### Table

Method

URL

Status Code

Timestamp

---

### Statistics

Total requests

Successes

Errors

---

### Traffic summary

Useful during demonstrations.

---

# 5. secure_certificate_pinning.py

Purpose:

Simulate defensive certificate validation.

---

Input:

Certificate fingerprint.

Example:

```text
SHA256(X)
```

---

Stored Values:

```text
Primary Pin

Backup Pin
```

---

Flow

```text
Certificate Received
↓
Generate SHA256
↓
Primary Match?
↓
Accept

No
↓
Backup Match?
↓
Accept

No
↓
Reject
```

---

# Example

Primary:

```text
ABC123
```

Backup:

```text
XYZ456
```

---

Incoming:

```text
ABC123
```

Result:

```text
Connection Allowed
```

---

Incoming:

```text
XYZ456
```

Result:

```text
Connection Allowed
```

---

Incoming:

```text
QWE999
```

Result:

```text
Connection Rejected
```

---

# Rotation Support

Current:

```text
Primary = A

Backup = B
```

Future:

```text
Primary = B

Backup = C
```

This avoids downtime.

---

# Fail Closed Principle

Correct:

```text
Unknown Pin
↓
Reject
```

Wrong:

```text
Unknown Pin
↓
Ignore
↓
Continue
```

---

# attack_vs_defense.md

Purpose:

Explain:

## Attack Side

HTTPS interception

Proxy certificates

MITM

---

## Defense Side

Certificate pinning

SHA256 fingerprints

Primary pins

Backup pins

Fail closed behavior

---

# pinning_best_practices.md

Contains:

### SHA256

### SPKI

### Rotation

### Backup Pins

### Primary Pins

### Fail Closed Design

### Defense In Depth

---

# Complete Attack Flow

```text
HTTP Toolkit Demo App
↓
HTTPS Request
↓
mitmproxy
↓
Certificate Generated
↓
Traffic Decrypted
↓
mitm_logger.py
↓
intercepted_requests.json
↓
JSON Report
↓
HTML Dashboard
```

---

# Complete Defensive Flow

```text
Server Certificate
↓
Extract Public Key
↓
SHA256
↓
Primary Match?
↓
Accept

No
↓
Backup Match?
↓
Accept

No
↓
Reject
```

---

# Final Folder Structure

```text
05-encryption-tls-pinning-mitm

│
├── mitm-demo
│      mitm_logger.py
│
├── defensive-pinning
│      secure_certificate_pinning.py
│
├── sample-data
│      intercepted_requests.json
│
├── reports
│      mitm_report.json
│      mitm_dashboard.html
│
├── documentation
│      attack_vs_defense.md
│      pinning_best_practices.md
│
├── screenshots
│
├── notes.md
│
└── README.md
```

---

# Final Outcome

Lab 5 demonstrates:

✓ HTTPS interception concepts

✓ TLS certificate validation

✓ Proxy architecture

✓ mitmproxy fundamentals

✓ Certificate pinning

✓ SHA256 fingerprints

✓ Primary pins

✓ Backup pins

✓ Rotation support

✓ Fail closed design

✓ JSON reports

✓ HTML dashboards

✓ Defense in depth

✓ Real-world mobile application security principles

This completes the theory foundation required before implementation.
