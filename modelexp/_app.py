import inspect, sys
import PyQt5.QtWidgets as qt5w

from ._gui.gui import Gui
from .models._model import Model
class App():
  """
  Container class for everything. A model.py program consists of four submodules
  data - the experimental data, how the data looks, how it can be loaded and how visualized
  model - the means to calculate a model for the data, how to visualize it and how to store it
  fit - the code to find parameters of a model such that it fits to the data best
  gui - the interface for the user to see data, model and call the fit

  The four submodules know of each other and can communicate with each other via the Modelpy class
  """

  def __init__(self, _gui=None):
    """
    Initializes Modelpy. Called as first function when starting the program
    """
    self.app = qt5w.QApplication(sys.argv)

    self._experiment = None
    self._data = None
    self._model = None
    self._fit = None

    self._gui = Gui if _gui is None else _gui
    self._gui = self._gui()

  def setExperiment(self, _experiment):
    if inspect.isclass(_experiment):
      _experiment = _experiment()
    self._experiment = _experiment
    self._experiment.setAxProps(self._gui)

  def setData(self, _data):
    assert(self._experiment), "Set an Experiment first before setting data."
    self._data = _data

  def setModel(self, _model):
    assert(self._experiment), "Set an Experiment first before setting a model."
    assert issubclass(_model, Model), 'Your model must be a subclass of Model'
    self._model = _model
    # self._gui.

  def setFit(self, _fit):
    self._fit = _fit

  def show(self):
    self._gui.setWindowTitle("ModelExp")
    self._gui.show()
    self.app.exec_()