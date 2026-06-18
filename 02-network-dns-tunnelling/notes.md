# DNS Tunnelling Detection Engine – Notes

# 1. DNS Fundamentals

## What is DNS?

DNS stands for **Domain Name System**.

DNS acts as the Internet's phonebook. Humans prefer remembering names such as:

* google.com
* github.com
* linkedin.com
* amazon.in

Computers communicate using IP addresses:

* 142.250.183.14
* 140.82.114.4

DNS translates domain names into IP addresses.

Example:

```text
google.com
↓
142.250.183.14
```

Without DNS, users would need to remember numerical IP addresses for every website.

---

## Why DNS Exists

Humans remember names more easily than numbers.

Instead of remembering:

```text
142.250.183.14
140.82.114.4
```

users simply type:

```text
google.com
github.com
```

DNS performs the translation automatically.

---

# 2. DNS Resolution Process

When a user enters:

```text
github.com
```

the computer does not know where GitHub is located.

It performs the following sequence:

```text
User
↓
Browser
↓
DNS Resolver
↓
DNS Server
↓
IP Address Returned
↓
Website Accessed
```

Example:

```text
github.com
↓
140.82.114.4
```

Once the IP address is obtained, the browser can establish a connection to the web server.

---

# 3. DNS Record Types

DNS stores different kinds of information in records.

---

## A Record

Maps a domain to an IPv4 address.

Example:

```text
google.com
↓
142.250.183.14
```

Most commonly used DNS record.

---

## AAAA Record

Maps a domain to an IPv6 address.

Example:

```text
google.com
↓
2404:6800:4007:80c::200e
```

---

## CNAME Record

CNAME stands for Canonical Name.

Used to create aliases.

Example:

```text
mail.company.com
↓
gmail.company.com
```

The alias points to another domain.

---

## TXT Record

Stores arbitrary textual information.

Examples:

```text
SPF Records
DKIM Records
Domain Verification
```

Example:

```text
google-site-verification=abc123
```

TXT records are frequently abused by malware for:

* Command and Control
* DNS Tunnelling
* Data Exfiltration

---

# 4. Why Attackers Abuse DNS

Most organizations block:

* FTP
* SSH
* Unknown applications

However, DNS traffic is almost always allowed because the Internet cannot function without DNS.

Attackers exploit this trust.

Instead of transmitting data through:

```text
HTTP
FTP
SMTP
```

they hide information inside:

```text
DNS Requests
```

Firewalls usually allow DNS traffic, making it an attractive communication channel.

---

# 5. DNS Tunnelling

DNS tunnelling is a technique where attackers hide data inside DNS queries or DNS responses.

Instead of sending information through HTTP, attackers encode information inside DNS requests.

Example:

Normal DNS query:

```text
google.com
```

Malicious DNS query:

```text
secretpassword.attacker.com
```

The attacker's DNS server receives the request and extracts:

```text
secretpassword
```

Thus data is exfiltrated through DNS.

---

## Why DNS Tunnelling Works

DNS servers simply forward requests.

They cannot determine whether:

```text
secretpassword.attacker.com
```

contains stolen information.

To DNS, it appears to be a normal domain request.

---

# 6. DNS Tunnelling Attack Flow

Typical attack sequence:

```text
Malware
↓
Steals Information
↓
Encodes Data
↓
Embeds Data Inside DNS Queries
↓
DNS Resolver Forwards Requests
↓
Attacker-Controlled DNS Server Receives Queries
↓
Extracts Hidden Data
```

Example:

```text
admin123.attacker.com
```

Attacker extracts:

```text
admin123
```

---

# 7. Base64 Encoding

DNS cannot carry arbitrary binary data.

Therefore attackers encode data before transmission.

Example:

Original text:

```text
admin123
```

Base64:

```text
YWRtaW4xMjM=
```

Embedded into DNS:

```text
YWRtaW4xMjM=.attacker.com
```

The attacker decodes it back to:

```text
admin123
```

---

## Common Encodings

### Base64

```text
admin123
↓
YWRtaW4xMjM=
```

---

### Hexadecimal

```text
admin123
↓
61646d696e313233
```

---

### Compression + Base64

Compress file

↓

Encode

↓

Split into chunks

↓

Transmit through DNS

---

# 8. File Exfiltration Through DNS

