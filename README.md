# Numeerisen datan visualisointikirjasto
## 1. Ohjelman rakennesuunnitelma
Ohjelmakirjasto on rakenteeltaan kaksiosainen. Prosessoiva osa laskee annetun datan ja käsittelee sen olioiksi ja listoiksi. Tämä osa tarkistaa tiedoston soveltuvuuden, järjestää sitä tarvittaessa, määrittää kuvaajan akselit ja lähettää datan visualisoivalle osalle.
Visualisoiva osa piirtää halutun tyyppisen kuvaajan uuteen ikkunaan. Tässä ikkunassa on vielä mahdollista säätää kuvaajaa mm. valitsemalla onko grid käytössä, zoomaamalla, tai lukemalla arvoja graafista.

Keskeisiä metodeja: Luokka: GraphData  Metodi: add_data: Lisää datapisteen
- Metodi: sort_data: Järjestää get_datan mukaisen listan alkiot järjestykseen xakselilla
- Metodi: get_data: Palauttaa listan kaikista graafin datapisteistä
Luokka: Point
- Metodi: get_graph: Palauttaa GraphDatan johon point kuuluu
Luokka: Graph
- Metodi: get_type: Palauttaa graafin tyypin (piirakka, pylväs, viiva jne.)
- Metodi: add_graphdata: Lisää graafille sen datajoukon
- Metodi: get_graphdata: Palauttaa graafin datan
- Metodi: set_dimensions: Valitsee oikean skaalauksen akseleille datan mukaan
- Metodi: draw_data: Piirtää datan
Luokka: VisualData  Metodi: draw_graph: Avaa uuden ikkunan johon graafi piirretään
- Metodi: draw_grid: Piirtää gridin
- Metodi: save_graph: Tallentaa näkymän kuvaksi
Luokka: file_IO
- Metodi: read_data: Lukee käyttäjän antamana tiedoston datan

## 2. Käyttötapakuvaus
Käyttäjä voi hyödyntää ohjelmakirjastoa joko ajamalla sen suoraan komentoriviltä (import) tai sitten lisäämällä sen omaan ohjelmaansa tai python koodiinsa (import NumVisMega). Käyttäjä on keränny numeerista dataa oikeassa formaatissa johonkin tiedostoon, jonka polun se antaa kutsuessaan kirjaston visualisointifunktiota. Samassa kutsussa käyttäjä myös määrittää datan tyypin, eli sen minkälaisen kuvaajan hän siitä haluaa. Kutsun jälkeen ohjelmakirjasto lukee ja käsittelee datan ja piirtää sen mukaisesti kuvaajan.
Kuvaaja piirtyy uuteen ikkunaan, josta käyttäjä voi lukea sitä käyttämällä esimerkiksi datakursoria. Ikkunassa on painikkeet gridin näyttämiselle tai piilottamiselle ja kuvan tallentamiselle kuvaformaatissa. Käyttäjä voi myös vaikuttaa näkymään käyttämällä komentoikkunaa.
Graafin ikkunasta voidaan myös vaihtaa datatiedostoa, jolloin ohjelmakirjasto piirtää samaan ikkunaan uuden kuvan.


## 3. Algoritmit
”Plot”
1. Käyttäjän datan lukeminen
- File_IO lukee käyttäjän antaman tiedoston rivi kerrallaan ja muodostaa näistä kaksi listaa, yhden molemmille akseleille.
- Yksi rivi on muotoa ”x-koordinaatti : y-koordinaatti” tai ”selite :  arvo”
2.  Käyttäjän datan käsittely
- File_IO lisää jokaista ”x, y” tuplea kohden yhden point olion
- X-akseli järjestetään sort-komennolla
3. Datan visualisointi
- PyQt5 piirtää oikeanmallisen kuvaajan uuteen ikkunaan
Pie-chart:
Laskee jokaisen palan koon ja osuuden ympyrästä.  
- Osuus: arvo / kaikkien_arvojen_summa
- Palan koko: 2*pi*osuus
Bar-chart:
- Laskee jokaisen pylvään kannan:
Graph_size:
- Graafin ääriarvot lasketaan luetun datan suurimpien ja pienimpien arvojen mukaan:
- Maksimiarvon mukaan pyöristetään seuraavaan tasalukuun
- Minimiarvon mukaan pyöristetään edelliseen tasalukuun
4. Visualisoinnin muokkaus/tallennus
- Ikkunan valinnoista voidaan joko piilottaa tai näyttää gridi
- Ikkunan valinnoista voidaan tallentaa graafi kuvana


