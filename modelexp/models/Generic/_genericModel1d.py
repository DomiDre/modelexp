from .._model import Model

class GenericModel1d(Model):
  """Class for models that are defined over one dimension

  Parameters
  ----------
  Model : Model
    Base Abstract class
  """
  def __init__(self, experiment):
    self.x = None
    self.y = None
    self.modelPlot = None
    super().__init__(experiment)

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