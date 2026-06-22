
# Lab 4 – JWT Authentication Bypass & Algorithm Confusion Attack

# Introduction

This lab focuses on JSON Web Tokens (JWT), one of the most widely used mechanisms for authentication and authorization in modern web applications and APIs.

The objective is to understand:

- How JWTs work internally.
- Why JWTs are stateless.
- How claims are used.
- How signatures protect tokens.
- How improper validation introduces vulnerabilities.
- How attackers exploit weak JWT implementations.
- How defenders securely validate tokens.

---

# Authentication vs Authorization

These two concepts are often confused, but they solve different problems.

---

## Authentication

Authentication answers the question:

> Who are you?

Authentication verifies the identity of a user.

Examples:

- Username and password
- OTP
- Biometrics
- Smart cards
- JWT tokens

Example:

User enters:

```text
Username: alice
Password: ********
```

Server verifies credentials.

If valid:

```text
Identity = Alice
```

Authentication succeeds.

---

### Examples of Authentication

Google login

```text
Email + Password
↓
Google verifies credentials
↓
User identity established
```

ATM

```text
Card + PIN
↓
Bank verifies customer
↓
Authentication succeeds
```

Fingerprint unlock

```text
Fingerprint
↓
Device verifies fingerprint
↓
User authenticated
```

---

## Authorization

Authorization answers:

> What are you allowed to do?

Authorization determines permissions after authentication.

Example:

User:

```text
Alice
Role = User
```

Allowed:

```text
✓ View Profile
✓ Change Password
✓ Edit Personal Data
```

Not Allowed:

```text
✗ Delete Users
✗ Access Admin Dashboard
✗ Change Server Configuration
```

---

### Authorization Example

Administrator:

```text
Role = admin
```

Permissions:

```text
✓ Create Users
✓ Delete Users
✓ Modify Database
✓ Access Logs
```

Normal user:

```text
Role = user
```

Permissions:

```text
✓ View Profile
✓ Upload Files
```

No access to admin functions.

---

## Relationship Between Authentication and Authorization

Authentication happens first.

```text
User
 ↓
Authentication
 ↓
Identity Established
 ↓
Authorization
 ↓
Access Granted
```

Example:

```text
User = Alice
Role = admin
```

Authentication verifies Alice.

Authorization grants administrator privileges.

---

# Session-Based Authentication

Traditional applications maintain sessions on the server.

Example:

```text
User
 ↓
Login
 ↓
Server validates credentials
 ↓
Creates Session ID
 ↓
Stores session in database
 ↓
Returns session cookie
```

Browser stores:

```text
SESSION_ID = x7k29ds2
```

For every request:

```text
Browser
 ↓
Sends Cookie
 ↓
Server checks session database
 ↓
Returns response
```

---

## Session Architecture

```text
User
 ↓
Login
 ↓
Session Created
 ↓
Database
 ↓
Session ID Returned
 ↓
Cookie Stored
 ↓
Future Requests Use Session
```

---

## Problems With Session-Based Authentication

### Server Must Maintain State

Server stores sessions.

Example:

```text
Session Table

Session ID      User
x73ab2          Alice
m82jq9          Bob
```

Large applications may have millions of sessions.

---

### Scalability Issues

Suppose there are multiple servers.

```text
Server 1
Server 2
Server 3
```

All servers need access to the same session database.

This increases complexity.

---

### Session Synchronization

Load balancers may route requests to different servers.

Session information must be synchronized.

This creates:

- Bottlenecks
- Additional infrastructure requirements
- Complexity

---

# Stateless Authentication

JWT solves this problem.

Server stores nothing.

Everything needed is inside the token.

---

## JWT Flow

```text
User
 ↓
Login
 ↓
Server Creates JWT
 ↓
Client Stores Token
 ↓
Client Sends Token
 ↓
Server Verifies Signature
 ↓
Access Granted
```

No database lookup is required.

---

## Advantages

### Scalability

No session storage.

Every server can independently verify tokens.

---

### Faster

No session database lookup.

---

### Microservices Friendly

Multiple services can verify the same token.

```text
Frontend
 ↓
API Gateway
 ↓
Service A
 ↓
Service B
 ↓
Service C
```

Each service verifies JWT independently.

---

### Suitable For Cloud Applications

Used heavily in:

- AWS
- Azure
- GCP
- Kubernetes
- REST APIs

---

# What Is JWT?

JWT stands for:

```text
JSON Web Token
```

Standard:

```text
RFC 7519
```

JWT is a compact token format used for:

- Authentication
- Authorization
- Information exchange

---

# Structure of JWT

A JWT consists of three parts.

```text
Header.Payload.Signature
```

Example:

```text
xxxxx.yyyyy.zzzzz
```

Separated by dots.

---

## Header

Contains metadata.

Example:

```json
{
 "alg":"HS256",
 "typ":"JWT"
}
```

alg:

Algorithm used.

Examples:

- HS256
- HS384
- HS512
- RS256

typ:

Token type.

Usually:

```text
JWT
```

---

## Payload

Contains claims.

Example:

```json
{
 "username":"alice",
 "role":"user"
}
```

Payload stores:

- User information
- Roles
- Permissions
- Expiration
- Metadata

Payload is visible.

It is NOT encrypted.

---

## Signature

Protects token integrity.

Generated using:

```text
Signature =
HMACSHA256(
base64(header)+"."+base64(payload),
secret
)
```

Signature prevents attackers from modifying token contents.

---

# Complete JWT Example

Header

```json
{
 "alg":"HS256",
 "typ":"JWT"
}
```

Payload

```json
{
 "username":"alice",
 "role":"user"
}
```

