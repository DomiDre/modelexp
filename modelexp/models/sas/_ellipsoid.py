from modelexp.models.sas import SAXSModel
from fortSAS import ellipsoid

class Ellipsoid(SAXSModel):
  def initParameters(self):
    self.params.add('l', 100)
    self.params.add('r', 100)
    self.params.add('alpha', 100)
    self.params.add('sldEllipsoid', 40e-6)
    self.params.add('sldSolvent', 10e-6)
    self.params.add('sigL', 0.0)
    self.params.add('sigR', 0.0)
    self.params.add('sigAlpha', 0.0)
    self.params.add('i0', 1)
    self.params.add('bg', 1e-6)


  def calcModel(self):
    self.I = self.params['i0'] * ellipsoid.formfactor(
      self.q,
      self.params['l'],
      self.params['r'],
      self.params['alpha'],
      self.params['sldEllipsoid'],
      self.params['sldSolvent'],
      self.params['sigL'],
      self.params['sigR'],
      self.params['sigAlpha'],
    ) + self.params['bg']

    self.r, self.sld = ellipsoid.sld(
      self.params['l'],
      self.params['sldEllipsoid'],
      self.params['sldSolvent']
    )
