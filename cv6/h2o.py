from fei.ppds import Semaphore, Mutex, Thread, Event, print
from random import randint
from time import sleep


class Barrier:
    def __init__(self, N):
        self.N = N
        self.counter = 0
        self.mutex = Mutex()
        self.semaphore = Semaphore(0)
 
    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.N:
            self.counter = 0
            self.semaphore.signal(self.N)
        self.mutex.unlock()
        self.semaphore.wait()


class Shared():
    def __init__(self):
        self.mutex = Semaphore(1)
        self.hydrogen = 0
        self.oxygen = 0      
        self.barrier = Barrier(3)
        self.oxygenQueue = Semaphore(0)
        self.hydrogenQueue = Semaphore(0)  

def bond():
    # vytvorenie molekuly nieco trva
    print("Bondujem sa")
    sleep(0.2 + randint(0, 3) / 10)

def oxygen(shared):
    shared.mutex.wait()
    shared.oxygen += 1

    print("Oxygen: Som sam")

    if(shared.hydrogen < 2):
        print("Oxygen: je nas malo, odomykam mutex")
        shared.mutex.signal()

    else:
        shared.oxygen -= 1
        shared.hydrogen -= 2
        shared.oxygenQueue.signal()
        shared.hydrogenQueue.signal(2)

    print("Oxygen: Cakam vo fronte kym bude dostatok hydrogenov")
    shared.oxygenQueue.wait()
    bond()

    print("Oxygen: Skoncil som bondovanie, cakam na bariere")
    shared.barrier.wait()
    shared.mutex.signal()


def hydrogen(shared):
    shared.mutex.wait()
    print("Hydrogen: prichadzam")
    shared.hydrogen += 1

    if(shared.hydrogen < 2 or shared.oxygen < 1):
        print("Hydrogen: je nas malo, odomykam mutex")
        shared.mutex.signal()

    else:
        shared.oxygen -= 1
        shared.hydrogen -= 2
        shared.oxygenQueue.signal()
        shared.hydrogenQueue.signal(2)

    print("Hydrogen: cakam v queue")
    shared.hydrogenQueue.wait()
    bond()

    print("Hydrogen: Skoncil som bondovanie, cakam na bariere")
    shared.barrier.wait()

threads = list()
shared = Shared()
for savage_id in range(0, 50):
    threads.append(Thread(oxygen, shared))

for cook_id in range(0, 100):
    threads.append(Thread(hydrogen, shared))

for t in threads:
    t.join()