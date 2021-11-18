import random

from memoryManegementUnit import MMU
from physicalPage import PhysicalPage
from process import Process
from virtualPage import VirtualPage
from matplotlib import pyplot as plt
import numpy as np




def main(set_size):
    physical_page_count = 12
    quant = 5
    working_set_size = set_size
    process_creation_time = 5
    tacts = 100000
    max_processes = 5
    fault_count = 0

    def plus():
        nonlocal fault_count
        fault_count += 1

    physical_pages = [PhysicalPage(None) for i in range(physical_page_count)]
    mmu = MMU(physical_pages, plus)
    processes = []
    pid = 0
    while tacts:
        if len(processes) != 0:
            process = processes.pop(0)
            process_time = min(process.ttl, quant)
            while process_time:
                process_time -= 1
                tacts -= 1
                process.ttl -= 1
                virtual_page = None
                if random.random() >= 0.9:
                    virtual_page = random.choice(process.virtual_pages)
                else:
                    virtual_page = random.choice(process.working_set())

                if random.random() >= 0.72:
                    mmu.write(virtual_page)
                else:
                    mmu.read(virtual_page)
                if tacts == 0:
                    break
            if process.ttl != 0:
                processes.append(process)
            else:
                for virtual_page in process.virtual_pages:
                    mmu.free(virtual_page)
        else:
            tacts -= 1
            if tacts % process_creation_time == 0 and len(processes) < max_processes:
                processes.append(
                    Process(
                        [
                            VirtualPage(False, False, False, None)
                            for _ in range(random.randint(working_set_size, physical_page_count * 2))
                        ],
                        15,
                        working_set_size
                    ))

    return fault_count


if __name__ == '__main__':
    x = []
    y = []
    for i in range(1, 21):
        print(i, main(i))
        x.append(i)
        y.append(main(i))
    plt.plot(x, y)
    plt.xlabel('Розмір робочого набору')
    plt.ylabel('Промахи')
    plt.title('Сторінкові промахи/Розмір робочого набору')
    plt.show()
