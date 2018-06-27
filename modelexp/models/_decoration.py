from abc import ABCMeta, abstractmethod

class Decoration(metaclass=ABCMeta):

  def __init__(self):
    pass

  @abstractmethod
  def apply(self):
    pass
