import numpy as np
from ._data import Data

class PrfData(Data):
  def __init__(self):
    super().__init__()
    self.x = []
    self.y = []
    self.m = []

  def setData(self, x, y, m):
    self.x = np.array(x)
    self.y = np.array(y)
    self.m = np.array(m)

  def getData(self):
    return self.x, self.y, self.m

  def getDomain(self):
    return self.x

  def getValues(self):
    return self.y

  def getModel(self):
    return self.m

  def getErrors(self):
    return np.sqrt(self.y)

  def plotData(self, ax):
    ax.errorbar(self.x, self.m, ls='None', marker='.', zorder=5)

  def sliceDomain(self, minX=-np.inf, maxX=np.inf):
    slicedDomain = np.logical_and(minX < self.x, self.x < maxX)
    self.xMask = self.x[~slicedDomain]
    self.yMask = self.y[~slicedDomain]
    self.mMask = self.m[~slicedDomain]
    self.x = self.x[slicedDomain]
    self.y = self.y[slicedDomain]
    self.m = self.m[slicedDomain]

  def addDataLine(self, dataline):
    assert len(dataline) == 3, 'Tried to add a dataline that does not have 3 elements to a XYE dataset: ' + str(dataline)
    self.x.append(dataline[0])
    self.y.append(dataline[1])
    self.m.append(dataline[2])

  def loadFromFile(self, filename):
    self.filename = filename
    x = []
    y = []
    m = []
    with open(filename, 'r') as f:
      next(f)
      next(f)
      next(f)
      next(f)
      for line in f:
        if line.startswith('#'):
          continue
        splitLine = line.strip().split()
        x.append(float(splitLine[0]))
        y.append(float(splitLine[1]))
        m.append(float(splitLine[2]))

    x = np.array(x)
    y = np.array(y)
    m = np.array(m)

    sortedArgs = np.argsort(x)
    x = x[sortedArgs]
    y = y[sortedArgs]
    m = m[sortedArgs]
    self.setData(x, y, m)