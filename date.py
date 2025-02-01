import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
from concurrent.futures import ThreadPoolExecutor

# Function to fetch the publication date from a URL
def fetch_publication_date(url):
    try:
        # Fetch the website HTML
        response = requests.get(url)
        html_content = response.text

        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Search for "datePublished" in the HTML text
        pattern = r'"datePublished":\s*"(.*?)"'  # Regular expression to find "datePublished"
        match = re.search(pattern, html_content)

        if match:
            date_published = match.group(1)  # Extract the date from the match
            return date_published
        else:
            return "Date Published not found"
    except Exception as e:
        return f"Error: {e}"

# Function to process a batch of URLs
def process_urls(urls):
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_publication_date, url): url for url in urls}
        for future in futures:
            url = futures[future]
            try:
                result = future.result()
                results.append((url, result))
            except Exception as e:
                results.append((url, f"Error: {e}"))
    return results

# Read the CSV file containing URLs
csv_file_path = "Dataset/news_excerpts_parsed.csv"  # Replace with the correct path to your CSV file
df_urls = pd.read_csv(csv_file_path)

# Split the URLs into batches for parallel processing
batch_size = 100  # Adjust the batch size as needed
url_batches = [df_urls['Link'][i:i + batch_size] for i in range(0, len(df_urls), batch_size)]

# Process each batch and collect the results
all_results = []
for batch in url_batches:
    batch_results = process_urls(batch)
    all_results.extend(batch_results)

# Create a DataFrame from the results
df_results = pd.DataFrame(all_results, columns=['Link', 'Date Published'])

# Save the results to a new CSV file
output_csv_file_path = "Dataset/news_excerpts_with_dates.csv"  # Replace with the correct path to save the output CSV file
df_results.to_csv(output_csv_file_path, index=False)

print("Publication dates have been extracted and saved to the output CSV file.")