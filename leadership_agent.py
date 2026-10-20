
# CAP 931 - Company Leadership Research Agent

from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup


def research_leadership(company_url):
    # Retrieve the company's homepage
    response = requests.get(company_url, timeout=10)
    response.raise_for_status()

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Keywords commonly used for leadership pages
    leadership_keywords = [
    "leadership",
    "management",
    "executives",
    "our team",
    "about us",
    "about",
    "company",
    "corporate",
    "board of directors",
    "senior leaders",
]
        # Exclude pages unrelated to leadership
    excluded_keywords = [
        "privacy",
        "diversity",
        "sustainability",
        "cybersecurity",
        "reports",
    ]

    leadership_links = []

    # Find links related to company leadership
    for link in soup.find_all("a", href=True):
        link_text = link.get_text(" ", strip=True).lower()
        link_url = link["href"].lower()
                # Skip unrelated pages
        if any(
            keyword in link_url
            for keyword in excluded_keywords
        ):
            continue

        if any(
            keyword in link_text or keyword.replace(" ", "-") in link_url
            for keyword in leadership_keywords
        ):
            full_url = urljoin(response.url, link["href"])

            # Keep only links on the same website
            if urlparse(full_url).netloc == urlparse(response.url).netloc:
                if full_url not in leadership_links:
                    leadership_links.append(full_url)

    
    # Discover leadership links from the About page
    for about_url in leadership_links[:3]:
        if "about" not in urlparse(about_url).path.lower():
            continue

        try:
            about_response = requests.get(about_url, timeout=10)
            about_response.raise_for_status()

            about_soup = BeautifulSoup(
                about_response.text, "html.parser"
            )

            for link in about_soup.find_all("a", href=True):
                link_text = link.get_text(" ", strip=True).lower()

                if "leadership" in link_text or "executives" in link_text:
                    full_url = urljoin(about_response.url, link["href"])

                    

                    # Allow links across Microsoft subdomains
                    parsed_url = urlparse(full_url)
                    hostname = (parsed_url.hostname or "").lower()

                    if (
                        parsed_url.scheme == "https"
                        and (
                            hostname == "microsoft.com"
                            or hostname.endswith(".microsoft.com")
                        )
                        and full_url not in leadership_links
                    ):
                        leadership_links.append(full_url)

        except requests.RequestException:
            continue

    # Retrieve text from discovered leadership pages
    leadership_content = []

    for page_url in leadership_links[:3]:
        try:
            page_response = requests.get(page_url, timeout=10)
            page_response.raise_for_status()

            content_type = page_response.headers.get(
                "Content-Type", ""
            ).lower()

            if "text/html" not in content_type:
                continue

            page_soup = BeautifulSoup(
                page_response.text, "html.parser"
            )

            for element in page_soup(["script", "style"]):
                element.decompose()

            page_text = page_soup.get_text(
                separator=" ", strip=True
            )

            leadership_content.append({
                "url": page_response.url,
                "content": page_text[:3000]
            })

        
        except requests.RequestException as error:
            leadership_content.append({
                "url": page_url,
                "status": "unavailable",
                "error": str(error),
                "content": ""
            })


    return {
        "company_url": response.url,
        "leadership_pages": leadership_links[:10],
        "leadership_content": leadership_content
    }

def extract_annual_report_leadership(report_url, reporting_year):
    # Download the annual report
    response = requests.get(report_url, timeout=10)
    response.raise_for_status()

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts and styles
    for element in soup(["script", "style"]):
        element.decompose()

    # Extract readable text
    page_text = soup.get_text(separator=" ", strip=True)

    # Locate the leadership section
    start_marker = (
        "DIRECTORS AND EXECUTIVE OFFICERS "
        "OF MICROSOFT CORPORATION"
    )

    end_marker = "Investor Relations Investor Relations"

    start = page_text.rfind(start_marker)
    end = page_text.find(end_marker, start)

    # Do not return unrelated content if markers are missing
    if start == -1 or end == -1 or end <= start:
        return {
            "source_url": response.url,
            "reporting_year": reporting_year,
            "status": "section_not_found",
            "leadership_text": ""
        }

    leadership_text = page_text[start:end].strip()

    return {
        "source_url": response.url,
        "reporting_year": reporting_year,
        "status": "success",
        "leadership_text": leadership_text
    }

