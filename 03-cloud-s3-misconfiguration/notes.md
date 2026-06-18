
# S3 Bucket Misconfiguration Scanner & Data Exposure Detector – Notes

# 1. Cloud Security Context

## What is Cloud Security?

Cloud security is the practice of protecting cloud-based systems, data, applications, storage services, identities, and infrastructure from unauthorized access, misuse, misconfiguration, data leakage, and attacks.

In traditional infrastructure, companies maintain their own servers, storage devices, and network equipment. In cloud computing, many of these responsibilities are shared between the cloud provider and the customer.

Examples of cloud providers:

* Amazon Web Services
* Microsoft Azure
* Google Cloud Platform

Cloud security is important because organizations store sensitive assets in the cloud, including:

* Customer records
* Financial reports
* Source code
* Application logs
* Database backups
* Machine learning datasets
* Employee records
* API keys
* Credentials
* Internal documents

Cloud platforms are powerful, but a small misconfiguration can expose a large amount of data.

---

# 2. Shared Responsibility Model

## What is the Shared Responsibility Model?

The shared responsibility model defines which security responsibilities belong to the cloud provider and which responsibilities belong to the customer.

In AWS:

AWS is responsible for security **of** the cloud.

The customer is responsible for security **in** the cloud.

---

## AWS Responsibility

AWS manages and secures:

* Physical data centers
* Hardware
* Networking infrastructure
* Storage infrastructure
* Availability zones
* Core cloud platform

Customers do not manage the physical machines behind S3.

---

## Customer Responsibility

Customers are responsible for configuring their cloud resources securely.

For S3, the customer is responsible for:

* Bucket permissions
* Bucket policies
* Access Control Lists
* Public access settings
* Encryption configuration
* Versioning configuration
* Object lifecycle rules
* Sensitive file management
* IAM permissions
* Monitoring and logging

This is why S3 misconfiguration is a customer-side cloud security issue.

---

# 3. What is Cloud Storage?

Cloud storage is a service that allows users and organizations to store data on remote infrastructure managed by a cloud provider.

Instead of buying and maintaining physical storage servers, users store data in cloud services.

Examples:

* Amazon S3
* Azure Blob Storage
* Google Cloud Storage

---

## Benefits of Cloud Storage

Cloud storage provides:

### Scalability

Storage can grow from a few files to petabytes of data.

---

### Durability

Cloud providers replicate data internally to prevent data loss.

---

### Availability

Data can be accessed when needed.

---

### Cost Efficiency

Users pay based on storage usage.

---

### Global Accessibility

Data can be accessed from applications, users, and services across the world.

---

## Security Challenge

Cloud storage is easy to create and use.

This also makes it easy to misconfigure.

A developer may create a bucket quickly for testing and forget to restrict access.

A team may enable website hosting and accidentally upload sensitive files.

Another team may forget encryption or versioning.

This is exactly why automated cloud security scanning is needed.

---

# 4. What is Amazon S3?

Amazon S3 stands for:

**Amazon Simple Storage Service**

It is AWS's object storage service.

S3 stores data as objects inside buckets.

---

## S3 Storage Model

Traditional file systems use folders and directories.

S3 uses:

* Buckets
* Objects
* Object keys

Example:

```text
Bucket
│
├── photo.jpg
├── report.pdf
├── backup.zip
└── database.sql
```

---

## Bucket

A bucket is a container for objects.

Example:

```text
company-backups
```

A bucket can contain many objects.

Buckets are globally unique across AWS.

This means no two AWS accounts can create the same bucket name globally.

---

## Object

An object is a file stored in S3.

Examples:

```text
salary.xlsx
database.sql
photo.png
backup.zip
customer_data.csv
```

Each object has:

* Key
* Data
* Metadata

---

## Object Key

The object key is the name or path of the object.

Example:

```text
documents/report.pdf
```

Although this looks like a folder path, S3 treats it as a key string.

S3 does not use folders internally in the same way a normal file system does.

---

## Metadata

Metadata is information about the object.

Examples:

* Content type
* Size
* Last modified timestamp
* Encryption status
* Storage class

---

# 5. Why S3 is Widely Used

S3 is used for many purposes.

## Static Website Hosting

Organizations can host static websites using S3.

Example files:

