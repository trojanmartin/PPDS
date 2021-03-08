from fei.ppds import Thread, Semaphore, print, Mutex
from time import sleep
from random import randint


class LightSwitch():
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0
 
    def lock(self, semaphore):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()
 
    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


class Shared():
    def __init__(self):
        self.room_empty = Semaphore(1)
        self.switch = LightSwitch()


def write(shared, thread_id):
    while True:
        shared.room_empty.wait()
        print("thread %d started writing" % thread_id)
        sleep(randint(1,10)/10)    
        print("thread %d finished writing" % thread_id)
        shared.room_empty.signal()


def read(shared, thread_id):
    while True:
        shared.switch.lock(shared.room_empty)
        print("thread %d started reading" % thread_id)
        sleep(randint(1,10)/10)
        print("thread %d finished reading" % thread_id)
        shared.switch.unlock(shared.room_empty)

"""
Vytvorime vlakna, ktore chceme synchronizovat.
Nezabudnime vytvorit aj zdielane synchronizacne objekty,
a dat ich ako argumenty kazdemu vlaknu, ktore chceme pomocou nich
synchronizovat.
"""
 
shared = Shared()
threads = []
 
for i in range(1):
    t = Thread(read, shared,i)
    threads.append(t)

for i in range(1):
    t = Thread(write, shared,i)
    threads.append(t)
 
for t in threads:
    t.join()