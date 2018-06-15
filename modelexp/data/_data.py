from abc import ABCMeta, abstractmethod

class Data(metaclass=ABCMeta):
  '''
  Abstract class to describe a model.
  Specific models are defined by classes that have to implemented the defined functions here.
  '''

  @abstractmethod
  def setData(self):
    '''
    How to set data
    '''
    pass

  @abstractmethod
  def loadFromFile(self):
    '''
    How to load data from file
    '''
    pass

  @abstractmethod
  def plotData(self, ptrGui):
    '''
    How to plot data
    '''
    self.fig = ptrGui.plotWidget.getFig()
    self.ax = ptrGui.plotWidget.getDataAx()
