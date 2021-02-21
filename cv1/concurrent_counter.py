from fei.ppds import Thread, Mutex


class Shared():
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end
        self.mutex = Mutex()


class Histogram(dict):
    def __init__(self, seq=[]):
        for item in seq:
            self[item] = self.get(item, 0) + 1


# Nespravne riesenie. Prakticky vzdy nastane uviaznutie.
# Zámok sa zamkne,
# avšak problém je že v prípade splnenej podmienky na riadku 25 cyklus skončí
# dané vlákno sa ukončí
# a zámok sa nikdy neodomkne.
def counter_deadlock(shared):
    while True:
        shared.mutex.lock()
        if shared.counter >= shared.end:
            break

        shared.array[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()


# Nespravne riesenie.
# Nastava OutOfIndex exception.
# Zámok síce chráni manipuláciu s premmenými array a counter,
# avšak môže nastať situácia
# kedy je prvé vlákno je na riadku 47 až 48, a druhé vlákno je na riadku 44.
# Podmienka nieje splnená.
# Preto druhé vlákno pokračuje ďalej
# medzitým však prvé vlákno zvýši honotu v premennej counter
# a druhé vlákno sa dostane mimo rozsah poľa.
def counter_out_of_index(shared):
    while True:
        if shared.counter >= shared.end:
            break

        shared.mutex.lock()
        shared.array[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()


# jedno zo "spravnych" rieseni. Zamok sa zamkne pristup k
# zdielanemu objektu a odomkne sa aj v pripade ze podmienka nieje splnena
def counter(shared):
    while True:
        shared.mutex.lock()
        if shared.counter < shared.end:
            shared.array[shared.counter] += 1
            shared.counter += 1
            shared.mutex.unlock()
        else:
            shared.mutex.unlock()
            break


for _ in range(100):
    sh = Shared(1_000_000)
    t1 = Thread(counter, sh)
    t2 = Thread(counter, sh)

    # čakanie na ukončenie činnosti vlákien.
    t1.join()
    t2.join()

    print(Histogram(sh.array))
