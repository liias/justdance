from gi.repository import Gtk
from model.tab import Tab
from ui.scrolled_window import DirectoryContentScrolledWindow

class Paned(Gtk.Paned):
  def __init__(self, controller):
    Gtk.Paned.__init__(self)
    self.controller = controller
    self.set_vexpand(True)
    self.directory_content_scrolled_window = DirectoryContentScrolledWindow(controller)
    self.tab = Tab()
    self.add(self.directory_content_scrolled_window)