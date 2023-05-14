from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass, field



@dataclass
class Subject(ABC):
  observers: list = field(init=False)

  @abstractmethod
  def attach(self, observer):
    pass

  @abstractmethod
  def dettach(self, observer):
    pass

  @abstractmethod
  def notify(self):
    pass
