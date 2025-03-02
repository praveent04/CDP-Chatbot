import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

# Function to fetch and parse documentation
def fetch_documentation(url):
    try:
        # Add a user-agent header to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract relevant text content (e.g., headings, paragraphs)
        content = ""
        for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'pre']):
            content += element.get_text(separator="\n") + "\n\n"

        return content.strip()
    except Exception as e:
        print(f"Error fetching documentation from {url}: {e}")
        return ""  # Return an empty string if fetching fails

# Function to extract relevant subpage links
def extract_relevant_links(main_url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(main_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links (adjust the selector based on the website structure)
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Convert relative URLs to absolute URLs
            full_url = urljoin(main_url, href)

            # Filter out irrelevant links (e.g., login, signup, blog, press)
            if "/docs/" in full_url and not any(
                x in full_url for x in ["/login", "/signup", "/blog", "/press", "/events", "/jobs"]
            ):
                links.append(full_url)

        # Remove duplicate links
        links = list(set(links))
        return links
    except Exception as e:
        print(f"Error extracting subpage links from {main_url}: {e}")
        return []

# Function to save documentation to a text file
def save_documentation(content, filename):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Documentation saved to {filename}")
    except Exception as e:
        print(f"Error saving documentation to {filename}: {e}")

# Main function to fetch and save documentation for all CDPs
def fetch_and_save_documentation():
    # Define the main URLs for each CDP
    cdp_docs = {
        "Segment": "https://segment.com/docs/?ref=nav",
        "mParticle": "https://docs.mparticle.com/",
        "Lytics": "https://docs.lytics.com/",
        "Zeotap": "https://docs.zeotap.com/home/en-us/",
    }

    # Create a directory to store the documentation
    output_dir = "cdp_documentation"
    os.makedirs(output_dir, exist_ok=True)

    # Fetch and save documentation for each CDP
    for platform, main_url in cdp_docs.items():
        print(f"Fetching documentation for {platform}...")

        # Step 1: Extract relevant subpage links
        subpage_links = extract_relevant_links(main_url)
        print(f"Found {len(subpage_links)} relevant subpages for {platform}.")

        # Step 2: Fetch content from each subpage
        all_content = ""
        for link in subpage_links:
            print(f"Fetching content from {link}...")
            content = fetch_documentation(link)
            if content:
                all_content += f"=== Content from {link} ===\n\n{content}\n\n"

        # Step 3: Save the combined content to a file
        if all_content:
            filename = os.path.join(output_dir, f"{platform}_documentation.txt")
            save_documentation(all_content, filename)
        else:
            print(f"No content fetched for {platform}.")

if __name__ == '__main__':
    fetch_and_save_documentation()