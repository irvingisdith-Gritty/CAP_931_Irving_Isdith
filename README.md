# CAP 931 — AI Sales Assistant Agent Prototype

**Project:** AI-Powered B2B Sales Intelligence Assistant  
**Developer:** Irving Isdith  
**Course:** Per Scholas — CAP 931

## 1. Project Overview

The AI Sales Assistant is a Python and Streamlit application designed to support B2B sales research and strategy development.

The application gathers website research, analyzes available competitor information, and uses a Groq-hosted language model to generate structured sales intelligence reports.

## 2. Key Features

- Interactive Streamlit user interface
- Company website research
- Competitor website research
- Leadership research, including a Microsoft 2025 Annual Report example
- AI-generated sales opportunity analysis
- Nine-section Sales Intelligence Report
- Research verification and assumption labeling
- Downloadable Markdown reports
- Error handling for inaccessible company websites

## 3. Technologies Used

- Python
- Streamlit
- Groq API
- Groq-hosted `openai/gpt-oss-20b` model
- Requests
- BeautifulSoup
- Visual Studio Code

## 4. Project Files

| File | Description |
|---|---|
| `app.py` | Main Streamlit application |
| `research_agent.py` | Company website research |
| `competitor_agent.py` | Competitor website research |
| `leadership_agent.py` | Leadership research |
| `test_groq.py` | Groq API connection testing |
| `test_ai.py` | AI testing |
| `pyproject.toml` | Project configuration and dependencies |

## 5. How to Run the Application

1. Open the project folder in VS Code.
2. Create and activate a Python virtual environment if one is not already available.
3. Install the project dependencies.
4. Configure a valid `GROQ_API_KEY` environment variable.
5. Launch the application:

```powershell
python -m streamlit run app.py
```

6. Open the local Streamlit URL shown in the terminal.
7. Enter the sales opportunity information and generate a report.

## 6. Report Structure

The application generates reports containing:

1. Executive Summary
2. Company Research and Business Context
3. Customer Challenges and Pain Points
4. Product Value Proposition
5. Competitive Landscape
6. Leadership and Decision-Maker Insights
7. Recommended Sales Strategy
8. Risks, Assumptions, and Verification Needs
9. Recommended Next Steps

## 7. Testing and Validation

The prototype was manually tested for:

- Successful AI report generation
- Missing or inaccessible company website research
- Missing competitor information
- Research isolation between Microsoft and IBM
- Historical leadership source identification
- Labeling of unsupported product capabilities
- Markdown report downloading

The tested scenarios passed. Additional testing would be required before production deployment.

## 8. Limitations

- Website access depends on external website availability and permissions.
- Some websites may block automated research requests.
- Leadership research from annual reports may contain historical information.
- AI-generated recommendations require human verification.
- The application is a prototype, not a production-ready sales intelligence platform.

## 9. Conclusion

The CAP 931 AI Sales Assistant demonstrates how Python, website research, prompt engineering, and large language models can be combined to support B2B sales research and decision-making.