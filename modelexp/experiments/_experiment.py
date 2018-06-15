from abc import ABCMeta, abstractmethod

class Experiment(metaclass=ABCMeta):
  '''
  Abstract class to describe an experiment.
  A complete experiment consists of experimental data and/or a model of it
  '''
  @abstractmethod
  def setData(self):
    pass

  @abstractmethod
  def setModel(self):
    pass