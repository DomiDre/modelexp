from ._refl import Reflectometry

class PolarizedReflectometry(Reflectometry):
  def __init__(self):
    super().__init__()
    self.nDatasets = 2
    self.datasetSpecificParams = {
      'polarization': ['p', 'm']
      }

  def setParameters(self):
    self.model.params['polarization_p'].value = 1
    self.model.params['polarization_m'].value = -1
