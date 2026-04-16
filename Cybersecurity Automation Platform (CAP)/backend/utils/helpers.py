import re
import socket
from urllib.parse import urlparse

def is_valid_url(url):
    """
    Validates if the provided string is a properly formatted URL.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_valid_ip(ip):
    """
    Validates if the provided string is a valid IPv4 address.
    """
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True
    except socket.error:
        return False

def format_api_response(status="success", message="", data=None, error=None):
    """
    Uniform response formatter for the API.
    """
    response = {
        "status": status,
        "message": message
    }
    if data is not None:
        response["data"] = data
    if error is not None:
        response["error"] = error
        
    return response

def sanitize_input(input_string):
    """
    Basic input sanitization to prevent simple XSS.
    Removes common dangerous tags.
    """
    if not isinstance(input_string, str):
        return input_string
        
    # Remove script tags and their contents
    sanitized = re.sub(r'<script.*?>.*?</script>', '', input_string, flags=re.IGNORECASE)
    # Remove inline event handlers (e.g. onerror=...)
    sanitized = re.sub(r'\bon\w+\s*=', '', sanitized, flags=re.IGNORECASE)
    
    return sanitized
