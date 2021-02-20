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

for _ in range(1000):
    sh = Shared(1_000_000)
    t1 = Thread(counter, sh)
    t2 = Thread(counter, sh)

    t1.join()
    t2.join()

    print(Histogram(sh.array))
