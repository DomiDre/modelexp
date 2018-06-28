from .._experiment import Experiment
import numpy as np
from ...gui.plotWidgetInset import PlotWidgetInset

class Saxs(Experiment):
  def __init__(self):
    super().__init__()
    self.plotWidgetClass = PlotWidgetInset

  def connectGui(self, gui):
    self.ptrGui = gui
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
    self.model.params = p
    self.model.updateModel()
    data0 = self.data.getDataset(0)
    model0 = self.model.getModelset(0)
    I_data0 = data0.getValues()
    I_error0 = data0.getErrors()
    I_model0 = model0.getValues()
    return (np.log(I_data0) - np.log(I_model0)) * I_data0 / I_error0

  def adjustAxToAddedData(self):
    data = self.data.getDataset(0)
    q_data = data.getDomain()
    I_data = data.getValues()
    self.ax.set_xlim(min(q_data), max(q_data))
    self.ax.set_ylim(min(I_data)*0.8, max(I_data)*1.2)

  def adjustAxToAddedModel(self):
    model = self.model.getModelset(0)
    if not hasattr(self, 'data'):
      q_model = model.getDomain()
      I_model = model.getValues()
      self.ax.set_xlim(min(q_model), max(q_model))
      self.ax.set_ylim(min(I_model), max(I_model))

    r_model = model.r
    sld_model = model.sld
    self.axInset.set_xlim(min(r_model)/10, max(r_model)/10)
    self.axInset.set_ylim(0, max(sld_model)/1e-6*1.2)

  def saveModelDataToFile(self, f):
    if hasattr(self, 'data') and hasattr(self, 'model'):
      data = self.data.getDataset(0)
      model = self.model.getModelset(0)
      q_data = data.getDomain()
      I_data = data.getValues()
      sI_data = data.getErrors()
      q_model = model.getDomain()
      I_model = model.getValues()
      assert(len(q_data) == len(q_model), 'Data and Model do not have the same length.')
      f.write('#q / A-1\tI / cm-1\tsI / cm-1\tImodel / cm-1\n')
      for i in range(len(q_data)):
        assert(np.isclose(q_data[i], q_model[i]), 'Data and Model arrays are not defined on same domain' )
        f.write(f'{q_data[i]}\t{I_data[i]}\t{sI_data[i]}\t{I_model[i]}\n')
    elif hasattr(self, 'data'):
      data = self.data.getDataset(0)
      q_data = data.getDomain()
      I_data = data.getValues()
      sI_data = data.getErrors()
      f.write('#q / A-1\tI / cm-1\tsI / cm-1\n')
      for i in range(len(q_data)):
        f.write(f'{q_data[i]}\t{I_data[i]}\t{sI_data[i]}\n')
    elif hasattr(self, 'model'):
      model = self.model.getModelset(0)
      q_model = model.getDomain()
      I_model = model.getValues()
      f.write('#q / A-1\tImodel / cm-1\n')
      for i in range(len(q_model)):
        f.write(f'{q_model[i]}\t{I_model[i]}\n')