Suppose malware steals:

```text
secret.pdf
```

The file contents are encoded and split into pieces.

Example:

```text
chunk1.attacker.com
chunk2.attacker.com
chunk3.attacker.com
chunk4.attacker.com
```

Each DNS query carries a fragment.

The attacker's DNS server reconstructs the original file.

---

# 9. TXT Record Abuse

TXT records normally store text information.

Legitimate uses:

* SPF
* DKIM
* Domain Verification

Attackers abuse TXT records for:

* Command and Control
* Malware Communication
* Data Exfiltration

Example:

Malware sends:

```text
command.attacker.com
```

DNS server responds with:

```text
TXT:
download malware.exe
```

Malware interprets the response and executes the command.

---

# 10. CNAME Abuse

CNAME records create aliases.

Example:

```text
mail.company.com
↓
gmail.company.com
```

Attackers may chain aliases to hide infrastructure.

Example:

```text
victim.attacker.com
↓
relay.attacker.net
↓
hidden.evil.org
```

This makes attribution more difficult.

---

# 11. PCAP Files

PCAP stands for Packet Capture.

A PCAP file contains recorded network traffic.

Think of a PCAP file as:

```text
A video recording of packets
```

It contains:

* DNS packets
* HTTP packets
* TCP packets
* UDP packets
* ICMP packets

Example:

```text
network_traffic.pcap
```

PCAP files are widely used for:

* Network Forensics
* Malware Analysis
* Incident Response
* Traffic Analysis

---

# 12. Live Traffic vs PCAP Analysis

## Live Traffic

```text
Packets
↓
Analyzer
↓
Detection
```

Advantages:

* Real-time monitoring

Disadvantages:

* More complex

---

## PCAP Analysis

```text
PCAP File
↓
Analyzer
↓
Detection
```

Advantages:

* Repeatable
* Safe
* Easier to debug

For this lab, PCAP analysis is preferred.

---

# 13. Scapy

Scapy is a Python packet manipulation library.

It is widely used for:

* Packet analysis
* Packet generation
* Network research
* Protocol testing

Example:

```python
from scapy.all import rdpcap

packets = rdpcap("traffic.pcap")
```

Scapy can:

* Read packets
* Create packets
* Modify packets
* Analyze network traffic

---

# 14. DPKT

DPKT is another packet processing library.

Advantages:

* Lightweight
* Fast
* Efficient for large PCAP files

Compared to Scapy:

| Scapy             | DPKT                 |
| ----------------- | -------------------- |
| Easier            | Faster               |
| Beginner Friendly | Performance Oriented |
| Rich Features     | Lightweight          |

Scapy will be used in this lab because it is easier to understand and suitable for learning.

# 15. Subdomains

A subdomain is a label that appears before the primary domain.

Example:

```text id="3v62l3"
mail.google.com
```

Components:

```text id="1zvpi7"
mail → Subdomain
google → Domain
com → Top Level Domain
```

Another example:

```text id="mcbt88"
drive.mail.google.com
```

Components:

```text id="zmd7ee"
drive → Subdomain
mail → Subdomain
google → Domain
com → TLD
```

Subdomains are commonly used to organize services.

Examples:

* mail.google.com
* maps.google.com
* docs.google.com

---

# Why Subdomains Matter

Normal organizations use only a few subdomains.

However, attackers often create very deep domain structures to hide information.

Example:

```text id="b5yvzm"
abc.def.xyz.secret.attacker.com
```

Such domains are uncommon in normal traffic.

Therefore, subdomains become an important detection feature.

---

# 16. Query Length

Query length refers to the total number of characters present in a DNS request.

Example:

Normal:

```text id="3euk3u"
google.com
```

Length ≈ 10

---

Normal:

```text id="gx4h4v"
github.com
```

Length ≈ 10

---

Suspicious:

```text id="qsy6yt"
aj92kd92j39dj82jd92jd92jd.attacker.com
```

Length ≈ 40+

---

Very Suspicious:

```text id="q2otrb"
aj92jd82jd92j39d92kd82jd92j39d92j39dj29dj29d.attacker.com
```

Length ≈ 60+

---

## Why Long Domains Occur

Attackers encode information before transmission.

Example:

Original:

```text id="2sgo7a"
admin123
```

Encoded:

