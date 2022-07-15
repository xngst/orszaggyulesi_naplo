# Országgyűlési Napló elemző
## Leírás:  
A csomag az Országgyűlési Napló pdf dokumentum letöltésére és elemzésére szolgál.
## A modullal lehetséges:
   1. az aktuális pdf dokumentum letöltése  
   2. pdf formátumból txt formátumba való átalakítása  
   3. a dokumentum tisztázása  
   4. a következő adatok kinyerése:
   
   * parlementi ciklus  
   * dokumentum szám
   * elnökök listája
   * jegyzők listája
   * törzsszöveg
   * felszólaló képviselők listája
   * tárgyalt határozati javaslatok listája
   * tárgyalt törvényjavaslatok listája
   * képviselői felszőlalások listája
   * felszólalás közben elhangzó és lejegyzett reakciók listája

Országgyűlési napló dokumentum forrása: https://www.parlament.hu/web/guest/orszaggyulesi-naplo

## Használat:  
### 1. Modul importálása


```python
>>> import hunparl as hp
>>> from pathlib import Path
>>> DOWN_DIR = Path("/home/xn/Downloads")
```

### 2. Letöltés
#### A parlament.hu oldalán legutoljára közzétett Országgyűlési napló letöltése (default) a megadott DOWN_DIR elérési útvonalra
forrás: https://www.parlament.hu/web/guest/orszaggyulesi-naplo

```python
>>> hp.scraper(DOWN_DIR)
```

    Országgyűlési Napló 17.szám.pdf mentve: /home/xn/Downloads/Országgyűlés  


#### Tetszőleges szám letöltése


```python
szam = "5"
>>> hp.scraper(DOWN_DIR, szam)
    Országgyűlési Napló 5.szám.pdf mentve: /home/xn/Downloads/Országgyűlés
```

### 3. ogy_naplo instancia létrehozása  
 
