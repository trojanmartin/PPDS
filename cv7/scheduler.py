from enum import Enum
from queue import Queue
import random


def test1():
    for a in range(5000):
        print("Test 1")
        yield


def test2():
    for a in range(5000):
        print("Test 2")
        yield


class Priority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3


class Coroutine:
    def __init__(self, method):
        self.method = method
        self.finished = False

    def IsFinished(self):
        return self.finished

    def run(self):
        try:
            self.method.send(None)
        except StopIteration:
            self.finished = True


class CoroutineScheduler:
    def __init__(self):
        self.low = Queue()
        self.normal = Queue()
        self.high = Queue()

    def add(self, method, priority):
        coroutine = Coroutine(method)
        self.schedule(coroutine, priority)

    def schedule(self, coroutine, priority):
        if priority == Priority.LOW:
            self.low.put(coroutine)

        if priority == Priority.NORMAL:
            self.normal.put(coroutine)

        if priority == Priority.HIGH:
            self.high.put(coroutine)

    def any(self):
        low = not self.low.empty()
        normal = not self.normal.empty()
        high = not self.high.empty()

        return low or normal or high

    def start(self):
        while self.any():
            val = random.randint(1, 10)

            if val >= 6:
                self.run(self.high, Priority.HIGH)

            elif val >= 3:
                self.run(self.normal, Priority.NORMAL)

            else:
                self.run(self.low, Priority.LOW)

    def run(self, queue, priority):
        if(queue.empty()):
            return

        coroutine = queue.get()
        coroutine.run()

        if(not coroutine.IsFinished()):
            self.schedule(coroutine, priority)

if __name__ == "__main__":
    scheduler = CoroutineScheduler()

    scheduler.add(test1(), Priority.HIGH)
    scheduler.add(test2(), Priority.LOW)

    scheduler.start()
