from fei.ppds import Semaphore, Mutex, Thread, Event, print
from random import randint
from time import sleep


class Barrier:
    def __init__(self, N):
        self.N = N
        self.counter = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)
 
    def wait(self):
        self.mutex.lock()
        self.counter += 1
    
        if self.counter == self.N:
            self.turnstile.signal()
        self.mutex.unlock()
         
        self.turnstile.wait()
        self.turnstile.signal()


class Shared():
    def __init__(self):
        self.mutex = Semaphore(1)
        self.hydrogen = 0
        self.oxygen = 0      
        self.barrier = Barrier(3)
        self.oxygenQueue = Semaphore(0)
        self.hydrogenQueue = Semaphore(0)  

def bond():
    pass

def oxygen(shared):
    shared.mutex.wait()
    shared.oxygen += 1

    if(shared.hydrogen < 2):
        shared.mutex.signal()

    else:
        shared.oxygen -= 1
        shared.hydrogen -= 2
        shared.oxygenQueue.signal()
        shared.hydrogenQueue.signal(2)

    shared.oxygenQueue.wait()
    bond()

    shared.barrier.wait()
    shared.mutex.signal()