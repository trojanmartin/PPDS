from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex
 
"""Vypisovat na monitor budeme pomocou funkcie 'print'
   importovanej z modulu 'ppds'.
   To kvoli tomu, aby neboli 'rozbite' vypisy.
"""
from fei.ppds import print
 
 
class SemaphoreSynchronizer:
    def __init__(self, n):
        self.n = n
        self.semaphores = [0] * (n)
        for i in range(n):
            self.semaphores[i] = Semaphore(0)
        for i in range(2):
            self.semaphores[i].signal()

    def signal(self, thread_id):
        self.semaphores[thread_id].signal()

    def wait(self, thread_id):
        self.semaphores[thread_id].wait()


class Fibonacci:
    def __init__(self,synchronizer, n):
        self.synchronizer = synchronizer
        self.n = n
        self.sequence = [0,1] + [0]*n

    def count_sequence(self,thread_id):
        self.synchronizer.wait(thread_id)
        self.sequence[thread_id + 2] = self.sequence[thread_id] + self.sequence[thread_id + 1] 

        if(self.n == thread_id + 1):
            return

        self.synchronizer.signal(thread_id + 1)


    """može sa zdať ako správne riesenie, problem ale je ten, 
        že čo ak sa nejake vlakno predbehne. napriklad vlakno 5 sa dostane k zámku skor ako vlakno 4
        tym padom vlakno 5 nema z coho ratat svoju hodnotu"""
    def count_sequence_not_working(self,thread_id):
        self.shared.mutex.lock()       
        print("thread %d is locked" % thread_id) 
        self.sequence[thread_id + 2] = self.sequence[thread_id] + self.sequence[thread_id + 1]
        self.shared.mutex.unlock()        
        

def test_sequence(sequence):
    i = len(sequence) - 1 
    while(i - 2 >= 0):
        if(sequence[i] != sequence[i - 2] + sequence[i - 1]):
            print("TEST FAILED")
            break

        i -=1
    
    print("TEST OK")


n = 5
semaphore_synchronizer = SemaphoreSynchronizer(n)
fib_counter = Fibonacci(semaphore_synchronizer,n)
threads = list()
for i in range(n):
    t = Thread(fib_counter.count_sequence,i)
    threads.append(t)
 
for t in threads:
    t.join()

print(fib_counter.sequence)
test_sequence(fib_counter.sequence)