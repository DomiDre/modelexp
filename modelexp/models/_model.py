from abc import ABCMeta, abstractmethod

class Model(metaclass=ABCMeta):
  '''
  Abstract class to describe a model.
  Specific models are defined by classes that have to implemented the defined functions here.
  '''

  @abstractmethod
  def defineDomain(self):
    '''
    On which space should the model be evaluated
    '''
    pass

  @abstractmethod
  def calcModel(self):
    '''
    How to calculate the model on the defined domain
    '''
    pass

  @abstractmethod
  def defineParameters(self):
    '''
    How to calculate the model on the defined domain
    '''
    pass

  @abstractmethod
  def plotModel(self, ptrGui):
    '''
    How to plot the model
    '''
    self.fig = ptrGui.plotWidget.getFig()
    self.ax = ptrGui.plotWidget.getDataAx()