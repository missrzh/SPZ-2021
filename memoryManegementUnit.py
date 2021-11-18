from typing import List

from physicalPage import PhysicalPage


class MMU:
    def __init__(self, physical_memory: List[PhysicalPage], fault):
        self.physical_memory = physical_memory
        self.clock_index = 0
        self.fault = fault

    def read(self, virtual_page):
        self.get_physical_page(virtual_page)
        virtual_page.r = True

    def write(self, virtual_page):
        self.get_physical_page(virtual_page)
        virtual_page.r = True
        virtual_page.m = True

    def free(self, virtual_page):
        if virtual_page.p:
            self.physical_memory[virtual_page.ppn].virtual_page = None

    def get_physical_page(self, virtual_page):
        for page in self.physical_memory:
            if page.virtual_page is None:
                page.virtual_page = virtual_page
                virtual_page.p = True
                virtual_page.r = False
                virtual_page.m = False
                virtual_page.ppn = self.clock_index
                return page
        if virtual_page.p:
            return self.physical_memory[virtual_page.ppn]
        else:
            self.fault()
            while self.physical_memory[self.clock_index].virtual_page.r:
                self.physical_memory[self.clock_index].virtual_page.r = False
                self.clock_index = (self.clock_index + 1) % len(self.physical_memory)
            self.physical_memory[self.clock_index].virtual_page.p = False
            self.physical_memory[self.clock_index].virtual_page = virtual_page
            virtual_page.p = True
            virtual_page.r = False
            virtual_page.m = False
            virtual_page.ppn = self.clock_index
            return self.physical_memory[self.clock_index]




