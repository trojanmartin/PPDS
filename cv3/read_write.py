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
        self.turnstile = Semaphore(1)
        self.switch = LightSwitch()


def write(shared, thread_id):
    while True:  
        shared.turnstile.wait()
        shared.room_empty.wait()
        print("thread %d started WRITING" % thread_id)
        sleep((randint(1,10)/10) + .3)    
        
        shared.turnstile.signal()
        shared.room_empty.signal()
        print("thread %d finished WRITING and signaled" % thread_id)
        


def read(shared, thread_id):
    while True:
        shared.turnstile.wait()
        shared.turnstile.signal()
        shared.switch.lock(shared.room_empty)
        print("thread %d started reading" % thread_id)
        sleep((randint(1,10)/10)+0.3)
        shared.switch.unlock(shared.room_empty)
        print("thread %d finished reading and signaled" % thread_id)

"""
Vytvorime vlakna, ktore chceme synchronizovat.
Nezabudnime vytvorit aj zdielane synchronizacne objekty,
a dat ich ako argumenty kazdemu vlaknu, ktore chceme pomocou nich
synchronizovat.
""" 
sh = Shared()
threads = []

readers = 5
writers = 1

for i in range(readers):
    t = Thread(read, sh,i)
    threads.append(t)

for i in range(writers):
    t = Thread(write, sh,i + readers)
    threads.append(t)

for t in threads:
    t.join()