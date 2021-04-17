# Országgyűlési Napló elemző
## Leírás:  
A csomag az Országgyűlési Napló pdf dokumentum letöltésére és elemzésére szolgál.
## A modullal lehetséges:
   1. az aktuális pdf dokumentum letöltése  
   2. pdf formátumból txt formátumba való átalakítása  
   3. a dokumentum tisztázása  
   4. a következő adatok kinyerése:
   
   * ciklus  
   * dokumentum szám
   * elnökök listája
   * jegyzők listája
   * törzsszöveg
   * felszólaló képviselők listája
   * tárgyalt határozati javaslatok listája
   * tárgyalt törvény javaslatok listája
   * képviselői felszőlalások listája
   * felszólalás közben elhangzó és legyzett reakciók listája

Országgyűlési napló dokumentum forrása: https://www.parlament.hu/web/guest/orszaggyulesi-naplo

### 1. Modul importálása


```python
from pathlib import Path
from pprint import pprint

import hunparl as hp

HOME_DIR = Path("/home/Downloaded")
```

### 2. Letöltés
#### 2.a A parlament.hu oldalán legutoljára közzétett Országgyűlési napló letöltése (default) a megadott HOME_DIR elérési útvonalra
forrás: https://www.parlament.hu/web/guest/orszaggyulesi-naplo

```python
hp.letolto.scraper(HOME_DIR)
```

    Országgyűlési Napló 186.szám.pdf mentve: /home/Downloaded
    CPU times: user 211 ms, sys: 11.2 ms, total: 222 ms
    Wall time: 335 ms


#### 2.b Tetszőleges szám letöltése


```python
szam = "100"
hp.letolto.scraper(HOME_DIR,szam)
```

    Országgyűlési Napló 100.szám.pdf mentve: /home/xunguist/Ipython_Notebooks/Scraper/Parlament/Downloaded


### 3. PDF formátumból TXT formátumba történő konvertálás


```python
konvertalt = hp.konvertalo.pdf_to_txt(HOME_DIR/"Országgyűlési Napló 100.szám.pdf")
```

```python
konvertalt[:100]
```

    '   2018-2022. országgyűlési ciklus   Budapest, 2019. december 3. kedd \n\n100. szám \n\n \n\n \n \n \n \n\n \n\nO'



### 4. Az átalakított dokumentum tisztázása

A dokumentum szövegéből eltávolítja:

1.  a sorvégi szóelvalasztáshoz használt "-" kötőjeleket  
2. időjelöléseket 
3. oldalszámokat  
4. oldal fejlecéket

```
tisztazott = hp.tisztazo.ogy_n_tisztazo(konvertalt)
```

### 5. Adatok kinyerése a tisztázott dokumentumból

#### 5.a Ciklus


```python
hp.parser.ciklus(tisztazott)
```
    '2018-2022'


#### 5.b Aktuális kiadvány száma


```python
hp.parser.szam(tisztazott)
```
    '100'

#### 5.c Parlamenti ülés dátuma

```python
hp.parser.ules_datum(tisztazott)
```




    '2019. december 3.'

#### 5.d Elnökök
(alelnökök és a háznagy)  
A Házbizottság az Országgyűlés döntés-előkészítő testülete,  
melynek elnöke az Országgyűlés elnöke, tagjai az Országgyűlés alelnökei,  
a képviselőcsoportok (frakciók) vezetői és a háznagy.  


```python
hp.parser.elnok_lista(tisztazott)
```

    ['Jakab István']

#### 5.e Jegyzők

```python
hp.parser.jegyzo_lista(tisztazott)
```
    ['Gelencsér Attila', 'Szilágyi György']
    

#### 5.f Törzsszöveg
> "ELNÖK: (A teremben lévők felállnak, [...] az ülést bezárom." közötti rész.  
> Nem tartalmazza:
* fedlap, 
* a tartalomjegyzék, 
* az ülésen jelen voltak listája, 
* a jegyzői aláírások
* impresszum


