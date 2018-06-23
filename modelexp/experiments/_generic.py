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