```text id="1tgsrl"
YWRtaW4xMjM=
```

The resulting DNS query becomes longer.

Thus:

```text id="30e9i7"
Long Query Length
↓
Potential Encoded Data
↓
Possible DNS Tunnelling
```

---

# 17. Subdomain Depth

Subdomain depth refers to the number of labels before the main domain.

Example:

```text id="7yzv2g"
mail.google.com
```

Depth = 1

---

Example:

```text id="vpljlwm"
drive.mail.google.com
```

Depth = 2

---

Example:

```text id="s6tm2z"
abc.def.xyz.secret.attacker.com
```

Depth = 4

---

## Why Deep Domains Are Suspicious

Attackers split encoded data into multiple labels.

Example:

```text id="2ud7yh"
chunk1.chunk2.chunk3.attacker.com
```

Large numbers of subdomains can indicate:

* DNS tunnelling
* Data exfiltration
* Command and Control

---

# 18. Shannon Entropy

Entropy measures randomness.

It was introduced by Claude Shannon and is widely used in:

* Cryptography
* Compression
* Malware Detection
* DNS Tunnelling Detection

---

## Low Entropy

Human-readable domains:

```text id="8y0el7"
google.com
amazon.com
linkedin.com
```

These contain predictable patterns.

Low entropy.

---

## High Entropy

Random strings:

```text id="o6ywdn"
aj92kd92ks82jd92k.attacker.com
```

These appear random.

High entropy.

---

## Why High Entropy Matters

Attackers often encode:

* Files
* Passwords
* Cookies
* Credentials

using:

* Base64
* Hexadecimal
* Compression

Encoded data looks random.

Therefore:

```text id="ab0t6n"
High Entropy
↓
Encoded Data
↓
Potential DNS Tunnelling
```

---

## Examples

Low Entropy:

```text id="ih9hgn"
mail.google.com
```

Entropy ≈ 2–3

---

Medium Entropy:

```text id="h7a2vx"
githubusercontent.com
```

Entropy ≈ 3–4

---

High Entropy:

```text id="waf3dg"
k29dj29dj92ks82jd.attacker.com
```

Entropy ≈ 4.5+

---

# 19. Query Frequency

Query frequency represents how many DNS requests are generated over a period of time.

Conceptually:

```text id="e8u2ee"
Number of Queries
-------------------
Time Interval
```

---

## Normal User

DNS requests:

```text id="sdl47f"
google.com
youtube.com
amazon.in
linkedin.com
```

Frequency:

20–100 requests/minute

Traffic is irregular.

---

## Malware

Suppose malware is exfiltrating data.

Requests:

```text id="p8m1lb"
chunk1.attacker.com
chunk2.attacker.com
chunk3.attacker.com
...
chunk500.attacker.com
```

Frequency:

500 requests/minute

This is abnormal.

---

## Why Frequency Matters

High frequency may indicate:

* DNS Tunnelling
* Command and Control
* Beaconing

---

# 20. Feature Extraction

Feature extraction means converting DNS traffic into measurable values.

Input:

```text id="nl9tnh"
aj92kd92ks82.chunk1.chunk2.attacker.com
```

Features extracted:

### Query Length

Number of characters.

---

### Entropy

Randomness.

---

### Subdomain Depth

Number of labels.

---

### Query Frequency

Requests per unit time.

---

### Repeated Patterns

chunk1

chunk2

chunk3

---

These features form the basis of detection.

---

# 21. Risk Scoring Engine

Every feature contributes to a risk score.

Example:

Domain:

```text id="v8r9u5"
aj92kd92ks82.chunk1.chunk2.attacker.com
```

---

Length:

Long

Score:

+3

---

Entropy:

High

Score:

+4

---

Subdomain Depth:

Large

Score:

+3

---

Frequency:

Very High

Score:

+5

---

Total:

```text id="4bjlwm"
3 + 4 + 3 + 5 = 15
```

---

# Risk Classification

Low

0–4

---

Medium

5–8

---

High

9–12

---

Critical

13+

---

# 22. Detection Pipeline

The DNS Tunnelling Detection Engine follows this architecture:

```text id="1azm8k"
DNS Query
        ↓
Feature Extraction
        ↓
Length Calculation
Entropy Calculation
Subdomain Depth Calculation
Frequency Analysis
Pattern Analysis
        ↓
Risk Scoring Engine
        ↓
Classification
        ↓
Recommendations
        ↓
Reports
```

