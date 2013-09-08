import subprocess
from gi.repository import Gtk

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="UGS - MEG Power Controller")
	Gtk.Window.set_default_size(self, 300, 20)

	self.grid = Gtk.Grid(column_spacing=40, row_spacing=10)
	self.add(self.grid)

        label1 = Gtk.Label("Video: gpio144 ")
	label1.set_justify(Gtk.Justification.LEFT)
	self.grid.add(label1)

        self.button1 = Gtk.Button(label="OFF")
        self.button1.connect("clicked", self.on_button1_clicked)
	self.grid.attach(self.button1, 1, 0, 1, 1)

        self.button2 = Gtk.Button(label="ON")
        self.button2.connect("clicked", self.on_button2_clicked)
	self.grid.attach_next_to(self.button2, self.button1, Gtk.PositionType.RIGHT, 1, 1)

        label2 = Gtk.Label("Queue: gpio144 ")
	label2.set_justify(Gtk.Justification.LEFT)
	self.grid.attach(label2, 0, 1, 1, 1)

        self.button3 = Gtk.Button(label="OFF")
        self.button3.connect("clicked", self.on_button3_clicked)
	self.grid.attach(self.button3, 1, 1, 1, 1)

        self.button4 = Gtk.Button(label="ON")
        self.button4.connect("clicked", self.on_button4_clicked)
	self.grid.attach_next_to(self.button4, self.button3, Gtk.PositionType.RIGHT, 1, 1)

        label3 = Gtk.Label("MySQL: gpio145 ")
	label3.set_justify(Gtk.Justification.LEFT)
	self.grid.attach(label3, 0, 2, 1, 1)

        self.button5 = Gtk.Button(label="OFF")
        self.button5.connect("clicked", self.on_button5_clicked)
	self.grid.attach(self.button5, 1, 2, 1, 1)

        self.button6 = Gtk.Button(label="ON")
        self.button6.connect("clicked", self.on_button6_clicked)
	self.grid.attach_next_to(self.button6, self.button5, Gtk.PositionType.RIGHT, 1, 1)

    def on_button1_clicked(self, widget):
	subprocess.call(["python", "udp_client.py", "video", "off"])
        print "Video: OFF"

    def on_button2_clicked(self, widget):
	subprocess.call(["python", "udp_client.py", "video", "on"])
        print "Video: ON"

    def on_button3_clicked(self, widget):
	subprocess.call(["python", "udp_client.py", "queue", "off"])
        print "Queue: OFF"

    def on_button4_clicked(self, widget):
	subprocess.call(["python", "udp_client.py", "queue", "on"])
        print "Queue: ON"

    def on_button5_clicked(self, widget):
	subprocess.call(["python", "udp_client.py", "mysql", "off"])
        print "MySQL: OFF"

    def on_button6_clicked(self, widget):
	subprocess.call(["python", "udp_client.py", "mysql", "on"])
        print "MySQL: ON"


win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
