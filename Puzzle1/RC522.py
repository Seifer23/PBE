#!/usr/bin/env python

#Importem els ports GPIO i la llibreria mfrc522
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class RfidRc522:

    def scanUid(self):
        try:
            lector = SimpleMFRC522()
            uid = lector.read_id()
            hexUid = hex(uid).upper()
        finally: GPIO.cleanup()
        return hexUid.strip("0X")

if __name__=="__main__":

        rf = RfidRc522()
        uid = rf.scanUid()
        print(uid)