```text
index.html
style.css
logo.png
```

---

## Application Storage

Applications store:

* Images
* Videos
* PDFs
* Documents
* User uploads

---

## Backups

S3 is commonly used for:

```text
database.sql
backup.zip
server-backup.tar.gz
```

---

## Data Lakes

Large organizations store analytics datasets in S3.

These may include:

* Transaction data
* Logs
* Customer records
* Machine learning datasets

---

## Logs

S3 stores logs such as:

* CloudTrail logs
* Application logs
* Load balancer logs
* Security logs

---

## Machine Learning Datasets

S3 is often used to store:

* Training data
* Model artifacts
* Evaluation datasets

---

# 6. Why Attackers Target S3

Attackers target S3 because buckets often contain valuable data.

Examples of sensitive data in S3:

```text
source_code.zip
customer_data.csv
database.sql
backup.zip
credentials.txt
.env
private.pem
config.json
salary.xlsx
```

If a bucket is public or poorly configured, an attacker may access sensitive data without compromising a server.

This makes S3 misconfiguration a serious cloud security risk.

---

# 7. Real-World Impact of S3 Misconfiguration

Misconfigured S3 buckets have caused many real-world data leaks.

Common causes include:

* Public bucket access
* Public object access
* Weak bucket policies
* Missing encryption
* Sensitive files uploaded to public website buckets
* Lack of monitoring

The issue is usually not that S3 itself is insecure.

The issue is that S3 is powerful and flexible, but users may configure it incorrectly.

---

# 8. MITRE ATT&CK Mapping

The problem statement maps to:

```text
T1530 – Data from Cloud Storage Object
```

This technique describes attackers accessing data stored in cloud storage services.

---

## Attack Flow

```text
Attacker
↓
Finds Public Bucket
↓
Accesses Cloud Storage Objects
↓
Downloads Sensitive Files
↓
Exfiltrates Data
↓
Data Breach
```

---

# 9. Problem Statement Interpretation

The hackathon problem statement says that hundreds of S3 buckets in an AWS organization have been created by different teams with inconsistent security policies.

This means the environment has:

* Many buckets
* Many teams
* No consistent security baseline
* Different permission settings
* Different encryption settings
* Different versioning settings
* Possible public exposure

The goal is to build an automated auditor that can scan all buckets and identify risks.

---

# 10. What the Scanner Must Detect

The scanner must check for:

## Public ACLs

Public access granted through legacy ACL permissions.

---

## Missing Server-Side Encryption

Buckets that do not enforce encryption for stored objects.

---

## Disabled Versioning

Buckets where object versioning is not enabled.

---

## Missing Bucket Policies

Buckets that do not have explicit security policies.

---

## Public Static Website Hosting

Buckets configured as public websites.

---

## Sensitive Files

Files with names or extensions that indicate sensitive data.

Examples:

```text
passwords.txt
database.sql
backup.zip
customer_data.csv
secret.txt
config.json
.env
private.pem
credentials.txt
users.csv
```

---

# 11. Security Objective of Lab 3

The goal of Lab 3 is not to attack AWS.

The goal is to build a defensive cloud security scanner.

The scanner should:

* Enumerate buckets
* Analyze bucket configurations
* Detect misconfigurations
* Assign severity ratings
* Generate JSON and CSV reports
* Generate an HTML dashboard
* Provide remediation recommendations
* Support dry-run remediation

---

# 12. Final Mental Model

```text
AWS Account
↓
S3 Buckets
↓
Bucket Configuration
↓
Security Checks
↓
Findings
↓
Risk Score
↓
Severity
↓
Recommendations
↓
Reports
```

This is the foundation of the S3 Bucket Misconfiguration Scanner.


# 13. Identity and Access Management (IAM)

## What is IAM?

IAM stands for **Identity and Access Management**.

IAM is AWS's mechanism for controlling:

* Who can access resources.
* What actions they can perform.
* Which services they can interact with.

Think of IAM as the gatekeeper of AWS.

Without IAM, every user would have unrestricted access to every resource.

---

## Why IAM Exists

Organizations contain:

* Developers
* Security engineers
* Database administrators
* Application servers
* CI/CD pipelines

Not everyone should have access to everything.

Example:

A developer should not automatically have access to payroll backups.