Encoded token:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJ1c2VybmFtZSI6ImFsaWNlIiwicm9sZSI6InVzZXIifQ.
k7sjf73jdj8d72hdk72j...
```

---

# Purpose of Signature

Signature guarantees:

## Integrity

Payload cannot be modified.

Changing:

```json
role = user
```

to

```json
role = admin
```

changes the signature.

Verification fails.

---

## Authenticity

Token was generated by the legitimate server.

---

## Tamper Detection

Any modification invalidates the token.

---

# JWT Does NOT Encrypt Data

Many beginners misunderstand this.

JWT provides:

✓ Integrity

✓ Authentication

✓ Tamper detection

JWT does NOT provide:

✗ Confidentiality

Payload can be decoded easily.

Example:

```json
{
 "username":"alice",
 "role":"admin"
}
```

Anyone possessing the token can read this information.

---

# Base64URL Encoding

JWT sections are encoded using Base64URL.

Encoding is not encryption.

Encoding simply converts data into text representation.

Example:

Original:

```json
{
 "role":"admin"
}
```

Encoded:

```text
eyJyb2xlIjoiYWRtaW4ifQ
```

Can easily be decoded.

---

## JWT Visualization

```text
Header
{
 alg : HS256
 typ : JWT
}
          ↓

Payload
{
 username : alice
 role : user
}

          ↓

Signature
Generated using secret key

          ↓

Header.Payload.Signature

          ↓

JWT Token
```

---

# Summary

Authentication:

```text
Who are you?
```

Authorization:

```text
What are you allowed to do?
```

Session Authentication:

```text
Stateful
```

JWT Authentication:

```text
Stateless
```

JWT Structure:

```text
Header.Payload.Signature
```

JWT Provides:

```text
✓ Integrity
✓ Authenticity
✓ Tamper Detection
```

JWT Does Not Provide:

```text
✗ Encryption
✗ Confidentiality
```

# Claims in JWT

The payload section of a JWT contains claims.

Claims are pieces of information stored inside the token.

Example:

```json
{
    "username":"alice",
    "role":"admin",
    "email":"alice@gmail.com"
}
```

Each key-value pair is called a claim.

Claims may represent:

- Identity
- Roles
- Permissions
- Metadata
- Token validity information

---

# Types of Claims

JWT defines three categories of claims:

## Registered Claims

Standard claims defined by RFC 7519.

Examples:

```text
iss
sub
aud
exp
iat
nbf
jti
```

These claims are optional but widely used.

---

## Public Claims

Custom claims agreed upon between applications.

Example:

```json
{
    "role":"admin",
    "department":"finance"
}
```

Public claims help applications exchange user information.

---

## Private Claims

Application-specific claims.

Example:

```json
{
    "employee_id":"EMP1002"
}
```

Private claims are meaningful only to the application using them.

---

# Registered Claims

## iss (Issuer)

Specifies who created the token.

Example:

```json
{
    "iss":"google.com"
}
```

During validation:

```python
if token["iss"] != "google.com":
    reject()
```

Purpose:

Ensure tokens are accepted only from trusted issuers.

---

## sub (Subject)

Identifies the owner of the token.

Example:

```json
{
    "sub":"alice"
}
```

Meaning:

```text
This token belongs to Alice.
```

---

## aud (Audience)

Defines who should use the token.

Example:

```json
{
    "aud":"payment-service"
}
```

If another service receives it:

```text
Reject token
```

Purpose:

Prevent token replay between services.

---

## exp (Expiration Time)

Defines when the token expires.

Example:

```json
{
    "exp":1782431000
}
```

Server checks:

```python
current_time > exp
```

If true:

```text
Token expired
```

Reject.

Purpose:

Limit token lifetime.

---

## iat (Issued At)

Stores the token creation time.

Example:

```json
{
    "iat":1718700000
}
```

Useful for:

- Session age tracking
- Auditing

---

## nbf (Not Before)

Token becomes valid only after a certain time.

Example:

```json
{
    "nbf":1718700100
}
```

Current time:

```text
1718700000
```

Token remains invalid until:

```text
1718700100
```

Purpose:

Delayed activation.

---

## jti (JWT ID)

Unique token identifier.

Example:

```json
{
    "jti":"837a29dk82"
}
```

Used for:

- Replay detection
- Token revocation
- Blacklists

---

# Example Payload

```json
{
    "iss":"auth.company.com",
    "sub":"alice",
    "aud":"payment-service",
    "exp":1782431000,
    "iat":1782420000,
    "role":"admin"
}
```

---

# HS256

HS256 stands for:

```text
HMAC + SHA256
```

HS256 uses symmetric cryptography.

The same secret is used for:

- Signing
- Verification

---

# Symmetric Cryptography

Secret:

```text
mysecret123
```

Signing:

```text
Header + Payload
↓
HMAC SHA256
↓
Signature
```

Verification:

```text
Header + Payload + mysecret123
↓
Generate Signature Again
↓
Compare
```

If signatures match:

```text
Token valid
```

---

# HS256 Architecture

```text
Server

Secret Key
mysecret123

↓ Sign

JWT

↓

Client

↓

Server

Verify using same secret
```

Only one key exists.

---

# Advantages of HS256

Fast.

Simple.

Compact.

Suitable for:

- Internal applications
- Single servers

---

# Disadvantages of HS256

Every verifier must know the secret.

If secret leaks:

```text
Attacker
↓
Generate Tokens
↓
Bypass Authentication
```

---

# RS256

RS256 stands for:

```text
RSA + SHA256
```

It uses asymmetric cryptography.

Two keys exist.

---

## Private Key

Secret.

Used for signing.

Example:

```text
private.pem
```

---

## Public Key

Shared publicly.

Used for verification.

Example:

```text
public.pem
```

---

# RS256 Architecture

```text
Private Key
(Server)

↓ Sign

JWT

↓

Client

↓

API

↓

