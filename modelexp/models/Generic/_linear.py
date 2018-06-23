from .._model import Model
from lmfit import Parameters

class Linear(Model):
  def defineDomain(self, x):
    '''
    On which space should the model be evaluated
    '''
    self.x = x

  def defineParameters(self, a0, b0):
    self.params = Parameters()
    self.params.add('a', a0) # slope
    self.params.add('b', b0) # y value at x=0

  def calcModel(self):
    '''
    How to calculate the model on the defined domain
    '''
    self.y = self.params['a']*self.x + self.params['b']

  def plotModel(self, ptrGui):
    super().plotModel(ptrGui)
    self.ax.plot(self.x, self.y)