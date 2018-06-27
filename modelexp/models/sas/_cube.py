from ._saxsModel import SAXSModel
from fortSAS import cube

class Cube(SAXSModel):
  def initParameters(self):
    self.params.add('a', 100)
    self.params.add('sldCube', 40e-6)
    self.params.add('sldSolvent', 10e-6)
    self.params.add('sigA', 0.)
    self.params.add('i0', 1)
    self.params.add('bg', 1e-6)


  def calcModel(self):
    self.I = self.params['i0'] * cube.formfactor(
      self.q,
      self.params['a'],
      self.params['sldCube'],
      self.params['sldSolvent'],
      self.params['sigA']
    ) + self.params['bg']

    self.r, self.sld = cube.sld(
      self.params['a'],
      self.params['sldCube'],
      self.params['sldSolvent']
    )
