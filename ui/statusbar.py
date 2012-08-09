from gi.repository import Gtk

class Statusbar(Gtk.Statusbar):
  def __init__(self, controller):
    Gtk.Statusbar.__init__(self)
    self.controller = controller
    self.status_label = Gtk.Label()
    self.add(self.status_label)
