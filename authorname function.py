import re
import requests
from bs4 import BeautifulSoup

def extract_author_from_url(url):
    try:
        # Fetch the content of the URL
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception for bad HTTP status codes
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find the author in common meta tags
        author = None
        
        # Check if the author's name is in the <meta> tags (common for structured data)
        meta_author = soup.find('meta', attrs={'name': 'author'})
        if meta_author:
            author = meta_author.get('content')
        
        # Check common HTML tags or classes where the author's name might appear
        if not author:
            author_tag = soup.find(['span', 'div', 'a'], class_=re.compile(r'.*author.*', re.I))  # Looking for common author-related class names
            if author_tag:
                author = author_tag.get_text(strip=True)
        
        # If still no author found, fall back to searching for common patterns in the text content
        if not author:
            text_content = soup.get_text()
            patterns = [
                r"By\s+([A-Za-z\s]+)",  # Matches "By Author Name"
                r"Written\s+by\s+([A-Za-z\s]+)",  # Matches "Written by Author Name"
                r"Author\s*[:\-]?\s*([A-Za-z\s]+)",  # Matches "Author: Author Name"
            ]
            for pattern in patterns:
                match = re.search(pattern, text_content)
                if match:
                    author = match.group(1).strip()
                    break
        
        # Return author if found, otherwise None
        return author if author else None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

# Example usage
url = 'https://edition.cnn.com/2022/08/02/europe/brittney-griner-trial-russia-tuesday/index.html'  # Replace with a real URL
author_name = extract_author_from_url(url)
print(f"Author: {author_name}")
