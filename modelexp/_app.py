from ._gui.gui import Gui

class App():
  """
  Container class for everything. A model.py program consists of four submodules
  data - the experimental data, how the data looks, how it can be loaded and how visualized
  model - the means to calculate a model for the data, how to visualize it and how to store it
  fit - the code to find parameters of a model such that it fits to the data best
  gui - the interface for the user to see data, model and call the fit

  The four submodules know of each other and can communicate with each other via the Modelpy class
  """

  def __init__(self):
    """
    Initializes Modelpy. Called as first function when starting the program
    """
    self._data = None
    self._model = None
    self._fit = None
    self._gui = None

  def setData(self, _data):
    self._data = _data

  def setModel(self, _model):
    self._model = _model

  def setFit(self, _fit):
    self._fit = _fit

  def setGui(self, _gui):
    self._gui = _gui

  def initGui(self):
    if not self._gui:
      self._gui = Gui

    if self._gui:
      self._gui()

# if __name__ == '__main__':
#   model = modelexp()
#   model.initGui()
