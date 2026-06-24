# 🔐 SECURITY.md

## 🧠 Secure Code Review Summary

This document summarizes the findings from a secure code review and automated tools assessment of this application.

---

## 🔍 Threat Modeling Notes

Link to Confluence page:https://ca-il-confluence.il.cyber-ark.com/spaces/rndp/pages/694873861/G2+-+Python+App+threat+modeling+Final+Exercise(https://ca-il-confluence.il.cyber-ark.com/display/RndSec/Threat+Modeling+Template+-+Recommended+Template)

---

## Security Findings

All Snyk findings (Open Source / SCA, Code / SAST, and Container) are published to this
repository's **Security tab → Code scanning alerts**:

https://github.com/cybr-champions-summary/g2-insecure-mongo-app-python/security/code-scanning

The scans run automatically on every push to `main`, so the alerts always reflect the current
state of the code — when you fix and merge an issue, its alert is resolved on the next run.

---

## Key Vulnerabilities Identified

> These are findings from manual secure code review that were **not** detected by Snyk (SAST/SCA) or Gitleaks automated scans.

### 1. JWT Signature Verification Disabled
- **Location**: `handlers/auth_handler.py` — `validate_token()`
- **Issue**: JWT validation uses `verify_signature: False` — signatures are not verified, allowing token forgery.
- **Risk**: Critical
- **Recommendation**: Enable JWT signature verification by removing `verify_signature: False`. Enforce HS256 (or RS256) signature validation on all token checks.

### 2. Mongo Express Exposed with Root Credentials
- **Location**: `docker-compose.yml` — Mongo Express service
- **Issue**: Mongo Express is authenticated with the MongoDB root password, set as a plaintext environment variable, with no access logging.
- **Risk**: High
- **Recommendation**: Use a dedicated least-privilege DB account for Mongo Express. Move credentials to a secrets manager. Restrict Mongo Express to localhost or remove from production deployments. Enable access logging.

### 3. No TLS / HTTPS for External-Facing Services
- **Location**: All external-facing services (Flask app port 8000, Mongo Express port 8081)
- **Issue**: No MFA and no TLS in the default deployment. All traffic is unencrypted.
- **Risk**: High
- **Recommendation**: Enable TLS/HTTPS for all services. Implement MFA for administrative access. Use HSTS headers.

### 4. MongoDB Client Uses Root Credentials (No Least Privilege)
- **Location**: `config.py`, `docker-compose.yml` — MongoDB client initialization
- **Issue**: The Flask app connects to MongoDB with root credentials that have full database access.
- **Risk**: High
- **Recommendation**: Create dedicated MongoDB users with minimal required permissions (read-only for queries, read-write only on specific collections). Remove root credentials from application code.

### 5. No Authorization Middleware / Defense-in-Depth
- **Location**: `handlers/auth_handler.py`, `handlers/item_handler.py`, `config.py`
- **Issue**: Authorization is inline ad-hoc checks with no middleware, decorators, or framework enforcement. No layered protection if any single control fails.
- **Risk**: High
- **Recommendation**: Implement authorization middleware/decorators for consistent enforcement. Add layered controls so compromise of one layer does not grant full access.

### 6. Complete Absence of Audit Logging (Repudiation)
- **Location**: All Flask handlers (`POST /auth/token`, `POST /auth/register`, `GET /items`, `POST /items`)
- **Issue**: No authentication events are logged. Login attempts, admin actions, and data access/modification are unrecorded, making brute-force attacks undetectable and forensics impossible.
- **Risk**: High
- **Recommendation**: Implement structured audit logging: log authentication attempts (timestamp, username, source IP, success/failure), admin operations, and all data access/modification events with authenticated user identity.

### 7. Broken Object Level Authorization (IDOR)
- **Location**: `handlers/item_handler.py` — `handle_get_item()`, `handle_post_item()`
- **Issue**: The API validates the token but does not verify if the user owns the item they are requesting or modifying. Any authenticated user can access other users' items.
- **Risk**: High
- **Recommendation**: Implement ownership checks before fetching or mutating records. Scope queries to the authenticated user's resources.

### 8. No Rate Limiting
- **Location**: Flask app — all endpoints (`POST /auth/token`, `POST /items`)
- **Issue**: No rate limiting or account lockout mechanism exists. Attackers can flood authentication endpoints with credential stuffing or DoS attacks.
- **Risk**: Medium
- **Recommendation**: Implement rate limiting (e.g., 5 requests/minute per IP) for authentication endpoints. Add account lockout after repeated failed attempts.

### 9. Plaintext Database Connection
- **Location**: Flask app to MongoDB connection, `config.py`, `docker-compose.yml`
- **Issue**: Internal network traffic between the Flask app and MongoDB is unencrypted. Credentials and data can be intercepted.
- **Risk**: Medium
- **Recommendation**: Enforce TLS connection strings between Flask and MongoDB. Configure MongoDB to require TLS for all client connections.

### 10. No Tenant Isolation
- **Location**: MongoDB (users and items collections), Flask app (items service)
- **Issue**: Single-tenant design with no data isolation between users/tenants.
- **Risk**: Medium
- **Recommendation**: Implement tenant-scoped queries and row-level access controls. Add tenant identifiers to data models. Enforce tenant boundaries at the service layer.

### 11. No WAF or DDoS Protection
- **Location**: All external-facing services (Flask app port 8000, Mongo Express port 8081), `docker-compose.yml`
- **Issue**: No Web Application Firewall in front of the application. No network-level rate limiting, IP reputation filtering, or volumetric attack mitigation.
- **Risk**: High
- **Recommendation**: Deploy a WAF (e.g., AWS WAF, Cloudflare) with rate-limiting rules, IP reputation blocking, and DDoS protection. Add connection limits at the reverse proxy level.

---

## Suggested Secure Practices

- [ ] Input validation implemented
- [x] Secrets are not hardcoded (JWT_SECRET and MONGO_URI moved to env vars)
- [ ] Database access follows least privilege principle
- [ ] Rate limiting or request throttling applied
- [x] Password hashing uses PBKDF2-SHA256 with salts (migrated from SHA-1)
- [x] Debug mode disabled in production
- [x] RSA key size increased to 2048 bits
- [ ] JWT signature verification enabled
- [ ] TLS/HTTPS configured for all services
- [ ] Audit logging implemented
- [ ] Authorization middleware/decorators added

---
## ✅ False Alarm

Snyk:
 ✗ [LOW] Use of Hardcoded Passwords
   Finding ID: bc4512b3-6409-4502-b64d-83ed00a82bbf
   Path: tests/test_api.py, line 33
   Info: Do not hardcode passwords in code. Found hardcoded password used in a dictionary key.

 ✗ [LOW] Use of Hardcoded Passwords
   Finding ID: 186b5614-bac2-478f-89a3-015fa150c04e
   Path: tests/test_api.py, line 78
   Info: Do not hardcode passwords in code. Found hardcoded password used in a dictionary key.





> 📌 Please complete all sections based on your findings. This document is required even if you do not compile or run the application.

