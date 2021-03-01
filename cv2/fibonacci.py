from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, Event, print


class SemaphoreSynchronizer:
    def __init__(self, n):
        self.n = n
        self.semaphores = [0] * (n)

        # vytvorím n semaforov
        for i in range(n):
            self.semaphores[i] = Semaphore(0)
        # prve vlakno nemusi na nič čakať, spustim ho hned na začiatku
        self.signal(0)

    def signal(self, thread_id):
        self.semaphores[thread_id].signal()

    def wait(self, thread_id):
        self.semaphores[thread_id].wait()


class EventSynchronizer:
    def __init__(self, n):
        self.n = n
        # vytvorím n eventov
        self.events = [0] * (n)
        for i in range(n):
            self.events[i] = Event()
        # prve vlakno nemusi na nič čakať, spustim ho hned na začiatku
        self.signal(0)

    def signal(self, thread_id):
        self.events[thread_id].signal()

    def wait(self, thread_id):
        self.events[thread_id].wait()


class Fibonacci:
    def __init__(self, synchronizer, n):
        self.synchronizer = synchronizer
        self.n = n
        self.sequence = [0, 1] + [0] * n

    def count_sequence(self, thread_id):
        # každé vlákno čaká kým mu bude povolený výpočet svojho čísla
        self.synchronizer.wait(thread_id)
        next = self.sequence[thread_id] + self.sequence[thread_id + 1]
        self.sequence[thread_id + 2] = next
        """ ak posledné vlákno spravilo svoj výpočet, funkcia skončí
        inak, vlákno signalizaciou odblokuje nasledjúce vlákno """
        if(self.n == thread_id + 1):
            return
        self.synchronizer.signal(thread_id + 1)

    """može sa zdať ako správne riesenie, problem ale je ten,
        že čo ak sa nejake vlakno predbehne.
        Napriklad vlakno 5 sa dostane k zámku skor ako vlakno 4
        tym padom vlakno 5 nema z coho ratat svoju hodnotu"""
    def count_sequence_not_working(self, thread_id):
        self.shared.mutex.lock()
        print("thread %d is locked" % thread_id)
        next = self.sequence[thread_id] + self.sequence[thread_id + 1]
        self.sequence[thread_id + 2] = next
        self.shared.mutex.unlock()


def test_sequence(sequence):
    i = len(sequence) - 1
    while(i - 2 >= 0):
        if(sequence[i] != sequence[i - 2] + sequence[i - 1]):
            print("TEST FAILED")
            return

        i -= 1
    print("TEST OK")


"""Odpovede na otazky:
    1. Podla mojho názoru, najmenší počet synchronizačných objektov je vždy N.
    A to z toho dovodu že každé vlákno vyžaduje inú dobu čakania,
    kym vykaná svoj výpočet.

    2. Pri riešení tohto zadania som použil synchronizačný vzor signalizácie.
    Pri signalizácii dáva jedno vlákno signál o nejakej udalosti ktorá nastala.
    V mojom prípade to je o dokončení svojho výpočtu.
    Čiže ked jedno vlákno vypočíta svoju hodnotu fibonacciho postupnosti,
    signalizáciou to oznámi nasledujúcemu,
    ktoré tým pádom vie že môže vykonať svoj výpočet.
"""

n = 999
# synchronizer = SemaphoreSynchronizer(n)
synchronizer = EventSynchronizer(n)

fib_counter = Fibonacci(synchronizer, n)

threads = list()
for i in range(n):
    t = Thread(fib_counter.count_sequence, i)
    threads.append(t)
for t in threads:
    t.join()

# print(fib_counter.sequence)
test_sequence(fib_counter.sequence)
