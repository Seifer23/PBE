#!/usr/bin/env python

#Importem els ports GPIO i la llibreria mfrc522
import RPi.GPIO as GPIO
import SimpleMFRC522

class Rfid:

    def __init__(self):
        self.lector = SimpleMFRC522.SimpleMFRC522()

    def scan_uid(self):
        uid = self.lector.read_id()
        return uid
    
if __name__=="__main__":

        rf = Rfid()
        uid = rf.scan_uid()
        print(uid)
        rf.lector.close()
