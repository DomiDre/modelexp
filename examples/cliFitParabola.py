import modelexp
from modelexp.experiments import Generic, SAXS
from modelexp.models.Generic import Parabola
from modelexp.data import XyeData
from modelexp.fit import LevenbergMarquardt
import numpy as np
import random

app = modelexp.Cli()

app.setExperiment(Generic)

modelRef = app.setModel(Parabola)
modelRef.defineDomain(np.linspace(-3, 3, 100))
modelRef.setParameters(1.5, 0.3, 2)

dataRef = app.setData(XyeData)
dataRef.loadFromFile('./parabolaData.xye')

fitRef = app.setFit(LevenbergMarquardt)

fitRef.fit()