from .._experiment import Experiment
import numpy as np

class SAXS(Experiment):

  def setAxProps(self):
    self.ax.set_xlabel(r'$\mathit{q} \, / \, \AA^{-1}$')
    self.ax.set_ylabel(r'$\mathit{I} \, / \, cm^{-1}$')
    self.ax.set_xscale('log')
    self.ax.set_yscale('log')
    self.ptrGui.plotWidget.draw_idle()# .tight_layout()

  def residuum(self, p):
    Idata = self.data.getValues()
    Ierror = self.data.getErrors()
    Imodel = self.model.getValues(p)
    return (
      (np.log(Idata) - np.log(Imodel)) * Idata / Ierror
    )