Verify using Public Key
```

---

# Advantages of RS256

Verification and signing are separated.

Public keys may be distributed safely.

Suitable for:

- OAuth
- OpenID Connect
- Microservices
- Enterprise systems

---

# Comparison Between HS256 and RS256

| Feature | HS256 | RS256 |
|----------|--------|--------|
| Key Type | Symmetric | Asymmetric |
| Keys | One | Two |
| Signing Key | Secret Key | Private Key |
| Verification Key | Same Secret | Public Key |
| Speed | Fast | Slower |
| Scalability | Lower | Higher |
| Enterprise Usage | Limited | High |

---

# Public Key Cryptography

Two keys exist.

## Public Key

Can be shared safely.

Example:

```text
public.pem
```

---

## Private Key

Must remain secret.

Example:

```text
private.pem
```

---

# Encryption

```text
Encrypt using Public Key
↓
Decrypt using Private Key
```

---

# Digital Signature

JWT uses signatures.

```text
Sign using Private Key
↓
Verify using Public Key
```

Purpose:

- Integrity
- Authenticity
- Tamper detection

---

# JWT Validation Process

When server receives:

```text
Authorization: Bearer eyJ...
```

It performs several steps.

---

## Step 1

Split token:

```text
Header.Payload.Signature
```

---

## Step 2

Decode header.

Example:

```json
{
    "alg":"HS256"
}
```

---

## Step 3

Decode payload.

Example:

```json
{
    "username":"alice",
    "role":"user"
}
```

---

## Step 4

Recompute signature.

For HS256:

```text
Header.Payload + secret
```

For RS256:

```text
Header.Payload + public key
```

---

## Step 5

Compare signatures.

If same:

```text
Accept token
```

Otherwise:

```text
Reject token
```

---

## Step 6

Validate claims.

Checks include:

### exp

Expired?

### iss

Correct issuer?

### aud

Correct audience?

### nbf

Token active?

### jti

Revoked?

---

# Complete JWT Validation Flow

```text
Request
↓
JWT Received
↓
Decode Header
↓
Decode Payload
↓
Verify Signature
↓
Validate Claims
↓
Authentication Success
↓
Authorization Checks
↓
Access Resource
```

---

# Security Assumptions

JWT security depends upon:

1. Signature verification is performed.
2. Algorithms are restricted.
3. Secrets remain protected.
4. Claims are validated.
5. Expired tokens are rejected.
6. Issuer and audience are verified.

If any assumption fails, attackers may exploit the implementation.

---

# Upcoming Attack Concepts

The following attacks exploit broken assumptions:

1. None Algorithm Attack

2. Claim Forgery

3. HS256 Secret Forgery

4. RS256 → HS256 Algorithm Confusion

5. Missing Claim Validation

6. Expired Token Reuse

7. Weak Secret Attacks

These concepts form the foundation of Lab 4.

# JWT Security Assumptions

JWT security depends on several assumptions.

```text
Token Received
↓
Signature Verified
↓
Claims Validated
↓
Access Granted
```

If any step fails:

```text
Authentication Bypass
Privilege Escalation
Unauthorized Access
```

may occur.

---

# None Algorithm Attack

## Background

Normal JWT header:

```json
{
    "alg":"HS256",
    "typ":"JWT"
}
```

The server verifies the signature using HS256.

---

## Malicious Header

Attacker changes:

```json
{
    "alg":"none",
    "typ":"JWT"
}
```

and removes the signature.

Token structure becomes:

```text
Header.Payload.
```

Notice:

```text
No signature exists.
```

---

## Historical Vulnerability

Some older JWT libraries trusted:

```json
{
    "alg":"none"
}
```

and skipped signature verification.

As a result:

```text
Header
Payload
(No Signature)
```

was accepted as valid.

---

## Attack Flow

```text
Legitimate Token
↓
Decode JWT
↓
Modify Payload
↓
role=user → role=admin
↓
alg=none
↓
Remove Signature
↓
Send Token
↓
Server Accepts Token
↓
Admin Access
```

---

## Example

Original Header:

```json
{
    "alg":"HS256",
    "typ":"JWT"
}
```

Original Payload:

```json
{
    "username":"alice",
    "role":"user"
}
```

Modified Payload:

```json
{
    "username":"alice",
    "role":"admin"
}
```

Modified Header:

```json
{
    "alg":"none",
    "typ":"JWT"
}
```

Signature:

```text
empty
```

Final Token:

```text
base64(header).base64(payload).
```

---

## Root Cause

Server trusted:

```text
Algorithm supplied by attacker.
```

instead of enforcing:

```text
HS256 only.
```

---

## Defense

Specify allowed algorithms:

```python
jwt.decode(
    token,
    secret,
    algorithms=["HS256"]
)
```

Never allow:

```python
algorithms=None
```

Never accept:

```text
alg=none
```

---

# Claim Forgery

Claims determine authorization.

Example:

```json
{
    "username":"bob",
    "role":"user"
}
```

Application:

```python
if role=="admin":
    show_admin_panel()
