# Memòria Puzzle 2 PBE

## Introducció

L'objectiu d'aquesta pràctica és desenvolupar una versió gràfica del puzzle anterior.

![](../.mdAssets/window1.png)
![](../.mdAssets/window2.png)

## Llibreries Necessàries

Per poder treballar amb el paquet de python de `PyGObject`  ens cal instal·lar aquests requisits:

```bash
sudo apt install libgirepository1.0-dev gcc libcairo2-dev 
sudo apt install pkg-config python3-dev gir1.2-gtk-4.0
```

| Nom                        | Funció                                                 |
| -------------------------- | ------------------------------------------------------ |
| **libgirepository1.0-dev** | Fitxers de desenvolupament per a GObject               |
| **gcc**                    | Compiladors GNU, utilitzada per compilar programes     |
| **libcairo2-dev**          | Conjunt de llibreries per a la llibreria gràfica Cairo |
| **pkg-config**             | Paquet per controlar la compilació de paquets          |
| **python3-dev**            | Fitxers de desenvolupament per a Python 3              |
| **gir1.2-gtk-4.0**         | Requeriment per la llibreria GTK 4.0                   |

`gcc` i `pkg-config` són llibreries que són necessàries per a compilar els paquets que instalarem amb `pip`.

```bash
pip3 install pycairo
pip3 install PyGObject
```

| Nom       | Funció                                                                    |
| --------- | ------------------------------------------------------------------------- |
| Pycairo   | Llibreria que implementa la funcionalitat de la llibreria Cairo en Python |
| PyGObject | Llibreria que implementa la funcionalitat de la llibreria GObject         |

## Programa

#### Imports

```python
import threading
import Rfid
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio 
```

En aquest fragment del programa importo les dependències necessàries per el programa.

| Nom           | Funció                                                                                                                                                                                                                                                                                                                                                 |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| threading     | Implementa la funcionalitat de thread, per poder executar la funció bloquejant del lector de targeta del Puzzle 1                                                                                                                                                                                                                                      |
| Rfid          | Importem el Puzzle 1 com a llibreria per poder fer crides a les funcions                                                                                                                                                                                                                                                                               |
| gi            | Llibreria GObject, controla l'entorn gràfic                                                                                                                                                                                                                                                                                                            |
| Gtk, Gdk, Gio | `Gtk`  és una llibreria per crear l'interfície d'usuari, essencial per tot el projecte       `Gdk`  és una llibreria imprescindible per desenvolupament d'interfícies gràfiques en python, usat per modificar el color de l'etiqueta en el nostre cas                                `Gio` és una llibreria que controla les operacions de input/outpu |

<div style="page-break-after: always;"></div>

#### \_\_init\_\_

El codi principal de la funció és un codi molt senzill. Simplement creem un objecte de la classe finestra i el mostrem en pantalla fent servir tres línies.

```python
class Finestra(Gtk.Window): 

    def __init__(self): ...

    def clean_uid(self, widget): ...

    def scan_uid(self): ...

    def close(self, widget): ...

win = Finestra()
win.show_all()
Gtk.main()
```

La major part del codi recau en aquesta part de crear un objecte de classe finestra. La funció `__init__` . Per tal d'elaborar en aquesta funció, la trencaré per parts

#### \_\_init\_\_: Rfid i CSS

```python
#Assignem el lector Rfid a self.lector
self.lector = Rfid.Rfid() 

#Inicialitzem el proveïdor de css
self.css = Gtk.CssProvider()
self.css.load_from_file(Gio.File.new_for_path("style.css"))
self.screen = Gdk.Screen.get_default()
self.context = Gtk.StyleContext()
self.context.add_provider_for_screen(self.screen, self.css, 
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
```

**Rfid:** Per poder treballar amb les funcions del Puzzle1, cal definir un objecte de la classe Rfid. L'hem definit a `self.lector`

**CSS**: Part del projecte era implementar que el fons del text de la finestra canvii de color. Amb aquesta idea, creem una variable `Gtk.CssProvider()` i fent servir `Gio.File.new_for_path()` li carrego el fitxer .css que inclou l'estil que vull implementar. 

<div style="page-break-after: always;"></div>

#### _\_init_\_: Propietats de la finestra

```python
Gtk.Window.__init__(self, title = "Puzzle2")
Gtk.Window.set_size_request(self, 300, 50)
self.connect("destroy", self.close)
self.set_resizable(False)
```

