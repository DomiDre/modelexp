from abc import ABC, abstractmethod

class Model(ABC):
  '''
  Abstract class to describe a model.
  Specific models are defined by classes that have to implemented the defined functions here.
  '''

  def __init__(self):
    self.defineDomain()

  @abstractmethod
  def defineDomain(self):
    '''
    On which space should the model be evaluated
    '''
    pass

  @abstractmethod
  def calcModel(self):
    '''
    How to calculate the model on the defined domain
    '''
    pass