Therefore permissions must be controlled.

---

# IAM Components

IAM consists of four major components:

## Users

Users represent individual identities.

Examples:

```text
Alice
Bob
AdminUser
```

Users authenticate using:

* Passwords
* Access keys
* MFA

---

## Groups

Groups contain multiple users.

Example:

```text
Developers
SecurityTeam
FinanceTeam
```

Permissions are assigned to groups rather than individual users.

---

## Roles

Roles provide temporary permissions.

Examples:

```text
EC2 Role
Lambda Role
Cross-Account Role
```

Roles are preferred because long-term credentials are avoided.

---

## Policies

Policies define permissions.

Policies are JSON documents.

Example:

```json
{
  "Effect":"Allow",
  "Action":"s3:GetObject",
  "Resource":"arn:aws:s3:::mybucket/*"
}
```

This means:

Allow reading objects inside mybucket.

---

# 14. S3 Security Layers

S3 security is enforced through multiple layers.

```text
IAM Policies
       ↓
Bucket Policies
       ↓
ACLs
       ↓
Public Access Block
       ↓
Object Permissions
```

AWS evaluates all layers together.

One misconfiguration may expose data.

---

# 15. Access Control Lists (ACLs)

ACL stands for Access Control List.

ACLs are the older mechanism for controlling access.

ACLs can be applied to:

* Buckets
* Individual objects

---

## Available Permissions

ACL permissions include:

```text
READ
WRITE
READ_ACP
WRITE_ACP
FULL_CONTROL
```

---

# Grantees

Permissions are granted to entities called grantees.

---

## Canonical User

Represents a specific AWS account.

Safe.

---

## AuthenticatedUsers Group

Represents any AWS user worldwide.

URI:

```text
http://acs.amazonaws.com/groups/global/AuthenticatedUsers
```

This is dangerous because millions of AWS users exist.

---

## AllUsers Group

Represents anonymous public users.

URI:

```text
http://acs.amazonaws.com/groups/global/AllUsers
```

This is extremely dangerous.

Anyone on the Internet can access the bucket.

---

# Example Dangerous ACL

Suppose:

Bucket:

```text
customer-backups
```

Permission:

```text
READ
```

Grantee:

```text
AllUsers
```

Attack flow:

```text
Attacker
↓
Discovers Bucket
↓
Downloads Objects
↓
Data Exposure
```

---

# Why Public ACLs are Dangerous

Public ACLs can expose:

```text
database.sql
salary.xlsx
backup.zip
customers.csv
```

This often leads directly to a data breach.

Therefore public ACLs are considered Critical severity.

---

# 16. Bucket Policies

Bucket policies are JSON documents attached to buckets.

They define who can perform actions.

Example:

```json
{
 "Effect":"Allow",
 "Principal":"*",
 "Action":"s3:GetObject",
 "Resource":"arn:aws:s3:::customer-data/*"
}
```

---

# Principal

Principal defines who receives permission.

Examples:

```text
Specific user
Specific account
IAM role
*
```

---

## Why Principal "*" is Dangerous

```json
"Principal":"*"
```

means:

Everyone.

Including anonymous Internet users.

---

# Dangerous Policy Example

```json
{
 "Effect":"Allow",
 "Principal":"*",
 "Action":"s3:GetObject",
 "Resource":"arn:aws:s3:::backup-bucket/*"
}
```

Attack chain:

```text
Attacker
↓
Reads Bucket
↓
Downloads Backup Files
↓
Sensitive Data Exposure
```

---

# Missing Bucket Policies

Buckets without policies may rely entirely on ACLs.

This creates:

* Inconsistent permissions
* Hard-to-manage security
* Accidental exposure

Therefore our scanner checks for missing bucket policies.

---

# 17. Public Access Block

AWS introduced Public Access Block to prevent accidental exposure.

It overrides dangerous settings.

---

## BlockPublicAcls

Blocks creation of public ACLs.

---

## IgnorePublicAcls

Ignores existing public ACLs.

---

## BlockPublicPolicy

Prevents dangerous public bucket policies.

---

## RestrictPublicBuckets

Restricts public access even if policies are present.

---

# Why Public Access Block Exists

Many breaches occurred because:

* Developers accidentally enabled public access.
* ACLs were misconfigured.
* Bucket policies allowed everyone.

