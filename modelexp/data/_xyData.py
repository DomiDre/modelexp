import numpy as np
from ._data import Data

class XyData(Data):
  def setData(self, x, y):
    """Set the data of an .xy file

    Parameters
    ----------
    x : :obj: `array_like`
      Domain
    y : :obj: `array_like`
      Values
    """

    self.x = np.array(x)
    self.y = np.array(y)

  def getData(self):
    return self.x, self.y

  def getDomain(self):
    return self.x

  def getValues(self):
    return self.y

  def getErrors(self):
    return np.zeros(len(self.y))

  def loadFromFile(self, filename):
    fileData = np.genfromtxt(filename)
    x = fileData[:,0]
    y = fileData[:,1]
    self.setData(x, y)

  def plotData(self):
    self.ax.plot(self.x, self.y, ls='None', marker='.', zorder=5)
    self.ptrExperiment.adjustAxToAddedData()
