# BC6X4X Mesterséges Intelligencia
# Féléves feladat[A feladat 2 file-t tartalmaz. A mesint.py tartalmazza a feladat megoldását, a test.py előre beégetett adatokkal rendelkezik, hogy lehessen tesztelni a programot. Config file nélkül nem működőképes]
## Feladat leírás:

## Probléma
> - **Flow-shop:** *A flow-shop feladat egy egyutas, többoperációs gyártásütemezési feladat.*
> - **Flow-shop munkaszünetekkel:** *Az alap feladat továbbfejlesztése munkaszünetekkel. A szünetek nem vághatják félbe az adott munkát, nem kezdődhet és nem végződhet szünetben.*
> - **Algoritmus: Szimulált hűtés:** *Ez az algoritmus az egyszerű szomszédsági keresésre épül, azzal a különbséggel, hogy a keresés során valamilyen valószínűségtől függ, hogy elfogadunk-e rosszabb eredményt.*
> - **Extra feladat:** *Több hűtési stratégia összehasonlítása, diagramm megjelenítéssel*

## Feladat részletes leírása
> - *Az erőforrások az ütemezési időszakban folyamatosan rendelkezésre állnak.*
> - *Az erőforrások egyszerre csak egy munkán dolgoznak.*
> - *A munkák legkorábbi indítási időontja nulla (bármikor indíthatóak).*
> - *Minden egyes munkához adott m számú operáció tartozik, melyeknek pontosan ismert a végrehajtási ideje.*
> - *Az operációk végrehajtási sorrendje kötött és minden munka esetében azonos.*
> - *Az operációk végrehajtása nem szakítható meg.*
> - *A gépek között a munkák várakozhatnak, a műveletközi tárolók mérete nem korlátos.*
> - *Az ütemezés célja az utolsóként elkészülő munka befejezési időpontjának minimalizálása.*

# Programszerkezet leírása
## main
> - *Program elindítása, seed beállítása*

## read_from_file
> - *Egy egyszerű file-reader a konfigurációk beolvasásához*
> - *Minden kiolvasott adatt visszakerül a main függvénybe, ahonnan elindul a feladat generálása.*

## generate_random_jobs
> - *Minden adatot a 'log.txt' file-ba ment a program.*
> - *Legenerálja a konfigurációk alapján a feladatot tartalmazó tömböket, majd elindítja a keresést.*
> - *A munkák az 'array_of_jobs' változóban vannak elmentve, amelyet a függvény generált.*

## start_search
> - *A függvény indítja a szömszédsági kereséseket egymás után egy ciklusban.*
> - *A szomszédsági keresés egy egyszerű ciklusban történik. A 'base' változó véletlenszerűen kiválasztott 2 elemét megcseréljük, ez lesz a 'data' változónk.*

## start_test
> - *Mindig a 'data' változó alapján folyik a keresés, jobb eredmény esetén(vagy ha a hűtés megengedi) a 'base' változó felülíródik a 'data' változó tartalmával.*
> - *A 'best_time_of_current_search' változó tartalmazza az adott keresés legjobb eredményét, a 'best_time_of_alltime_search' változó tartalmazza az eddigi összes keresés legjobb eredményét.*
> - *A 'base' változó tartalmazza az alaphalmazt, ami alapján folyik a keresés, míg a 'data' változó tartalmazza a base egyik változatát.*
> - *Így mindig a legjobb eredmény egy újább változatával keresünk.*
> - *A 'best_found_solution' változó tartalmazza az eddigi legjobb kombinációt.*
> - *Megcserélés után lefuttatjuk a szimulált hűtés algoritmust(simulation), majd az eredmény alapján eldöntjük, hogy jó-e az eredmény.*
> - *Ha az eredmény jobb, mint a keresések legjobbja, akkor új bázist választunk. Amennyiben rosszabb az eredmény, eldöntjük a hűtéssel, hogy elfogadjuk-e vagy sem.*
> - *Ha elfogadjuk a rosszabb eredményt, akkor új bázist választunk. Ha nem fogadjuk el, akkor megy tovább a ciklus a változatlan bázissal.*

## simulation
> - *A kombinációk idejének kiszámításáért felelős függvény.*
> - *A 'Current_work' változó tárolja az adott gép munkájának hosszúságát, a 'Current_done' változó pedig az adott gép által már elkészített munkákat tárolja.*
> - *A ciklusunk addig megy, amíg az utolsó gép be nem fejezi az utolsó munkáját.*
> - *A ciklusban az időt folyamatosan növeljük iterációnként, a 'Current_work' változót pedig folyamatosan csökkentjük.*
> - *Amennyiben a 'Current_work' változó eléri a 0-át, azaz befejezte az adott munkát, akkor a 'Current_done' változót növeljük 1-el, a 'Current_work' változót bedig beállítjuk a következő munka hosszúságára.*
> - *Mielőtt elkezdjük csökkenteni a 'Current_work' változót, előtte leellenőrizzük, hogy a munkát nem zavarja-e az adott szünet.(check_pauses_and_current_work)*
> - *Leellenőrizzük a ciklus után, hogy jobb eredményt kaptunk-e, majd visszatérünk a start_test függvénybe, majd a start_search függvénybe.*

## check_pauses_and_current_work
> - *A szünetek ellenörzéséért felelős függvény*
> - *Egy ciklusban végigmegy az összes munkaszüneten, majd leellenörzi az adott munkát.*
> - *A munka nem kezdődhet szünetben, nem fejeződhet be szünetben és a munkát nem vághatja félbe a szünet.*

## print_array
> - *Egy egyszerű függvény, amely a tömbök szebb kiíratásáért felelős.*
