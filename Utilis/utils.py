# utils.py
from urllib.parse import urlparse, urlunparse

def clean_linkedin_url(url):
    if not isinstance(url, str):
        raise ValueError("The URL must be a string.")
    
    parsed_url = urlparse(url)
    if '/company/' in parsed_url.path:
        path_parts = parsed_url.path.split('/')
        company_index = path_parts.index('company')
        base_path = '/'.join(path_parts[:company_index + 2])

        cleaned_url = urlunparse((parsed_url.scheme, parsed_url.netloc, base_path, '', '', ''))
    else:
        cleaned_url = url

    return cleaned_url