```python
>>> naplo = hp.ogy_naplo(DOWN_DIR/"Országgyűlési Napló 17.szám.pdf")
```
#### elérési útvonal  
```python
>>> naplo.path  
PosixPath('/home/xn/Downloads/Országgyűlési Napló 17.szám.pdf')
```
#### nyers pdf-ből konvertált szöveg
```python
>>> naplo.text[:100]
'   2022-2026. országgyűlési ciklus   Budapest, 2022. június 27. hétfő \n\n17. szám \n\n \n\n \n \n \n \n\n \n\nOrszággyűlési Napló \n\nKövér László, Jakab István és dr. Oláh Lajos \n\nelnöklete alatt \n\n \n\nJegyzők: His'
```
#### tisztázott szöveg
```python
>>> naplo.tisztazott[:200]  
' 2022-2026. országgyűlési ciklus Budapest, 2022. június 27. hétfő   17. szám                  Országgyűlési Napló   Kövér László, Jakab István és dr. Oláh Lajos   elnöklete alatt      Jegyzők: Hiszéke'
```
#### törzsszöveg
```python
>>> naplo.torzs_szoveg[:200]  
'ELNÖK: (A teremben lévők felállnak, és ezzel köszöntik a választópolgárok közösségét. Amikor az  ülést vezető elnök helyet foglal, a teremben lévők is  leülnek.) Tisztelt Képviselőtársaim! Az Országgy'
```
#### kiadási szám
```python
>>> naplo.szam  
'17'
```
#### parlementi ciklus
```python
>>> naplo.ciklus  
'2022-2026'
```
#### ülés dátuma
```python
>>> naplo.ules_datum  
'2022. június 27.'
```
#### elnök lista
```python
>>> naplo.elnok_lista  
['Kövér László, Jakab István', 'dr. Oláh Lajos']
```
#### jegyző lista  
```python
>>> naplo.jegyzo_lista
['Hiszékeny Dezső', 'Szabó Sándor', 'dr. Szűcs Lajos', 'dr. Vinnai Győző']
```
#### említett törvényjavaslatok 
```python
>>> naplo.torvenyjavaslatok  
['T/286', 'T/287']
```
#### említett határozati javaslatok 
```python
>>> naplo.hatarozati_javaslat_lista  
[]
```
#### kepviselő lista
(nem egyenlő a felszólalók listájával)  
```python
>>> naplo.kepviselo_lista  
['BAKOS BERNADETT', 'BALASSA PÉTER', 'BARKÓCZI BALÁZS', 'BENCZE JÁNOS', 'BERKI SÁNDOR', 'DR. APÁTI ISTVÁN', 'DR. BRENNER KOLOMAN', 'DR. FÓNAGY JÁNOS', 'DR. FÜRJES BALÁZS', 'DR. HARANGOZÓ TAMÁS', 'DR. KERESZTES LÁSZLÓ LÓRÁNT', 'DR. KONCZ ZSÓFIA', 'DR. KÁLLAI MÁRIA', 'DR. LUKÁCS LÁSZLÓ GYÖRGY', 'DR. MELLÁR TAMÁS', 'DR. RÉPÁSSY RÓBERT', 'DR. SIMICSKÓ ISTVÁN', 'DR. VARGA JUDIT', 'DÓCS DÁVID', 'DÖMÖTÖR CSABA', 'DÚRÓ DÓRA', 'FARKAS SÁNDOR', 'FEKETE-GYŐR ANDRÁS', 'FÖLDESI GYULA', 'FÖLDI LÁSZLÓ', 'GY. NÉMETH ERZSÉBET', 'HALÁSZ JÁNOS', 'HEGEDÜS ANDREA', 'HISZÉKENY DEZSŐ', 'JAKAB PÉTER', 'KANÁSZ-NAGY MÁTÉ', 'KOMJÁTHI IMRE', 'KÁLMÁN OLGA', 'MAGYAR LEVENTE', 'MENCZER TAMÁS', 'MIHÁLFFY BÉLA', 'NACSA LŐRINC', 'NÉMETH SZILÁRD ISTVÁN', 'ORBÁN VIKTOR', 'OROSZ ANNA', 'RÉTVÁRI BENCE', 'SEBIÁN-PETROVSZKI LÁSZLÓ', 'SZABÓ REBEKA', 'SZABÓ SÁNDOR', 'TOMPOS MÁRTON KRISTÓF', 'TORDAI BENCE', 'TOROCZKAI LÁSZLÓ', 'TUZSON BENCE', 'TÁLLAI ANDRÁS', 'TÓTH ENDRE', 'UNGÁR PÉTER', 'VAJDA ZOLTÁN', 'VARGA ZOLTÁN', 'VARJU LÁSZLÓ', 'VITÁLYOS ESZTER', 'Z. KÁRPÁT DÁNIEL']
```
#### kepviselői felszólalás szótar
```python
>>> naplo.kepviseloi_felszolalas_szotar  

* kulcsok
naplo.kepviseloi_felszolalas_szotar.keys()
dict_keys(['BAKOS BERNADETT', 'BALASSA PÉTER', 'BARKÓCZI BALÁZS', 'BENCZE JÁNOS', 'BERKI SÁNDOR', 'DR. APÁTI ISTVÁN', 'DR. BRENNER KOLOMAN', 'DR. FÓNAGY JÁNOS', 'DR. FÜRJES BALÁZS', 'DR. HARANGOZÓ TAMÁS', 'DR. KERESZTES LÁSZLÓ LÓRÁNT', 'DR. KONCZ ZSÓFIA', 'DR. KÁLLAI MÁRIA', 'DR. LUKÁCS LÁSZLÓ GYÖRGY', 'DR. MELLÁR TAMÁS', 'DR. RÉPÁSSY RÓBERT', 'DR. SIMICSKÓ ISTVÁN', 'DR. VARGA JUDIT', 'DÓCS DÁVID', 'DÖMÖTÖR CSABA', 'DÚRÓ DÓRA', 'FARKAS SÁNDOR', 'FEKETE-GYŐR ANDRÁS', 'FÖLDESI GYULA', 'FÖLDI LÁSZLÓ', 'GY. NÉMETH ERZSÉBET', 'HALÁSZ JÁNOS', 'HEGEDÜS ANDREA', 'HISZÉKENY DEZSŐ', 'JAKAB PÉTER', 'KANÁSZ-NAGY MÁTÉ', 'KOMJÁTHI IMRE', 'KÁLMÁN OLGA', 'MAGYAR LEVENTE', 'MENCZER TAMÁS', 'MIHÁLFFY BÉLA', 'NACSA LŐRINC', 'NÉMETH SZILÁRD ISTVÁN', 'ORBÁN VIKTOR', 'OROSZ ANNA', 'RÉTVÁRI BENCE', 'SEBIÁN-PETROVSZKI LÁSZLÓ', 'SZABÓ REBEKA', 'SZABÓ SÁNDOR', 'TOMPOS MÁRTON KRISTÓF', 'TORDAI BENCE', 'TOROCZKAI LÁSZLÓ', 'TUZSON BENCE', 'TÁLLAI ANDRÁS', 'TÓTH ENDRE', 'UNGÁR PÉTER', 'VAJDA ZOLTÁN', 'VARGA ZOLTÁN', 'VARJU LÁSZLÓ', 'VITÁLYOS ESZTER', 'Z. KÁRPÁT DÁNIEL'])
  
* kulcs használata
>>> naplo.kepviseloi_felszolalas_szotar["BAKOS BERNADETT"]

['BAKOS BERNADETT (LMP): Köszönöm a szót,  elnök úr. Tisztelt Ház! Tisztelt Államtitkár Asszony!   Az LMP határozati javaslatot nyújtott be a klímabérlet bevezetéséről. Javaslatunk szerint ez a bérlet havi  5 ezer forintba kerülne, *(...)*  köszönöm. (Taps az ellenzéki pártok soraiban.)     ', 'BAKOS BERNADETT (LMP): Köszönöm, a válaszát azonban sajnos *(...)* úgyhogy nem fogadom el a válaszát. (Taps az ellenzéki oldalon.)     ']
```

#### reakció szótar
```python
>>> naplo.reakcio_szotar["BAKOS BERNADETT"]
[['(Taps az ellenzéki pártok soraiban.)'], ['(Taps az ellenzéki oldalon.)']]
```