```

---

## Attack

Attacker changes:

```json
{
    "username":"bob",
    "role":"admin"
}
```

If signature verification is disabled:

```text
Privilege Escalation
```

occurs.

---

# Frequently Targeted Claims

## role

```json
{
    "role":"admin"
}
```

---

## is_admin

```json
{
    "is_admin":true
}
```

---

## permissions

```json
{
    "permissions":["delete_users"]
}
```

---

## subscription

```json
{
    "subscription":"premium"
}
```

---

## username

```json
{
    "username":"administrator"
}
```

---

# Expired Token Reuse

Payload:

```json
{
    "exp":1710000000
}
```

Current time:

```text
1720000000
```

Token should be rejected.

---

## Vulnerability

Server disables expiration checks:

```python
verify_exp=False
```

---

## Attack Flow

```text
Stolen Token
↓
Token Expired
↓
Server Ignores exp
↓
Token Accepted
↓
Unauthorized Access
```

---

# Missing Issuer Validation

Payload:

```json
{
    "iss":"evil.com"
}
```

Expected issuer:

```text
auth.company.com
```

If issuer validation is absent:

```text
Attacker-issued token accepted.
```

---

# Missing Audience Validation

Token intended for:

```json
{
    "aud":"payment-service"
}
```

Inventory service accepts it.

Result:

```text
Cross-Service Token Replay
```

---

# Weak Secret Attack

HS256 security depends entirely on the secret.

Weak examples:

```text
secret
password
admin123
mysecret
```

Strong examples:

```text
$9aKx#P81!qLm@6Wd
```

---

## Attack Flow

```text
JWT Token
↓
Brute Force Secret
↓
Secret Found
↓
Forge Token
↓
Admin Access
```

---

## Example

Secret:

```text
secret123
```

Attacker discovers:

```text
secret123
```

and creates:

```json
{
    "username":"attacker",
    "role":"admin"
}
```

with a valid signature.

---

# Summary

| Vulnerability | Root Cause |
|---------------|------------|
| None Algorithm Attack | Signature verification bypass |
| Claim Forgery | Trusting unverified claims |
| Expired Token Reuse | exp not checked |
| Missing Issuer Validation | iss not validated |
| Missing Audience Validation | aud not validated |
| Weak Secret Attack | Weak HS256 secret |

# JWT Security Vulnerabilities

JWT security depends on several assumptions.

```text
Token Received
↓
Signature Verified
↓
Claims Validated
↓
Access Granted
```

If any assumption fails, attackers may bypass authentication or escalate privileges.

---

# RS256 → HS256 Algorithm Confusion Attack

This is one of the most famous JWT vulnerabilities.

The attack abuses confusion between:

- Symmetric cryptography (HS256)
- Asymmetric cryptography (RS256)

combined with one critical mistake:

```text
Trusting the algorithm supplied by the token itself.
```

---

# Normal RS256 Authentication

Server possesses two keys:

Private key:

```text
private.pem
```

Public key:

```text
public.pem
```

Private key:

- Secret
- Used for signing

Public key:

- Shared publicly
- Used for verification

---

# Normal Flow

```text
Server
(private.pem)
↓
Signs JWT
↓
JWT Token
↓
Client
↓
API
(public.pem)
↓
Verify Signature
↓
Access Granted
```

Only the private key can create valid signatures.

---

# Why Public Keys Are Public

Public keys are intentionally public.

Examples:

- Google OAuth
- OpenID Connect
- JWKS endpoints
- Microservices

Anyone can download them.

Example:

```text
https://accounts.google.com/.well-known/jwks.json
```

This is normal.

---

# Vulnerable Server Logic

Server code:

```python
alg = header["alg"]

if alg == "RS256":
    verify_with_public_key()

elif alg == "HS256":
    verify_with_secret()
```

Problem:

```python
header["alg"]
```

comes from the attacker-controlled token.

---

# Original Token

Header:

```json
{
  "alg":"RS256",
  "typ":"JWT"
}
```

Payload:

```json
{
  "username":"alice",
  "role":"user"
}
```

Signature created using:

```text
private.pem
```

Verification uses:

```text
public.pem
```

---

# Attack Step 1

Attacker modifies header:

```json
{
  "alg":"HS256",
  "typ":"JWT"
}
```

Payload:

```json
{
  "username":"attacker",
  "role":"admin"
}
```

---

# Attack Step 2

Attacker already knows:

```text
public.pem
```

because it is public.

The attacker now uses:

```text
HMACSHA256(
header.payload,
public.pem
)
```

to generate a new signature.

---

# Attack Step 3

Server reads:

```json
{
  "alg":"HS256"
}
```

and thinks:

```text
This is an HS256 token.
```

It uses:

```text
public.pem
```

as the HMAC secret.

Since both attacker and server use the same value:

```text
Signature matches.
```

---

# Result

Payload:

```json
{
  "username":"attacker",
  "role":"admin"
}
```

is accepted.

Authentication bypass occurs.

---

# Attack Chain

```text
RS256 Token
↓
Attacker obtains public.pem
↓
Change alg to HS256
↓
Forge role=admin
↓
Sign using public.pem
↓
Send token
↓
Server trusts alg field
↓
Uses public.pem as HMAC secret
↓
Signature matches
↓
Admin Access
```

---

# Root Cause

The vulnerability is NOT RSA.

The vulnerability is NOT HMAC.

The vulnerability is:

```text
Trusting attacker-controlled algorithm values.
```

---

# Incorrect Implementation

Bad:

```python
alg = token.header["alg"]

verify_using(alg)
```

---

# Correct Implementation

Good:

```python
jwt.decode(
    token,
    public_key,
    algorithms=["RS256"]
)
```

The algorithm should come from server configuration.

Never from the token.

---

# Algorithm Pinning

Algorithm pinning means:

```text
Accept only one predefined algorithm.
```

Examples:

```python
algorithms=["HS256"]
```

or

```python
algorithms=["RS256"]
```

All other algorithms are rejected.

---

# Why Modern Libraries Are Safer

Old libraries:

```python
jwt.decode(token,key)
```

trusted the algorithm inside the token.

Modern libraries require:

```python
algorithms=["RS256"]
```

which prevents algorithm confusion attacks.

---

# Complete JWT Attack Landscape

None Algorithm Attack
↓
Signature Disabled

Claim Forgery
↓
Claims Trusted

Weak Secret Attack
↓
Secret Guessed

RS256→HS256 Attack
↓
Algorithm Confusion

Missing Claim Validation
↓
iss, aud, exp ignored

Expired Token Reuse
↓
verify_exp=False


# Weak Secret Attacks

HS256 uses one secret for:

- Signing
- Verification

Security depends entirely upon the strength of this secret.

---

# Weak Secrets

Examples:

```text
secret
password
admin
admin123
welcome
qwerty
mysecret
test123
```

These secrets have low entropy and are easily guessable.

---

# Strong Secrets

Examples:

```text
A$8#Kd92!LpQ@17XzM4^Nc
T#9vL$28Pq@M7xRb!5Jd%F2Z
```

Characteristics:

- Random
- Long
- High entropy
- Uppercase characters
- Lowercase characters
- Numbers
- Symbols

---

# Attack Principle

Attacker obtains a JWT:

```text
Header.Payload.Signature
```

Header and Payload are visible.

Signature is visible.

Only the secret is unknown.

Attacker repeatedly guesses secrets and computes signatures.

When signatures match:

```text
Secret Found
```

Attacker can now forge tokens.

---

# Dictionary Attack

Uses common passwords.

Example:

```text
rockyou.txt

