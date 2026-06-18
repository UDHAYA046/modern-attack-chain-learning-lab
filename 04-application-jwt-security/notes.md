
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