---

# Detection Features Used In This Lab

The detector combines:

* Query Length
* Shannon Entropy
* Subdomain Depth
* Query Frequency
* Repeated Patterns

No single feature is sufficient.

Detection relies on combining multiple indicators.

This reduces false positives and improves reliability.


# 23. Beaconing

Beaconing refers to periodic communication between malware and attacker-controlled infrastructure.

Think of beaconing as malware saying:

```text
"Hey, I'm still alive."
```

at regular intervals.

Example:

```text
ping1.attacker.com
ping2.attacker.com
ping3.attacker.com
```

every 60 seconds.

---

## Why Attackers Use Beaconing

Attackers use beaconing to:

* Maintain persistence
* Receive commands
* Upload stolen data
* Download additional payloads
* Check if the infected host is still active

---

## Normal Human Traffic vs Beaconing

Human traffic is irregular:

```text
google.com
youtube.com
github.com
linkedin.com
```

The intervals vary.

Beaconing traffic is very regular:

```text
60 sec
60 sec
60 sec
60 sec
```

Regular timing often indicates automated activity.

---

# 24. Command and Control (C2)

Command and Control refers to communication between malware and attacker infrastructure.

Attack Flow:

```text
Attacker
↓
Command Server
↓
Malware
↓
Victim Machine
```

The attacker sends instructions and malware executes them.

Examples:

* Download malware
* Upload files
* Execute commands
* Sleep
* Start exfiltration

---

## DNS-Based Command and Control

Instead of HTTP, attackers may use DNS.

Example:

Malware sends:

```text
status.attacker.com
```

The DNS server replies:

TXT Record:

```text
download_payload.exe
```

Malware interprets the response and executes commands.

---

## Why DNS C2 Is Effective

DNS traffic is:

* Trusted
* Allowed by firewalls
* Essential for Internet communication

Therefore, DNS provides an excellent covert communication channel.

---

# 25. Domain Generation Algorithms (DGA)

DGA stands for:

```text
Domain Generation Algorithm
```

Instead of contacting:

```text
evil.com
```

malware generates thousands of random domains:

```text
k29dj92.com
aj82kd92.net
j39dk29.org
```

If one domain is blocked, malware simply tries another.

---

## Why Attackers Use DGA

DGA provides:

* Resilience
* Evasion
* Infrastructure rotation

Defenders may block:

```text
evil.com
```

but malware can generate:

```text
j39dk29.com
```

the next day.

---

## DGA Characteristics

DGA domains often exhibit:

### High Entropy

```text
aj92ks82jd92.com
```

---

### Random Characters

Not human-readable.

---

### Short Lifetime

Domains appear and disappear rapidly.

---

### Large Numbers

Thousands of domains may be generated daily.

---

# 26. False Positives

Not every strange domain is malicious.

Example:

```text
cloudfront.net
akamai.net
cdn77.net
```

These may appear random but are legitimate.

---

## Why False Positives Matter

A detector that flags everything becomes useless.

Goal:

```text
High Detection Rate
+
Low False Positives
```

---

## Detection Philosophy

One suspicious feature alone should not indicate malicious activity.

Example:

Long domain alone ≠ malicious.

High entropy alone ≠ malicious.

Multiple indicators together provide stronger evidence.

---

# 27. CDN Domains

CDN stands for:

```text
Content Delivery Network
```

Examples:

* Cloudflare
* Akamai
* AWS CloudFront

Example domain:

```text
d3j4k8.cloudfront.net
```

Looks random.

But completely legitimate.

---

## Purpose of CDNs

CDNs improve:

* Performance
* Availability
* Latency

Therefore many legitimate domains may appear suspicious.

---

# 28. Cloud Service Domains

Cloud providers automatically generate hostnames.

Examples:

AWS:

```text
ec2-34-100-120.compute.amazonaws.com
```

Azure:

```text
vm123.westus.cloudapp.azure.com
```

Google Cloud:

```text
instance-1.c.project.internal
```

These domains are not malicious.

---

## Important Principle

Long domains do not automatically imply attacks.

Detection should combine:

* Length
* Entropy
* Frequency
* Depth
* Repeated patterns

---

