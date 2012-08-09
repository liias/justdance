from gi.repository import Gtk
import logging

logger = logging.getLogger(__name__)

class PathButton(Gtk.ToggleToolButton):
  def __init__(self, controller, path_part, *args, **kwargs):
    Gtk.ToggleToolButton.__init__(self, *args, **kwargs)
    self.controller = controller
    self.set_path_part(path_part)
    #  Enables label to show even when toolbar is in image mode
    self.set_is_important(True)
    self.connect("toggled", self.on_toggled)
    logger.debug("Added path button for '%s' with full path '%s'" % (self.path_part.path, self.path_part.get_full_path()))

  def set_path_part(self, path_part):
    self.path_part = path_part
    self.set_label(path_part.get_name())
    if self.is_current():
      self.set_active(True)

  def is_current(self):
    return self.path_part.get_full_path() == self.controller.path.current_active_path

  def on_toggled(self, widget):
    if self.get_active():
      logger.debug("on_directory_button_toggled")
      self.controller.go_to_path(self.path_part.get_full_path())
    else:
      widget.set_active(True)
      return False