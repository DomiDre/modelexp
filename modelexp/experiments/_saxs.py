from ._experiment import Experiment
# from ..data._xyeData import XyeData
# from ..models._model import Model

class SAXS(Experiment):
  def setData(self, data):
    self.data = data

  def setModel(self, model):
    self.model = model

  def setAxProps(self, ptrGui):
    self.fig = ptrGui.plotWidget.getFig()
    self.ax = ptrGui.plotWidget.getDataAx()

    self.ax.set_xlabel(r'$\mathit{q} \, / \, \AA^{-1}$')
    self.ax.set_ylabel(r'$\mathit{I} \, / \, cm^{-1}$')
    self.ax.set_xscale('log')
    self.ax.set_yscale('log')
    ptrGui.plotWidget.draw_idle()# .tight_layout()

