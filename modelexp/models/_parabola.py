from ._model import Model
from lmfit import Parameters

class Parabola(Model):
  def defineDomain(self, x):
    '''
    On which space should the model be evaluated
    '''
    self.x = x

  def defineParameters(self, a0, x0, c0):
    self.p = Parameters()
    self.p.add('a', a0) # Amplitude of parabola
    self.p.add('x0', x0) # center of parabola
    self.p.add('c', c0) # y value at x=x0

  def calcModel(self):
    '''
    How to calculate the model on the defined domain
    '''
    self.y = self.p['a']*(self.x - self.p['x0'])**2 + self.p['c']

  def plotModel(self, ptrGui):
    super().plotModel(ptrGui)
    self.ax.plot(self.x, self.y)