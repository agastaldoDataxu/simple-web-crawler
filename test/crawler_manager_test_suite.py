'''
Created on 31 Mar 2017

@author: alessiogastaldo
'''
import unittest
import hashlib
import responses
import requests
import mock
import urllib2
import json

from crawler_manager import CrawlManager
from mock import self


class CrawlerManagerTest(unittest.TestCase):

    def setUp(self):
        self.crawler = CrawlManager("https://gocardless.com", 5)
        result, response = self.crawler.url_fetcher(
            "https://gocardless.com")
        self.invalid_page_content = response.read()

        result, response = self.crawler.url_fetcher(
            "https://gocardless.com/new-to-direct-debit/")
        self.valid_page_content = response.read()

    def tearDown(self):
        self.crawler = None

    def testInstanceCreation(self):
        self.assertIsInstance(
            self.crawler, CrawlManager, "Error while creating crawler instance")
        pass

    def testUrlValidationForExistingContent(self):
        print "Test urlValidation for already crawled page"

        hashed_content = hashlib.md5(self.invalid_page_content)
        hex_hashed_content = hashed_content.hexdigest()
        self.crawler.content_checksum = hex_hashed_content

        result, error_message = self.crawler.url_validation(
            "https://gocardless.com")

        self.assertFalse(result)
        self.assertEqual(error_message, "Page already crawled..")

    def testUrlValdiationForContentType(self):
        print "Test urlValidation for invalid content type"

        result, error_message = self.crawler.url_validation(
            "https://static.ads-twitter.com/oct.js")

        self.assertFalse(result)
        self.assertEqual(
            error_message, "Content type filter response KO, page can't be analyzed")

    def testUrlValidationForPolitness(self):
        print "Test urlValidation for URL in robots.txt"

        result, error_message = self.crawler.url_validation(
            "https://gocardless.com/users/sign_in")

        self.assertFalse(result)
        self.assertEqual(
            error_message, "URL is not respecting robots.txt")

    def testUrlValidationForValidUrl(self):
        print "Test urlValidation for valid URL"

        result, page_content = self.crawler.url_validation(
            "https://gocardless.com/new-to-direct-debit/")

        self.assertTrue(result)
        self.assertEqual(
            self.valid_page_content, page_content)

    def testCrawlCompleteCycle(self):
        print "Test crawl for complete crawl cycle"

        crawl_results = self.crawler.crawl()
        is_json = True
        try:
            json_object = json.loads(crawl_results)
        except ValueError, e:
            is_json = False

        self.assertTrue(is_json)

if __name__ == "__main__":
    unittest.main()
