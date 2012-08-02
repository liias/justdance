from gi.repository import Gtk
from directory_content_icon_view import DirectoryContentIconView

class DirectoryContentScrolledWindow(Gtk.ScrolledWindow):
  def __init__(self, controller):
    Gtk.ScrolledWindow.__init__(self)
    self.controller = controller
    self.icon_view = DirectoryContentIconView(controller)
    self.add(self.icon_view)