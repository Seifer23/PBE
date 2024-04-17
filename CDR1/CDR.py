import threading
import Rfid
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio, GLib

class Finestra(Gtk.Window):

    def __init__(self):

        #Window Initialization
        Gtk.Window.__init__(self, title = "Critical Design Review")
        Gtk.Window.set_size_request(self, 1000, 700)
        self.set_resizable(False)
        self.connect("destroy", self.close)
        self.prompt_init()
        
        #Inicialitzem el proveïdor de css
        self.css = Gtk.CssProvider()
        self.css.load_from_file(Gio.File.new_for_path("style.css"))
        self.screen = Gdk.Screen.get_default()
        self.context = Gtk.StyleContext()
        self.context.add_provider_for_screen(self.screen, self.css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)  

    def prompt_init(self):

        self.lector = Rfid.Rfid()
        self.login_box = Gtk.Box(orientation = "vertical")
        self.login_box.get_style_context().add_class("login-box")
        self.add(self.login_box)
        self.login_box.show()

        #Etiqueta del UID
        self.login_label_box = Gtk.Box()
        self.login_label_box.get_style_context().add_class("login-label-box")
        self.login_label = Gtk.Label(label = "Please, login with your university card")
        self.login_label.get_style_context().add_class("login-label")
        #self.login_label.set_line_wrap(True)
        self.login_label.set_size_request(300, 100)
        self.login_label_box.set_center_widget(self.login_label)
        self.login_box.add(self.login_label_box)
        
        #Thread del lector
        self.login_thread = threading.Thread(target = self.login_scan)
        self.login_thread.daemon = True
        self.login_thread.start()

    def login_clear(self, widget):
       
        #Evitem que el botó faci res si encara no s'ha llegit cap targeta
        if not self.login_thread.is_alive():
            self.login_label.set_label("Please, login with your university card")

            #Tornem a iniciar el thread
            self.login_thread = threading.Thread(target = self.login_scan)
            self.login_thread.start()

    def login_scan(self):

        self.uid = self.lector.scan_uid()
        GLib.idle_add(self.login_print, self.uid)

    def login_print(self, uid):

        self.login_label.set_label("UID: " + uid)
    
    def login_login(self, widget):

        #TODO: Fer login al server amb PHP
        #si funciona el login cal amagar el login_layout i obrir el 
        #query_layout amb les funcions layout.show() i layout.hide()
        print("Do not call this function, WIP")

    def close(self, widget):
        
        self.lector.lector.close()
        Gtk.main_quit()

if __name__ == "__main__":
         
    win = Finestra()
    win.show_all()
    Gtk.main()

