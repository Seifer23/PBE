# Code by Simon Monk https://github.com/simonmonk/ and modified

from mfrc522 import MFRC522
import RPi.GPIO as GPIO
  
class SimpleMFRC522:

  READER = None
  
  KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
  BLOCK_ADDRS = [8, 9, 10]
  
  def __init__(self):
    self.READER = MFRC522()
  
  def read(self):
      id, text = self.read_no_block()
      while not id:
          id, text = self.read_no_block()
      return id, text

  def read_id(self):
    id = self.read_id_no_block()
    while not id:
      id = self.read_id_no_block()

    if len(id) == 7:
        return str(id) + "0"
    return id

  def read_id_no_block(self):
      (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None
      (status, uid) = self.READER.MFRC522_Anticoll()
      if status != self.READER.MI_OK:
          return None
      return self.uid_to_hex(uid).upper()
      
  def uid_to_hex(self, uid):
      n = 0
      for i in range(0, 4):
          n = n * 256 + uid[i]
      return hex(n).upper().strip("0X")


  def close(self):
      GPIO.cleanup()
