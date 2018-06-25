from ._experiment import Experiment
from ..data import Data
from ..models import Model

import numpy as np
class Generic(Experiment):

  def setAxProps(self):
    self.ax.set_xlabel(r'$\mathit{x}$')
    self.ax.set_ylabel(r'$\mathit{y}$')
    self.ptrGui.plotWidget.draw_idle()# .tight_layout()

  def residuum(self, p):
    return (self.data.getValues() - self.model.getValues(p)) / self.data.getErrors()

  def adjustAxToAddedData(self):
    x_data = self.data.getDomain()
    y_data = self.data.getValues()
    self.ax.set_xlim(min(x_data), max(x_data))
    self.ax.set_ylim(min(y_data), max(y_data))

  def adjustAxToAddedModel(self):
    if not hasattr(self, 'data'):
      x_model = self.model.getDomain()
      y_model = self.model.getValues()
      self.ax.set_xlim(min(x_model), max(x_model))
      self.ax.set_ylim(min(y_model), max(y_model))

  def saveModelDataToFile(self, f):
    if hasattr(self, 'data') and hasattr(self, 'model'):
      x_data = self.data.getDomain()
      y_data = self.data.getValues()
      sy_data = self.data.getErrors()
      x_model = self.model.getDomain()
      y_model = self.model.getValues()
      assert(len(x_data) == len(x_model), 'Data and Model do not have the same length.')
      f.write('#x\ty\tsy\tymodel\n')
      for i in range(len(x_data)):
        assert(np.isclose(x_data[i], x_model[i]), 'Data and Model arrays are not defined on same domain' )
        f.write(f'{x_data[i]}\t{y_data[i]}\t{sy_data[i]}\t{y_model[i]}\n')
    elif hasattr(self, 'data'):
      x_data = self.data.getDomain()
      y_data = self.data.getValues()
      sy_data = self.data.getErrors()
      f.write('#x\ty\tsy\n')
      for i in range(len(x_data)):
        f.write(f'{x_data[i]}\t{y_data[i]}\t{sy_data[i]}\n')
    elif hasattr(self, 'model'):
      x_model = self.model.getDomain()
      y_model = self.model.getValues()
      f.write('#x\tymodel\n')
      for i in range(len(x_model)):
        f.write(f'{x_model[i]}\t{y_model[i]}\n')