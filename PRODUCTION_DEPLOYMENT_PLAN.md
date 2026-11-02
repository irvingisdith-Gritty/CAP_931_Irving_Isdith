# CAP 931 — AI Sales Assistant Agent
## Production Deployment and Operational Readiness Plan

**Project:** CAP 931 — Sales Agent Prototype Using Multi-Agent GPT Models  
**Purpose:** Define the infrastructure, security controls, scalability requirements, monitoring strategy, and maintenance procedures needed to deploy the existing prototype in a production environment.

### 1. Executive Overview

The CAP 931 AI Sales Assistant is a Python-based Streamlit application that helps sales representatives research prospective companies, analyze competitors, identify leadership information, and generate structured sales intelligence reports using a Groq-hosted large language model.

The current prototype demonstrates a functional research and reporting workflow. However, additional infrastructure, security controls, testing, and operational procedures would be required before production deployment.

This document distinguishes between implemented prototype capabilities and proposed production enhancements.

### 2. Proposed Deployment Architecture

The production application would use the following architecture:

**User → HTTPS Load Balancer → Streamlit Application → Research Services → Groq API → Sales Intelligence Report**

Supporting infrastructure would include:

- Containerized application hosting.
- HTTPS termination and TLS certificate management.
- A managed database for customer profiles and saved reports.
- Object storage for uploaded documents.
- Background workers for research and report generation.
- Centralized logging and monitoring.
- A secrets manager for API credentials.

**Current status:** The prototype runs locally using Python, Streamlit, and Groq. The proposed cloud infrastructure has not been deployed.

### 3. Security and Access Control

#### Authentication and Authorization

Production users would authenticate through a trusted identity provider using OpenID Connect or another suitable authentication standard.

Role-based access control would restrict access to customer records, uploaded documents, and generated reports.

#### API Key Management

The Groq API key would be stored in a managed secrets service rather than application source code.

Secrets would be rotated periodically, access would follow least-privilege principles, and credentials would never be written to application logs.

#### Website Retrieval Security

The existing research implementation includes protections such as HTTPS-only retrieval, public-IP validation, redirect restrictions, TLS certificate verification, and response-size limits.

Additional production controls would include:

- Network-level restrictions preventing access to internal services.
- DNS and IP validation throughout outbound requests.
- URL normalization and strict input validation.
- Request timeouts and download limits.
- Controlled outbound network access.
- Security testing for SSRF and redirect bypasses.

These measures would reduce risks associated with researching user-supplied websites.

The existing protections have been tested in selected scenarios but have not undergone a complete security audit.

#### Uploaded Document Security

Uploaded PDF, DOCX, and TXT files would be subject to:

- File-type and content validation.
- Strict upload-size limits.
- Malware scanning.
- Secure temporary storage.
- Restricted file access.
- Automatic retention and deletion policies.

Uploaded documents and retrieved website content would be treated as untrusted data rather than executable instructions.

### 4. Scalability and Performance

The production application would support multiple simultaneous users through horizontally scalable application instances.

Long-running research operations would be processed using background workers and a managed task queue.

Additional performance improvements would include:

- Caching frequently requested public company information.
- Rate limiting per user and organization.
- Timeouts for external API requests.
- Retry policies with exponential backoff.
- Request concurrency limits.
- Resource monitoring and autoscaling.

Performance testing would establish acceptable response times and determine infrastructure requirements before launch.

### 5. Persistent Storage and Data Management

A managed relational database, such as PostgreSQL, could store:

- Customer account profiles.
- Research history.
- Generated report metadata.
- User preferences.
- Research timestamps.
- Source references.

Encrypted object storage would hold uploaded documents and generated report files.

Data retention policies would define when customer information, research records, and uploaded files must be deleted.

Database backups would be encrypted and tested through scheduled restoration exercises.

### 6. Monitoring and Observability

Production monitoring would track:

