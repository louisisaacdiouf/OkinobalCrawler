# -*- coding: utf-8 -*-

import argparse
import re
import requests
from bs4 import BeautifulSoup

def scan_links(html_content, base_url):
    soup = BeautifulSoup(html_content, "html.parser")
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href is not None:
            if not any(substring in href for substring in [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".css","javascript", "mailto:", "tel:", "/ads", "file", "upload", "photo", "image", "video"]) and (href.endswith(".html") or href.endswith(".html/") or (not any(char in href for char in ["?", "=", "#"]) and len([c for c in href if c == "/"]) <= 1 and not href.startswith("/") and not href.startswith("http"))):
                if href.startswith("/"):
                    href = base_url + href
                elif not href.startswith(base_url):
                    href = base_url + "/" + href
                links.append(href)
    return links

def scan_website(base_url):
    if base_url[-1] == "/":
        start_url = base_url
    else:
        start_url = base_url + "/"

    visited = []
    links = []
    queue = [start_url]
    while queue:
        url = queue.pop(0)
        visited.append(url)
        print(url)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                html_content = response.text
                new_links = scan_links(html_content, base_url)
                for link in new_links:
                    if link not in links and link not in visited:
                        links.append(link)
                        queue.append(link)
        except:
            pass
    return links

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Website Crawler")
    parser.add_argument("domain", type=str, help="Domain to crawl")
    args = parser.parse_args()

    domain = args.domain
    links = scan_website(domain)
    print("Links found:")
    for link in links:
        print(link)
