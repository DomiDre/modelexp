from .._model import Model

class SAXSModel(Model):
  """Class for models that are defined over one dimension

  Parameters
  ----------
  Model : Model
    Base Abstract class
  """
  def __init__(self, experiment):
    self.q = None
    self.I = None
    self.r = None
    self.sld = None
    self.modelPlot = None
    self.sldPlot = None
    super().__init__(experiment)

  def connectGui(self, gui):
    self.ptrGui = gui
    self.fig = self.ptrGui.plotWidget.getFig()
    self.ax, self.axInset = self.ptrGui.plotWidget.getAllAx()

  def defineDomain(self, q):
    '''
    On which space should the model be evaluated
    '''
    self.q = q

  def getDomain(self):
    return self.q

  def getValues(self, p):
    self.params = p
    self.calcModel()
    return self.I

  def getSld(self):
    return self.sld

  def plotModel(self):
    '''
    Define how to plot the model
    '''
    if self.modelPlot:
      self.modelPlot.set_ydata(self.I)
      self.sldPlot.set_xdata(self.r / 10)
      self.sldPlot.set_ydata(self.sld / 1e-6)
    else:
      self.modelPlot, = self.ax.plot(
        self.q, self.I, marker='None', color='black', zorder=10
      )
      self.sldPlot, = self.axInset.plot(
        self.r / 10, self.sld / 1e-6, marker='None', color='black', zorder=10
      )
      self.ptrExperiment.adjustAxToAddedModel()

  def updateModel(self):
    '''
    How to update the model when parameters are changed
    '''
    self.calcModel()
    self.plotModel()