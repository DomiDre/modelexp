import numpy as np
from ._dataContainer import DataContainer

class MultiData(DataContainer):
  '''
  To load data files which have multiple datasets included
  '''
  def loadFromFile(self, filename, readParams=True):
    self.filename = filename
    if readParams:
      fileAtParams = False
      self.params = {}
    else:
      self.params = None

    with open(filename, 'r') as f:
      newData = None
      for line in f:
        if line.strip() == '': # empty line
          continue
        elif line.startswith('#'):
          if readParams: # read fit parameters from file
            if fileAtParams:
              if ('[[Correlations]]' in line) or ('[[Data]]' in line):
                fileAtParams = False
                readParams = False
              else:
                splitLine = line.split('#')[1].strip()
                if splitLine != '':
                  paramName, paramData  = splitLine.split(':', 1)
                  paramValue = float(paramData.strip().split(' ',1)[0])
                  if ('fixed' in paramData):
                    paramStd = 0
                  else:
                    paramStd = float(
                      paramData.strip().split('+/-',)[1].strip().split(' ', 1)[0]
                    )
                  self.params[paramName] = {
                    'name': paramName,
                    'value': paramValue,
                    'std': paramStd
                  }
            elif '[[Variables]]' in line:
              fileAtParams = True
              continue
          elif '[[Data]]' in line:
            # new data set is being started
            if newData is not None: # old dataset in memory? store it
              self.nDatasets += 1
              self.datasets.append(newData)

            # start a new dataset
            newData = self.dataClass()
            newData.suffix = line.split('[[Data]]',1)[1].strip()
            newData.filename = self.filename
          else: # commented line
            continue
        else:
          # line is not empty and does not start with '#'

          # remove any comments in line, then split by whitespace or tab
          splitLine = [float(x) for x in line.strip().split('#',1)[0].split()]
          newData.addDataLine(splitLine)