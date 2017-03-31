'''
Created on 29 Mar 2017

@author: alessiogastaldo
'''
from reppy.robots import Robots


class Filter():

    def __init__(self, seed_url, user_agent):
        self.seed_url = seed_url
        self.user_agent = user_agent
        self.robots_url = Robots.robots_url(seed_url)
        self.robots = Robots.fetch(self.robots_url)
        self.accepted_header_content_type = "text/html"

    def can_page_be_fetched(self, page_url):
        result = self.robots.allowed(page_url, self.user_agent)
        return result

    def has_content_type(self, content_type):

        if content_type is not None and self.accepted_header_content_type in content_type:
            return True
        else:
            return False
