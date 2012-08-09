# -*- coding: utf-8 -*-
import logging
from gi.repository import Gtk, Gio
from just_dance_controller import JustDanceController
from ui.window import JustDanceWindow

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

class JustDanceApplication(Gtk.Application):
  def __init__(self):
    logger.info("Just Dance started")
    Gtk.Application.__init__(self, application_id="apps.filemanagers.justdance",
      flags=Gio.ApplicationFlags.FLAGS_NONE)
    self.connect("activate", self.on_activate)

  def on_activate(self, data=None):
    logger.info("Just Dance activated")
    controller = JustDanceController()
    window = JustDanceWindow(controller, type=Gtk.WindowType.TOPLEVEL)
    window.set_default_size(400, 400)
    controller.set_window(window)
    window.show_all()
    self.add_window(window)