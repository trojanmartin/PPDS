import queue
from enum import Enum

def test1():
    while True:
        print "Test 1"
        yield


def test2():
    while True:
        print "Test 2"
        yield


class Coroutine:
    def __init__(self, method):
        self.method = method
        self.finished = False

    def run(self):
        try:
            self.method.send()
        except GeneratorExit:
            self.finished = True


class CoroutineScheduler:
    def __init__(self):
        self.couroutines = PriorityQueue()

    def add(self, couroutine, priority):
        self.couroutines.put((priority, couroutine))     
    

    def run(self):
        while True:
            self.couroutines.pop()



    