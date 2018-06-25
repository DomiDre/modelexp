import numpy as np
from ._data import Data

class XyeData(Data):
  def setData(self, x, y, e):
    """Set the data of an .xye file

    Parameters
    ----------
    x : :obj: `array_like`
      Domain
    y : :obj: `array_like`
      Values
    e : :obj: `array_like`
      Errors
    """

    self.x = np.array(x)
    self.y = np.array(y)
    self.e = e

  def getDomain(self):
    return self.x

  def getValues(self):
    return self.y

  def getErrors(self):
    return self.e

  def loadFromFile(self, filename):
    fileData = np.genfromtxt(filename)
    x = fileData[:,0]
    y = fileData[:,1]
    e = fileData[:,2]
    self.setData(x, y, e)

  def plotData(self):
    self.ax.errorbar(self.x, self.y, self.e, ls='None', marker='.', zorder=5)
    self.ptrExperiment.adjustAxToAddedData()