Public Access Block acts as an additional safety layer.

---

# 18. Server-Side Encryption

Encryption protects stored data.

Even if storage media is compromised, encrypted data remains unreadable.

---

# Types of Encryption

## SSE-S3

AWS-managed encryption.

Uses AES-256.

Easy to enable.

Recommended minimum.

---

## SSE-KMS

Uses AWS Key Management Service.

Provides:

* Key rotation
* Logging
* Auditing
* Fine-grained permissions

More secure.

---

## SSE-C

Customer supplies encryption keys.

Rarely used.

---

# Why Missing Encryption is Dangerous

Without encryption:

```text
Compromised Storage
↓
Readable Files
↓
Sensitive Information Exposure
```

Examples:

```text
customers.csv
database.sql
salary.xlsx
```

Therefore missing encryption is a high-risk issue.

---

# 19. Versioning

Versioning preserves historical copies of objects.

Example:

Initial file:

```text
report.pdf
```

Updated file:

```text
report_v2.pdf
```

Internally:

```text
Version 1
Version 2
Version 3
```

are maintained.

---

# Why Versioning Matters

## Accidental Deletion

User deletes:

```text
backup.zip
```

Previous version can be restored.

---

## Ransomware Protection

Attack:

```text
Encrypt files
↓
Overwrite originals
```

Versioning allows recovery.

---

## Insider Threats

Deleted objects can be restored.

---

# Why Disabled Versioning is Risky

Without versioning:

```text
Delete Object
↓
Permanent Loss
```

Therefore disabled versioning receives Medium severity.

---

# 20. Website Hosting

S3 supports static website hosting.

Example files:

```text
index.html
style.css
logo.png
```

The bucket becomes publicly accessible.

---

# Website Hosting Risks

Sometimes developers accidentally upload:

```text
database.sql
backup.zip
config.json
passwords.txt
.env
```

along with website files.

Since website buckets require public access, sensitive data becomes exposed.

---

# 21. Sensitive File Detection

Our scanner searches for filenames such as:

```text
passwords.txt
database.sql
backup.zip
users.csv
credentials.txt
.env
config.json
private.pem
```

These files often contain:

* Passwords
* Database dumps
* API keys
* Secrets
* Certificates

If found inside public buckets, severity becomes Critical.

---

# 22. Risk Classification

## Low

No issues detected.

---

## Medium

Versioning disabled.

---

## High

Missing bucket policy.

---

## Critical

Public ACLs.

Missing encryption.

Sensitive files exposed.

Public website bucket containing secrets.

---

# Detection Philosophy

The scanner is defensive.

It does not attack AWS.

Its purpose is to:

* Identify misconfigurations.
* Reduce attack surface.
* Prevent data breaches.
* Provide recommendations.
* Improve cloud security posture.

This completes Part 2.

Part 3 will cover:

* boto3 fundamentals
* Bucket enumeration APIs
* Scanner architecture
* Risk scoring engine
* Auto-remediation
* Dry-run mode
* JSON reports
* CSV summaries
* HTML dashboard
* Final architecture
* MITRE ATT&CK mapping


# 23. boto3

## What is boto3?

boto3 is AWS's official Software Development Kit (SDK) for Python.

It allows Python programs to interact with AWS services.

Examples:

* S3
* EC2
* IAM
* Lambda
* DynamoDB
* CloudWatch

Our scanner uses boto3 to communicate with Amazon S3.

---

## Why boto3 is Needed

Without boto3, Python cannot interact with AWS resources.

Using boto3, we can:

* Enumerate buckets.
* Read bucket ACLs.
* Read bucket policies.
* Check encryption.
* Check versioning.
* Inspect website hosting.
* List objects.
* Generate reports.
* Perform remediation.

---

# Authentication

Before interacting with AWS, boto3 needs credentials.

Credentials can come from:

## AWS CLI

```bash
aws configure
```

Stores:

* Access Key ID
* Secret Access Key
* Default Region

---

## Environment Variables

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

---

## IAM Roles

Preferred approach in production.

Because:

* No hardcoded credentials.
* Temporary permissions.
* Better security.

---

# Creating an S3 Client

Example:

```python
import boto3

s3 = boto3.client("s3")
```

