from .._experiment import Experiment
import numpy as np
from ...gui.plotWidgetInset import PlotWidgetInset

class Saxs(Experiment):
  def __init__(self):
    self.plotWidgetClass = PlotWidgetInset

  def connectGui(self, gui):
    self.ptrGui = gui
    self.ptrGui.layoutPlot
    self.fig = self.ptrGui.plotWidget.getFig()
    self.ax, self.axInset = self.ptrGui.plotWidget.getAllAx()

  def setAxProps(self):
    self.ax.set_xlabel(r'$\mathit{q} \, / \, \AA^{-1}$')
    self.ax.set_ylabel(r'$\mathit{I} \, / \, cm^{-1}$')
    self.ax.set_xscale('log')
    self.ax.set_yscale('log')

    self.axInset.set_xlabel(r"$\mathit{x} \, / \, \AA$")
    self.axInset.set_ylabel(r"$SLD$")

    self.ptrGui.plotWidget.draw_idle()# .tight_layout()

  def residuum(self, p):
    Idata = self.data.getValues()
    Ierror = self.data.getErrors()
    Imodel = self.model.getValues(p)
    return (
      (np.log(Idata) - np.log(Imodel)) * Idata / Ierror
    )

  def adjustAxToAddedData(self):
    q_data = self.data.getDomain()
    I_data = self.data.getValues()
    self.ax.set_xlim(min(q_data), max(q_data))
    self.ax.set_ylim(min(I_data)*0.8, max(I_data)*1.2)

  def adjustAxToAddedModel(self):
    if not hasattr(self, 'data'):
      x_model = self.model.getDomain()
      y_model = self.model.I
      self.ax.set_xlim(min(x_model), max(x_model))
      self.ax.set_ylim(min(y_model), max(y_model))

    r_model = self.model.r
    sld_model = self.model.sld
    self.axInset.set_xlim(min(r_model)/10, max(r_model)/10)
    self.axInset.set_ylim(0, max(sld_model)/1e-6*1.2)
