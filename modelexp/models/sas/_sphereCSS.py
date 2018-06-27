from modelexp.models.sas import SAXSModel
from fortSAS import sphere_css

class SphereCSS(SAXSModel):
  def initParameters(self):
    self.params.add('r', 100)
    self.params.add('dShell', 30)
    self.params.add('dSurfactant', 20)
    self.params.add('sldCore', 40e-6)
    self.params.add('sldShell', 30e-6)
    self.params.add('sldSurfactant', 40e-6)
    self.params.add('sldSolvent', 10e-6)
    self.params.add('sigR', 0.05)
    self.params.add('sigDShell', 0)
    self.params.add('sigDSurfactant', 0)
    self.params.add('i0', 1)
    self.params.add('bg', 1e-6)


  def calcModel(self):
    self.I = self.params['i0'] * sphere_css.formfactor(
      self.q,
      self.params['r'],
      self.params['dShell'],
      self.params['dSurfactant'],
      self.params['sldCore'],
      self.params['sldShell'],
      self.params['sldSurfactant'],
      self.params['sldSolvent'],
      self.params['sigR'],
      self.params['sigDShell'],
      self.params['sigDSurfactant']
    ) + self.params['bg']

    self.r, self.sld = sphere_css.sld(
      self.params['r'],
      self.params['dShell'],
      self.params['dSurfactant'],
      self.params['sldCore'],
      self.params['sldShell'],
      self.params['sldSurfactant'],
      self.params['sldSolvent'],
    )
