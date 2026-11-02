# CAP 931 — Final Improvement Report
## Build a Sales Agent Prototype Using Multi-Agent GPT Models

**Project:** CAP 931 — Sales Intelligence Agent  
**Report Date:** November 2, 2026  
**Purpose:** Document improvements made in response to instructor feedback.

---

## 1. Executive Summary

The CAP 931 project is a Python-based sales intelligence prototype developed using Streamlit, Groq-hosted large language models, and specialized research components.

The application helps sales representatives analyze prospective accounts, identify potential customer challenges, examine competitive positioning, and develop sales strategies.

Following the initial instructor evaluation, the project was enhanced to improve document processing, security, automated testing, model evaluation, and production deployment planning.

The improvements focus on strengthening the technical implementation and providing measurable evidence of system performance.

## 2. Document Processing Improvements

The application supports uploading and extracting text from three document formats:

- PDF
- DOCX
- TXT

Document processing is implemented in `document_processor.py`.

The implementation includes a 5 MB upload-size limit, unsupported-format rejection, empty-document detection, and a 15,000-character extraction limit.

DOCX extraction includes paragraphs and table contents.

These improvements support the use of product documentation as additional context for sales intelligence analysis.

## 3. Research and Security Enhancements

The project includes an enhanced research module, `research_agent_multipage.py`.

Security improvements include:

- HTTPS-only URL validation.
- Rejection of localhost and private IP addresses.
- DNS-based checks for publicly routable addresses.
- Restrictions on redirects.
- TLS-enabled network requests.
- Response-size controls.
- Same-host multipage research.

These measures reduce exposure to unsafe external requests.

However, the prototype has not undergone a comprehensive production security audit.

## 4. Automated Testing

Automated tests were implemented using pytest.

Two test modules were created:

**`tests/test_research_security.py`**

Seven tests cover URL validation, including HTTP rejection, localhost rejection, private and loopback IP restrictions, valid public HTTPS addresses, and DNS resolution failures.

**`tests/test_document_processor.py`**

Nine tests cover TXT, DOCX, and PDF extraction, unsupported file formats, empty documents, oversized uploads, text truncation, missing uploads, and DOCX table extraction.

**Test execution command:**

`uv run python -m pytest tests/ -v`

**Recorded result: 16 tests passed.**

These tests provide repeatable evidence that the covered security-validation and document-processing functions behave as expected.

They do not constitute complete end-to-end testing of the entire application.

## 5. LLM Model Comparison

Two Groq-hosted language models were evaluated:

- `openai/gpt-oss-20b`
- `openai/gpt-oss-120b`

Both models received the same sales intelligence prompt and system instructions.

The benchmark used temperature 0 and a maximum completion-token setting of 3,000.

### Performance Results

| Metric | GPT-OSS-20B | GPT-OSS-120B |
|---|---:|---:|
| Response time | 1.604 seconds | 3.084 seconds |
| Input tokens | 233 | 233 |
| Output tokens | 958 | 1,320 |
| Request status | Successful | Successful |

In this benchmark, GPT-OSS-20B completed its request faster and generated fewer output tokens.

These results represent one recorded execution per model and should not be interpreted as statistically representative performance measurements.

## 6. Model Output Quality Evaluation

Both generated reports were reviewed against five criteria, each worth 20 points.

| Criterion | GPT-OSS-20B | GPT-OSS-120B |
|---|---:|---:|
| Report completeness | 20 | 20 |
| Factual accuracy and grounding | 12 | 14 |
| Evidence classification | 12 | 16 |
| Sales relevance | 16 | 17 |
| Clarity and organization | 18 | 19 |
| **Total** | **78/100** | **86/100** |

These scores are a qualitative evaluation conducted for this project, not official instructor grades.

### Key Findings

GPT-OSS-20B produced a complete, organized report with lower latency.

However, it incorrectly labeled a user-provided product claim as verified and described possible product capabilities without sufficient supporting evidence.

GPT-OSS-120B provided stronger distinctions between product claims, potential benefits, and verification requirements.

Nevertheless, it suggested obtaining official product positioning from Microsoft, even though the prompt did not establish Microsoft as the product manufacturer.

Both models therefore demonstrated the need for human review and independent verification of AI-generated sales intelligence.

### Model Selection

GPT-OSS-20B remains a reasonable default for the prototype because it demonstrated lower latency in the recorded test.

GPT-OSS-120B is a potential alternative for tasks where the higher qualitative score observed in this evaluation justifies additional response time.

Further benchmarking is required before making production-level model selection decisions.

## 7. Production Deployment Planning

A separate document, `PRODUCTION_DEPLOYMENT_PLAN.md`, describes recommended production architecture and operational controls.

The plan addresses:

- Authentication and role-based access control.
- Secure API key and secrets management.
- Input validation and upload security.
- Scalable application hosting.
- Background processing and caching.
- Persistent storage.
- Logging, monitoring, and alerting.
- CI/CD and rollback procedures.
- Reliability, cost management, and operational testing.

These items are documented as production recommendations unless separately verified as implemented.

## 8. Remaining Limitations

Despite the improvements, several limitations remain:

1. Automated tests do not yet cover every application component or end-to-end workflow.
2. The research process does not provide comprehensive autonomous discovery across all relevant external sources.
3. Model quality scoring is based on a limited evaluation sample.
4. API pricing and cost per report have not yet been verified and calculated.
5. Production authentication, persistent storage, monitoring, and deployment infrastructure require additional implementation.
6. AI-generated claims must still be reviewed for factual accuracy and source reliability.

## 9. Conclusion

The CAP 931 improvements strengthen the prototype in areas identified by the initial instructor feedback.

The project now includes documented document-processing capabilities, security validation, automated test evidence, a two-model performance comparison, a qualitative output assessment, and a production deployment plan.

The evaluation also demonstrates an important practical limitation of large language models: well-written sales reports can contain unsupported assumptions or misclassify information as verified.

Future development should focus on broader test coverage, source verification, repeated model benchmarks, cost analysis, and implementation of production infrastructure.

The project provides a stronger foundation for continued development of a reliable AI-assisted sales intelligence application.

---

## Supporting Project Files

- `app.py`
- `document_processor.py`
- `research_agent_multipage.py`
- `competitor_agent.py`
- `leadership_agent.py`
- `tests/test_research_security.py`
- `tests/test_document_processor.py`
- `model_comparison.py`
- `model_comparison_results.csv`
- `model_comparison_review.txt`
- `model_quality_scores.csv`
- `PRODUCTION_DEPLOYMENT_PLAN.md`
- `README.md`