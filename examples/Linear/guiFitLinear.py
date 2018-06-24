import modelexp
from modelexp.experiments import Generic
from modelexp.models.Generic import Linear
from modelexp.data import XyeData
from modelexp.fit import LevenbergMarquardt

app = modelexp.App()

app.setExperiment(Generic)

dataRef = app.setData(XyeData)
dataRef.loadFromFile('./linearData.xye')
dataRef.plotData()

modelRef = app.setModel(Linear)
modelRef.setParameters(1.5, 1)
modelRef.setParamLimits('m', -5, 5)
modelRef.setParamLimits('y0', -10, 10)

app.setFit(LevenbergMarquardt)

app.show()