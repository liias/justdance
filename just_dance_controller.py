import mimetypes
import os
import time
from gi.repository import Gtk, Gio
from path import Path

class JustDanceController(object):
  window = None

  def __init__(self):
    self.default_dir_path = os.getenv("HOME")
    self.current_dir_path = ""
    self.path = Path(self)
    self.is_skip_hidden_files = False

  @property
  def icon_view(self):
    return self.window.paned.directory_content_scrolled_window.icon_view

  def set_window(self, window):
    self.window = window

  def list_dir(self):
    time_start = time.time()
    #    self.icon_view.freeze_child_notify()
    #    self.icon_view.set_model(None)
    try:
      self.icon_view.clear_items()
      directory_listing = os.listdir(self.path.current_active_path)
      for filename in directory_listing:
        # Skip hidden files
        if self.is_skip_hidden_files and filename[0] == '.':
          continue
        file_path = os.path.join(self.path.current_active_path, filename)
        if os.path.isdir(file_path):
          self.icon_view.add_item(filename, Gtk.STOCK_DIRECTORY, True)
        else:
          mime_type, encoding = mimetypes.guess_type(file_path, False)
          if mime_type:
            icon = Gio.content_type_get_icon(mime_type)
            self.icon_view.add_with_icon(filename, icon, False)
          else:
            self.icon_view.add_item(filename, Gtk.STOCK_FILE, False)
          #     print filename
      self.window.set_number_of_files(len(directory_listing))
    except OSError as oe:
      print oe
      #    self.icon_view.set_model(self.icon_view.list_store_model)
    #    self.icon_view.thaw_child_notify()
    print "Time elapsed: %s" % (time.time() - time_start)

  def set_current_path(self, path):
    self.current_dir_path = path

  def get_current_path(self):
    return self.current_dir_path

  def open_file_in_current_directory(self, sub_path):
    file_path = self.path.get_sub_path_as_full_path(sub_path)
    os.system('/usr/bin/xdg-open %s' % file_path)


