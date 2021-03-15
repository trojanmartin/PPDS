# Cvičenie 4

- Ide o úlohu vzájomného vylúčenia, keďže procesy môžeme rozdeliť do dvoch kategórii. 
Pre obe kategórie platí, že viacerí členovia kategórie môžu naraz pristupovať k údajom.
Je to tak kvoli tomu ,že monitory k dátam iba pristupujú a teda ich nemodifikuju. 
Zároveň je možné aby aj čidlá zapisovali naraz, keďže každé čidlo zapisuje na 
vlastné miesto. 
Zároveň je potrebné riešiť problém vyhladovania. Keďže monitorov je 8, a čidlá sú len 3, je potrebné
dať prioritu pre čidlá.
Monitory taktiež môžu začať čítať dáta až vtedy, keď už všetky čidlá aspoň raz zapísali dáta.   

- Vzájomné vylúčenie bude implementačne riešené pomocou LightSwitch-u. Tým zabezpečíme že v jednom čase môže k dátam
pristúpiť vždy len jedna skupina procesov. Pre to aby boli čidlá uprednostnené je taktiež potrebné použitie dvoch lighswitchov.
- To aby monitory začali čítať až po zapísaní prvých dát všetkými čidlami implementujeme pomocou bariéry a následnej signalizácie. Bariéra bude implementovaná pomocou Eventu a monitory budú čakať až kým sa daný event nenastavaví. To sa udeje
keď všetky čidlá vykonajú svoje merianie aspoň raz.
## Pseudo kód
```py
def init():
    cidla_ls = LightSwitch()
    monitor_ls = LightSwitch()
    no_cidla = Semaphore(1)
    no_monitor = Semaphore(1)
    //Bariera, inicializovana na pocet cidiel (3)
    barrier = SimpleBarrier(3)

def monitor(monitor_id):
    while True:
        //Monitory čakajú kým čidlá prvýkrát zapíšu dáta
        barrier.event.wait()
        //čakanie kym všetky čidlá opustia "miestnosť" 
        no_monitor.wait()
        pocet_citajucich_monitorov = monitor_ls.lock(self.no_cidla)
        no_monitor.signal()
        waiting = randint(40, 50)/1000
        print('monit "%02d": pocet_citajucich_monitorov=%02d, trvanie_citania=%03f\n' % (monitor_id, pocet_citajucich_monitorov, waiting))
        //simulacia vykeslovania
        sleep(waiting)
        //
        monitor_ls.unlock(no_cidla)
        
//parametrom funkcie je doba cakania, aby sme vedeli rozlišovať medzi čidla P,T a H
def cidlo(cidlo_id, waiting):
    while True:
        //medzi pokusmi čidlo čaká 50-60ms
        sleep(randint(50, 60)/1000)
        
        //prve čidlo zamkne "izbu" pred monitormi, tymto si prednostne vyžiada pristup
        pocet_zapisujucich_cidiel = cidla_ls.lock(no_monitor)
        //caka sa kym monitory vyprazdna miestnost
        no_cidla.wait()
        no_cidla.signal()
        print('cidlo "%02d": pocet_zapisujucich_cidiel=%02d, trvanie_zapisu=%03f\n' % (cidlo_id, pocet_zapisujucich_cidiel, waiting))
        //simulacia času zapisovania
        sleep(waiting)
                
        //čaká sa kým všetky tri cidla skončia prvé zapisovani dat
        //Bariera je implementovana pomocou Eventu, čiže pri dalšich iteraciach nijako neovplyvnuje beh programu
        barrier.wait()
        
        //posledny odomnke miesnosť
        cidla_ls.unlock(no_monitor)
```
 
