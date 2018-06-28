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

  def initMagneticParameters(self):
    self.params.add('magSldSuperball', 5e-6, min=0)
    self.params.add('magSldSolvent', 0, vary=False)

    self.addConstantParam('magSldSolvent')

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

  def calcMagneticModel(self):
    self.I = self.params['i0'] * superball.magnetic_formfactor(
      self.q,
      self.params['r'],
      self.params['pVal'],
      self.params['sldSuperball'],
      self.params['sldSolvent'],
      self.params['sigR'],
      self.params['magSldSuperball'],
      self.params['magSldSolvent'],
      self.params['xi'],
      self.params['sin2alpha'],
      self.params['polarization'],
      self.x_herm, self.w_herm, self.x_leg, self.w_leg
    ) + self.params['bg']

    self.r, self.sld = superball.sld(
      self.params['r'],
      self.params['sldSuperball'],
      self.params['sldSolvent']
    )

    self.rMag, self.sldMag = superball.sld(
      self.params['r'],
      self.params['magSldSuperball'],
      self.params['magSldSolvent'],
    )
