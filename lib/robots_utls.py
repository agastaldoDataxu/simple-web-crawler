'''
Created on 28 Mar 2017

@author: alessiogastaldo
'''

from reppy.robots import Robots
from reppy.cache import RobotsCache


USER_AGENT = "alessiog-crawler"
# This utility uses `requests` to fetch the content

robots_url = Robots.robots_url('https://gocardless.com/new-to-direct-debit/')
robots = Robots.fetch('https://gocardless.com/robots.txt')
am_i_allowed = robots.allowed(
    'https://gocardless.com/pay/', USER_AGENT)

# Get the rules for a specific agent
agent = robots.agent(USER_AGENT)
is_my_agent_allowed = agent.allowed(
    'https://gocardless.com/new-to-direct-debit/')

print am_i_allowed
print is_my_agent_allowed
print robots_url