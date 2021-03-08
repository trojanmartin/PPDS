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


def write(shared, thread_id, cycles, wait):
    for _ in range(cycles):  
   #     shared.turnstile.wait()
        shared.room_empty.wait()
        print("thread %d started WRITING" % thread_id)
        sleep(wait + (randint(1,10)/10))    
        
    #    shared.turnstile.signal()
        shared.room_empty.signal()
        print("thread %d finished WRITING and signaled" % thread_id)
        


def read(shared, thread_id, cycles, wait):
    for _ in range(cycles):
    #    shared.turnstile.wait()
    #    shared.turnstile.signal()
        shared.switch.lock(shared.room_empty)
        print("thread %d started reading" % thread_id)
        sleep(wait +(randint(1,10)/10))
        shared.switch.unlock(shared.room_empty)
        print("thread %d finished reading and signaled" % thread_id)



sh = Shared()
threads = []

readers = 10
writers = 1

cycles = 50
waiting = 0.3

for i in range(readers):
    t = Thread(read, sh,i,cycles, waiting)
    threads.append(t)

for i in range(writers):
    t = Thread(write, sh,i + readers,cycles,waiting)
    threads.append(t)

for t in threads:
    t.join()