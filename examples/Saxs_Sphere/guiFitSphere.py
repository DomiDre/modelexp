import modelexp
from modelexp.experiments.Sas import Saxs
from modelexp.models.Sas import Sphere
from modelexp.data import XyeData
from modelexp.fit import LevenbergMarquardt

app = modelexp.App()

app.setExperiment(Saxs)

dataRef = app.setData(XyeData)
dataRef.loadFromFile('./saxsSphereData.xye')
dataRef.plotData()

modelRef = app.setModel(Sphere)
modelRef.setParam('R', 62.5, minVal=0, maxVal=100)
modelRef.setParam('SLDsphere', 45e-6, vary=False)
modelRef.setParam('SLDsolvent', 10e-6, vary=False)
modelRef.setParam('sigR', 0.07, minVal=0, maxVal=0.2)
modelRef.setParam('I0', 0.4, minVal=0, maxVal=10)
modelRef.setParam('bg', 0, vary=False)

app.setFit(LevenbergMarquardt)

app.show()