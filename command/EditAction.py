from abc import ABC, abstractmethod
from dataclasses import dataclass, field

class EditAction(ABC):
  @abstractmethod
  def execute_do(self):
    pass

  @abstractmethod
  def execute_undo(self):
    pass
