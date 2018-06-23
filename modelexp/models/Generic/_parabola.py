from .._model import Model
from lmfit import Parameters

class Parabola(Model):
  '''
  Model to describe a parabola
  Init defines
    ptrGui
    ptrExperiment
    fig
    ax
    p
    calls initParameters()
  '''

  def initParameters(self):
    '''
    Called by __init__ at creation of model
    '''
    self.params.add('a', 1) # Amplitude of parabola
    self.params.add('x0', 1) # center of parabola
    self.params.add('c', 1) # y value at x=x0

    self.modelPlot = None

  def defineDomain(self, x):
    '''
    On which space should the model be evaluated
    '''
    self.x = x

  def getDomain(self):
    return self.x

  def getValues(self, p):
    self.params = p
    self.calcModel()
    return self.y

  def setParameters(self, a0, x0, c0):
    '''
    Update the parameters
    '''
    self.params['a'].value = a0 # Amplitude of parabola
    self.params['x0'].value = x0 # center of parabola
    self.params['c'].value = c0 # y value at x=x0

  def calcModel(self):
    '''
    How to calculate the model on the defined domain
    '''
    self.y = self.params['a']*(self.x - self.params['x0'])**2 + self.params['c']

  def plotModel(self):
    '''
    Define how to plot the model
    '''
    if self.modelPlot:
      self.modelPlot.set_ydata(self.y)
    else:
      self.modelPlot, = self.ax.plot(
        self.x, self.y, marker='None', color='black', zorder=10
      )

  def updateModel(self):
    '''
    How to update the model when parameters are changed
    '''
    self.calcModel()
    self.plotModel()
    # self.modelPlot.set_ydata(self.y)