password
admin
secret
welcome
secret123
```

Much faster than brute force.

---

# Brute Force Attack

Tries all combinations:

```text
aaaa
aaab
aaac
...
```

Until the correct secret is discovered.

---

# Consequences

Suppose:

Secret:

```text
secret123
```

Attacker finds the secret.

Creates:

```json
{
 "username":"attacker",
 "role":"admin"
}
```

Generates a valid signature.

Server accepts token.

Authentication bypass occurs.

---

# Entropy

Entropy measures randomness.

Low entropy:

```text
admin123
```

High entropy:

```text
P@7#Lm$29Xq!Vb8R
```

High entropy secrets are harder to guess.

---

# Good JWT Secrets

Minimum:

32 bytes

Recommended:

64 bytes

Properties:

- Random
- High entropy
- Not dictionary words
- Contains symbols, numbers and mixed case

---

# HS256 vs RS256

HS256:

```text
One Secret
↓
Sign
↓
Verify
```

Secret compromise allows token forgery.

---

RS256:

```text
Private Key
↓
Sign

Public Key
↓
Verify
```

Private key never leaves the server.

Therefore RS256 is resistant to weak-secret attacks.

# JWT Hardening and Secure Validation

JWT vulnerabilities usually occur because the application does not validate the token correctly.

A JWT should never be trusted just because it is present in the request.

A secure application must verify:

- The token signature
- The allowed algorithm
- The issuer
- The audience
- The expiration time
- The token activation time
- The token ID
- The authorization claims

---

# Core Security Principle

JWT security depends on this rule:

```text
Never trust attacker-controlled token content before verification.
```

The token header and payload are both controlled by whoever sends the token.

That means an attacker can modify:

```json
{
  "alg": "none"
}
```

or:

```json
{
  "role": "admin"
}
```

A secure server must verify the signature and claims before using any information inside the token.

---

# Principle 1 — Never Trust the JWT Header

The JWT header contains the algorithm.

Example:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

The dangerous mistake is allowing the token itself to decide how it should be verified.

Bad logic:

```python
alg = token.header["alg"]
verify_using(alg)
```

This is unsafe because the attacker controls the header.

An attacker can change:

```json
{
  "alg": "RS256"
}
```

to:

```json
{
  "alg": "HS256"
}
```

or:

```json
{
  "alg": "none"
}
```

This creates vulnerabilities such as:

- None Algorithm Attack
- RS256 to HS256 Algorithm Confusion
- Signature bypass

---

# Correct Approach — Algorithm Pinning

Algorithm pinning means the server defines the accepted algorithm.

The token does not decide it.

Example for HS256:

```python
jwt.decode(
    token,
    secret,
    algorithms=["HS256"]
)
```

Example for RS256:

```python
jwt.decode(
    token,
    public_key,
    algorithms=["RS256"]
)
```

This means:

```text
Only this algorithm is accepted.
All other algorithms are rejected.
```

If an attacker changes the header to:

```json
{
  "alg": "none"
}
```

or:

```json
{
  "alg": "HS256"
}
```

when the server expects RS256, the token is rejected.

---

# Principle 2 — Reject the none Algorithm

The `none` algorithm means no signature.

A JWT using `alg:none` looks like:

```text
Header.Payload.
```

There is no signature after the final dot.

This should never be accepted in production authentication systems.

Accepting unsigned JWTs allows attackers to:

- Modify the payload
- Change role values
- Impersonate users
- Gain admin access

Defense:

```text
Reject all unsigned tokens.
Never allow alg:none.
Always require a valid signature.
```

---

# Principle 3 — Verify Signature Before Reading Claims

Claims should not be trusted until the signature is verified.

Wrong flow:

```text
Receive Token
↓
Decode Payload
↓
Read role=admin
↓
Grant Admin Access
↓
Verify Signature Later
```

This is insecure.

Correct flow:

```text
Receive Token
↓
Verify Signature
↓
Validate Claims
↓
Read Role
↓
Authorize Access
```

The server should never make authorization decisions based on unverified claims.

---

# Principle 4 — Validate Expiration Time

The `exp` claim defines when the token expires.

Example:

```json
{
  "exp": 1782431000
}
```

If the current time is greater than `exp`, the token is expired.

Expired tokens must be rejected.

Why this matters:

If a token is stolen, expiration limits how long it can be abused.

Bad practice:

```python
verify_exp = False
```

Risk:

```text
Old stolen tokens may remain usable forever.
```

Good practice:

```text
Use short-lived access tokens.
Reject expired tokens.
Use refresh tokens separately if needed.
```

---

# Principle 5 — Validate Issuer

The `iss` claim identifies who issued the token.

Example:

```json
{
  "iss": "auth.company.com"
}
```

The server should verify that the issuer matches the trusted identity provider.

Expected issuer:

```text
auth.company.com
```

Malicious issuer:

```text
evil.com
```

If issuer validation is missing, an attacker may create a token from an untrusted source and the application may accept it.

Defense:

```python
jwt.decode(
    token,
    key,
    algorithms=["RS256"],
    issuer="auth.company.com"
)
```

---

# Principle 6 — Validate Audience

The `aud` claim defines the intended recipient of the token.

Example:

```json
{
  "aud": "payment-service"
}
```

A token intended for the payment service should not be accepted by the inventory service.

Without audience validation, attackers may reuse tokens across services.

This is called:

```text
Cross-service token replay.
```

Defense:

```python
jwt.decode(
    token,
    key,
    algorithms=["RS256"],
    audience="payment-service"
)
```

---

# Principle 7 — Validate Not Before

The `nbf` claim means "not before."

Example:

```json
{
  "nbf": 1782431000
}
```

The token should not be accepted before this time.

If the current time is earlier than `nbf`, the token must be rejected.

This prevents premature token usage.

---

# Principle 8 — Validate JWT ID

The `jti` claim is a unique identifier for the token.

Example:

```json
{
  "jti": "837a29dk82"
}
```

It is useful for:

- Token revocation
- Replay detection
- Blacklisting compromised tokens
- Audit trails

Example:

If a token is compromised, its `jti` can be added to a denylist.

Then even if the signature is valid, the token can be rejected.

---

# Principle 9 — Use Strong Secrets for HS256

HS256 depends completely on a shared secret.

Weak secret:

```text
secret123
```

Strong secret:

```text
T#9vL$28Pq@M7xRb!5Jd%F2Z
```

A good HS256 secret should be:

- Random
- Long
- High entropy
- At least 32 bytes
- Preferably 64 bytes
- Not a dictionary word
- Not reused across environments

If the HS256 secret is weak, attackers can brute-force it and forge valid tokens.

---

# Principle 10 — Protect Private Keys for RS256

RS256 uses:

```text
Private key → signs tokens
Public key  → verifies tokens
```

The private key must remain secret.

If the private key leaks, attackers can generate valid RS256 tokens.

Good practices:

- Store private keys in secure secret managers
- Rotate keys periodically
- Use restricted file permissions
- Do not commit keys to GitHub
- Use environment variables or vault systems

---

# Principle 11 — Use Short-Lived Access Tokens

Long-lived tokens increase risk.

Bad:

```text
Token valid for 365 days
```

Better:

```text
Token valid for 15 minutes
```

Short-lived tokens reduce the damage window if a token is stolen.

Refresh tokens can be used separately to obtain new access tokens.

---

# Principle 12 — Use HTTPS

JWTs are bearer tokens.

This means:

```text
Whoever possesses the token can use it.
```

If JWTs are transmitted over HTTP, attackers on the network may capture them.

Attack flow:

```text
User sends JWT over HTTP
↓
Attacker sniffs network traffic
↓
Token stolen
↓
Attacker replays token
↓
Unauthorized access
```

Defense:

```text
Always use HTTPS.
```

---

# Principle 13 — Never Store Sensitive Data Inside JWT

JWT payloads are Base64URL encoded.

They are not encrypted.

Anyone with the token can decode the payload.

Bad payload:

```json
{
  "username": "alice",
  "password": "admin123",
  "credit_card": "4111-xxxx"
}
```

Good payload:

```json
{
  "sub": "user123",
  "role": "user",
  "exp": 1782431000
}
```

JWT provides:

```text
Integrity
Authenticity
Tamper detection
```

JWT does not provide:

```text
Confidentiality
Encryption
Secrecy
```

---

# Secure JWT Validation Flow

A secure JWT validation flow should look like this:

```text
Request Received
↓
Extract JWT from Authorization Header
↓
Reject Missing Token
↓
Enforce Expected Algorithm
↓
Verify Signature
↓
Reject Invalid Signature
↓
Validate exp
↓
Validate iss
↓
Validate aud
↓
Validate nbf
↓
Check jti Revocation Status
↓
Read Claims
↓
Apply Authorization Logic
↓
Grant or Deny Access
```

---

# Mapping Defenses to Attacks

| Attack | Root Cause | Defense |
|---|---|---|
| None Algorithm Attack | Unsigned tokens accepted | Reject `alg:none` and pin algorithms |
| Claim Forgery | Claims trusted without valid signature | Verify signature before reading claims |
| Expired Token Reuse | `exp` ignored | Enforce expiration validation |
| Missing Issuer Validation | Any issuer accepted | Validate `iss` |
| Missing Audience Validation | Token accepted by wrong service | Validate `aud` |
| Weak Secret Attack | Guessable HS256 secret | Use high-entropy secrets |
| RS256 to HS256 Confusion | Token controls algorithm | Pin algorithm server-side |
| Replay Attack | Same token reused repeatedly | Use `jti`, expiry, and revocation lists |
| Token Sniffing | Token sent insecurely | Use HTTPS |
| Sensitive Data Exposure | Payload contains secrets | Never store secrets in JWT |

---

# Key Takeaway

JWTs are not unsafe by default.

JWTs become unsafe when developers:

- Trust token headers
- Skip signature verification
- Accept `none`
- Use weak secrets
- Ignore expiration
- Ignore issuer and audience
- Store sensitive data in payloads
- Make authorization decisions before validation

Secure JWT usage requires strict validation and clear separation between authentication, authorization, and token parsing.

# Lab 4 Implementation Architecture

The objective of Lab 4 is to safely understand JWT authentication weaknesses by creating an intentionally vulnerable local application and attacking it in a controlled environment.

This lab must remain:

- Local
- Self-contained
- Educational
- Defensive in purpose

The system is divided into four major components:

1. Vulnerable Flask API
2. JWT Attack Toolkit
3. Secure Validator
4. Reporting and Hardening Module

---

# Overall Architecture

```text
User
↓
Vulnerable Flask API
↓
Normal JWT Generation
↓
JWT Attack Toolkit
↓
Forged Tokens
↓
/admin Endpoint
↓
Attack Result
↓
Secure Validator
↓
JSON Report
HTML Dashboard
Hardening Guide
```

---

# Component 1 — Vulnerable Flask API

The Flask application intentionally contains JWT weaknesses.

Purpose:

Allow safe experimentation.

The API contains three endpoints:

```text
/login
/profile
/admin
```

---

# /login Endpoint

Purpose:

Generate a JWT for a normal user.

Example payload:

```json
{
    "username":"alice",
    "role":"user"
}
```

Example response:

```json
{
    "token":"eyJhbGc..."
}
```

---

# /profile Endpoint

Purpose:

Allow authenticated users to view their profile.

Requirements:

- Token required
- Signature verification performed
- Claims extracted

Example response:

```json
{
    "username":"alice",
    "role":"user"
}
```

---

# /admin Endpoint

Purpose:

Demonstrate authorization.

Normal behavior:

```text
Only role=admin may access.
```

Attack objective:

Forge tokens to gain administrator privileges.

---

# Component 2 — JWT Attack Toolkit

The attack toolkit generates manipulated tokens.

Its purpose is educational.

It attacks only the local Flask API.

No real systems are involved.

---

# None Algorithm Attack

Purpose:

Demonstrate signature bypass.

Attack flow:

```text
Legitimate Token
↓
Modify Header
↓
alg=none
↓
Remove Signature
↓
Modify role=user → admin
↓
Send Token
↓
Observe Result
```

---

# Claim Forgery

Purpose:

Demonstrate privilege escalation.

Example:

Original:

```json
{
    "role":"user"
}
```

Modified:

```json
{
    "role":"admin"
}
```

If signature verification is broken:

```text
Admin Access
```

may occur.

---

# RS256 → HS256 Algorithm Confusion

Purpose:

Demonstrate algorithm confusion.

Attack flow:

```text
Obtain public.pem
↓
Change alg=RS256 → HS256
↓
Use public key as HMAC secret
↓
Forge role=admin
↓
Generate Signature
↓
Send Token
↓
Observe Result
```

---

# Weak Secret Demonstration

Purpose:

Show why weak HS256 secrets are dangerous.

Example secret:

```text
secret123
```

Attack flow:

```text
JWT
↓
Guess Secret
↓
Generate Valid Signature
↓
Forge Token
↓
Admin Access
```

---

# Component 3 — Secure Validator

Purpose:

Demonstrate defensive JWT validation.

The secure validator performs:

- Algorithm pinning
- Signature verification
- exp validation
- iss validation
- aud validation
- nbf validation
- Role checks

This component demonstrates proper JWT security.

---

# Secure Validation Flow

```text
Receive Token
↓
Verify Signature
↓
Validate Algorithm
↓
Validate exp
↓
Validate iss
↓
Validate aud
↓
Validate nbf
↓
Extract Claims
↓
Authorization Checks
↓
Access Granted
```

---

# Component 4 — Reporting System

Purpose:

Document attack results.

Outputs:

```text
jwt_attack_report.json
jwt_security_dashboard.html
```

---

# JSON Report

Contains:

- Attack Name
- Vulnerability
- Forged Token Type
- Result
- Severity
- Recommendation

---

# HTML Dashboard

Contains:

- Attack Name
- Description
- Result
- Risk Level
- Mitigation

---

# Hardening Guide

Maps attacks to defenses.

Example:

| Attack | Defense |
|---------|---------|
| alg:none | Algorithm Pinning |
| Claim Forgery | Signature Verification |
| Algorithm Confusion | Fixed RS256 |
| Weak Secret | High Entropy Secret |
| Replay Attack | exp + jti |

---

# Security Boundary

This project:

✓ Uses local Flask APIs

✓ Uses simulated users

✓ Uses self-generated keys

✓ Demonstrates vulnerabilities safely

This project does not:

✗ Attack external systems

✗ Use third-party APIs

✗ Access real accounts

✗ Interact with production environments

---

# Folder Structure

```text
04-application-jwt-security
│
├── README.md
├── notes.md
│
├── src
│     vulnerable_api.py
│     jwt_attack_toolkit.py
│     secure_validator.py
│
├── keys
│     private.pem
│     public.pem
│
├── sample-data
│     sample_tokens.json
│
├── reports
│     jwt_attack_report.json
│     jwt_dashboard.html
│
└── terminal_screenshots.docx
```

---

# Problem Statement Mapping

Requirement:

Local Vulnerable API

Implementation:

Flask API

Status:

✓

---

Requirement:

alg:none attack

Implementation:

Attack Toolkit

Status:

✓

---

Requirement:

RS256→HS256 Confusion

Implementation:

Algorithm Confusion Module

Status:

✓

---

Requirement:

Claim Forgery

Implementation:

Role Escalation Module

Status:

✓

---

Requirement:

Hardening Guide

Implementation:

Secure Validator

Status:

✓

---

Requirement:

Python + Flask + PyJWT + cryptography

Implementation:

Core Stack

Status:

✓

---

# Final Lab Architecture

```text
Vulnerable Flask API
↓
JWT Generation
↓
Attack Toolkit
↓
Forged Tokens
↓
/admin Endpoint
↓
Results
↓
Secure Validator
↓
JSON Report
HTML Dashboard
Hardening Guide
```

This architecture fully satisfies the Lab 4 problem statement.

# Flask Fundamentals

Flask is a lightweight Python web framework used for building:

- REST APIs
- Authentication systems
- Microservices
- Backend applications

Flask follows a request-response model.

---

# Basic Flask Architecture

```text
Client
↓
HTTP Request
↓
Flask Route
↓
Python Function
↓
Response
```

Example:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World"
```

