# Projekt zespołowy: __Stacja pogodowa__

Skład grupy:
- Rafał Jaworski
- Jarosław Kot
- Przemysław Wojda
- Mikołaj Szmajdziński

## Opis
System stacji pogodowej oparty o czujniki temperatury, wilgotności, ciśnienia przedstawiający te dane na stronie internetowej będącej progresywną aplikacją webową. **W aktualnej konfiguracji system działa na adresie: 172.20.10.2**.

## Wykorzystane technologie:
- npm
- framework Vue.js z pluginem Axios
- webpack
- [PWA (Progressive Web App)](https://web.dev/what-are-pwas/)
- SQLite3
- Flask (REST API)

## Wykorzystane czujniki oraz komponenty
- Raspberry Pi
- DHT22
- PMS5003
- BMP280

## Instalacja wymaganych paczek pythona
    Stacja_pogodowa/pip3 install -r paczki.txt

## Skrypt uruchamiający cały system
    Stacja_pogodowa/chmod+x run.sh
    Stacja_pogodowa/./run.sh

## Uruchamianie wersji testowej aplikacji/strony
_Wymaga repozytorium npm_

_W przypadku Linuxa:_

    sudo apt-get install npm

[_W przypadku Windowsa_](https://nodejs.org/en/download/)

Uruchamianie branch'a testowego:

    PWA/npm run dev

## Uruchamianie sererwa REST
    REST/python3 server.py
## Uruchamianie symulacji wyników
    SensorParser/python3 sensor_parser.py