## 4. Tietorakenteet
Ohjelmakirjasto ei vaadi mitään erityisiä itse ohjelmoitavia tietorakenteita, lähinnä dynaamisia rakenteita.
Käyttäjän antamasta tiedostosta luetut datapisteet tallennetaan omiksi olioikseen, jotka tallennetaan yksiulotteiseen listaan. Tämä lista kuuluu luotuun Graph olioon, johon kuuluu myös akseleiden pituudet omana listanaan.
Mikäli käyttäjä tahtoo tallentaa saamansa grafiikan, tallentaa ohjelmakirjasto sen hänelle jpg tai png formaatissa.
## 6. Aikataulu

Ohjelmakirjaston tarkemmassa suunnittelussa pyritään noudattamaan top-down – lähestymistapaa ja toteutuksessa bottom-up – lähestymistapaa. Toteutuksen aikana eri moduuleita pyritään yksikkötestaamaan.
Tarkempi aikataulu 24.2 – 15.3 Algoritmien ja tiedostonkäsittelyn rakentamista
- Tiedostonkäsittely
- Datankäsittely
- Prosessoivan puolen testaus
16.3 – 24.3 Visualisoinnin rakentamista
- PyQt5
- Ikkunan luominen, datan visualisointi
- Ulkoasun silmämääräinen testaus
25.3 - 5.4 Yksikkötestausta
6.4 - 24.4 kaiken mahdollisen hiominen ja testaaminen, sekä dokumentointi
### Arvio ajankäytöstä
Algoritmien ja tiedostonkäsittelyn toteuttaminen   30h
Prosessoivan osan testaaminen ja korjaaminen   10h
Visualisoivan osan toteuttaminen    30h
Viimeistely, testaaminen ja korjaaminen   20h
Dokumentointi      10h
YHTEENSÄ:      100h

## 7. Yksikkötestaussuunnitelma
Yksikkötestauksessa painopiste on prosessoivan osan testaamisella. Testattavia asioita ovat tiedostonluku ja käsittely, sekä olioiden ja kuvan parametrien luominen. Testaaminen tulee tapahtumaan syöttämällä erilaista dataa ohjelmaan ja tarkistamalla ohjelman toiminnan olevan tarkoituksenmukaista.
Tiedoston lukeminen testataan syöttämällä virheellisiä tiedostoja ohjelmaan. Näistä ohjelma joko nostaa virheilmoituksen ja keskeyttää toimintansa, tai sitten ohittaa viallisen datapisteen, mutta ilmoittaa siitä.
Datan muotoilu tarkistetaan testaamalla että syötetty data on oikeassa formaatissa. Jos tiedosto ei ole järjestetty, järjestää kirjasto x-akselin järjestykseen.  Voidaan testata virheellisellä x-akselilla.
Akselien skaalaus testataan syöttämällä erikoisia ääritapauksia sisältäviä arvoja ohjelmaan.  Näistä ohjelman tulee tehdä informatiivinen ja standardien mukainen kuvaaja.
Selitteiden piirtäminen testataan antamalla erikoismerkkisiä ja eripituisia selitteitä.  Näistä ohjelman tulee piirtää oikeanlainen ”string” graafiseen ikkunaan.  Piirtäminen taas tutkitaan antamalla ääriarvoja tai monia pisteitä.
