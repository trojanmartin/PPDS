from fei.ppds import Thread, Semaphore, print
 
 
class Shared():
    def __init__(self):
        self.room_empty = Semaphore(1)
 
 
"""
Vytvorime vlakna, ktore chceme synchronizovat.
Nezabudnime vytvorit aj zdielane synchronizacne objekty,
a dat ich ako argumenty kazdemu vlaknu, ktore chceme pomocou nich
synchronizovat.
"""
 
shared = Shared()
threads = []
 
for i in range(10):
    t = Thread(writer_thread, f"Writer {i}", shared)
    threads.append(t)
 
for t in threads:
    t.join()