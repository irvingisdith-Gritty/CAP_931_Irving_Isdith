# CAP 931 - Company Research Agent

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlunparse
from urllib3.util.connection import allowed_gai_family
from urllib3.connectionpool import HTTPSConnectionPool
from urllib3.connection import HTTPSConnection
from urllib3.connectionpool import HTTPSConnectionPool
from urllib3.exceptions import ConnectTimeoutError, NewConnectionError
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager
import ipaddress
import socket
def is_public_ip(ip_address):
    """Return True only for globally routable IP addresses."""
    try:
        return ipaddress.ip_address(ip_address).is_global
    except ValueError:
        return False
def create_public_connection(
    address,
    timeout=10,
    source_address=None,
    socket_options=None
):
    """Connect only to a validated public IP address."""

    host, port = address

    addresses = socket.getaddrinfo(
        host,
        port,
        allowed_gai_family(),
        socket.SOCK_STREAM
    )

    for family, socktype, proto, _, sockaddr in addresses:
        ip = sockaddr[0]

        if not is_public_ip(ip):
            raise ValueError(
                f"Connection blocked: {ip} is not a public IP."
            )

    last_error = None

    for family, socktype, proto, _, sockaddr in addresses:
        sock = socket.socket(family, socktype, proto)

        try:
            if socket_options:
                for option in socket_options:
                    sock.setsockopt(*option)

            sock.settimeout(timeout)

            if source_address:
                sock.bind(source_address)

            sock.connect(sockaddr)
            return sock

        except OSError as error:
            last_error = error
            sock.close()

    if last_error:
        raise last_error

    raise OSError("No valid public connection available.")
from urllib3.connection import HTTPSConnection
from urllib3.exceptions import ConnectTimeoutError, NewConnectionError


class SecureHTTPSConnection(HTTPSConnection):
    from urllib3.connectionpool import HTTPSConnectionPool


class SecureHTTPSConnectionPool(HTTPSConnectionPool):
    """HTTPS pool that uses our validated connection class."""

    ConnectionCls = SecureHTTPSConnection
    """HTTPS connection pool using our validated connection class."""
    from requests.adapters import HTTPAdapter
from urllib3 import PoolManager


class SecureHTTPSConnection(HTTPSConnection):
    """HTTPS connection that blocks non-public IP addresses."""

    def _new_conn(self):
        try:
            return create_public_connection(
                (self._dns_host, self.port),
                timeout=self.timeout,
                source_address=self.source_address,
                socket_options=self.socket_options,
            )
        except TimeoutError as error:
            raise ConnectTimeoutError(
                self,
                f"Connection to {self.host} timed out."
            ) from error
        except OSError as error:
            raise NewConnectionError(
                self,
                f"Secure connection failed: {error}"
            ) from error


class SecureHTTPSConnectionPool(HTTPSConnectionPool):
    """HTTPS pool using our secure connection class."""

    ConnectionCls = SecureHTTPSConnection


class SecureHTTPSAdapter(HTTPAdapter):
    """Requests adapter using our secure HTTPS connection pool."""

    def init_poolmanager(
        self,
        connections,
        maxsize,
        block=False,
        **pool_kwargs
    ):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            **pool_kwargs
        )

        self.poolmanager.pool_classes_by_scheme[
            "https"
        ] = SecureHTTPSConnectionPool

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
    """Research a company homepage and up to three related pages."""

    company_url = validate_company_url(company_url)

    session = requests.Session()
    session.trust_env = False
    session.mount("https://", SecureHTTPSAdapter())

    MAX_PAGE_BYTES = 2_000_000
    MAX_PAGES = 4

    def fetch_page(url):
        """Safely fetch and parse a company webpage."""

        url = validate_company_url(url)

        with session.get(
            url,
            timeout=10,
            allow_redirects=False,
            stream=True
        ) as response:

            if 300 <= response.status_code < 400:
                raise ValueError(
                    "Redirect blocked for security."
                )

            response.raise_for_status()

            content_type = response.headers.get(
                "Content-Type", ""
            ).lower()

            if "text/html" not in content_type:
                raise ValueError(
                    f"Unsupported content type: {content_type}"
                )

            content = bytearray()

            for chunk in response.iter_content(chunk_size=8192):
                content.extend(chunk)

                if len(content) > MAX_PAGE_BYTES:
                    raise ValueError(
                        "Page exceeds maximum allowed size."
                    )

            encoding = response.encoding or "utf-8"

            soup = BeautifulSoup(
                content.decode(encoding, errors="replace"),
                "html.parser"
            )

            for element in soup(["script", "style"]):
                element.decompose()

            text = soup.get_text(
                separator=" ",
                strip=True
            )

            return soup, text[:3000]

    try:
        # Fetch homepage
        homepage_soup, homepage_text = fetch_page(company_url)

        results = [
            f"Source URL: {company_url}\n"
            f"Website Content:\n{homepage_text}"
        ]

        # Discover relevant pages
        discovered_links = discover_company_links(
            homepage_soup,
            company_url
        )

        # Fetch up to three additional pages
        for link in discovered_links[:MAX_PAGES - 1]:
            try:
                _, page_text = fetch_page(link)

                results.append(
                    f"Source URL: {link}\n"
                    f"Website Content:\n{page_text}"
                )

            except (requests.RequestException, ValueError) as error:
                results.append(
                    f"Source URL: {link}\n"
                    f"Page unavailable: {error}"
                )

        return "\n\n---\n\n".join(results)

    finally:
        session.close()

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
