from gui.gui import Gui
from data.xyeData import XyeData

class Model():
  def __init__(self):
    self.data = None
    self.gui = None
    self.model = None
    self.fit = None

    self.setComponents()

  def setComponents(self):
    self.setGui()
    self.setModel()
    self.setFit()
    self.setData()

  def setGui(self):
    self.gui = Gui

  def setModel(self):
    pass

  def setFit(self):
    pass

  def setData(self):
    pass

  def initGui(self):
    if self.gui:
      self.gui()

if __name__ == '__main__':
  model = Model()
  model.initGui()