En aquest bloc desenvolupem 3 funcions clau:

- Inicialitzem una finestra fent servir `Gtk.Window.__init__()` i li donem el títol de Puzzle2. 

- Connectem la creueta per tancar la finestra a una funció diferent de `Gtk.main_quit` per solucionar un problema que apareixia amb l'implementació del Puzzle1. 

- Definim una mida per la finestra i restringim la habilitat de canviar la mida.

#### _\_init_\_: Estructura de la finestra

```python
self.box = Gtk.Box(orientation = "vertical")
self.add(self.box)

self.uid_box = Gtk.Box()
self.uid_box.set_border_width(5)
self.uid_box.get_style_context().add_class("uid-box")
self.uid_box.get_style_context().add_class("uid-box-blue")

self.uid_label = Gtk.Label(label="Please, login with your university card")
self.uid_label.set_size_request(300, 50)
self.uid_label.set_line_wrap(True)
self.uid_box.add(self.uid_label)

self.clear_btn = Gtk.Button(label = "Clear")
self.clear_btn.connect("clicked", self.clear_uid)

self.box.add(self.uid_box)
self.box.add(self.clear_btn)
```

En aquest fragment definim tots els elements visibles de la finestra. Els elements segueixen aquesta estructura: 

```
self.box
├── self.clear_btn
└── self.uid_box
    └── self.uid_label
```

| Nom                | Funció                                                                                                                                                     |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **self.box**       | Element principal de la finestra. Permet posicionar el botó a sota de l'etiqueta del UID mitjançant l'instrucció `orientation = vertical` en la declaració |
| **self.uid_box**   | Caixa contenidora de `self.uid_label`. Serveix per permetre canviar el color del fons de l'etiqueta quan es detecta un UID                                 |
| **self.uid_label** | Etiqueta del UID                                                                                                                                           |
| **self.clear_btn** | Botó que permet borrar el UID i tornar a cercar per un altre                                                                                               |

He trobat que aquesta és l'estructura més clara per poder implementar totes les funcionalitats desitjades.

#### _\_init_\_: Threading

```python
self.thread = threading.Thread(target = self.scan_uid)
self.thread.daemon = True
self.thread.start()
```

Com que la funcionalitat del Puzzle 1 és bloquejant, cal executar-la en un thread separat. Això s'aconsegueix inicialitzant un objecte de classe thread i assignant-li la funció `self.scan_uid`

#### clean_uid

```python
def clear_uid(self, widget):

    if not self.thread.is_alive():
        self.uid_label.set_label("Please, login with your university card")
        self.uid_box.get_style_context().add_class("uid-box-blue")
        self.uid_box.get_style_context().remove_class("uid-box-red")

        self.thread = threading.Thread(target = self.scan_uid)
        self.thread.start()
```

La funció `self.clean_uid` es crida quan l'usuari prem el botó. La seva funció és borrar el UID, restablir el color del fons i tornar a incialitzar el thread. La funcionalitat d'aquesta funció depèn de que no hi hagi cap thread en marxa.

#### scan_uid

```python
def scan_uid(self):

    uid = self.lector.scan_uid()
    self.uid_label.set_label("UID:" + uid)
    self.uid_box.get_style_context().add_class("uid-box-red")
    self.uid_box.get_style_context().remove_class("uid-box-blue")
```

La funció `self.scan_uid` és la funció que crida el thread. Aquesa funció crida a la llibreria del Puzzle1, i quan aquesta acaba imprimeix el resultat en l'etiqueta i canvia el color del fons.

#### close

```python
def close(self, widget):

    self.lector.lector.close()
    Gtk.main_quit()
```

El sensor `RFID-RC522` requereix tancar els ports GPIO un cop es deixa de fer servir. Per poder implementar això, connecto el botó de tancar la finestra a la funció `self.close`, que crida a la funció close de la llibreria del Puzzle1 i tanca la finestra.

<div style="page-break-after: always;"></div>

## Codi Sencer

