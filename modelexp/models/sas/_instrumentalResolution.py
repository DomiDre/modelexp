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
    self.ptrModel.params.add('dTheta', 1e-4, min=0, max=1e-3)
    self.ptrModel.params.add('wavelength', 1.34145, min=1, max= 10, vary = False)
    self.ptrModel.params.add('dWavelength', 0.05, min=0, max=0.1)

  def apply(self, q, Imodel):
    '''
    Define how to modify the
    '''
    sigQ = np.sqrt(
      (self.ptrModel.params['dWavelength'] * q)**2 +
      (4 * np.pi / self.ptrModel.params['wavelength'] * self.ptrModel.params['dTheta'])**2
    )
    return math.resolution_smear(q, Imodel, sigQ)