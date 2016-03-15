class Version(object):
  def __init__(self):
    pass
  def tag(self):
    return "1.0"
  def git(self):
    return "@git@"
  def date(self):
    return ""
  def name(self):
    sA = []
    sA.append(self.tag())
    sA.append(self.git())
    sA.append(self.date())
    return " ".join(sA)
class Version(object):
  def __init__(self):
    pass
  def tag(self):
    return "1.0.1"
  def git(self):
    return "@git@"
  def date(self):
    return "2014-05-09 20:00"
  def name(self):
    sA = []
    sA.append(self.tag())
    sA.append(self.git())
    sA.append(self.date())
    return " ".join(sA)
