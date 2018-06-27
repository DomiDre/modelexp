from .._model import Model
from .._decoration import Decoration

import numpy as np
from fortSAS import math

class InstrumentalResolution(Decoration):
  """Decorator class that takes the output of a model class and adds parameters
  for instrumental resolution and smear it out

  Parameters
  ----------
  Model : Model
    Base Abstract class
  """
  def __init__(self, model):
    self.ptrModel = Model # define which class ptrModel has

    self.ptrModel = model
    self.ptrModel.params.add('dTheta', 1e-3, min=0)
    self.ptrModel.params.add('wavelength', 1.34145, min=0)
    self.ptrModel.params.add('dWavelengthRelative', 0.05, min=0)

  def apply(self):
    '''
    Define how to modify the
    '''
    q = self.ptrModel.getDomain()
    Imodel = self.ptrModel.getValues()
    sigQ = np.sqrt(
      (self.ptrModel.params['dWavelengthRelative'] * q)**2 +
      (4 * np.pi / self.ptrModel.params['wavelength'] * self.ptrModel.params['dTheta'])**2
    )

    return math.resolution_smear(q, Imodel, sigQ)