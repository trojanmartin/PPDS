from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex
 
"""Vypisovat na monitor budeme pomocou funkcie 'print'
   importovanej z modulu 'ppds'.
   To kvoli tomu, aby neboli 'rozbite' vypisy.
"""
from fei.ppds import print
 
 
class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.counter = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)
 
    def wait(self):
        """Mutexom chránime zdielanu hodnotu counter"""
        self.mutex.lock()
        self.counter += 1
    
        if self.counter == self.N:
            self.turnstile.signal()
        self.mutex.unlock()

        """synchronizacny vzor turniket. V jednom čase ním prejde
        len jedno vlákno. A následne signalizuje možnosť prechodu dalsiemu vlaknu""" 
        self.turnstile.wait()
        self.turnstile.signal()
 
 
def barrier_example(barrier, thread_id):
    """Predpokladajme, ze nas program vytvara a spusta 5 vlakien,
    ktore vykonavaju nasledovnu funkciu, ktorej argumentom je
    zdielany objekt jednoduchej bariery
    """
    sleep(randint(1,10)/10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("vlakno %d po bariere" % thread_id)
 
 
# priklad pouzitia ADT SimpleBarrier
sb = SimpleBarrier(5)
 
threads = list()
for i in range(5):
    t = Thread(barrier_example,sb, i)
    threads.append(t)
 
for t in threads:
    t.join()