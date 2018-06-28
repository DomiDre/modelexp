from ._model import Model
import sys
from lmfit import Parameters
import numpy as np
from ._decoration import Decoration

try:
  from ..experiments import Experiment
except ImportError:
  pass

class ModelContainer():
  '''
  Container class to hold multiple Model objects.
  Depending on the experiment multiple datasets are stored in the container.
  '''
  def __init__(self, modelClass, experiment=None, decoration=None, gui=None):
    assert issubclass(modelClass, Model), 'The model class has to be derived from Model'
    self.modelClass = modelClass
    self.nModelsets = 0 # number of datasets
    self.modelsets = []

    self.decoration = decoration

    self.params = Parameters() # empty parameter container

    if gui is not None:
      self.connectGui(gui)

    if (experiment is not None): #if experiment is defined
      self.ptrExperiment = experiment

      # check whether data was already loaded
      if (hasattr(self.ptrExperiment, 'data')):
        # add for every loaded dataset a modelset on respective domain
        for i in range(self.ptrExperiment.data.nDatasets):
          data = self.ptrExperiment.data.getDataset(i)
          self.addModel(data.getDomain(), data.suffix)

  def addModel(self, domain, suffix=''):
    newModel = self.modelClass()
    newModel.defineDomain(domain)
    newModel.initParameters()
    if (self.decoration is not None) and issubclass(self.decoration, Decoration):
      newModel._setDecoration(self.decoration)
    newModel.suffix = suffix
    self.modelsets.append(newModel)
    self.nModelsets += 1

    # when as much models have been added as expected for the experiment
    # -> initialize the parameters
    if self.nModelsets == self.ptrExperiment.nDatasets:
      self.initParameters()

      # if gui is available connect and thereby initialize the parameter sliders
      if hasattr(self, 'ptrGui'):
        self.ptrGui.connectModel(self)
        for i in range(self.nModelsets):
          self.getModelset(i).connectGui(self.ptrGui)

  def initParameters(self):
    datasetSpecificParams = self.ptrExperiment.datasetSpecificParams
    addedParams = []

    for i in range(self.nModelsets):
      model = self.getModelset(i)
      params = model.params
      for parameter in params:
        p = params[parameter]
        if parameter in datasetSpecificParams:
          self.params.add(
            parameter + '_' + model.suffix, p.value,
            min=p.min, max=p.max, vary=p.vary
          )
        elif parameter in addedParams:
          continue
        else:
          self.params.add(p)

  def connectGui(self, gui):
    self.ptrGui = gui

  def getParameters(self):
    return self.params

  def getModelset(self, i):
    return self.modelsets[i]

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

  def plotModel(self):
    for i in range(self.nModelsets):
      self.getModelset(i).plotModel()

  def updateModel(self):
    # create a parameter container for each sub model respectively
    p = Parameters()
    for parameter in self.params:
      if not parameter in self.ptrExperiment.datasetSpecificParams:
        p.add(self.params[parameter])

    for i in range(self.nModelsets):
      subModel = self.getModelset(i)

      subP = p.copy()
      for parameter in self.ptrExperiment.datasetSpecificParams:
        suffixParameter = parameter + '_' + subModel.suffix
        if suffixParameter in self.params:
          specParam = self.params[suffixParameter]
          subP.add(
            parameter, specParam.value,
            min=specParam.min, max=specParam.max, vary=specParam.vary
          )
      subModel.params = subP
      subModel.calcDecoratedModel()

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

  def calcModel(self):
    for i in range(self.nModelsets):
      self.getModelset(i).calcDecoratedModel()