from abc import ABCMeta, abstractmethod
from ..experiments import Experiment
from ..data import Data
from ..models import Model

class Fit(metaclass=ABCMeta):
  '''
  Abstract class to describe a fit routine.
  Specifi fit rountines are defined by a class that has to implement
  the defined functions here.
  '''
  def __init__(self, experiment, data, model):
    self.ptrExperiment: Experiment = experiment
    self.ptrData: Data = data
    self.ptrModel: Model = model

  def connectGui(self, gui):
    self.ptrGui = gui

  @abstractmethod
  def fit(self):
    """Calls the fit function to find the minimal parameters of the Model that
    are best suited to describe the Data. Fit routines generally start from the
    parameters that are initially set in Model before calling fit function.
    """
    pass