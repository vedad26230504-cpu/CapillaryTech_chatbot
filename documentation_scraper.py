import requests
from bs4 import BeautifulSoup
import time
import json
import os
from urllib.parse import urljoin

class DocumentationScraper:
    def __init__(self, base_url, output_folder="scraped_data"):
        self.base_url = base_url
        self.visited_urls = set()
        self.output_folder = output_folder

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        self.ignore_patterns = ['signin', 'login', 'logout', 'pdf', '.jpg', '.png', '.gif']

    def is_valid_url(self, url):
        if not url.startswith(self.base_url):
            return False
        return not any(pattern in url for pattern in self.ignore_patterns)

    def extract_text_with_structure(self, soup):
        content = {}
        content['title'] = soup.title.text if soup.title else "No Title"

        main = soup.find('main') or soup.find('div', class_='content') or soup
        headings = main.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        sections = []

        for heading in headings:
            section = {'heading': heading.text.strip(), 'level': int(heading.name[1]), 'content': []}
            current = heading.next_sibling
            while current and not (hasattr(current, 'name') and current.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                if hasattr(current, 'text') and current.text.strip():
                    if current.name in ['pre', 'code']:
                        section['content'].append({'type': 'code', 'text': current.text.strip()})
                    elif current.name in ['p', 'li', 'td', 'div']:
                        section['content'].append({'type': 'text', 'text': current.text.strip()})
                current = current.next_sibling
            sections.append(section)

        content['sections'] = sections
        content['standalone_text'] = [p.text.strip() for p in main.find_all(['p', 'li']) if p.text.strip()]
        return content

    def scrape_page(self, url):
        if url in self.visited_urls or not self.is_valid_url(url):
            return None, []
        self.visited_urls.add(url)

        try:
            res = requests.get(url, timeout=10)
            if res.status_code != 200:
                return None, []
            soup = BeautifulSoup(res.text, 'lxml')
            content = self.extract_text_with_structure(soup)
            content['url'] = url

            links = []
            for a in soup.find_all('a', href=True):
                full_url = urljoin(url, a['href'])
                if self.is_valid_url(full_url) and full_url not in self.visited_urls:
                    links.append(full_url)

            return content, links
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None, []

    def crawl(self, start_url=None, max_pages=50):
        if start_url is None:
            start_url = self.base_url
        queue = [start_url]
        doc_id = 0
        count = 0

        while queue and count < max_pages:
            url = queue.pop(0)
            content, links = self.scrape_page(url)
            if content:
                with open(f"{self.output_folder}/doc_{doc_id}.json", "w", encoding="utf-8") as f:
                    json.dump(content, f, indent=2, ensure_ascii=False)
                doc_id += 1
                count += 1
            queue.extend(links)
            time.sleep(1)
        print(f"Scraped {count} pages.").  what do i name this cell ?
