from ._data import Data

class DataContainer():
  '''
  Container class to hold multiple Data objects.
  Depending on the experiment multiple datasets are stored in the container.
  '''
  def __init__(self, dataClass, experiment=None):
    assert issubclass(dataClass, Data), 'The data class has to be derived from Data'
    self.dataClass = dataClass
    self.nDatasets = 0 # number of datasets
    self.datasets = []

    if (experiment is not None):
      self.ptrExperiment = experiment
      self.ptrExperiment.connectData(self)

  def connectGui(self, gui):
    self.ptrGui = gui
    self.fig = self.ptrGui.plotWidget.getFig()
    self.ax = self.ptrGui.plotWidget.getDataAx()

  def getDataset(self, i):
    return self.datasets[i]

  def loadFromFile(self, filename, suffix=None):
    newData = self.dataClass()
    newData.loadFromFile(filename)
    if suffix is None:
      suffix = f'{self.nDatasets}'
    newData.suffix = suffix
    self.nDatasets += 1
    self.datasets.append(newData)

  def plotData(self):
    for i in range(self.nDatasets):
      self.getDataset(i).plotData(self.ax)
    self.ptrExperiment.adjustAxToAddedData()

  def draw(self):
    self.ptrGui.update()
