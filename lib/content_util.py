'''
Created on 29 Mar 2017

@author: alessiogastaldo

Util module to extract links in a page and retrieve static assets
'''

from BeautifulSoup import BeautifulSoup
import re
import urlparse

HTML_TAG_REF = "href"


def extract_links(page_content, page_url):
    new_links = []

    soup = BeautifulSoup(page_content)
    # making sure HTML is not broken
    soup.prettify()
    for tag in soup.findAll("a", href=True):
        tag[HTML_TAG_REF] = urlparse.urljoin(page_url, tag[HTML_TAG_REF])
        new_links.append(tag[HTML_TAG_REF])

    return new_links


def get_static_assets(page_content, page_url):
    static_assets = []

    soup = BeautifulSoup(page_content)
    # making sure HTML is not broken
    soup.prettify()

    for tag in soup.findAll('img'):
        if tag.get("src"):
            tag["src"] = urlparse.urljoin("https://gocardless.com", tag['src'])
            static_assets.append(tag['src'])

    for tag in soup.findAll('script', {"src": True}):
        if tag.get("src"):
            tag['src'] = urlparse.urljoin("https://gocardless.com", tag['src'])
            static_assets.append(tag['src'])

    for tag in soup.findAll('link', rel="stylesheet"):
        if tag.get("href"):
            tag['href'] = urlparse.urljoin(
                "https://gocardless.com", tag['href'])
            static_assets.append(tag['href'])

    return static_assets
