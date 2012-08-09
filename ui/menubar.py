from gi.repository import Gtk

class MenuBar(Gtk.MenuBar):
  def __init__(self, controller):
    Gtk.MenuBar.__init__(self)
    self.controller = controller
    file_menu = Gtk.Menu()
    file_menu_item = Gtk.MenuItem("File")
    exit = Gtk.MenuItem("Exit")
    exit.connect("activate", Gtk.main_quit)
    file_menu.append(exit)
    file_menu_item.set_submenu(file_menu)
    self.add(file_menu_item)