'''
Created on 29 Mar 2017

@author: alessiogastaldo

CrawlManager class that expose the function crawl().
It can be initialised through a seed_url and queue_max_size that 
restrict the size of the queue to a certain limit
'''
import sys
import getopt
from BeautifulSoup import BeautifulSoup
import urllib2
import hashlib
import re
import logging
from urlparse import urlparse
import json

from filter_util import Filter
import content_util
from url_queue import URLQueue

logger = logging.getLogger(__name__)


class CrawlManager():

    def __init__(self, seed_url, crawler_queue_max_size):

        self.url_queue = URLQueue()  # queue to store URL to crawl
        self.content_checksum = []  # list to store seen content
        self.user_agent = "darthvader_crawler"  # being a polite crawler
        self.seed_url = seed_url
        self.domain = urlparse(seed_url).hostname
        self.filter = Filter(seed_url, self.user_agent)
        self.crawler_queue_max_size = crawler_queue_max_size

    def url_fetcher(self, page_url):
        response = None
        error_message = ""

        request = urllib2.Request(page_url)
        request.add_header('User-agent', self.user_agent)

        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            error_message = "HTTPError = {}".format(str(e.code))
            logger.error(error_message)
        except urllib2.URLError, e:
            error_message = "URLError = {}".format(str(e.reason))
            logger.error(error_message)
        except httplib.HTTPException, e:
            error_message = "HTTPException: {}".format(e)
            logger.error(error_message)
        except Exception as e:
            error_message = "Generic exception happened: {}".format(e)
            logger.error(error_message)

        return error_message, response

    # header + content seen validation + robots + generic HHTP get issue
    def url_validation(self, page_url):

        error_message, response = self.url_fetcher(page_url)

        if len(error_message) > 0:
            return False, error_message

        content_type = response.info()["Content-Type"]
        if self.filter.has_content_type(content_type):
            logger.info("Content type filter: OK")
        else:
            error_message = "Content type filter response KO, page can't be analyzed"
            logger.error(error_message)
            return False, error_message

        if self.filter.can_page_be_fetched(page_url):
            logger.info("URL is respecting the robots.txt")
        else:
            error_message = "URL is not respecting robots.txt"
            logger.error(error_message)
            return False, error_message

        page_content = response.read()
        hashed_content = hashlib.md5(page_content)
        hex_hashed_content = hashed_content.hexdigest()

        if len(self.content_checksum) == 0:
            logger.info("First iteration, safe to proceed..")
            return True, page_content
        elif hex_hashed_content in self.content_checksum:
            error_message = "Page already crawled.."
            logger.error(error_message)
            return False, error_message

        logger.info("All validation checks passed")
        response.close()
        return True, page_content

    def crawl(self):

        logger.info("Starting crawling")
        first_iteration = True
        page_content = None
        # once crawler_queue_max_size is reached,we won't add any new link
        max_queue_size = False
        response_object = {}

        logger.info("Validating seed url")
        result, page_content = self.url_validation(self.seed_url)

        if result:
            logger.info(
                "We can proceed with crawling Seed URL: {}".format(self.seed_url))
        else:
            logger.error("The Seed URL provided can't be used for crawling: {}".format(
                page_content))
            sys.exit()

        self.url_queue.enqueue(self.seed_url)

        while self.url_queue.size() > 0:
            current_url = self.url_queue.dequeue()
            validation_result = True

            if not first_iteration:
                validation_result, page_content = self.url_validation(
                    current_url)
            else:
                first_iteration = False

            if not validation_result:
                logger.info(
                    "Crawler can't process this URL {}, reason: {}".format(current_url, page_content))
                continue

            # extracting links and adding them to queue
            if not max_queue_size and self.url_queue.size() <= self.crawler_queue_max_size:
                new_links = content_util.extract_links(
                    page_content, current_url)
                for link in new_links:
                    if urlparse(link).hostname == self.domain and self.url_queue.is_in_queue(link) == False:
                        self.url_queue.enqueue(link)
            else:
                max_queue_size = True

            # processing static assets
            static_assets = content_util.get_static_assets(
                page_content, current_url)

            # building response object
            response_object[current_url] = static_assets

            # updating content_checksum
            hashed_content = hashlib.md5(page_content)
            hex_hashed_content = hashed_content.hexdigest()
            self.content_checksum.append(hex_hashed_content)

        return json.dumps(response_object)
