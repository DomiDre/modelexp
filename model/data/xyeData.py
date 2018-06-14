import numpy as np
class XyeData:
  def __init__(self):
    self.x = None
    self.y = None
    self.e = None

  def setData(self, x, y, e):
    self.x = x
    self.y = y
    self.e = e

  def loadColFile(self, filename):
    fileData = np.genfromtxt(filename)
    x = fileData[:,0]
    y = fileData[:,1]
    e = fileData[:,2]
    self.setData(x, y, e)

  def plotData(self, ptrGui):
    fig = ptrGui.plotWidget.getFig()
    ax = ptrGui.plotWidget.getDataAx()
    ax.errorbar(self.x, self.y, self.e)
    ptrGui.plotWidget.updatedDataAx()
    