| Metric | Purpose |
|---|---|
| Application uptime | Measure availability |
| Research request failures | Identify inaccessible websites |
| Groq API latency | Monitor model response time |
| Token consumption | Estimate API usage |
| Report generation time | Identify performance bottlenecks |
| Authentication failures | Detect suspicious access |
| Upload processing errors | Monitor document handling |
| Infrastructure utilization | Support capacity planning |

Centralized logs would capture operational events without storing API keys, unnecessary personal information, or sensitive customer documents.

Alerts would notify administrators when error rates, latency, or infrastructure usage exceed defined thresholds.

### 7. Reliability and Error Handling

The production application would implement:

- Clear error messages for users.
- Graceful handling of unavailable websites.
- Request retries for temporary failures.
- Circuit breakers for repeatedly failing external services.
- Recovery procedures for interrupted research jobs.
- Health checks for application instances.
- Database backup and restoration procedures.

Failed research operations would be recorded with sufficient diagnostic information to support troubleshooting.

### 8. CI/CD and Maintenance

A continuous integration and deployment pipeline would automate:

1. Python syntax and dependency checks.
2. Unit testing.
3. Integration testing.
4. Security and dependency scanning.
5. Container image creation.
6. Deployment to a staging environment.
7. Controlled production releases.

Changes would be reviewed before deployment.

Versioned releases and rollback procedures would allow administrators to restore a previously working application if an update causes failures.

Dependencies would be reviewed and updated regularly.

### 9. Cost Management

Production cost controls would include:

- Per-user API usage quotas.
- Organization-level spending limits.
- Token usage monitoring.
- Research request limits.
- Caching to reduce duplicate requests.
- Storage retention policies.
- Budget alerts.
- Periodic infrastructure cost reviews.

Model selection would consider response quality, latency, and operational cost.

A controlled comparison of available models would be conducted before production deployment.

### 10. Production Testing Strategy

Before release, the application would undergo:

**Functional testing:** Confirm that all required inputs and reporting features work correctly.

**Security testing:** Evaluate authentication, authorization, file uploads, SSRF protections, and credential handling.

**Load testing:** Measure performance under simultaneous user requests.

**Integration testing:** Verify research modules, document processing, and Groq API interactions.

**Output evaluation:** Assess report completeness, factual grounding, evidence classification, and unsupported claims.

**Recovery testing:** Validate backup restoration, service restart procedures, and rollback capabilities.

### 11. Deployment Roadmap

| Phase | Activities | Completion Criteria |
|---|---|---|
| Phase 1 — Security | Authentication, secrets management, input validation | Security review passed |
| Phase 2 — Infrastructure | Containerization, HTTPS hosting, database, storage | Staging environment operational |
| Phase 3 — Scalability | Background jobs, caching, quotas | Load tests meet defined targets |
| Phase 4 — Monitoring | Logs, metrics, alerts | Operational dashboards functional |
| Phase 5 — Testing | Automated tests, security scans, output evaluation | Release acceptance criteria satisfied |
| Phase 6 — Production | Controlled deployment, monitoring, rollback readiness | Production release approved |

### 12. Current Prototype Limitations

The existing CAP 931 prototype does not currently include:

- Production authentication and authorization.
- Managed cloud hosting.
- Persistent customer account storage.
- Background job processing.
- Centralized monitoring and alerting.
- Automated production deployment.
- A completed security audit.
- A comprehensive automated test suite.

These capabilities are proposed enhancements rather than existing features.

### 13. Conclusion

The CAP 931 AI Sales Assistant demonstrates a functional foundation for AI-assisted B2B sales research.

Its modular architecture, website research capabilities, document processing, and structured AI reporting provide a starting point for future development.

A production deployment would require additional security, scalability, reliability, monitoring, and maintenance controls.

Implementing the proposed roadmap would improve operational readiness while preserving the core research and sales intelligence capabilities demonstrated by the prototype.