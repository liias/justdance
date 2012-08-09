from gi.repository import Gtk
from ui.menubar import MenuBar
from ui.paned import Paned
from ui.statusbar import Statusbar
from ui.toolbar import Toolbar

class JustDanceWindow(Gtk.Window):
  def __init__(self, controller, *args, **kwargs):
    Gtk.Window.__init__(self, title="Just Dance", *args, **kwargs)
    self.controller = controller
    self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    self.main_menu = MenuBar(controller)
    self.toolbar = Toolbar(controller)
    self.set_default(self.toolbar.go_button)
    self.paned = Paned(controller)
    self.status_bar = Statusbar(controller)
    self.main_box.add(self.main_menu)
    self.main_box.add(self.toolbar)
    self.main_box.add(self.paned)
    self.main_box.add(self.status_bar)
    self.add(self.main_box)

  def set_number_of_files(self, number_of_items):
    self.status_bar.status_label.set_text("%d items" % number_of_items)