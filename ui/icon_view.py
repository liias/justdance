from gi.repository import Gtk, GdkPixbuf, Gio
from gi._glib import GError
import logging
import time

logger = logging.getLogger(__name__)


class DirectoryContentIconView(Gtk.IconView):
  COLUMN_LABEL = 0
  COLUMN_ICON = 1
  COLUMN_IS_DIRECTORY = 2

  def __init__(self, controller):
    Gtk.IconView.__init__(self)
    self.controller = controller
    self.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
    self.list_store_model = Gtk.ListStore(str, GdkPixbuf.Pixbuf, bool)

    self.set_model(self.list_store_model)
    self.set_text_column(self.COLUMN_LABEL)
    self.set_pixbuf_column(self.COLUMN_ICON)
    self.list_store_model.set_sort_column_id(self.COLUMN_LABEL, Gtk.SortType.ASCENDING)
    #    self.list_store_model.set_default_sort_func(lambda x: None)
    time_start = time.time()
    self.icon_theme = Gtk.IconTheme.get_default()
    #    self.default_icon = self.icon_theme.lookup_icon("gtk-directory", 16, 0).load_icon()
    #    self.icon_directory = self.icon_theme.lookup_icon("gtk-directory", 16, 0).load_icon()
    self.default_icon = self.icon_theme.load_icon(Gtk.STOCK_FILE, Gtk.IconSize.DIALOG, Gtk.IconLookupFlags.USE_BUILTIN)
    self.icon_directory = self.icon_theme.load_icon(Gtk.STOCK_DIRECTORY, Gtk.IconSize.DIALOG, Gtk.IconLookupFlags.USE_BUILTIN)
    print "Icon Time elapsed: %s" % (time.time() - time_start)
    self.connect("size-allocate", self.on_size_allocate)
    self.connect("item-activated", self.on_icon_activated)

  def on_icon_activated(self, widget, tree_path):
  #    logger.debug("Activated: '%s'" % tree_path)
    model = widget.get_model()
    path = model[tree_path][self.COLUMN_LABEL]
    is_directory = model[tree_path][self.COLUMN_IS_DIRECTORY]

    if not is_directory:
      self.controller.open_file_in_current_directory(path)

      #      os.system('/usr/bin/xdg-open /home/user/Examples/case_Contact.pdf')
      #      xdg-open
      return

    logger.debug("Activated directory with path '%s'" % path)
    #TODO: Move functional code away from toolbar
    self.controller.go_to_sub_path(path)

  #    self.current_directory = self.current_directory + os.path.sep + path

  #    self.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, [], DRAG_ACTION)

  #    self.connect("drag-data-get", self.on_drag_data_get)

  #  def on_drag_data_get(self, widget, drag_context, data, info, time):
  #    selected_path = self.get_selected_items()[0]
  #    selected_iter = self.get_model().get_iter(selected_path)
  #
  #    if info == TARGET_ENTRY_TEXT:
  #      text = self.get_model().get_value(selected_iter, COLUMN_TEXT)
  #      data.set_text(text, -1)
  #    elif info == TARGET_ENTRY_PIXBUF:
  #      pixbuf = self.get_model().get_value(selected_iter, COLUMN_PIXBUF)
  #      data.set_pixbuf(pixbuf)

  def on_size_allocate(self, widget, allocation):
  #    print "ok"
    [self.set_columns(m) for m in [1, self.get_columns()]]

  def clear_items(self):
    self.list_store_model.clear()

  def add_item(self, text, icon_name, is_directory):
    pixbuf = self.render_icon(icon_name, Gtk.IconSize.DIALOG, None)
    self.list_store_model.append([text, pixbuf, is_directory])

  def add_with_icon(self, text, icon, is_directory):
  #    pixbuf = theme.load_icon (((ThemedIcon) icon).get_names ()[0], size, Gtk.IconLookupFlags.USE_BUILTIN);
    try:
      pixbuf = self.icon_theme.load_icon(icon.get_names()[0], 48, Gtk.IconLookupFlags.USE_BUILTIN)
    except GError as e:
      pixbuf = self.render_icon(Gtk.STOCK_FILE, Gtk.IconSize.DIALOG, None)
      logger.debug("wrong %s" % e)
    self.list_store_model.append([text, pixbuf, is_directory])

  def get_icon_from_mime_type(self, mime_type):
    return Gio.content_type_get_icon(mime_type)