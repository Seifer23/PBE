import threading #Threads
import Rfid #Llibreria del Puzzle 1
import gi #

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio, GLib #llibreries de Gtk

class Finestra(Gtk.Window):

    def __init__(self):

        #Assignem el lector Rfid a self.lector
        self.lector = Rfid.Rfid() 

        #Inicialitzem el proveïdor de css
        self.css = Gtk.CssProvider()
        self.css.load_from_file(Gio.File.new_for_path("style.css"))
        self.screen = Gdk.Screen.get_default()
        self.context = Gtk.StyleContext()
        self.context.add_provider_for_screen(self.screen, self.css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        #Propietats de la finestra
        Gtk.Window.__init__(self, title = "Puzzle2")
        Gtk.Window.set_size_request(self, 300, 50)
        self.connect("destroy", self.close)
        self.set_resizable(False)

        #Caixa principal
        self.box = Gtk.Box(orientation = "vertical")
        self.add(self.box)

        #Caixa que conté el uid
        self.uid_box = Gtk.Box()
        self.uid_box.set_border_width(5)
        self.uid_box.get_style_context().add_class("uid-box")
        self.uid_box.get_style_context().add_class("uid-box-blue")
        self.uid_label = Gtk.Label(label = "Please, login with your university card")
        self.uid_label.set_size_request(300, 50)
        self.uid_label.set_line_wrap(True)
        self.uid_box.add(self.uid_label)

        #Botó
        self.clear_btn = Gtk.Button(label = "Clear")
        self.clear_btn.connect("clicked", self.clear_uid)
        
        #Afegim tot a la capxai principal
        self.box.add(self.uid_box)
        self.box.add(self.clear_btn)

        #Thread del lector
        self.thread = threading.Thread(target = self.scan_uid)
        self.thread.daemon = True
        self.thread.start()

    def clear_uid(self, widget):

        #Evitem que el botó faci res si encara no s'ha llegit cap targeta
        if not self.thread.is_alive():
            self.uid_label.set_label("Please, login with your university card")
            self.uid_box.get_style_context().add_class("uid-box-blue")
            self.uid_box.get_style_context().remove_class("uid-box-red")
            
            #Tornem a iniciar el thread
            self.thread = threading.Thread(target = self.scan_uid)
            self.thread.start()

    def scan_uid(self):

        uid = self.lector.scan_uid()
        GLib.idle_add(self.print_uid, uid)

    def print_uid(self, uid):

        self.uid_label.set_label("UID:" + uid)
        self.uid_box.get_style_context().add_class("uid-box-red")
        self.uid_box.get_style_context().remove_class("uid-box-blue")

    def close(self, widget):

        self.lector.lector.close()
        Gtk.main_quit()

win = Finestra()
win.show_all()
Gtk.main()
