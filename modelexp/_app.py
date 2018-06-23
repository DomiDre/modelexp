import inspect, sys
import PyQt5.QtWidgets as qt5w
from .gui._gui import Gui
from .models._model import Model
from .data._data import Data
from .experiments._experiment import Experiment
from .fit._fit import Fit

class App():
  """
  Container class for everything. A model.py program consists of five submodules
  The submodules are initialized in the following order
  gui - the interface for the user to see data, model and call the fit
  experiment - defines the general display and structure of the data to expect
  data - the experimental data, how the data looks, how it can be loaded and how visualized
  model - the means to calculate a model for the data, how to visualize it and how to store it
  fit - the code to find parameters of a model such that it fits to the data best

  The five submodules know of each other and can communicate with each other via the Modelpy class
  """

  def __init__(self, _gui=None):
    """
    Initializes Modelpy. Called as first function when starting the program
    """
    self._app = qt5w.QApplication(sys.argv)

    self._experiment: Experiment = None
    self.data: Data = None
    self.model: Model = None
    self.fit: Fit = None

    self._gui:Gui = Gui if _gui is None else _gui
    self._gui = self._gui()

  def setExperiment(self, _experiment):
    """Tell the app which kind of experiment it should treat

    Parameters
    ----------
    _experiment : Experiment
      Class that describes how data and model of a certain experiment look like
    """
    assert(self._gui), "The gui must be set before setting the Experiment"
    assert issubclass(_experiment, Experiment), 'Your experiment must be a subclass of Experiment (and not initialized)'
    self._experiment: Experiment = _experiment(self._gui)
    self._experiment.setAxProps()

    self._gui.connectExperiment(self._experiment)

  def setData(self, _data):
    """Tell the app which kind of data it should treat

    Parameters
    ----------
    _data : Data
      Class that describes which format the data is of and how to plot it
    """
    assert(self._gui), "The GUI must be set and initialized."
    assert(self._experiment), "Set an Experiment first before setting data."
    assert issubclass(_data, Data), 'Your data must be a subclass of Data (and not initialized)'

    self.data = _data(self._gui, self._experiment)
    self._gui.connectData(self.data)
    self._experiment.connectData(self.data)

  def setModel(self, _model):
    """Tell the app which kind of model it should treat

    Parameters
    ----------
    _model : Model
      Class that describes how the model is calculated and displayed
    """
    assert(self._gui), "The GUI must be set and initialized."
    assert(self._experiment), "Set an Experiment first before setting a model."
    assert issubclass(_model, Model), 'Your model must be a subclass of Model (and not initialized)'

    # initialize the model and connect it to the gui and the experiment
    self.model = _model(self._gui, self._experiment)
    self._gui.connectModel(self.model)
    self._experiment.connectModel(self.model)

  def setFit(self, _fit):
    """Tell the app with which algorithm the data should be fitted

    Parameters
    ----------
    _fit : Fit
      Class that describes how to find the best parameters of a model for a dataset
    """
    assert(self._gui), 'The GUI must be set and initialized'
    assert(self._experiment), 'Set the Experiment before setting the Fit routine'
    assert(self.data), 'Set the data before setting the Fit routine'
    assert(self.model), 'Set the model before setting the Fit routine'
    assert issubclass(_fit, Fit), 'Your fit routine must be a subclass of Fit (and not initialized)'
    self.fit = _fit(self._gui, self._experiment, self.data, self.model)
    self._gui.connectFit(self.fit)

  def show(self):
    if(self.model):
      self.model.calcModel()
      self.model.plotModel()
    self._gui.setWindowTitle("ModelExp")
    self._gui.show()
    self._app.exec_()