from dataclasses import dataclass
from abc import ABC, abstractmethod
from consts.Stack import StackState, StackType

@dataclass
class UndoStackObserver(ABC):
  @abstractmethod
  def stack_empty(self, type: StackType):
    pass

  @abstractmethod
  def stack_not_empty(self, type: StackType):
    pass
