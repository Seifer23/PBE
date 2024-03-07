import threading
import RfidRc522
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class FinestraP2(Gtk.Window):

    def __init__(self):

        #Creem la finestra
        Gtk.Window.__init__(self, title = "Puzzle2")
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(5)
        self.set_resizable(False)

        #Caixa que conté els dos widgets
        
        self.box = Gtk.Box(orientation = "vertical", spacing = 20)
        self.add(self.box)
        
        ##Caixa que conté el label del uid (ho faig per organitzar la finestra)
        self.uidBox = Gtk.Box(spacing = 20)
        self.uidLabel = Gtk.Label(label = "Place the tag on the sensor")
        self.uidBox.pack_start(self.uidLabel, True, True, 0)
         
        #Caixa que conté els dos botons (clear i el botó temporal de close)
        #TODO: Eliminar la caixa abans de presentar
        
        self.btnBox = Gtk.Box()
        
        self.closeBtn = Gtk.Button(label = "Close")
        self.closeBtn.connect("destroy", Gtk.main_quit)
        self.clearBtn = Gtk.Button(label = "Clear")
        self.clearBtn.connect("clicked", self.clear_uid)

        self.btnBox.pack_start(self.clearBtn, True, True, 0)
        self.btnBox.pack_start(self.closeBtn, True, True, 0)

        ##Afegim les subcaixes dins de la caixa principal
        self.box.pack_start(self.uidBox, True, True, 0)
        self.box.pack_start(self.btnBox, True, True, 0)
        
        ##Threading
        thread = threading.Thread(target = self.printUid)
        thread.setDaemon(True)
        thread.start()

    def clear_uid(self, widget):
        self.uidLabel.set_label("Place the tag on the sensor")
        thread = threading.Thread(target = self.printUid)
        thread.start()

    def printUid(self):
        lector = RfidRc522.RfidRc522()
        uid = lector.scanUid()
        self.uidLabel.set_label(uid)

win = FinestraP2()
win.show_all()
Gtk.main()
