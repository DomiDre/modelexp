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
      q_model = self.model.getDomain()
      I_model = self.model.I
      self.ax.set_xlim(min(q_model), max(q_model))
      self.ax.set_ylim(min(I_model), max(I_model))

    r_model = self.model.r
    sld_model = self.model.sld
    self.axInset.set_xlim(min(r_model)/10, max(r_model)/10)
    self.axInset.set_ylim(0, max(sld_model)/1e-6*1.2)

  def saveModelDataToFile(self, f):
    if hasattr(self, 'data') and hasattr(self, 'model'):
      q_data = self.data.getDomain()
      I_data = self.data.getValues()
      sI_data = self.data.getErrors()
      q_model = self.model.getDomain()
      I_model = self.model.I
      assert(len(q_data) == len(q_model), 'Data and Model do not have the same length.')
      f.write('#q / A-1\tI / cm-1\tsI / cm-1\t Imodel / cm-1\n')
      for i in range(len(q_data)):
        assert(np.isclose(q_data[i], q_model[i]), 'Data and Model arrays are not defined on same domain' )
        f.write(f'{q_data[i]}\t{I_data[i]}\t{sI_data[i]}\t{I_model[i]}\n')
    elif hasattr(self, 'data'):
      q_data = self.data.getDomain()
      I_data = self.data.getValues()
      sI_data = self.data.getErrors()
      f.write('#q / A-1\tI / cm-1\tsI / cm-1\n')
      for i in range(len(q_data)):
        f.write(f'{q_data[i]}\t{I_data[i]}\t{sI_data[i]}\n')
    elif hasattr(self, 'model'):
      q_model = self.model.getDomain()
      I_model = self.model.I
      f.write('#q / A-1\tImodel / cm-1\n')
      for i in range(len(q_model)):
        f.write(f'{q_model[i]}\t{I_model[i]}\n')