When a request reaches:

```text
/
```

Flask executes:

```python
home()
```

and returns:

```text
Hello World
```

---

# Why Flask For Lab 4?

Flask is ideal because:

- Small and simple
- Easy JWT integration
- REST API support
- Suitable for demonstrating vulnerabilities
- Commonly used in real applications

---

# REST APIs

REST APIs expose resources using HTTP methods.

Examples:

GET

```text
/profile
```

POST

```text
/login
```

DELETE

```text
/delete-user
```

PUT

```text
/update-profile
```

---

# Our API Architecture

The vulnerable API contains:

```text
/login
/profile
/admin
```

---

# /login Endpoint

Purpose:

Generate JWT.

Input:

```json
{
    "username":"alice"
}
```

Output:

```json
{
    "token":"eyJ..."
}
```

---

# /profile Endpoint

Purpose:

Return user information.

Requires JWT.

Example response:

```json
{
    "username":"alice",
    "role":"user"
}
```

---

# /admin Endpoint

Purpose:

Administrator-only resource.

Checks:

```python
role == "admin"
```

Returns:

```json
{
    "message":"Admin Access Granted"
}
```

Attack objective:

Bypass this authorization.

---

# HTTP Request Flow

```text
Browser
↓
HTTP Request
↓
Flask Route
↓
JWT Validation
↓
Authorization
↓
Response
```

