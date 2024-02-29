# Memoria Puzzle 1 PBE

## Introducció

L'objectiu d'aquest puzzle és aconseguir la conexió entre la raspberry pi i el lector RFID.

## Connexió

Per aconseguir connectar el lector RFID-RC522 a la Raspberry Pi hem de connectar els pins corresponents a la Raspberry Pi.

| **PIN RFID** | Pin Raspberry | Funció                                          |
|:------------:|:-------------:|:----------------------------------------------- |
| SDA          | Pin 24        | Serial Data Line                                |
| SCK          | Pin 23        | Serial Clock                                    |
| MOSI         | Pin 19        | Master Out Slave In, enviar data al mòdul RFID  |
| MISO         | Pin 21        | Master In Slave Out, enviar data a la Raspberry |
| GND          | Pin 6         | Cable ground                                    |
| RST          | Pin 22        | Reset                                           |
| 3.3V         | Pin 1         | Power Supply                                    |

<img title="" src="file:///C:/Users/salva/AppData/Roaming/marktext/images/2024-02-26-18-27-28-GPIO-Pinout-Diagram-2.png" alt="" width="507" data-align="center">

Un cop connectat el lector a la Raspberry Pi, hen de centrar-nos en la raspberry pi per completar la connexió. 

Per poder comunicar-nos amb el lector, hem de configurar la Raspberry Pi per fer servir el bus spi. Per tal de fer això, hem de connectar-nos via _SSH_ a la placa i fer servir el commandament:

```bash
sudo raspi_config
```

I un cop al menú hem de navegar fins a l'opció de _Interface Options_, i un cop dins d'aquesta opció activar el mòdul SPI.

<img title="" src="file:///C:/Users/salva/AppData/Roaming/marktext/images/2024-02-26-18-33-15-image.png" alt="" width="481" data-align="center"><img title="" src="file:///C:/Users/salva/AppData/Roaming/marktext/images/2024-02-26-18-34-43-image.png" alt="" width="481" data-align="center">

Un cop activat el mòdul cal reiniciar la placa.

```bash
sudo reboot
```

<div style="page-break-after: always;"></div>

Ara la placa ja es pot comunicar amb el lector, però per poder programar la seva funció hem d'instalar paquets a la raspberry pi:

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-dev python3-pip python3-venv
```

| Nom              | Funció                                                          |
|:---------------- | --------------------------------------------------------------- |
| **python3-dev**  | Llibreries necessàries per programar i compilar el fitxer _.py_ |
| **python3-pip**  | Instalador de paquets de Python                                 |
| **python3-venv** | Paquet per generar entorns virtuals de Python                   |
| **spidev**       | Llibreria de python que controla les comunicacions en SPI       |
| **mfrc522**      | Llibreria per controlar el lector RFID-RC522                    |

Amb aquests paquets instalats, ara només ens falta iniciar l'entorn virtual on programarem aquest puzzle.

```bash
mkdir PBE
cd PBE
python3 -m venv env
source env/bin/activate
```

I un cop dins d'aquest entorn virtual podem instal·lar els paquets de python que farem servir per comunicar-nos amb el lector.

```bash
sudo pip3 install spidev
sudo pip3 install mfrc522
```

| Nom         | Funció                                                    |
|:----------- | --------------------------------------------------------- |
| **spidev**  | Llibreria de python que controla les comunicacions en SPI |
| **mfrc522** | Llibreria per controlar el lector RFID-RC522              |

<div style="page-break-after: always;"></div>

## Programa

Aquest codi permet a la Raspberry pi llegir el UID de la targeta

```python
#!/usr/bin/env python

#Importem els ports GPIO i la llibreria mfrc522
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class RfidRc522:

    def scanUid(self):
        lector = SimpleMFRC522()
        uid = lector.read_id()
        hexUid = hex(uid).upper()
        return hexUid

if __name__=="__main__":
#cal posar el codi dins de l'estructura try-finally per executar
#GPIO.cleanup() per evitar problemes amb altres programes
    try:
        rf = RfidRc522()
        uid = rf.scanUid()
        print(uid.strip("0X"))
    finally:
        GPIO.cleanup()
```

<div style="page-break-after: always;"></div>

## Lectura del contingut i escriptura

Aquest lector permet molt més que llegir el _UID_ de les targetes, també permet escriure contingut en les targetes.

Per tal de fer això, podem augmentar la classe RfidRc522:

```python
class RfidRc522:

    def scanUid(self):
        lector = SimpleMFRC522()
        uid = lector.read_id()
        hexUid = hex(uid).upper()
        return hexUid

    def scan(self):
        lector = SimpleMFRC522()
        id, text = lector.read()
        return id, text

    def write(self, text):
        lector = SimpleMFRC522()
        print("Place your tag on the sensor")
        lector.write(text)
        print("Data has been written to the tag")
```

Amb aquesta definició de la classe ja podem realitzar les dues funcions bàsiques de la targeta.
