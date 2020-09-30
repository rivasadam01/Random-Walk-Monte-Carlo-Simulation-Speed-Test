"""Random Walk & Monte Carlo Simulation

I was learning about Threading and Multiprocessing using the time.sleep
to simulate long calculations when I can across
a youtube video: https://www.youtube.com/watch?v=BfS2H1y6tzQ 
explaining the random walk & monte carlo simulation. So I wanted to see
the speed difference between single and multicore processes.

The simulation will run 20,000 walks.
For each walk it will walk up to 30 blocks.
Then it will calculate the percentage if a transport is needed or not.

The program will give you a menu to chose which version of the simulation to use.
Single or multiprocess"""

import random
import multiprocessing
import time

number_of_walks = 20000
number_of_blocks = 30


def random_walk(n):
    x, y = 0, 0
    for i in range(n):
        (dx, dy) = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        x += dx
        y += dy
    return (x, y)


class MyProcess(multiprocessing.Process):
    def __init__(self, number_of_walks, current_block_number):
        multiprocessing.Process.__init__(self)
        self.current_block_number = current_block_number
        self.number_of_walks = number_of_walks

    def run(self):
        no_transport = 0
        for i in range(self.number_of_walks):
            x, y = random_walk(self.current_block_number)
            distance = abs(x) + abs(y)
            if distance <= 4:
                no_transport += 1
        no_transport_percentage = float(no_transport) / self.number_of_walks * 100
        print(
            f"[*] Multi Core - Walk size = {self.current_block_number}, Percentage of no transport = {no_transport_percentage}%")


def no_multi_processing():
    start = time.perf_counter()
    for current_block_number in range(1, number_of_blocks + 1):
        no_transport = 0
        for current_walk in range(number_of_walks):
            x, y = random_walk(current_block_number)
            distance = abs(x) + abs(y)
            if distance <= 4:
                no_transport += 1
        no_transport_percentage = float(no_transport) / number_of_walks * 100
        print(
            f"[*] Single Core - Walk Size = {current_block_number}, Percentage of no transport needed = {no_transport_percentage}")
    finish = time.perf_counter()
    elapsed_time = round(finish - start, 2)
    print(f"\n\n[*] Single process took {elapsed_time} seconds to complete!")
    input("Press enter to continue")


def multi_processing():
    processes = []
    start = time.perf_counter()
    for current_block_number in range(1, number_of_blocks + 1):
        proc = MyProcess(number_of_walks, current_block_number)
        processes.append(proc)
        proc.start()
    for proc in processes:
        proc.join()
    finish = time.perf_counter()
    elapsed_time = round(finish - start, 2)
    print(f"\n\n[*] Multiprocess took {elapsed_time} seconds to complete!")
    input("Press enter to continue")


if __name__ == "__main__":
    option = {1: multi_processing,
              2: no_multi_processing}
    while True:
        print("1 multiprocess")
        print("2 single process")
        print("x exit")
        cmd = input("->>")
        try:
            if cmd == "x":
                exit(0)
            selection = int(cmd)
            option[selection]()
        except KeyError:
            print("\n\n[*] Invalid Option!\n\n")
