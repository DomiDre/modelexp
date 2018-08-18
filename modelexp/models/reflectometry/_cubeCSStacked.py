from ._reflModel import ReflectometryModel
from fortRefl import nanocubes, algorithms
import numpy as np

class CubeCSStacked(ReflectometryModel):
  '''
  Model to describe the formfactor of a sphere
  '''
  def initParameters(self):
    self.params.add("i0", 1, min = 0, max = 2, vary = False)
    self.params.add("bg", 2.1e-06, min = 0.0, max = 0.0001, vary = False)
    self.params.add("roughness", 11.84, min = 0.0, max = 20, vary = True)
    self.params.add("packingDensity", 0.517, min = 0.0, max = 1.0, vary = True)
    self.params.add("a", 50, min = 0, max = 100, vary = True)
    self.params.add("d", 20, min = 0, max = 40, vary = True)
    self.params.add("nLayers", 5, min= 1, max=10, vary=False)
    self.params.add('sldCore', 8e-6, min= 0, max = 40e-6, vary=False)
    self.params.add('sldShell', 10e-7, min= 0, max = 40e-6, vary=False)
    self.params.add('sldMatrix', 0e-6, min= 0, max = 40e-6, vary=False)
    self.params.add('sldSubstrate', 2e-6, min= 0, max = 40e-6, vary=False)
    self.params.add('coverage', 1, min= 0, max = 1, vary=True)
    self.params.add('roughnessSubstrate', 5, min= 0, max = 20, vary=True)

  def initMagneticParameters(self):
    self.params.add('magSldCore', 1e-6)
    self.params.add('magSldShell', 0, vary=False)

    self.addConstantParam('magSldShell')

  def calcModel(self):
    nLayers = int(self.params['nLayers'].value)
    a = self.params['a'].value
    d = self.params['d'].value
    packing_densities = [self.params["packingDensity"].value] * nLayers

    thickness, sld = nanocubes.cube_cs_stacked(
      self.params['sldCore'].value,
      self.params['sldShell'].value,
      self.params['sldMatrix'].value,
      self.params['sldSubstrate'].value,
      a,
      d,
      packing_densities
    )
    thickness, sld = nanocubes.cube_cs_stacked(
      self.params['sldCore'].value,
      self.params['sldShell'].value,
      self.params['sldMatrix'].value,
      self.params['sldSubstrate'].value,
      a,
      d,
      packing_densities
    )
    roughness = [self.params["roughness"].value]*len(sld)
    Isubstrate = algorithms.parrat(
      self.q,
      [self.params['sldSubstrate'].value, 0],
      [self.params['roughnessSubstrate'], self.params['roughnessSubstrate']],
      [0, 0]
    )
    IparticleLayer = algorithms.parrat(self.q, sld, roughness, thickness)

    self.z = np.linspace(-thickness[0], nLayers*(a+2*d)+a, 100)
    self.I = self.params["i0"] * (
      self.params['coverage'] * IparticleLayer + (1-self.params['coverage']) * Isubstrate
    )  + self.params["bg"]
    self.sld = algorithms.roughsld_thick_layers(self.z, sld, roughness, thickness).real

  def calcMagneticModel(self):
    self.calcModel()
    # self.I = self.params['i0'] * sphere.magnetic_formfactor(
    #   self.q,
    #   self.params['r'],
    #   self.params['sldCore'],
    #   self.params['sldSolvent'],
    #   self.params['sigR'],
    #   self.params['magSldCore'],
    #   self.params['magSldSolvent'],
    #   self.params['xi'],
    #   self.params['sin2alpha'],
    #   self.params['polarization'],
    # ) + self.params['bg']

    # self.r, self.sld = sphere.sld(
    #   self.params['r'],
    #   self.params['sldCore'],
    #   self.params['sldSolvent']
    # )

    # self.rMag, self.sldMag = sphere.sld(
    #   self.params['r'],
    #   self.params['magSldCore'],
    #   self.params['magSldMatrix']
    # )