```python
torzsszoveg = hp.parser.torzs_szoveg(tisztazott)
print(torzsszoveg[:100])
```

    ELNÖK: (A teremben lévők felállnak, és ezzel köszöntik a választópolgárok közösségét. Amikor az  ülé


#### 5.g Felszólaló képviselők listája
> Különbözhet az ülésen jelenlévők listájától


```python
kepv_list = hp.parser.kepviselo_lista(torzsszoveg)
kepv_list
```

    ['BANGÓNÉ BORBÉLY ILDIKÓ',
     'BECSÓ ZSOLT',
     'BÁNKI ERIK',
     'DR. APÁTI ISTVÁN',
     'DR. KERESZTES LÁSZLÓ LÓRÁNT',
     'DR. LATORCAI JÁNOS',
     'DR. LUKÁCS LÁSZLÓ GYÖRGY',
     'DR. MELLÁR TAMÁS',
     'DR. ORBÁN BALÁZS',
     'DR. RÉTVÁRI BENCE',
     'DR. TAPOLCZAI GERGELY',
     'DR. VÖLNER PÁL',
     'DÚRÓ DÓRA',
     'FARKAS GERGELY',
     'GELENCSÉR ATTILA',
     'GRÉCZY ZSOLT',
     'MAGYAR ZOLTÁN',
     'NACSA LŐRINC',
     'NUNKOVICS TIBOR',
     'NYITRAI ZSOLT',
     'SCHANDA TAMÁS JÁNOS',
     'UNGÁR PÉTER',
     'VARGA MIHÁLY',
     'Z. KÁRPÁT DÁNIEL']

#### 5.h Tárgyalt határozati javaslatok listája

```python
hp.parser.hatarozati_javaslat_lista(torzsszoveg)
```

    ['H/7380', 'H/7840', 'H/7960', 'H/8191']

#### 5.i Tárgyalt törvény javaslatok listája

```python
hp.parser.torveny_javaslat_lista(torzsszoveg)
```
    ['T/6265',
     'T/6576',
     'T/7021',
     'T/7686',
     'T/7688',
     'T/7701',
     'T/7839',
     'T/7846',
     'T/7996',
     'T/7997',
     'T/8000',
     'T/8001',
     'T/8002',
     'T/8003',
     'T/8012',
     'T/8015',
     'T/8027',
     'T/8032',
     'T/8036',
     'T/8038',
     'T/8190']

#### 5.j Képviselői felszőlalások szótára
> Kulcs: képviselő neve  
> Érték: felszólalás(ok) listája  
> Mivel a kulcs gyakran lista értéket tartalmaz, abba indexelésekkel tudunk belépni.  
> Ha egy képviselő csak egyszer szólal fel, akkor nem kell indexelést használni.  

```python
kepv_felsz_dict = hp.parser.kepviseloi_felszolalas_szotar(torzsszoveg,kepv_list)
print("Kulcsok:")
pprint(kepv_felsz_dict.keys())
```

    Kulcsok:
    dict_keys(['BANGÓNÉ BORBÉLY ILDIKÓ', 'BECSÓ ZSOLT', 'BÁNKI ERIK', 'DR. APÁTI ISTVÁN', 'DR. KERESZTES LÁSZLÓ LÓRÁNT', 'DR. LATORCAI JÁNOS', 'DR. LUKÁCS LÁSZLÓ GYÖRGY', 'DR. MELLÁR TAMÁS', 'DR. ORBÁN BALÁZS', 'DR. RÉTVÁRI BENCE', 'DR. TAPOLCZAI GERGELY', 'DR. VÖLNER PÁL', 'DÚRÓ DÓRA', 'FARKAS GERGELY', 'GELENCSÉR ATTILA', 'GRÉCZY ZSOLT', 'MAGYAR ZOLTÁN', 'NACSA LŐRINC', 'NUNKOVICS TIBOR', 'NYITRAI ZSOLT', 'SCHANDA TAMÁS JÁNOS', 'UNGÁR PÉTER', 'VARGA MIHÁLY', 'Z. KÁRPÁT DÁNIEL'])

```python
print("Kulcs-Érték pár:")
BBI = kepv_felsz_dict['BANGÓNÉ BORBÉLY ILDIKÓ']
print(type(BBI))
print(type(BBI[0]))
BBI[0][:100]
```
    Kulcs-Érték pár:

    'BANGÓNÉ BORBÉLY ILDIKÓ (MSZP): Köszönöm szépen, elnök úr. Tisztelt Képviselőtársak!  A múlt héten vo'

#### 5.k Felszólalás közben elhangzó és legyzett reakciók listája


```python
hp.parser.reakcio_lista(kepv_felsz_dict['BÁNKI ERIK'])
```

    ['(Zaj. - Az elnök csenget.)', '(Taps a kormánypárti padsorokban.)']
