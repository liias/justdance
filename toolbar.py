from gi.repository import Gtk
import logging
import os
import time

logger = logging.getLogger(__name__)

class Toolbar(Gtk.Toolbar):
  def __init__(self, controller):
    Gtk.Toolbar.__init__(self)
    self.controller = controller
    #Track path toolbar items
    self.path_button_items = {}
    context = self.get_style_context()
    context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)

    self.up_button = Gtk.ToolButton(Gtk.STOCK_GO_UP)
    self.up_button.connect("clicked", self.on_up_button_clicked)

    self.home_button = Gtk.ToolButton(Gtk.STOCK_HOME)
    self.home_button.connect("clicked", self.on_home_button_clicked)

    self.path_entry_item = Gtk.ToolItem()
    self.path_entry_item.set_expand(True)
    self.path_entry = Gtk.Entry()
    #    self.path_entry.set_hexpand(True)
    self.path_entry.set_activates_default(True)
    self.path_entry.set_text(controller.default_dir_path)
    self.path_entry_item.add(self.path_entry)
    self.go_button_item = Gtk.ToolItem()
    self.go_button = Gtk.Button("Go")
    self.go_button.connect("clicked", self.on_go_button_clicked)
    self.go_button.set_can_default(True)
    self.go_button_item.add(self.go_button)
    self.add(self.home_button)
    self.add(self.up_button)
    self.add(self.path_entry_item)
    self.add(self.go_button_item)

  def get_normalized_path(self):
    return os.path.normpath(self.controller.get_current_path())

  def set_entry_to_current_path(self):
    self.path_entry.set_text(self.controller.path.current_active_path)

  def go_to_sub_path(self, sub_path):
    full_path = self.controller.path.get_sub_path_as_full_path(sub_path)
    self.go_to_path(full_path)

    #toggled signal is emitted with set_active, but toggle signal also uses the clicked handler


  def go_to_path(self, path):
    time_start = time.time()
    #    TODO: verify that path is valid?
    self.controller.path.navigate_to_path(path)
    self.controller.list_dir()
    self.set_entry_to_current_path()
    self.add_button_for_each_directory()
    print "Go to path Time elapsed: %s" % (time.time() - time_start)

  def get_current_button(self):
    if not self.controller.path.current_active_path in self.path_button_items:
      return False
    return self.path_button_items[self.controller.path.current_active_path]

  def get_last_button(self):
    if not self.controller.path.current_full_path in self.path_button_items:
      return False
    return self.path_button_items[self.controller.path.current_full_path]

  def on_up_button_clicked(self, widget):
    parent_path = self.controller.path.get_parent_directory_path()
    logger.debug("Up button clicked, parent path is %s" % parent_path)
    if parent_path:
      self.go_to_path(parent_path)

  def on_home_button_clicked(self, widget):
    home_path = os.path.realpath(os.path.expanduser('~'))
    self.go_to_path(home_path)

  def on_go_button_clicked(self, widget):
    dir_path = self.path_entry.get_text()
    if dir_path:
      self.go_to_path(dir_path)

  def on_directory_button_clicked(self, widget, path):
    if widget.get_active():
      logger.warn("ONDIRBUTTONCLICKED")
      self.go_to_path(path)

  def delete_unused_buttons(self):
    for full_path, item in self.path_button_items.iteritems():
      logger.debug("Deleting toolbar item for path '%s'" % full_path)
      self.remove(item)
    self.path_button_items.clear()

  def add_button_for_each_directory(self):
    logger.debug("Current path has %d parts" % len(self.controller.path.current_active_path_parts))
    self.delete_unused_buttons()
    for path_part in self.controller.path.current_full_path_parts:
      self.add_path_button(path_part)
    self.show_all()

  def add_path_button(self, path_part):
    path = path_part.path
    full_path = path_part.full_path
    logger.debug("Adding path button for '%s' with full path '%s'" % (path, full_path))
    path_button = Gtk.ToggleToolButton(label=path)
    #  Enables label to show even when toolbar is in image mode
    path_button.set_is_important(True)
    #if active element
    if full_path == self.controller.path.current_active_path:
      path_button.set_active(True)
    path_button.connect("clicked", self.on_directory_button_clicked, full_path)
    self.path_button_items[full_path] = path_button
    self.add(path_button)