---

# Authorization Header

JWT tokens are transmitted using:

```http
Authorization: Bearer eyJhbGc...
```

Structure:

```text
Bearer <JWT>
```

Server extracts:

```text
eyJhbGc...
```

and validates it.

---

# Route Protection

Typical workflow:

```text
Request
↓
Extract JWT
↓
Verify Signature
↓
Decode Payload
↓
Read Claims
↓
Execute Route
```

---

# User Roles

Normal User:

```json
{
    "username":"alice",
    "role":"user"
}
```

Administrator:

```json
{
    "username":"admin",
    "role":"admin"
}
```

Admin route performs:

```python
if role == "admin":
    grant_access()
```

This is the authorization logic attackers attempt to bypass.

---

# JWT Generation Process

JWT creation consists of three stages:

1. Header creation
2. Payload creation
3. Signature generation

---

# Step 1 — Header

Example:

```json
{
    "alg":"HS256",
    "typ":"JWT"
}
```

Purpose:

Specify:

- Token type
- Algorithm

---

# Step 2 — Payload

Example:

```json
{
    "username":"alice",
    "role":"user",
    "exp":1782431000
}
```

Contains:

- Claims
- User information
- Expiration
- Roles

---

# Step 3 — Signature Generation

For HS256:

```text
Signature =
HMACSHA256(
Base64(Header)+"."+Base64(Payload),
Secret
)
```

