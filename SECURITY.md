# 🔐 SECURITY.md

## 🧠 Secure Code Review Summary

This document summarizes the findings from a secure code review and automated tools assessment of this application.

---

## 🔍 Threat Modeling Notes

Link to Confluence page: [https://ca-il-confluence.il.cyber-ark.com/display/RndSec/Threat+Modeling+Template+-+Recommended+Template](https://ca-il-confluence.il.cyber-ark.com/display/RndSec/Threat+Modeling+Template+-+Recommended+Template)

---

## Security Findings

All Snyk findings (Open Source / SCA, Code / SAST, and Container) are published to this
repository's **Security tab → Code scanning alerts**:

https://github.com/cybr-champions-summary/g2-insecure-mongo-app-python/security/code-scanning

The scans run automatically on every push to `main`, so the alerts always reflect the current
state of the code — when you fix and merge an issue, its alert is resolved on the next run.

---

## ⚠️ Key Vulnerabilities Identified

### 1. [Vulnerability Name or Category]
- **Location**: [File/Class/Method]
- **Issue**: [Brief description of the issue]
- **Risk**: [Low / Medium / High / Critical]
- **Recommendation**: [What should be done to fix it]

### 2. [Vulnerability Name or Category]
- **Location**: [File/Class/Method]
- **Issue**: [Brief description of the issue]
- **Risk**: [Low / Medium / High / Critical]
- **Recommendation**: [What should be done to fix it]

...

Fill it as you feel for the most high priority vulnerabilities you find

---

## ✅ Suggested Secure Practices

- [ ] Input validation implemented
- [ ] Secrets are not hardcoded
- [ ] Database access follows least privilege principle
- [ ] Rate limiting or request throttling applied

---

> 📌 Please complete all sections based on your findings. This document is required even if you do not compile or run the application.

