import logging
import os
from model.path_part import PathPart

logger = logging.getLogger(__name__)

class Path(object):
  def __init__(self, controller):
    self.controller = controller
    # e.g /home/madis/Downloads
    self.previous_full_path = ""
    self.current_full_path = ""
    # e.g /home/madis
    self.previous_active_path = ""
    self.current_active_path = ""
    # Index is full path, value is only the directory name
    self.current_active_path_parts = []
    self.current_full_path_parts = []

  @staticmethod
  def to_normalized(path):
    return os.path.normpath(path)

  @staticmethod
  def to_parts(path):
    return path.split(os.sep)

  @staticmethod
  def to_path(parts):
    return os.sep.join(parts)

  @staticmethod
  def generate_path_parts(path):
    path_parts = Path.to_parts(path)
    indexed_path_parts = []
    for index in range(0, len(path_parts)):
      path = path_parts[index]
      full_path = os.sep.join(path_parts[:(index + 1)])
      part = PathPart(full_path, path)
      indexed_path_parts.append(part)
    return indexed_path_parts

  def set_last_path_as_previous(self):
    self.previous_active_path = self.current_active_path

  def generate_current_active_path_parts(self):
    self.current_active_path_parts = self.generate_path_parts(self.current_active_path)

  def generate_current_full_path_parts(self):
    self.current_full_path_parts = self.generate_path_parts(self.current_full_path)

  def set_current_active_path(self, active_path):
    self.set_last_path_as_previous()
    self.current_active_path = active_path
    self.generate_current_active_path_parts()

  def set_current_full_path(self, full_path):
    self.previous_full_path = self.current_full_path
    self.current_full_path = full_path
    self.generate_current_full_path_parts()

  def navigate_to_path(self, active_path):
    logger.debug("NAVIGATE to '%s'" % active_path)
    active_path = self.to_normalized(active_path)
    self.set_current_active_path(active_path)
    if not self.is_parent_of_previous_full_path():
      self.set_current_full_path(active_path)
    logger.debug("Active path: '%s'; Full path: '%s'" % (self.current_active_path, self.current_full_path))

  def is_parent_of_previous_full_path(self):
    return self.previous_full_path.startswith(self.current_active_path)

  # Returns False if no previous path
  def get_previous_path(self):
    if self.previous_active_path:
      return self.previous_active_path
    return False

  # Returns False if no next path
  def get_next_path(self):
    if self.current_active_path != self.current_full_path:
      logger.debug(
        "Difference between full and active path: %s" % self.get_full_and_active_difference()
      )
      return self.current_full_path
    return False

  def get_full_and_active_difference(self):
    if self.current_active_path != self.current_full_path:
      return self.current_full_path[len(self.current_active_path):]
    return ""

  def get_parent_directory_path(self):
    if len(self.current_active_path_parts) > 1:
      return os.path.dirname(self.current_active_path)
    return False

  def get_sub_path_as_full_path(self, sub_path):
    return os.path.join(self.current_active_path, sub_path)