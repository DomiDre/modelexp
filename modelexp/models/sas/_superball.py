from modelexp.models.sas import SAXSModel
from fortSAS import superball

from numpy.polynomial.hermite import hermgauss
from numpy.polynomial.legendre import leggauss

class Superball(SAXSModel):
  def __init__(self):
    super().__init__()
    self.x_herm, self.w_herm = hermgauss(15)
    self.x_leg, self.w_leg = leggauss(10)

  def initParameters(self):
    self.params.add('r', 100)
    self.params.add('pVal', 2.3)
    self.params.add('sldSuperball', 40e-6)
    self.params.add('sldSolvent', 10e-6)
    self.params.add('sigR', 0.)
    self.params.add('i0', 1)
    self.params.add('bg', 1e-6)


  def calcModel(self):
    self.I = self.params['i0'] * superball.formfactor(
      self.q,
      self.params['r'],
      self.params['pVal'],
      self.params['sldSuperball'],
      self.params['sldSolvent'],
      self.params['sigR'],
      self.x_herm, self.w_herm, self.x_leg, self.w_leg
    ) + self.params['bg']

    self.r, self.sld = superball.sld(
      self.params['r'],
      self.params['sldSuperball'],
      self.params['sldSolvent']
    )
