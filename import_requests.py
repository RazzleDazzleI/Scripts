import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import os
import time

# Replace with your credentials
EMAIL = "you@example.com"
API_TOKEN = "your_api_token"
BASE_URL = "https://sitesage.atlassian.net/wiki"
AUTH = HTTPBasicAuth(EMAIL, API_TOKEN)

# Create output directory
os.makedirs("confluence_pages", exist_ok=True)

def fetch_all_pages(start=0, limit=50):
    pages = []
    while True:
        url = f"{BASE_URL}/rest/api/content?limit={limit}&start={start}&expand=body.storage"
        response = requests.get(url, auth=AUTH)
        data = response.json()

        pages.extend(data.get("results", []))
        if data["_links"].get("next"):
            start += limit
            time.sleep(1)  # avoid hammering the server
        else:
            break
    return pages

def save_page(page):
    title = page["title"].replace("/", "_")  # Clean file name
    content_html = page["body"]["storage"]["value"]

    # Optional: convert HTML to plain text
    soup = BeautifulSoup(content_html, "html.parser")
    plain_text = soup.get_text()

    # Save as .txt
    with open(f"confluence_pages/{title}.txt", "w", encoding="utf-8") as f:
        f.write(plain_text)

    # Optional: save raw HTML too
    # with open(f"confluence_pages/{title}.html", "w", encoding="utf-8") as f:
    #     f.write(content_html)

def main():
    print("Fetching all Confluence pages...")
    pages = fetch_all_pages()
    print(f"Found {len(pages)} pages.")
    for page in pages:
        save_page(page)
    print("Download complete. Files saved to `confluence_pages/` folder.")

if __name__ == "__main__":
    main()
