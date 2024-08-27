import requests
from bs4 import BeautifulSoup
import urllib.parse

def fetch_page(url):
    """Fetch the content of a web page."""
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_links(html, base_url):
    """Extract all unique links from the HTML content."""
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']
        full_link = urllib.parse.urljoin(base_url, link)  
        links.add(full_link)
    return links

def crawl(url, max_depth=2):
    """Crawl a website up to a specified depth."""
    visited = set()
    to_visit = [url]
    
    for depth in range(max_depth):
        current_level = to_visit[:]
        to_visit = []
        print(f"Depth {depth}:")
        
        for url in current_level:
            if url in visited:
                continue

            visited.add(url)
            print(f"Fetching: {url}")

            html = fetch_page(url)
            if html:
                links = extract_links(html, url)
                for link in links:
                    if link not in visited and link not in to_visit:
                        to_visit.append(link)

if __name__ == "__main__":
    start_url = input("Enter the URL to start crawling: ")
    depth = int(input("Enter the depth of crawling: "))
    crawl(start_url, max_depth=depth)
