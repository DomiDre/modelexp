from ._saxsModel import SAXSModel
from fortSAS import sphere

class Sphere(SAXSModel):
  '''
  Model to describe the formfactor of a sphere
  '''
  def initParameters(self):
    self.params.add('r', 100)
    self.params.add('sldSphere', 40e-6)
    self.params.add('sldSolvent', 10e-6)
    self.params.add('sigR', 0)
    self.params.add('i0', 1)
    self.params.add('bg', 1e-6)


  def calcModel(self):
    self.I = self.params['i0'] * sphere.formfactor(
      self.q,
      self.params['r'],
      self.params['sldSphere'],
      self.params['sldSolvent'],
      self.params['sigR']
    ) + self.params['bg']

    self.r, self.sld = sphere.sld(
      self.params['r'],
      self.params['sldSphere'],
      self.params['sldSolvent']
    )