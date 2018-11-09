from ._genericModel1d import GenericModel1d

class Lorentzian(GenericModel1d):
  '''
  Model to describe a parabola
  '''

  def initParameters(self):
    self.params.add('a', 1) # Amplitude of parabola
    self.params.add('x0', 1) # center of parabola
    self.params.add('gamma', 1) # fwhm
    self.params.add('offset', 0) # offset

  def calcModel(self):
    self.y = (
      self.params['a']/(1 + 4*((self.x - self.params['x0']) / self.params['gamma'])**2)
      + self.params['offset']
    )
