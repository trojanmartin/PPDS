from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex
 
"""Vypisovat na monitor budeme pomocou funkcie 'print'
   importovanej z modulu 'ppds'.
   To kvoli tomu, aby neboli 'rozbite' vypisy.
"""
from fei.ppds import print
 
 
class SharedObject:
    def __init__(self, N):
        self.N = N
        self.fibonacci = [0,1]
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)


    def wait(self):
        pass


class Fibonacci:
    def __init__(self,shared, n):
        self.shared = shared
        self.sequence = [0,1] + [0]*n 
        self.n = n
    """može sa zdať ako správne riesenie, problem ale je ten, 
        že čo ak sa nejake vlakno predbehne. napriklad vlakno 5 sa dostane k zámku skor ako vlakno 4
        tym padom vlakno 5 nema z coho ratat svoju hodnotu"""
    def count_sequence(self,thread_id):
        self.shared.mutex.lock()       
        print("thread %d is locked" % thread_id) 
        self.sequence[thread_id + 2] = self.sequence[thread_id] + self.sequence[thread_id + 1]
        self.shared.mutex.unlock()        
        

n = 20
shared = SharedObject(n)
fib_counter = Fibonacci(shared,n)
threads = list()
for i in range(n):
    t = Thread(fib_counter.count_sequence,i)
    threads.append(t)
 
for t in threads:
    t.join()

print(fib_counter.sequence)