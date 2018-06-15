import numpy as np
from ._data import Data

class XyeData(Data):
  def __init__(self):
    self.x = None
    self.y = None
    self.e = None

  def setData(self, x, y, e):
    self.x = x
    self.y = y
    self.e = e

  def loadFromFile(self, filename):
    fileData = np.genfromtxt(filename)
    x = fileData[:,0]
    y = fileData[:,1]
    e = fileData[:,2]
    self.setData(x, y, e)

  def plotData(self, ptrGui):
    super().plotData(ptrGui)
    self.ax.errorbar(self.x, self.y, self.e)
    ptrGui.plotWidget.updatedDataAx()
