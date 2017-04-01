'''
Created on 29 Mar 2017

@author: alessiogastaldo

Class with queue implementation. This queue is used by the crawler to insert new links
'''


class URLQueue():

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def is_in_queue(self, element):
        return True if element in self.items else False
