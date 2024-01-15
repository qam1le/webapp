# Vietų atpažinimo ir atvaizdavimo web aplikacija

Django WEB aplikacija su CRUD funkcionalumu, autentifikacija. 
Pagrindinis funkcionalumas:
- Nuotraukų valdymas (įkėlimas, koregavimas, pašalinimas, paieška, koordinačių ištraukimas iš metaduomenų + Vision AI vietovės spėjimas + charakteristikos sąrašo grąžinimas)
- Žemėlapių valdymas (sukūrimas, peržiūra, pašalinimas)

## Sukurta naudojant

|   |   |
| ------ | ------ |
| Django | atvirojo kodo karkasas, palengvinantis web kūrimą naudojant Python kalbą (papildomai, nuolatos yra išleidžiami saugumo atnaujinimai - mažesnė žmogiškų klaidų tikimybė, didesnis saugumas) |
| Bootstrap | CSS dizaino kūrimas, pritaikomumas įvairiems ekrano dydžiams |
| MySQL | duomenų bazė |
| Vision AI | nuotraukų analizei naudojamas mašininis modelis (koordinatės pagal didžiausią pasitikėjimo indeksą turintį objektą (angl. The Confidence Score) ir charakteristikų sąrašo grąžinimas (angl. labels), kurie naudojami nuotraukų filtravimui |

## Paleidimas lokalioje mašinoje

Išankstiniai reikalavimai: Python, Django, MySQL (paleidimui galima naudoti XAMPP)

config turėtų leisti nuskaityti failus esančius .env faile. (jį reikia sukurti ir palikti pagrindinėje projekto direktorijoje). Esant problemoms, galima pakeisti config() su reikiamomis tekstinių eilučių reikšmėmis (t.y. pvz.: ALLOWED_HOSTS =  [config('ALLOWED_HOSTS')] į ALLOWED_HOSTS = ['127.0.0.2'])

Papildomai: pakeisti settings.py failo konfigūracijas, kaip ALLOWED_HOSTS, 
Reikia sukurto Django projekto, tuomet reikia paleisti virtualią aplinką (environment), tai galima padaryti per konsolę (CMD):

```sh
cd Scripts
activate
```
Reikia patekti į pačios programos direktoriją, kur yra manage.py failas:
```sh
cd webapp
```

Svarbu parsisiųsti ir įrašyti projektui reikalingas bibliotekas, tai galima padaryti:
```sh
pip install -r requirements. txt
```

Esant paleistai duomenų bazei (naudojant XAMPP, Apache+MySQL), jos užpildymas pagal models.py:

```sh
python manage.py migrate
python manage.py makemigrations
```

Galiausiai, galima paleisti pačią Django aplikaciją:
```sh
python manage.py runserver 127.0.0.2
```
IP adresas gali būti betkuris localhost adresas, svarbu jį pakeisti settings.py faile.

Aplikacija turėtų pasileisti ir veikti.
