# Cvičenie 8

- Cieľom aplikácie je stiahnutie obsahu stránky google.com, a počas trvania requestu informovať o prebiehajúcom requeste pomocou výpisu do konzoly.

- V synchrónnej verzii možme vidiet že nieje možné splniť cieľ aplikácie. Totižto, request je blokujúci a počas jeho trvania nieje možné v danom vlákne vykonávať nič iné. Dalo by sa to vyriešiť druhým vláknom, ktorého úlohou by bol výpis.

- V asynchrónnej verzii aplikácie sme využili modul aiohttp pomocou ktoré sme vytvorili asynchrónny request na stránku google.com. Počas trvania requestu sa vlákno uvoľní a je k dispozícii pre metódu Progress ,ktorej úlohu je výpis na obrazovku.