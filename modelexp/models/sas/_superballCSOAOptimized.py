from modelexp.models.sas import SAXSModel
from fortSAS import superball_new_cs, sphere

import numpy as np
from numpy.polynomial.hermite import hermgauss
from numpy.polynomial.legendre import leggauss

class SuperballCSOAOptimized(SAXSModel):
  def initParameters(self):
    self.params.add('r', 100)
    self.params.add('d', 20)
    self.params.add('pVal', 2.3)
    self.params.add('pShell', 2.3)
    self.params.add('sldCore', 40e-6)
    self.params.add('sldShell', 8e-6)
    self.params.add('sldSolvent', 10e-6)
    self.params.add('sigR', 0.)
    self.params.add('i0', 1)
    self.params.add('bg', 1e-6)
    self.params.add('orderHermite', 20)
    self.params.add('orderLegendre', 20)
    self.addConstantParam('orderHermite')
    self.addConstantParam('orderLegendre')
    self.params.add('i0Oleic', 1)
    self.params.add('rOleic', 20)

  def initMagneticParameters(self):
    self.params.add('magSldCore', 5e-6, min=0)
    self.params.add('magSldShell', 0, min=0, vary=False)
    self.params.add('magSldSolvent', 0, vary=False)

    self.addConstantParam('magSldShell')
    self.addConstantParam('magSldSolvent')

  def calcModel(self):
    self.x_herm, self.w_herm = hermgauss(int(self.params['orderHermite']))
    self.x_leg, self.w_leg = leggauss(int(self.params['orderLegendre']))

    self.I = self.params['i0'] * superball_new_cs.formfactor(
      self.q,
      self.params['r'],
      self.params['d'],
      self.params['pVal'],
      self.params['pShell'],
      self.params['sldCore'],
      self.params['sldShell'],
      self.params['sldSolvent'],
      self.params['sigR'],
      self.x_herm, self.w_herm, self.x_leg, self.w_leg
    ) + self.params['i0Oleic'] * sphere.formfactor(
      self.q,
      self.params['rOleic'],
      self.params['sldShell'],
      self.params['sldSolvent'],
      0
    ) + self.params['bg']

    r1, sld1 = superball_new_cs.sld(
      self.params['r'],
      self.params['d'],
      self.params['sldCore'],
      self.params['sldShell'],
      self.params['sldSolvent']
    )
    r2, sld2 = sphere.sld(
      self.params['rOleic'],
      self.params['sldShell'],
      self.params['sldSolvent']
    )
    self.r = np.concatenate([r1, r1[::-1], r2])
    self.sld = np.concatenate([sld1, sld1[::-1], sld2])


  def calcMagneticModel(self):
    self.x_herm, self.w_herm = hermgauss(int(self.params['orderHermite']))
    self.x_leg, self.w_leg = leggauss(int(self.params['orderLegendre']))

    self.I = self.params['i0'] * superball_new_cs.magnetic_formfactor(
      self.q,
      self.params['r'],
      self.params['d'],
      self.params['pVal'],
      self.params['pShell'],
      self.params['sldCore'],
      self.params['sldShell'],
      self.params['sldSolvent'],
      self.params['sigR'],
      self.params['magSldCore'],
      self.params['magSldShell'],
      self.params['magSldSolvent'],
      self.params['xi'],
      self.params['sin2alpha'],
      self.params['polarization'],
      self.x_herm, self.w_herm, self.x_leg, self.w_leg
    ) + self.params['i0Oleic'] * sphere.formfactor(
      self.q,
      self.params['rOleic'],
      self.params['sldShell'],
      self.params['sldSolvent'],
      0
    ) + self.params['bg']

    r1, sld1 = superball_new_cs.sld(
      self.params['r'],
      self.params['d'],
      self.params['sldCore'],
      self.params['sldShell'],
      self.params['sldSolvent']
    )

    r2, sld2 = sphere.sld(
      self.params['rOleic'],
      self.params['sldShell'],
      self.params['sldSolvent']
    )
    self.r = np.concatenate([r1, r1[::-1], r2])
    self.sld = np.concatenate([sld1, sld1[::-1], sld2])

    rMag1, sldMag1 = superball_new_cs.sld(
      self.params['r'],
      self.params['d'],
      self.params['magSldCore'],
      self.params['magSldShell'],
      self.params['magSldSolvent'],
    )

    rMag2, sldMag2 = sphere.sld(
      self.params['rOleic'],
      0,
      0
    )
    self.rMag = np.concatenate([rMag1, rMag1[::-1], rMag2])
    self.sldMag = np.concatenate([sldMag1, sldMag1[::-1], sldMag2])