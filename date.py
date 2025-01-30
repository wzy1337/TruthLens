from bs4 import BeautifulSoup
import re
import requests

# Step 1: Fetch the website HTML
url = "https://www.channelnewsasia.com/singapore/general-election-workers-party-background-screening-candidates-4894171"  # Replace with the URL of the website
response = requests.get(url)
html_content = response.text

# Step 2: Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Step 3: Search for "datePublished" in the HTML text
pattern = r'"datePublished":\s*"(.*?)"'  # Regular expression to find "datePublished"
match = re.search(pattern, html_content)

if match:
    date_published = match.group(1)  # Extract the date from the match
    print(f"Date Published: {date_published}")
else:
    print("Date Published not found!")