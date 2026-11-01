# CAP 931 - Company Research Agent

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlunparse
import ipaddress
import socket


def validate_company_url(url):
    parsed = urlparse(url)

    if parsed.scheme != "https":
       raise ValueError("Only HTTPS URLs are allowed.")

    hostname = parsed.hostname

    if not hostname:
        raise ValueError("A valid hostname is required.")

    if hostname.lower() == "localhost":
        raise ValueError("Localhost URLs are not allowed.")

    try:
        addresses = socket.getaddrinfo(
            hostname,
            None,
            type=socket.SOCK_STREAM
        )
    except socket.gaierror:
        raise ValueError("Unable to resolve the website hostname.")

    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])

        if not ip.is_global:
            raise ValueError(
                "Private, local, or reserved network addresses are not allowed."
            )

    return url


def discover_company_links(soup, base_url):
    keywords = ("about", "products", "services", "solutions")
    discovered_links = []

    base_domain = urlparse(base_url).hostname

    for link in soup.find_all("a", href=True):
        href = link["href"]

        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        # Only consider HTTPS links on the same hostname
        if parsed.scheme != "https":
            continue

        if parsed.hostname != base_domain:
            continue

        # Remove fragments such as #section
        clean_url = urlunparse(parsed._replace(fragment=""))

        # Look for relevant company pages
        if any(keyword in parsed.path.lower() for keyword in keywords):
            if clean_url not in discovered_links:
                discovered_links.append(clean_url)

    return discovered_links[:3]



def research_company(company_url):
    company_url = validate_company_url(company_url)

    # Request the webpage
        # Use a session that ignores environment proxy settings
    session = requests.Session()
    session.trust_env = False

    # Request the validated webpage
    response = session.get(
        company_url,
        timeout=10,
        allow_redirects=False
    )

    # Check whether the request succeeded
        # Detect redirects without following them
    if 300 <= response.status_code < 400:
        raise ValueError(
            "Website returned a redirect. "
            "Automatic redirects are disabled for security."
        )
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
