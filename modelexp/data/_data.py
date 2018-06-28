from abc import ABCMeta, abstractmethod

class Data(metaclass=ABCMeta):
  '''
  Abstract class to describe a model.
  Specific models are defined by classes that have to implemented the defined functions here.
  '''
  def __init__(self):
    self.suffix = ''

  @abstractmethod
  def setData(self):
    '''
    How to set data
    '''
    pass

  @abstractmethod
  def getData(self):
    '''
    Return all data
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

  @abstractmethod
  def getDomain(self):
    pass

  @abstractmethod
  def getValues(self):
    pass

  @abstractmethod
  def getErrors(self):
    pass

  @abstractmethod
  def sliceDomain(self):
    pass