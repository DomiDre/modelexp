from abc import ABCMeta, abstractmethod
from ..data import Data
from ..models import Model
class Experiment(metaclass=ABCMeta):
  """
  Abstract class to describe an experiment.
  A complete experiment consists of experimental data and/or a model of it
  """
  def __init__(self):
    pass

  def connectGui(self, gui):
    self.ptrGui = gui
    self.fig = self.ptrGui.plotWidget.getFig()
    self.ax = self.ptrGui.plotWidget.getDataAx()

  def connectData(self, data):
    self.data: Data = data

  def connectModel(self, model):
    self.model: Model = model

  @abstractmethod
  def setAxProps(self):
    pass

  @abstractmethod
  def residuum(self):
    """
    Returns the distance between data and model
    Should take the parameter of the model as argument and update the model values
    on call according to the given parameters
    """