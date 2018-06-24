from abc import ABCMeta, abstractmethod
from lmfit import Parameters

try:
  from ..experiments import Experiment
except ImportError:
  pass

class Model(metaclass=ABCMeta):
  """Abstract class to describe a model.
  Specific models are defined by classes that have to implemented the defined functions here.
  """
  def __init__(self, experiment):
    self.ptrExperiment = experiment

    self.params = Parameters()
    self.initParameters()

    if (hasattr(self.ptrExperiment, 'data')):
      self.defineDomain(self.ptrExperiment.data.getDomain())

  def getParameters(self):
    return self.params

  def connectGui(self, gui):
    self.ptrGui = gui
    self.fig = self.ptrGui.plotWidget.getFig()
    self.ax = self.ptrGui.plotWidget.getDataAx()

  def setParamLimits(self, paramName, minVal, maxVal):
    self.params[paramName].min = minVal
    self.params[paramName].max = maxVal
    if (hasattr(self, 'ptrGui')):
      self.ptrGui.updateSlider(paramName)

  @abstractmethod
  def initParameters(self):
    """Initialize the parameter names at beginning

    """
    pass

  @abstractmethod
  def defineDomain(self):
    """On which space should the model be evaluated

    """
    pass

  @abstractmethod
  def getDomain(self):
    """Returns the domain on which the model is defined

    """
    pass

  @abstractmethod
  def getValues(self):
    """Returns the values of the model

    """
    pass

  @abstractmethod
  def calcModel(self):
    """How to calculate the model on the defined domain

    """
    pass

  @abstractmethod
  def setParameters(self):
    """Update the parameters

    """
    pass

  @abstractmethod
  def plotModel(self):
    """Define how to plot the model

    """
    pass

  @abstractmethod
  def updateModel(self):
    """How to update the model when parameters are changed

    """
    pass

  def draw(self):
    self.ptrGui.update()