from ._fit import Fit
import lmfit

class LevenbergMarquardt(Fit):
  def fit(self, print_result=True):
    fit_result = lmfit.minimize(
      self.ptrExperiment.residuum, self.ptrModel.params, method='leastsq'
    )

    if (print_result):
      lmfit.fit_report(fit_result)

    # Update the parameters of model
    self.ptrModel.params = fit_result.params
    self.ptrModel.updateModel()
    self.ptrGui.update()
    return fit_result