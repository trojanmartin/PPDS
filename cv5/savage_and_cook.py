from fei.ppds import Semaphore, Mutex, Thread, Event, print
from random import randint
from time import sleep

"""M, N a K su parametre modelu, nie synchronizacie ako takej.
Preto ich nedavame do zdielaneho objektu.
    M - pocet porcii misionara, ktore sa zmestia do hrnca.
    N - pocet divochov v kmeni (kuchara nepocitame).
    K - pocet kucharov
"""
M = 5
N = 3
K = 3


class Shared:
    def __init__(self):
        self.mutex = Mutex()
        self.cook_mutex = Mutex()
        self.signaled = False
        self.servings = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Event()


def get_serving_from_pot(savage_id, shared):
    """Pristupujeme ku zdielanej premennej.
    Funkcia je volana pri zamknutom mutexe, preto netreba
    riesit serializaciu v ramci samotnej funkcie.
    """

    print("divoch %2d: beriem si porciu" % savage_id)
    shared.servings -= 1


def eat(savage_id):
    print("divoch %2d: hodujem" % savage_id)
    # Zjedenie porcie misionara nieco trva...
    sleep(0.2 + randint(0, 3) / 10)


def savage(savage_id, shared):
    while True:
        # Nasleduje klasicke riesenie problemu hodujucich divochov.
        shared.mutex.lock()
        print("divoch %2d: pocet zostavajucich porcii v hrnci je %2d" %
              (savage_id, shared.servings))
        if shared.servings == 0:
            print("divoch %2d: budim kucharov" % savage_id)
            shared.empty_pot.set()
            shared.full_pot.wait()
        get_serving_from_pot(savage_id, shared)
        shared.mutex.unlock()

        eat(savage_id)


def cooking(cook_id):
    # navarenie jedla tiez cosi trva...
    print("kuchar %2d vari" % cook_id)
    sleep(0.4 + randint(0, 2) / 10)


def put_servings_in_pot(cook_id, shared):
    """M je pocet porcii, ktore vklada kuchar do hrnca.
    Hrniec je reprezentovany zdielanou premennou servings.
    Ta udrziava informaciu o tom, kolko porcii je v hrnci k dispozicii.
    """
    print("kuchar %2d vklada missionara do hrnca" % cook_id)
    shared.servings += 1


def cook(cook_id, M, shared):
    while True:

        """Vsetci kuchari cakaju kym bude hrniec prazdny.
        Ked sa hrniec vyprazdni zacnu vsetci varit.
        """
        shared.empty_pot.wait()
        cooking(cook_id)

        """Ak uz je hrnciec plny, a zaroven event o prazdnom hrnci
        nieje nastaveny, dam signal divochom ze mozu hodovat
        Ak je event nastaveny a vlakno sa nachadza v mutexe, znamena
        to ze niekto pred nim uz oznamil divochom radostnu spravu o plnom hrnci
        a dane vlakno nemusi robit nic"""
        shared.cook_mutex.lock()
        if(M == shared.servings and shared.empty_pot.isSet()):
            shared.empty_pot.clear()
            print("kuchar %2d oznamuje divochom ze hrnciec je plny" % cook_id)
            shared.full_pot.signal()

        shared.empty_pot.wait()
        put_servings_in_pot(cook_id, shared)
        shared.cook_mutex.unlock()


def init_and_run(N, M):
    """Spustenie modelu"""
    threads = list()
    shared = Shared()
    for savage_id in range(0, N):
        threads.append(Thread(savage, savage_id, shared))

    for cook_id in range(0, K):
        threads.append(Thread(cook, cook_id, M, shared))

    for t in threads:
        t.join()


if __name__ == "__main__":
    init_and_run(N, M)
