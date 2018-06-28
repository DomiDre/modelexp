from ._sas import Sas

class Sanspol(Sas):
  def __init__(self):
    super().__init__()

    self.nDatasets = 4
    self.datasetSpecificParams = {
      'dTheta': ['sa', 'la'],
      'polarization': ['p', 'm']
      }

  def setParameters(self):
    self.model.params['polarization_p'].value = 1
    self.model.params['polarization_m'].value = -1

