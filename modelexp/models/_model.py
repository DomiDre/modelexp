from abc import ABCMeta, abstractmethod
from lmfit import Parameters
import numpy as np
import sys
try:
  from ..experiments import Experiment
except ImportError:
  pass

class Model(metaclass=ABCMeta):
  """Abstract class to describe a model.
  Specific models are defined by classes that have to implemented the defined functions here.
  """
  def __init__(self, experiment=None):
    if (experiment is not None):
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

  def setParam(self, paramName, paramVal, minVal=-np.inf, maxVal=np.inf, vary=True):
    assert paramName in self.params, (
      'Tried to add a parameter that is not defined in the model. '+
      'Please define a new extended model if you wish to add parameters.'
    )
    self.params[paramName].value = paramVal
    self.params[paramName].min = minVal
    self.params[paramName].max = maxVal
    self.params[paramName].vary = vary
    if (hasattr(self, 'ptrGui')):
      self.ptrGui.updateSlider(paramName)


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

  def updateParamsToFile(self):
    self.ptrGui.updateParamsVaryFromCheckbox()
    script_file_name = sys.argv[0]
    script_file = open(script_file_name, "r")
    script_file_string = ""
    for line in script_file:
      if "setParam" in line:
        if line.strip().startswith("#"):
          script_file_string += line
          continue

        prefix, suffix = line.split('setParam(', 1)
        parameter_name, suffix = suffix.split(',', 1)
        parameter_name = parameter_name.replace('"', '').replace("'", "")
        line_end = suffix.split(')')[-1]
        para_value = self.params[parameter_name].value
        para_min = self.params[parameter_name].min
        para_max = self.params[parameter_name].max
        para_vary = self.params[parameter_name].vary
        script_file_string += (
          prefix + 'setParam("' + parameter_name + '", ' +
          str(para_value) + ", " + " minVal = " + str(para_min) + ", " +
            "maxVal = " + str(para_max) + ", " + "vary = " + str(para_vary) +
            ")" + line_end
        )
      else:
        script_file_string += line
    script_file.close()
    script_file = open(script_file_name, "w")
    script_file.write(script_file_string)
    script_file.close()
    print("Updated script file: " + script_file_name)