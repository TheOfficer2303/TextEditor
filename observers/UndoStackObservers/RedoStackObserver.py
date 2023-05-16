from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class RedoStackObserver(ABC):
  @abstractmethod
  def stack_empty(self):
    pass

  @abstractmethod
  def stack_not_empty(self):
    pass