# 29. MITRE ATT&CK Mapping

MITRE ATT&CK provides a knowledge base describing attacker techniques.

---

## T1071.004

Application Layer Protocol : DNS

Attackers use DNS for:

* Command and Control
* Data Exfiltration
* Malware Communication

---

## T1001

Data Obfuscation

Attackers hide data through:

* Encoding
* Compression
* Obfuscation

Examples:

* Base64
* Hexadecimal

---

## T1105

Ingress Tool Transfer

Attackers download additional tools and payloads.

Examples:

* Malware updates
* Secondary payloads

---

## T1095

Non-Application Layer Protocol

Alternative communication channels are used to evade detection.

---

# 30. Detection Features

The DNS Tunnelling Detection Engine analyzes:

---

## Query Length

Long domains may contain hidden data.

---

## Shannon Entropy

Random-looking strings may indicate encoded information.

---

## Subdomain Depth

Large numbers of labels may indicate tunnelling.

---

## Query Frequency

High request rates may indicate:

* Beaconing
* C2 traffic
* Data exfiltration

---

## Repeated Patterns

Examples:

```text
chunk1.attacker.com
chunk2.attacker.com
chunk3.attacker.com
```

Repeated sequences often indicate file transfer.

---

# 31. Risk Classification

Low

```text
0 – 4
```

Minimal risk.

---

Medium

```text
5 – 8
```

Some suspicious characteristics.

---

High

```text
9 – 12
```

Multiple indicators present.

---

Critical

```text
13+
```

Strong evidence of DNS tunnelling or malicious communication.

---

# 32. Final Architecture

```text
Input Layer
│
├── Simulated DNS Dataset
├── DNS Log Dataset
└── Optional PCAP Input

                ↓

Feature Extraction Layer
│
├── Query Length
├── Shannon Entropy
├── Subdomain Depth
├── Query Frequency
└── Pattern Detection

                ↓

Detection Layer
│
├── DNS Tunnelling Indicators
├── DGA Detection
├── Beaconing Detection
└── False Positive Awareness

                ↓

Risk Engine
│
├── Risk Score
├── Risk Level
├── Findings
└── Recommendations

                ↓

Output Layer
│
├── JSON Report
├── CSV Summary
└── HTML Dashboard
```

---

# 33. Detection Pipeline

```text
DNS Query
        ↓

Feature Extraction
        ↓

Length Calculation
Entropy Calculation
Subdomain Depth Analysis
Frequency Analysis
Pattern Analysis

        ↓

Risk Scoring Engine

        ↓

Classification

Low
Medium
High
Critical

        ↓

Recommendations

        ↓

JSON Report
CSV Summary
HTML Dashboard
```

---

# 34. Detection Philosophy

The purpose of this project is NOT to detect malware directly.

The goal is to identify abnormal DNS behavior.

Indicators include:

* Long domains
* High entropy
* Deep subdomains
* High query frequency
* Repeated patterns
* Beaconing behavior
* DGA characteristics

Detection is based on combining multiple indicators rather than relying on a single feature.

This reduces false positives and improves confidence.

---

# 35. Learning Outcome

After completing this lab, I should be able to:

* Explain DNS internals
* Understand DNS tunnelling attacks
* Recognize data exfiltration techniques
* Analyze DNS traffic
* Understand entropy and randomness
* Detect beaconing behavior
* Explain Command and Control mechanisms
* Understand DGA domains
* Interpret MITRE ATT&CK mappings
* Build a DNS Tunnelling Detection Engine
* Generate JSON, CSV, and HTML reports
* Perform packet analysis using Scapy and PCAP files

---

# Lab 2 Theory Status

DNS Fundamentals ✅

DNS Tunnelling Basics ✅

Attack Mechanisms ✅

Base64 Encoding ✅

TXT Record Abuse ✅

CNAME Abuse ✅

PCAP Files ✅

Scapy and DPKT ✅

Query Length ✅

Subdomain Depth ✅

Entropy ✅

Frequency Analysis ✅

Beaconing ✅

Command and Control ✅

Domain Generation Algorithms ✅

False Positives ✅

MITRE ATT&CK Mapping ✅

Detection Features ✅

Risk Scoring ✅

Final Architecture ✅

Detection Philosophy ✅

Lab 2 Theory : COMPLETE ✅
