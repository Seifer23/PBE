import threading
import Rfid
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class FinestraP2(Gtk.Window):

    def __init__(self):
        self.lector = Rfid.Rfid()

        #Creem la finestra
        Gtk.Window.__init__(self, title = "Puzzle2")
        Gtk.Window.set_default_size(self, 300,50)
        self.connect("destroy", self.close)
        self.set_border_width(5)
        self.set_resizable(False)

        #Caixa que conté els dos widgets
        
        self.box = Gtk.Box(orientation = "vertical")
        self.add(self.box)
        
        ##Caixa que conté el label del uid (ho faig per organitzar la finestra)
        self.uidBox = Gtk.EventBox()
        self.uidLabel = Gtk.Label(label = "\nPlace the tag on the sensor\n")
        #self.uidBox.pack_start(self.uidLabel, True, True, 0)
        self.uidBox.add(self.uidLabel)

        #Caixa que conté els dos botons (clear i el botó temporal de close)
        #TODO: Eliminar la caixa abans de presentar
        
        self.btnBox = Gtk.Box()
        
        self.clearBtn = Gtk.Button(label = "Clear")
        self.clearBtn.connect("clicked", self.clear_uid)
        self.btnBox.pack_start(self.clearBtn, True, True, 0)

        ##Afegim les subcaixes dins de la caixa principal
        self.box.pack_start(self.uidBox, True, True, 0)
        self.box.pack_start(self.btnBox, True, True, 0)
        
        ##Threading
        self.thread = threading.Thread(target = self.scan_uid)
        self.thread.daemon = True
        self.thread.start()
    
    #funció que reinicia el thread per llegir el uid
    def clear_uid(self, widget):
        if not self.thread.is_alive():
            self.uidLabel.set_label('\nPlace the tag on the sensor\n')
            self.thread = threading.Thread(target = self.scan_uid)
            self.thread.start()

    #funció que crida el thread
    def scan_uid(self):
        uid = self.lector.scan_uid()
        self.uidLabel.set_label("\n" + uid + "\n")

    #funció que tanca la finestra (lligada a "destroy")
    def close(self, widget):
        self.lector.lector.close()
        Gtk.main_quit()
    

win = FinestraP2()
win.show_all()
Gtk.main()
