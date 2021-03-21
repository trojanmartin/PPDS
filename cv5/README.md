# Cvičenie 4

- Ide o úlohu Hodujúcich divochov, ktorá je založená na myšlienke Producentov a konzumentov.
Je však rozšírená o sledovanie stavu buffra, kedy kuchári nemôžu navariť viac
ako sa zmestí do hrnca.  

## Pseudo kód
```py
M = 5
N = 3
K = 3


def init():
    mutex = Mutex()
    cook_mutex = Mutex()
    signaled = False
    servings = 0
    full_pot = Semaphore(0)
    empty_pot = Event()


def get_serving_from_pot(savage_id, shared):
    print("divoch %2d: beriem si porciu" % savage_id)
    shared.servings -= 1


def eat(savage_id):
    print("divoch %2d: hodujem" % savage_id)
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
    // navarenie jedla tiez cosi trva...
    print("kuchar %2d vari" % cook_id)
    sleep(0.4 + randint(0, 2) / 10)


def put_servings_in_pot(cook_id, shared):
    print("kuchar %2d vklada missionara do hrnca" % cook_id)
    shared.servings += 1


def cook(cook_id, M, shared):
    while True:

        /* Vsetci kuchari cakaju kym bude hrniec prazdny.
        Ked sa hrniec vyprazdni zacnu vsetci varit.
        */

        shared.empty_pot.wait()
        cooking(cook_id)

        /* Ak uz je hrnciec plny, a zaroven event o prazdnom hrnci
        nieje nastaveny, dam signal divochom ze mozu hodovat
        Ak je event nastaveny a vlakno sa nachadza v mutexe, znamena
        to ze niekto pred nim uz oznamil divochom radostnu spravu o plnom hrnci
        a dane vlakno nemusi robit nic */
        
        shared.cook_mutex.lock()
        if(M == shared.servings && shared.empty_pot.isSet()):
            shared.empty_pot.clear()
            print("kuchar %2d oznamuje divochom ze hrnciec je plny" % cook_id)
            shared.full_pot.signal()

        // ak mam navarene, ale nedal som porciu do hrnca, musim cakat kym hrniec bude volny
        shared.empty_pot.wait()
        put_servings_in_pot(cook_id, shared)

        shared.cook_mutex.unlock()
```
 
