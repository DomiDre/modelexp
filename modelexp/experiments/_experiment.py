from abc import ABCMeta, abstractmethod
class Experiment(metaclass=ABCMeta):
  """
  Abstract class to describe an experiment.
  A complete experiment consists of experimental data and/or a model of it
  """
  def __init__(self):
    """Set plotWidgetClass here to change it before it's initialized in between
    initialization of Experiment and connectGui
    """
    self.plotWidgetClass = None

    self.nDatasets = 1
    self.datasetSpecificParams = []

  def connectGui(self, gui):
    self.ptrGui = gui
    self.fig = self.ptrGui.plotWidget.getFig()
    self.ax = self.ptrGui.plotWidget.getDataAx()

  def connectData(self, data):
    self.data = data

  def connectModel(self, model):
    self.model = model

  @abstractmethod
  def setAxProps(self):
    pass

  @abstractmethod
  def residuum(self):
    """Returns the distance between data and model. Should take the parameter
    of the model as argument and update the model values
    on call according to the given parameters
    """

  @abstractmethod
  def adjustAxToAddedData(self):
    """Called when Data is added to the experiment for a GUI App,
    to adjust that the data is displayed accordingly.
    """
    pass

  @abstractmethod
  def adjustAxToAddedModel(self):
    """Called when Model is added to the experiment for a GUI App,
    to adjust that the model is displayed accordingly.
    """
    pass

  @abstractmethod
  def saveModelDataToFile(self):
    """Define how data and model is stored to file
    """
    pass