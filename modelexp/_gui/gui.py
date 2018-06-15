import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
import PyQt5.QtWidgets as qt5w
from matplotlib.figure import Figure
import warnings, sys
import numpy as np
import screeninfo
from .plotWidget import PlotWidget

# remove some annoying deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning, module='matplotlib')

class Gui:
  def __init__(self):
    app = qt5w.QApplication(sys.argv)
    mainWindow = GuiMainWindow()
    mainWindow.setWindowTitle("ModelExp")
    mainWindow.show()
    app.exec_()

class GuiMainWindow(qt5w.QMainWindow):
  def __init__(self, plotWidget = None):
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

    # initialize plotWidget, either the passed by argument or the default
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
        model.py gui
        Written by Dominique Dresen (2018)

        Contact: Dominique.Dresen@uni-koeln.de

        General purpose gui for usage in model.py
        """)


if __name__ == '__main__':
  Gui()