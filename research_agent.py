# CAP 931 - Company Research Agent

import requests
from bs4 import BeautifulSoup


def research_company(company_url):

    # Request the webpage
    response = requests.get(
        company_url,
        timeout=10
    )

    # Check whether the request succeeded
    response.raise_for_status()
        # Verify that the website returns HTML
    content_type = response.headers.get("Content-Type", "").lower()

    if "text/html" not in content_type:
        raise ValueError(
            f"Unsupported content type: {content_type}"
        )

    # Parse the HTML
    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Remove scripts and styles
    for element in soup(["script", "style"]):
        element.decompose()

    # Extract readable text
    company_text = soup.get_text(
        separator=" ",
        strip=True
    )
    return (
        f"Source URL: {response.url}\n\n"
        f"Website Content:\n{company_text[:3000]}"
)

    