The client acts as a bridge between Python and AWS S3.

---

# 24. Bucket Enumeration

## Why Enumeration Matters

Organizations may contain:

```text
100 buckets
500 buckets
1000 buckets
```

Security teams cannot inspect each bucket manually.

Automation is necessary.

---

# list_buckets()

API:

```python
response = s3.list_buckets()
```

Returns:

```python
{
 "Buckets":[
     {"Name":"finance-backups"},
     {"Name":"website-assets"},
     {"Name":"logs-bucket"}
 ]
}
```

---

# Enumeration Loop

Example:

```python
for bucket in response["Buckets"]:
    print(bucket["Name"])
```

Output:

```text
finance-backups
website-assets
logs-bucket
```

Every bucket will be inspected individually.

---

# 25. ACL Inspection

API:

```python
s3.get_bucket_acl()
```

Purpose:

Determine whether permissions are granted to:

* AllUsers
* AuthenticatedUsers

---

# Dangerous ACL Example

```text
Grantee:
AllUsers

Permission:
READ
```

Meaning:

Anyone on the Internet can access the bucket.

Severity:

Critical

---

# 26. Bucket Policy Inspection

API:

```python
s3.get_bucket_policy()
```

Returns a JSON policy.

Scanner searches for:

```json
"Principal":"*"
```

and:

```json
"Effect":"Allow"
```

Together they indicate public access.

---

# Why Public Policies Are Dangerous

Attack flow:

```text
Attacker
↓
Find Public Bucket
↓
Download Objects
↓
Sensitive Data Exposure
```

Severity:

Critical

---

# 27. Encryption Inspection

API:

```python
s3.get_bucket_encryption()
```

Possible states:

## SSE-S3

Uses AES-256.

Secure.

---

## SSE-KMS

Uses Key Management Service.

Provides:

* Logging
* Auditing
* Key rotation

Most secure.

---

## Missing Encryption

No protection exists.

Severity:

High

---

# 28. Versioning Inspection

API:

```python
s3.get_bucket_versioning()
```

Possible values:

```text
Enabled
Suspended
None
```

---

# Why Versioning Matters

Without versioning:

```text
Delete Object
↓
Permanent Loss
```

Versioning protects against:

* Accidental deletion.
* Ransomware.
* Insider threats.

Severity:

Medium

---

# 29. Website Hosting Inspection

API:

```python
s3.get_bucket_website()
```

Purpose:

Determine whether the bucket hosts a website.

Website buckets are usually public.

---

# Risk

Sensitive files may accidentally become public.

Examples:

```text
database.sql
backup.zip
users.csv
config.json
.env
```

Severity:

High or Critical.

---

# 30. Object Enumeration

API:

```python
s3.list_objects_v2()
```

Example output:

```text
index.html
logo.png
backup.zip
database.sql
```

Objects are analyzed for sensitive names and extensions.

---

# Sensitive Extensions

Examples:

```text
.sql
.csv
.zip
.txt
.env
.pem
.json
```

Examples:

```text
database.sql
passwords.txt
private.pem
backup.zip
```

Finding these inside public buckets is extremely dangerous.

---

# 31. Risk Scoring Engine

Each finding contributes to a score.

---

Public ACL

+10

---

Public Bucket Policy

+10

---

Missing Encryption

+8

---

Disabled Versioning

+4

---

Website Hosting

+3

---

Sensitive Files

+12

---

Example

```text
Public ACL
+10

Missing Encryption
+8

Sensitive Files
+12

Total = 30
```

---

# Severity Classification

```text
0-4      Low

5-9      Medium

10-19    High

20+      Critical
```

---

# 32. Recommendation Engine

The scanner provides recommendations.

---

Finding:

Public ACL

Recommendation:

```text
Enable Block Public Access.
```

---

Finding:

Missing Encryption

Recommendation:

```text
Enable SSE-S3 or SSE-KMS.
```

---

Finding:

Versioning Disabled

Recommendation:

```text
Enable versioning.
```

---

Finding:

Sensitive Files

Recommendation:

```text
Remove or restrict access immediately.
```

---

# 33. Auto-Remediation

The scanner can automatically fix issues.

---

## Block Public Access

API:

```python
put_public_access_block()
```

---

## Enable Encryption

API:

