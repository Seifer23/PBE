#!/usr/bin/env python

#Importem els ports GPIO i la llibreria MFRC522
import RPi.GPIO as GPIO
from mfrc522 import MFRC522

class Rfid:

    def __init__(self):
        self.lector = MFRC522()
       
    def try_uid(self):
        #Cridant a mètodes de la llibreria MFRC522 intento llegir uid un cop

        (status, TagType) = self.lector.MFRC522_Request(self.lector.PICC_REQIDL)
        if status != self.lector.MI_OK:
            return None
        (status, uid) = self.lector.MFRC522_Anticoll()
        if status != self.lector.MI_OK:
            return None
        return self.uid_to_hex(uid)

    def read_uid(self):
        #Si la crida a uid no ha funcionat, es reintenta fins que funcioni

        uid = self.try_uid()
        while not uid:
            uid = self.try_uid()
        return uid

    def uid_to_hex(self, uid):
        #Reescric el uid resultant en hexadecimal

        n = 0
        for i in range(0,4):
            n = n * 256 + uid[i]
        return hex(n).upper().strip("0X")

    def close(self):
        #Cal tancar els ports GPIO per evitar problemes
        GPIO.cleanup()

if __name__=="__main__":
        rf = Rfid()
        uid = rf.read_uid()
        print(uid)
        rf.close()
