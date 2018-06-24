import modelexp
from modelexp.experiments import Generic
from modelexp.models.Generic import Linear
from modelexp.data import XyeData
from modelexp.fit import LevenbergMarquardt
import numpy as np
import random

app = modelexp.Cli()

app.setExperiment(Generic)

dataRef = app.setData(XyeData)
dataRef.loadFromFile('./linearData.xye')

modelRef = app.setModel(Linear)

fitRef = app.setFit(LevenbergMarquardt)

fitRef.fit()