```python
put_bucket_encryption()
```

---

## Enable Versioning

API:

```python
put_bucket_versioning()
```

---

# Why Automatic Fixes Can Be Dangerous

Changing bucket settings may:

* Break applications.
* Break websites.
* Affect other teams.
* Disrupt production.

Therefore automatic changes should be used carefully.

---

# 34. Dry Run Mode

Dry run performs no actual modifications.

Instead:

```text
[DRY RUN]

Would enable encryption.

Would block public access.

Would enable versioning.
```

Safe for production environments.

---

# 35. JSON Reports

JSON reports are machine-readable.

Example:

```json
{
 "bucket":"finance-backups",
 "severity":"Critical",
 "risk_score":30
}
```

Useful for:

* Automation.
* SIEM integration.
* APIs.

---

# 36. CSV Reports

CSV reports are human-readable.

Example:

```text
Bucket,Score,Severity

finance-backups,30,Critical
website-assets,12,High
logs-bucket,0,Low
```

Useful for:

* Excel.
* Auditing.
* Reporting.

---

# 37. HTML Dashboard

Displays:

| Bucket          | Score | Severity |
| --------------- | ----- | -------- |
| finance-backups | 30    | Critical |
| logs-bucket     | 0     | Low      |

Includes:

* Findings
* Recommendations
* Color-coded severity

Provides easy visualization.

---

# 38. CLI Output

Example:

```text
====================

Bucket:
finance-backups

Severity:
CRITICAL

Findings

✓ Public ACL

✓ Missing Encryption

✓ Sensitive Files

Recommendations

✓ Enable SSE-S3

✓ Enable Block Public Access

✓ Remove Sensitive Files

====================
```

---

# 39. Detection Pipeline

```text
AWS Account
      ↓
Enumerate Buckets
      ↓
ACL Inspection
      ↓
Bucket Policy Inspection
      ↓
Encryption Inspection
      ↓
Versioning Inspection
      ↓
Website Inspection
      ↓
Object Enumeration
      ↓
Sensitive File Detection
      ↓
Risk Scoring Engine
      ↓
Severity Classification
      ↓
Recommendations
      ↓
JSON Report
CSV Report
HTML Dashboard
CLI Output
```

---

# 40. MITRE ATT&CK Mapping

Technique:

```text
T1530

Data from Cloud Storage Object
```

Attack Chain:

```text
Attacker
↓
Discovers Public Bucket
↓
Downloads Objects
↓
Sensitive Data Exposure
↓
Exfiltration
```

---

# 41. Final Architecture

```text
AWS Account
      │
      ▼
Bucket Enumerator
      │
      ▼
ACL Analyzer
      │
      ▼
Bucket Policy Analyzer
      │
      ▼
Encryption Analyzer
      │
      ▼
Versioning Analyzer
      │
      ▼
Website Hosting Analyzer
      │
      ▼
Sensitive File Detector
      │
      ▼
Risk Scoring Engine
      │
      ▼
Recommendation Engine
      │
 ┌────┼─────┐
 ▼    ▼     ▼

JSON CSV HTML
Report Report Dashboard

       │
       ▼

Optional Auto-Remediation
(Dry Run Supported)
```

---

# 42. Learning Outcomes

After completing Lab 3, I should be able to explain:

* S3 architecture.
* IAM and bucket permissions.
* ACLs and bucket policies.
* Public access risks.
* Encryption and versioning.
* Website hosting risks.
* Sensitive file exposure.
* boto3 fundamentals.
* Bucket enumeration.
* Risk scoring.
* Report generation.
* Auto-remediation.
* MITRE ATT&CK T1530.

---

# Lab 3 Theory Status

S3 Fundamentals ✅

IAM ✅

ACLs ✅

Bucket Policies ✅

Public Access Block ✅

Encryption ✅

Versioning ✅

Website Hosting ✅

Sensitive Files ✅

boto3 APIs ✅

Bucket Enumeration ✅

Risk Scoring ✅

Recommendations ✅

Auto-Remediation ✅

Dry Run Mode ✅

JSON Reports ✅

CSV Reports ✅

HTML Dashboard ✅

CLI Output ✅

MITRE ATT&CK Mapping ✅

Final Architecture ✅

Lab 3 Theory Complete ✅
