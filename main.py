#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys
from gi.repository import Gtk
from just_dance_controller import JustDanceController
from just_dance_window import JustDanceWindow

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

#dir_path = "/home/madis"

def main(argv):
  logger.info("Just Dance started")
  controller = JustDanceController()
  window = JustDanceWindow(controller)
  window.connect("delete-event", Gtk.main_quit)
  window.set_default_size(400, 400)
  controller.set_window(window)
  window.show_all()

  #  builder.connect_signals({
  #    "on_justdance_window_remove": Gtk.main_quit,
  #    "on_dirlist_button_clicked": list_dir
  #  })
  #  window = builder.get_object("justdance_window")
  #  paned = builder.get_object("paned")
  #  directory_content_scrolled_window = DirectoryContentScrolledWindow()
  #  paned.add(directory_content_scrolled_window)
  Gtk.main()

if __name__ == "__main__":
  main(sys.argv[1:])