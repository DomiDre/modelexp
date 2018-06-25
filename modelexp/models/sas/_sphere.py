from ._saxsModel import SAXSModel
from fortSAS import sphere

class Sphere(SAXSModel):
  '''
  Model to describe the formfactor of a sphere
  '''
  def initParameters(self):
    self.params.add('R', 100)
    self.params.add('SLDsphere', 40e-6)
    self.params.add('SLDsolvent', 10e-6)
    self.params.add('sigR', 0)
    self.params.add('I0', 1)
    self.params.add('bg', 1e-6)


  def calcModel(self):
    self.I = self.params['I0'] * sphere.formfactor(
      self.q,
      self.params['R'],
      self.params['SLDsphere'],
      self.params['SLDsolvent'],
      self.params['sigR']
    ) + self.params['bg']

    self.r, self.sld = sphere.sld(
      self.params['R'],
      self.params['SLDsphere'],
      self.params['SLDsolvent']
    )