import modelexp
from modelexp.models import Parabola
from modelexp.experiments import SAXS
import numpy as np


app = modelexp.App()

app.setExperiment(SAXS)


# model = Parabola()
# model.defineDomain(np.linspace(-3, 3, 100))
# app.setModel(model)


app.show()