---

# Complete Token

```text
Header.Payload.Signature
```

Example:

```text
eyJhbGc...
.
eyJ1c2...
.
aj72jdh...
```

---

# Base64 Encoding

JWT components are Base64URL encoded.

Encoding is NOT encryption.

---

Original:

```json
{
    "role":"admin"
}
```

Encoded:

```text
eyJyb2xlIjoiYWRtaW4ifQ
```

Anyone can decode this.

JWT provides:

✓ Integrity

Not:

✗ Confidentiality

---

# JWT Structure

## Header

Example:

```json
{
    "alg":"HS256",
    "typ":"JWT"
}
```

Purpose:

Describe algorithm.

---

## Payload

Example:

```json
{
    "username":"alice",
    "role":"user"
}
```

Purpose:

Store claims.

---

## Signature

Purpose:

Guarantee:

- Integrity
- Authenticity
- Tamper detection

---

# PyJWT Library

PyJWT is the most popular Python JWT library.

Import:

```python
import jwt
```

---

# Generating Tokens

Example:

```python
payload = {
    "username":"alice",
    "role":"user"
}

token = jwt.encode(
    payload,
    secret,
    algorithm="HS256"
)
```

Produces:

```text
eyJhbGc...
```

---

# Token Verification

Example:

```python
decoded = jwt.decode(
    token,
    secret,
    algorithms=["HS256"]
)
```

Returns:

```json
{
    "username":"alice",
    "role":"user"
}
```

---

# Internal Working Of Verification

Step 1

Split token:

```text
Header.Payload.Signature
```

---

Step 2

Decode header:

```json
{
    "alg":"HS256"
}
```

---

Step 3

Decode payload:

```json
{
    "username":"alice",
    "role":"user"
}
```

---

Step 4

Recompute signature:

```text
Header.Payload + Secret
↓
HMAC SHA256
↓
Generated Signature
```

---

Step 5

Compare signatures.

Match:

```text
Token Valid
```

Mismatch:

```text
Reject Token
```

---

Step 6

Validate Claims

Checks:

```text
exp
iss
aud
nbf
jti
```

---

# Request Flow Inside Our Vulnerable API

```text
User
↓
POST /login
↓
JWT Generated
↓
Client Receives Token
↓
Stores Token
↓
GET /profile
↓
Authorization Header
↓
JWT Validation
↓
Claims Extraction
↓
Profile Returned
```

---

# Request Flow To Admin Endpoint

```text
User
↓
Authorization Header
↓
Extract JWT
↓
Decode Token
↓
Read role Claim
↓
role == admin ?
↓
Grant or Deny Access
```

Attackers target this flow.

---

# Vulnerable Authentication Flow

```text
Receive Token
↓
Decode Payload
↓
Read role=admin
↓
Grant Access
↓
Verify Signature Later
```

Problem:

Claims are trusted before verification.

---

# Secure Authentication Flow

```text
Receive Token
↓
Verify Signature
↓
Validate Claims
↓
Read Role
↓
Authorize User
↓
Grant Access
```

---

# Decorators In Flask

Decorators allow code execution before routes.

Example:

```python
@token_required
```

Workflow:

```text
Request
↓
Decorator
↓
JWT Verification
↓
Route Execution
```

Example:

```python
@app.route("/profile")
@token_required
def profile():
    return profile_data
```

Only authenticated users reach:

```python
profile()
```

---

# Typical Lab 4 Execution Flow

```text
POST /login
↓
Generate Normal JWT
↓
JWT Attack Toolkit
↓
None Algorithm Attack
Claim Forgery
RS256→HS256 Confusion
Weak Secret Demonstration
↓
Forged Token
↓
GET /admin
↓
Observe Response
↓
Secure Validator
↓
Generate Reports
```

---

# Final Lab Architecture

```text
Vulnerable Flask API
↓
JWT Generator
↓
JWT Attack Toolkit
↓
Forged Tokens
↓
Admin Endpoint
↓
Results
↓
Secure Validator
↓
JSON Report
HTML Dashboard
Hardening Guide
```
