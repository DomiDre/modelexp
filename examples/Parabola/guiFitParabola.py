import modelexp
from modelexp.experiments import Generic
from modelexp.models.Generic import Parabola
from modelexp.data import XyeData
from modelexp.fit import LevenbergMarquardt

app = modelexp.App()

app.setExperiment(Generic)

dataRef = app.setData(XyeData)
dataRef.loadFromFile('./parabolaData.xye')
dataRef.plotData()

modelRef = app.setModel(Parabola)
modelRef.setParameters(1.5, 0.3, 2)
modelRef.setParamLimits('a', -5, 5)
modelRef.setParamLimits('x0', -3, 3)
modelRef.setParamLimits('c', -2, 2)

app.setFit(LevenbergMarquardt)

app.show()