```python
import threading #Threads
import Rfid #Llibreria del Puzzle 1
import gi #

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio #llibreries de Gtk

class Finestra(Gtk.Window):

    def __init__(self):

        #Assignem el lector Rfid a self.lector
        self.lector = Rfid.Rfid() 

        #Inicialitzem el proveïdor de css
        self.css = Gtk.CssProvider()
        self.css.load_from_file(Gio.File.new_for_path("style.css"))
        self.screen = Gdk.Screen.get_default()
        self.context = Gtk.StyleContext()
        self.context.add_provider_for_screen(self.screen, self.css,
 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

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
        self.uid_label = Gtk.Label(label = 
"Please, login with your university card")
        self.uid_label.set_size_request(300, 50)
        self.uid_label.set_line_wrap(True)
        self.uid_box.add(self.uid_label)     
```

```python
        
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
            self.uid_label.set_label(
"Please, login with your university card")
            self.uid_box.get_style_context().add_class("uid-box-blue")
            self.uid_box.get_style_context().remove_class("uid-box-red")

            #Tornem a iniciar el thread
            self.thread = threading.Thread(target = self.scan_uid)
            self.thread.start()

    def scan_uid(self):

        uid = self.lector.scan_uid()
        self.uid_label.set_label("UID:" + uid)
        self.uid_box.get_style_context().add_class("uid-box-red")
        self.uid_box.get_style_context().remove_class("uid-box-blue")

    def close(self, widget):

        self.lector.lector.close()
        Gtk.main_quit()

win = Finestra()
win.show_all()
Gtk.main()
```

<div style="page-break-after: always;"></div>

## Codi CSS

```css
.uid-box-blue {
        background-color: #0096FF;
}
.uid-box-red {
    background-color: #ff3131;
}
.uid-box{
    border-radius: 10px;
}
```

## Problemes

Durant el desenvolupament m'he trobat dos problemes significatius:

### Primer Problema: Estructura de Carpetes

El meu repositori segueix aquesta estructura de carpetes:

```md
.
├── Puzzle1
│   ├── Rfid.py
│   └── SimpleMFRC522.py
└── Puzzle2
    ├── P2.py
    └── style.css
```

Això em generava problemes a l'hora de cridar a `Rfid.py` com a llibreria en el fitxer principal del Puzzle2, `P2.py`. Per tal de solucionar aquest problema, vaig decidir crear un enllaç simbòlic a Rfid.py en la carpeta de P2.py

```bash
ln -s Rfid.py ../Puzzle1/Rfid.py
```

Això alhora em generava un problema, doncs com que Rfid.py crida al fitxer `SimpleMFRC522.py` com a dependència vaig haver de crear un enllaç simbòlic també per aquest fitxer.

```bash
ln -s SimpleMFRC522.py ../Puzzle2/SimpleMFRC522.py
```

D'aquesta manera, la meva estructura final de fitxers és aquesta:

```
.
├── Puzzle1
│   ├── Rfid.py
│   └── SimpleMFRC522.py
└── Puzzle2
    ├── P2.py
    ├── Rfid.py -> ../Puzzle1/Rfid.py
    ├── SimpleMFRC522.py -> ../Puzzle1/SimpleMFRC522.py
    └── style.css
```

### Segon Problema: Rendiment del meu ordinador i VNC

Un altre dels problemes que vaig trobar va ser amb el programa VNC. L'ordinador que faig servir per programar aquests puzzles és un ThinkPad del 2014, que a dia d'avui ja no té les millors prestacions. Degut a això, intentar visualitzar un escriptori remot mitjaçant VNC és una tasca complicada que de vegades resulta en que es congeli l'ordinador. Per solucionar això, com que el meu sistema operatiu és GNU/Linux puc cridar ssh d'aquesta manera:

```bash
ssh -Y rpi@PBEpi.local
```

Aquest argument permet que ssh transmeti les finestres que obro en la raspberry pi a la pantalla del meu ordinador, de manera que la demanda de recursos del portàtil disminueix.

### Tercer Problema: Estandaritzar la mida de la finestra

El text d'una `Gtk.Label` queda centrat per defecte. Tot i això, com que nosaltres volem que tingui dos missatges diferents de diferentes longituds, el canvi de longitud causava que la finestra canviés de mida cada vegada que el text canviava de _Please, login with your university card_ a un UID.

Per poder solucionar aquest problema, vaig establir una mida definida a la `self.uid_label` en la declaració.

```python
self.uid_label.set_size_request(300, 50)
```

D'aquesta manera, l'etiqueta tindrà la mateixa mida independentment del contingut.
