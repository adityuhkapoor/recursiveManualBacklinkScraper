import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
import random
import string

visited_urls = set()
YOUR_USER_AGENT_HERE = "idk" # look up What is My User Agent on google chrome and copy and paste it, swapping out idk
def generate_random_file_name(extension='txt'):
    """
    Generates a random filename with the specified extension.
    """
    random_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{random_name}.{extension}"

class LinkCrawler:
    def __init__(self):
        self.headers = {
            "User-Agent": (
                YOUR_USER_AGENT_HERE
            )
        }
        self.file_name = generate_random_file_name()

    def crawl_links(self, start_url):
        """
        Recursively crawls outbound links from a given start URL and writes them to a file.
        """
        if start_url in visited_urls:
            return

        visited_urls.add(start_url)
        links_to_visit = self.fetch_links(start_url)

        if links_to_visit:
            i = 0
            while i < len(links_to_visit):
                link = links_to_visit[i]
                if link not in visited_urls:
                    with open(self.file_name, "a") as file:
                        file.write(f"{link}\n")
                    self.crawl_links(link)
                    time.sleep(0.5)  # To avoid overloading the server
                i += 1

    def fetch_links(self, url):
        """
        Extracts outbound links from the given URL.
        """
        print(f"Scraping links from: {url}")

        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            all_links = soup.find_all('a')
            outbound_links = []
            index = 0

            while index < len(all_links):
                link_tag = all_links[index]
                href = link_tag.get('href')
                if href:
                    absolute_url = urljoin(url, href)
                    parsed_url = urlparse(absolute_url)
                    if parsed_url.scheme in ['http', 'https'] and absolute_url not in visited_urls:
                        outbound_links.append(absolute_url)
                index += 1

            print(f"Collected outbound links: {outbound_links}")
            return outbound_links

        except (requests.RequestException, requests.Timeout) as error:
            print(f"Error accessing {url}: {error}")
            with open('error_log.txt', 'a') as error_file:
                error_file.write(f"Error at {url}: {error}\n")
            return []
