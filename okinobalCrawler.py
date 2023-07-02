# -*- coding: utf-8 -*-

import argparse
import re
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def is_internal_link(url, base_url):
    parsed_url = urlparse(url)
    parsed_base_url = urlparse(base_url)
    return parsed_url.netloc == parsed_base_url.netloc

def is_valid_link(url, base_url):
    file_extensions = (".jpg", ".jpeg", ".png", ".gif", ".pdf")
    invalid_keywords = (".css", "javascript", "mailto:", "tel:", "/ads", "file", "upload", "photo", "image", "video")
    parsed_url = urlparse(url)

    if parsed_url.scheme and parsed_url.netloc:
        return is_internal_link(url, base_url) and not url.endswith(file_extensions)
    else:
        return not any(keyword in url for keyword in invalid_keywords) and (url.endswith("/") or url.endswith(".html") or urljoin(base_url, url).endswith("/"))

def scan_links(html_content, base_url):
    soup = BeautifulSoup(html_content, "html.parser")
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href is not None and is_valid_link(href, base_url):
            absolute_url = urljoin(base_url, href)
            links.append(absolute_url)
    return links

def scan_website(base_url):
    visited = set()
    links = []
    queue = [base_url]

    while queue:
        url = queue.pop(0)
        visited.add(url)
        print(url)

        try:
            response = requests.get(url)
            if response.status_code == 200:
                html_content = response.text
                new_links = scan_links(html_content, url)
                for link in new_links:
                    if link not in links and link not in visited:
                        links.append(link)
                        queue.append(link)
        except:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Website Crawler")
    parser.add_argument("domain", type=str, help="Domain to crawl")
    args = parser.parse_args()

    domain = args.domain
    print("Links found:")
    scan_website(domain)
    print("\n-----------------------------------\nScan Terminé.")
