from queue import PriorityQueue
from enum import Enum

def test1():
    while True:
        print("Test 1")
        yield


def test2():
    for a  in range(10):
        print("Test 2")
        yield


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
        self.couroutines = PriorityQueue()

    def add(self, method, priority):
        coroutine = Coroutine(method)
        self.couroutines.put((priority, coroutine))     
     

    def run(self):
        while True:
            (priority, cor) = self.couroutines.get()
            cor.run()

            if not cor.IsFinished():
                self.couroutines.put((priority, cor))




if __name__ == "__main__":
    scheduler = CoroutineScheduler()

    scheduler.add(test1(),5)
    scheduler.add(test2(),4)

    scheduler.run()
