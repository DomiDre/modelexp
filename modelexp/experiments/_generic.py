from ._experiment import Experiment
from ..data import Data
from ..models import Model

class Generic(Experiment):

  def setAxProps(self):
    self.ax.set_xlabel(r'$\mathit{x}$')
    self.ax.set_ylabel(r'$\mathit{y}$')
    self.ptrGui.plotWidget.draw_idle()# .tight_layout()

  def residuum(self, p):
    return self.data.getValues() - self.model.getValues(p)

  def adjustAxToAddedData(self):
    x_data = self.data.getDomain()
    y_data = self.data.getValues()
    self.ax.set_xlim(min(x_data), max(x_data))
    self.ax.set_xlim(min(y_data), max(y_data))

  def adjustAxToAddedModel(self):
    if not hasattr(self, 'data'):
      x_model = self.model.getDomain()
      y_model = self.model.getValues()
      self.ax.set_xlim(min(x_model), max(x_model))
      self.ax.set_xlim(min(y_model), max(y_model))

  def saveModelDataToFile(self, f):
    pass