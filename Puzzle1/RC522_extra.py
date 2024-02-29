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

    def scan(self):
        try:
            lector = SimpleMFRC522()
            id, text = lector.read()
        finally: GPIO.cleanup()
        return hex(id).upper(), text

    def write(self, text):
        try:
            lector = SimpleMFRC522()
            print("Place your tag on the sensor")
            lector.write(text)
            print("Data has been written to the tag")
        finally: GPIO.cleanup()

if __name__=="__main__":

        rf = RfidRc522()
        uid = rf.scanUid()
        print(uid)
