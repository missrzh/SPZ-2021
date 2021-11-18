import random


class Process:
    def __init__(self, virtual_pages, ttl, ww_size):
        self.virtual_pages = virtual_pages
        self.ttl = ttl
        self.ww_size = ww_size

    def working_set(self):
        return self.virtual_pages[:self.ww_size]

    def change_working_set(self):
        random.shuffle(self.virtual_pages)
