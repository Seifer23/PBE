import threading
import Rfid, Request
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

        #Per tal de poder canviar el layout, creem un stack
        self.stack = Gtk.Stack()
        self.stack.set_transition_duration(0)
        self.add(self.stack)
        self.login_init()
        self.query_init()
        self.stack.set_visible_child_name("login")

        #Inicialitzem el proveïdor de css
        self.css = Gtk.CssProvider()
        self.css.load_from_file(Gio.File.new_for_path("style.css"))
        self.screen = Gdk.Screen.get_default()
        self.context = Gtk.StyleContext()
        self.context.add_provider_for_screen(self.screen, self.css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)  

        self.req = Request.Request()


    def login_init(self):

        self.lector = Rfid.Rfid()
        self.login_box = Gtk.Box(orientation = "vertical")
        self.login_box.get_style_context().add_class("login-box")

        #Etiqueta del UID
        self.login_label_box = Gtk.Box()
        self.login_label_box.get_style_context().add_class("login-label-box")
        self.login_label = Gtk.Label(label = "Please, login with your university card")
        self.login_label.get_style_context().add_class("login-label")
        #self.login_label.set_line_wrap(True)
        self.login_label.set_size_request(300, 100)
        self.login_label_box.set_center_widget(self.login_label)
        self.login_box.add(self.login_label_box)
        self.stack.add_named(self.login_box, "login")
        
        #Thread del lector
        self.lector_thread = threading.Thread(target = self.login_scan)
        self.lector_thread.daemon = True
        self.lector_thread.start()

    def query_init(self):

        self.name = "Placeholder"
        self.query_box = Gtk.Box(orientation = "vertical")
        self.stack.add_named(self.query_box, "query")  
         
        self.query_username_box = Gtk.Box()
        self.query_username_box.set_border_width(4)
        self.query_username_label = Gtk.Label()
        self.query_username_box.pack_start(self.query_username_label, False, False, 0)
        self.query_username_box.pack_start(Gtk.Label(), True, True, 0)
        self.query_box.pack_start(self.query_username_box, False, False, 0)

        self.query_logout_button = Gtk.Button(label = "Logout")
        self.query_logout_button.connect("clicked", self.query_logout)
        self.query_username_box.pack_end(self.query_logout_button, False, False, 0)

        self.query_input = Gtk.Entry()
        self.query_box.pack_start(self.query_input, False, False, 0)
        self.query_input.connect("activate", self.query_process)

        self.query_table_window = Gtk.ScrolledWindow()
        self.query_table_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.query_table_type = Gtk.Label()
        self.query_box.pack_start(self.query_table_type, False, False, 0)
        self.query_table_window.hide()
        self.query_table = Gtk.TreeView()
        self.query_table.set_model(Gtk.ListStore())
        self.query_table_window.add(self.query_table)

        self.query_box.pack_start(self.query_table_window, True, True, 15)

#******************************************************************
#****** FUNCIONS relacionades amb la pantalla de demanar UID ******
#******************************************************************

    def login_clear(self, widget):
       
        #Evitem que el botó faci res si encara no s'ha llegit cap targeta
        if not self.lector_thread.is_alive():
            self.login_label.set_label("Please, login with your university card")

            #Tornem a iniciar el thread
            self.lector_thread = threading.Thread(target = self.login_scan)
            self.lector_thread.start()

    def login_scan(self):

        self.uid = self.lector.scan_uid()
        GLib.idle_add(self.login_print, self.uid)

    def login_print(self, uid):

        self.login_label.set_label("UID: " + self.uid)
        self.aux_thread = threading.Thread(target = self.login_login)  
        self.aux_thread.daemon = True
        self.aux_thread.start()
    def login_login(self):

        self.name = self.req.login(self.uid);
        GLib.idle_add(self.login_processor, self.name)

    def login_processor(self,login_information): 
        
        if(self.name is None):
            self.login_label.set_label("User not registered")

            self.lector_thread = threading.Thread(target = self.login_scan)
            self.lector_thread.start()  

        else:
            self.stack.set_visible_child_name("query") 
            self.query_username_label.set_markup(f"<span foreground='black'>Welcome</span><span foreground='blue'> {self.name}</span>")

#**********************************************************************            
#***** FUNCIONS RELACIONADES AMB LA PANTALLA UN COP INICIAT SESSIÓ*****
#**********************************************************************

    def query_logout(self, widget):
        
        self.login_label.set_label("Please, login with your university card")
        self.aux_thread = threading.Thread(target = self.req.logout)
        self.aux_thread.start()
        self.stack.set_visible_child_name("login")

        self.lector_thread = threading.Thread(target = self.login_scan)
        self.lector_thread.start()

    def query_process(self, widget):

       query = widget.get_text()
       self.aux_thread = threading.Thread(target = self.query_get, args=(query,))
       self.aux_thread.start()

    def query_get(self, query):

        data = self.req.get(query)
        GLib.idle_add(self.query_data_display, data, query)

    def query_data_display(self, data, query):

        self.query_table.get_model().clear()
        self.query_table_type.show()
        for col in self.query_table.get_columns():
            self.query_table.remove_column(col)
        if  data is None:

            self.query_table_type.set_label("This table doesn't exist")

        elif len(data) == 0:

            self.query_table_type.set_label("No elements in table table")

        else:

            self.query_table_type.set_label("table")
            column_names = list(data[0].keys())
            model = Gtk.ListStore(*[str] * len(column_names))
            self.query_table.set_model(model)
            for i, column_name in enumerate(column_names):
                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(column_name, renderer, text=i)
                self.query_table.append_column(column)
    
            for item in data:
                row = [str(item.get(col, "")) for col in column_names]
                model.append(row)

        print(data)

    def close(self, widget):
        
        self.lector.lector.close()
        Gtk.main_quit()
        

if __name__ == "__main__":
    

    win = Finestra()
    win.show_all()
    Gtk.main()

