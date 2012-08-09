class PathPart(object):
  def __init__(self, full_path, path):
    self.full_path = full_path
    self.path = path

  def get_real_path(self):
    if self.path == "":
      return "/"
    return self.path

  def get_name(self):
    if self.path == "":
      return "/"
    return self.path

  def get_full_path(self):
    if self.full_path == "":
      return "/"
    return self.full_path