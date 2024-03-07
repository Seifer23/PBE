#!/usr/bin/env python

#Importem els ports GPIO i la llibreria mfrc522
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class RfidRc522:
    def __init__(self):
        self.lector = SimpleMFRC522()
        
    def scanUid(self):
        try:
            uid = self.lector.read_id()
        finally: GPIO.cleanup()
        return hex(uid).upper().strip("0X")

if __name__=="__main__":

        rf = RfidRc522()
        uid = rf.scanUid()
        print(uid)
