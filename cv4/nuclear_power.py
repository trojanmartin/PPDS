from fei.ppds import Thread, Semaphore, print, Mutex, Event
from time import sleep
from random import randint


class LightSwitch():
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, semaphore):
        self.mutex.lock()
        count = self.counter
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()
        return count

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()

class SimpleBarrier:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.mutex = Mutex()        
        self.event = Event()
    
    def wait_with_events(self):
        self.mutex.lock()        
        self.count += 1
        if self.count == self.n:
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()



class Elektraren():
    def __init__(self):
        self.cidla_ls = LightSwitch()        
        self.monitor_ls = LightSwitch()
        self.no_cidla = Semaphore(1)
        self.no_monitor = Semaphore(1)
        self.barrier = SimpleBarrier(3)        
        self.data_ready = Event()

    def monitor(self,monitor_id):
        while True:              
            self.barrier.event.wait()         
            self.no_monitor.wait()                       

            pocet_citajucich_monitorov = self.monitor_ls.lock(self.no_cidla)
            self.no_monitor.signal()
            waiting = randint(40,50)/1000
            print('monit "%02d": pocet_citajucich_monitorov=%02d, trvanie_citania=%03f\n' % (monitor_id,pocet_citajucich_monitorov,waiting))
            sleep(waiting)            
            self.monitor_ls.unlock(self.no_cidla)


    def cidlo(self, cidlo_id, waiting):
        while True:
            sleep(randint(50,60)/1000)
            
            pocet_zapisujucich_cidiel = self.cidla_ls.lock(self.no_monitor)
            self.no_cidla.wait()

            print('cidlo "%02d": pocet_zapisujucich_cidiel=%02d, trvanie_zapisu=%03f\n' % (cidlo_id,pocet_zapisujucich_cidiel,waiting))
            sleep(waiting)  

            self.no_cidla.signal()     
            self.barrier.wait_with_events()
            self.cidla_ls.unlock(self.no_monitor)
            
            
elek = Elektraren()
threads = []
for i in range(2):
    t = Thread(elek.cidlo, i,randint(10,20)/1000)
    threads.append(t)

t = Thread(elek.cidlo, 2, randint(20,25)/1000)
threads.append(t)

for i in range(8):
    t = Thread(elek.monitor, i)
    threads.append(t)

for t in threads:
    t.join()
