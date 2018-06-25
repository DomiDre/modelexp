import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
import PyQt5.QtWidgets as qt5w
from matplotlib.figure import Figure
import warnings
import numpy as np
import screeninfo
from .plotWidget import PlotWidget

from ..fit import Fit
from ..experiments import Experiment
from ..models import Model
from ..data import Data

# remove some annoying deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning, module='matplotlib')

class Gui(qt5w.QMainWindow):
  def __init__(self):
    '''
    Defines the main layout of the page. Where is the canvas, where the buttons.
    Define the menu.
    '''
    super().__init__()

    self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    # Menubar
    self.fileMenu = qt5w.QMenu('&File', self)
    self.fileMenu.addAction('&Quit', self.fileQuit, 'Ctrl+C')
    self.menuBar().addMenu(self.fileMenu)

    self.helpMenu = qt5w.QMenu('&Help', self)
    self.helpMenu.addAction('&About', self.about)
    self.menuBar().addSeparator()
    self.menuBar().addMenu(self.helpMenu)

    # main widgets
    self.mainContainer = qt5w.QWidget(self) # widget that contains everything
    self.plotContainer = qt5w.QWidget(self) # widget to include plot window
    self.parameterWidget = qt5w.QWidget(self) # widget for control of the parameters
    self.buttonWidget = qt5w.QWidget(self) # widget that contains control buttons

    # define layout of everything
    self.layout = qt5w.QGridLayout(self.mainContainer)
    self.layout.addWidget(self.plotContainer, 0, 0) # upper left
    self.layout.addWidget(self.parameterWidget, 0, 1) # upper right
    self.layout.addWidget(self.buttonWidget, 1, 1) # lower right

    # set size of window depending on screen resolution
    screen_resolution = screeninfo.get_monitors()[0]
    self.layout.setColumnMinimumWidth(0, screen_resolution.width/2)
    self.layout.setRowMinimumHeight(0, screen_resolution.height/2)

    self.mainContainer.setFocus() # set focus onto the main widget
    self.setCentralWidget(self.mainContainer)
    self.statusBar().showMessage("model.py gui")

  def initPlot(self, plotWidget=None):
    # initialize plotWidget (after experiment is set)
    # either passed by argument or the default
    self.plotWidget = plotWidget(self) if plotWidget else PlotWidget(self)

    self.layoutPlot = qt5w.QVBoxLayout(self.plotContainer)
    self.layoutPlot.addWidget(self.plotWidget)
    self.layoutPlot.addWidget(self.plotWidget.toolbar)

  def closeEvent(self, event):
    self.fileQuit()

  def fileQuit(self):
    self.close()

  def about(self):
    qt5w.QMessageBox.about(self, "About",
        """
        ModelExp
        Written by Dominique Dresen (2018)

        Contact: Dominique.Dresen@uni-koeln.de

        General purpose gui for usage in ModelExp
        """)

  def connectExperiment(self, ptrExperiment):
    self.ptrExperiment: Experiment = ptrExperiment

  def connectModel(self, ptrModel):
    self.ptrModel: Model = ptrModel
    self.initializeParameterSliders()

  def connectData(self, ptrData):
    self.ptrData: Data = ptrData

  def connectFit(self, ptrFit):
    self.ptrFit: Fit = ptrFit
    self.setFitButtons()

  def initializeParameterSliders(self):
    '''
    Function called once at the beginning to initialize a sliderbar for every
    parameter in the model
    '''
    #create the parameter widget
    self.parameterLayout = qt5w.QGridLayout(self.parameterWidget)
    self.sliders = {}
    self.checkboxes = {}

    self.sliderNumPts = 1000
    parameters = self.ptrModel.getParameters()
    for i, parameter in enumerate(parameters):
      sliderLabel = qt5w.QLabel(parameter)
      sliderBar = qt5w.QSlider(QtCore.Qt.Horizontal, self)
      checkbox = qt5w.QCheckBox(self)

      currentParameter = parameters[parameter]

      sliderBar.setRange(0, self.sliderNumPts)
      sliderBar.setTickInterval(5)
      sliderBar.setSingleStep(1)
      sliderBar.setPageStep(10)

      curVal = currentParameter.value
      minVal = currentParameter.min
      maxVal = currentParameter.max

      if minVal == -np.inf:
        if curVal > 0:
          minVal = 0
        elif curVal < 0:
          minVal = 10*curVal
        else:
          minVal = -1
        currentParameter.min = minVal

      if maxVal == np.inf:
        if curVal > 0:
          maxVal = 10*curVal
        elif curVal < 0:
          maxVal = 0
        else:
          maxVal = 1
        currentParameter.max = maxVal

      delta = (maxVal - minVal)/self.sliderNumPts
      checkbox.setChecked(currentParameter.vary)
      sliderValue = int((curVal-minVal)/delta)
      sliderBar.setValue(sliderValue)
      newValue = minVal + sliderBar.value()*delta
      if newValue > 1e3 or newValue < 1e-3:
        prec = '{:.3e}'
      else:
        prec = '{:.3f}'
      sliderBar.label = qt5w.QLabel(prec.format(newValue))

      sliderBar.valueChanged.connect(self.sliderValueChanged)
      self.parameterLayout.addWidget(sliderLabel, i, 0)
      self.parameterLayout.addWidget(sliderBar, i, 1)
      self.parameterLayout.addWidget(sliderBar.label, i, 2)
      self.parameterLayout.addWidget(checkbox, i, 3)
      self.sliders[parameter] = sliderBar
      self.checkboxes[parameter] = checkbox
    self.sliderInverseDict = dict(zip(self.sliders.values(),self.sliders.keys()))

  def sliderValueChanged(self, value):
    '''
    Called whenever the user slides a bar.
    '''
    changedSlider = self.sender()
    currentParameter = self.ptrModel.getParameters()[self.sliderInverseDict[changedSlider]]

    minVal = currentParameter.min
    maxVal = currentParameter.max
    delta = (maxVal - minVal)/self.sliderNumPts
    newValue = minVal + changedSlider.value()*delta
    if abs(newValue) > 1e3 or (abs(newValue) < 1e-3):
      prec = '{:.3e}'
    else:
      prec = '{:.3f}'
    changedSlider.label.setText(prec.format(newValue))
    currentParameter.value = newValue
    self.ptrModel.updateModel()
    self.update()

  def update(self):
    '''
    Can be called from the outside to refresh the plot canvas.
    '''
    self.plotWidget.updatedDataAx()

  def updateSlidersValueFromParams(self):
    for parameter in self.ptrModel.params:
      self.updateSlider(parameter)

  def updateParamsVaryFromCheckbox(self):
    for parameter in self.ptrModel.params:
      self.ptrModel.params[parameter].vary =\
        self.checkboxes[parameter].isChecked()

  def updateSlider(self, parameter):
    currentParam = self.ptrModel.params[parameter]
    sliderBar = self.sliders[parameter]

    curVal = currentParam.value
    minVal = currentParam.min
    maxVal = currentParam.max
    if minVal == -np.inf:
      if curVal > 0:
        minVal = 0
      elif curVal < 0:
        minVal = 10*curVal
      else:
        minVal = -1
      currentParam.min = minVal

    if maxVal == np.inf:
      if curVal > 0:
        maxVal = 10*curVal
      elif curVal < 0:
        maxVal = 0
      else:
        maxVal = 1
      currentParam.max = maxVal
    delta = (maxVal - minVal)/self.sliderNumPts
    sliderValue = int((curVal-minVal)/delta)
    sliderBar.setValue(sliderValue)
    self.checkboxes[parameter].setChecked(currentParam.vary)

  def setFitButtons(self):
    def addButton(buttonLabel, buttonTooltip, buttonFunction):
        newButton = qt5w.QPushButton(buttonLabel, self)
        newButton.setToolTip(buttonTooltip)
        newButton.clicked.connect(buttonFunction)
        return newButton
    self.buttonLayout = qt5w.QVBoxLayout(self.buttonWidget)

    def guiFit():
      self.ptrFit.fit()
      self.updateSlidersValueFromParams()
      self.update()

    self.buttonLayout.addWidget(
      addButton(
        'Fit',
        'Fit parameters of the model to the data',
        guiFit
      )
    )

    def exportFit():
      self.ptrFit.exportResult('fit_result.dat')

    self.buttonLayout.addWidget(
      addButton(
        'Export Fit Result',
        'Save fit result of model & data to file',
        exportFit
      )
    )

    def updateParamsInFile():
      self.ptrModel.updateParamsToFile()

    self.buttonLayout.addWidget(
      addButton(
        'Update Parameters in File',
        'Set values in fit file to current parameter values',
        updateParamsInFile
      )
    )