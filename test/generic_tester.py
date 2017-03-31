'''
Created on 29 Mar 2017

@author: alessiogastaldo
'''

import urllib2
import hashlib
from BeautifulSoup import BeautifulSoup
import re
import urlparse


response = urllib2.urlopen('https://gocardless.com')


data = response.read()

soup = BeautifulSoup(data)

for tag in soup.findAll('a', href=True):
    tag['href'] = urlparse.urljoin("https://gocardless.com", tag['href'])
    # print tag['href']


for tag in soup.findAll('img'):
    tag['src'] = urlparse.urljoin("https://gocardless.com", tag['src'])
   # print tag['src']


for tag in soup.findAll('script', {"src": True}):
    tag['src'] = urlparse.urljoin("https://gocardless.com", tag['src'])
    # print tag['src']

for tag in soup.findAll('link', rel="stylesheet"):
    tag['href'] = urlparse.urljoin("https://gocardless.com", tag['href'])
    print tag['href']
