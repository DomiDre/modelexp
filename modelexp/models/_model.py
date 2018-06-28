from abc import ABCMeta, abstractmethod
from lmfit import Parameters
from ._decoration import Decoration

class Model(metaclass=ABCMeta):
  """Abstract class to describe a model.
  Specific models are defined by classes that have to implemented the defined functions here.
  """
  def __init__(self):
    self.params = Parameters()
    self.decoration = Decoration
    self.suffix = ''

  def _setDecoration(self, decoratingClass):
    self.decoration = decoratingClass(self)


  @abstractmethod
  def initParameters(self):
    """Initialize the parameter names at beginning

    """
    pass

  @abstractmethod
  def connectGui(self):
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
  def calcDecoratedModel(self):
    """How to treat an additional decoration class to a model
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