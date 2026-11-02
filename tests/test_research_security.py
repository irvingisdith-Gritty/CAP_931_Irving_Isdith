# CAP 931 - Automated Research Security Tests

import socket
from unittest.mock import patch

import pytest

from research_agent_multipage import validate_company_url


# ==========================================================
# TEST 1 - Reject HTTP URLs
# ==========================================================

def test_reject_http_url():
    with pytest.raises(ValueError, match="Only HTTPS"):
        validate_company_url("http://example.com")


# ==========================================================
# TEST 2 - Reject Localhost
# ==========================================================

def test_reject_localhost():
    with pytest.raises(ValueError, match="Localhost"):
        validate_company_url("https://localhost")


# ==========================================================
# TEST 3 - Reject Missing Hostname
# ==========================================================

def test_reject_missing_hostname():
    with pytest.raises(ValueError, match="valid hostname"):
        validate_company_url("https://")


# ==========================================================
# TEST 4 - Reject Private IP Addresses
# ==========================================================

@patch("research_agent_multipage.socket.getaddrinfo")
def test_reject_private_ip(mock_dns):

    mock_dns.return_value = [
        (
            socket.AF_INET,
            socket.SOCK_STREAM,
            6,
            "",
            ("192.168.1.10", 443),
        )
    ]

    with pytest.raises(ValueError, match="Private"):
        validate_company_url("https://internal.example.com")


# ==========================================================
# TEST 5 - Reject Loopback IP Addresses
# ==========================================================

@patch("research_agent_multipage.socket.getaddrinfo")
def test_reject_loopback_ip(mock_dns):

    mock_dns.return_value = [
        (
            socket.AF_INET,
            socket.SOCK_STREAM,
            6,
            "",
            ("127.0.0.1", 443),
        )
    ]

    with pytest.raises(ValueError, match="Private"):
        validate_company_url("https://loopback.example.com")


# ==========================================================
# TEST 6 - Accept Public HTTPS URLs
# ==========================================================

@patch("research_agent_multipage.socket.getaddrinfo")
def test_accept_public_https(mock_dns):

    mock_dns.return_value = [
        (
            socket.AF_INET,
            socket.SOCK_STREAM,
            6,
            "",
            ("8.8.8.8", 443),
        )
    ]

    result = validate_company_url("https://example.com")

    assert result == "https://example.com"


# ==========================================================
# TEST 7 - Reject DNS Resolution Failures
# ==========================================================

@patch("research_agent_multipage.socket.getaddrinfo")
def test_reject_dns_failure(mock_dns):

    mock_dns.side_effect = socket.gaierror()

    with pytest.raises(ValueError, match="Unable to resolve"):
        validate_company_url("https://invalid.example")