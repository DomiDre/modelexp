from ._fit import Fit
import lmfit

class LevenbergMarquardt(Fit):
  def fit(self):
    fit_result = lmfit.minimize(
      self.ptrExperiment.residuum, self.ptrModel.params, method='leastsq'
    )
    print(lmfit.fit_report(fit_result))

    # Update the parameters of model
    self.ptrModel.params = fit_result.params
    return fit_result