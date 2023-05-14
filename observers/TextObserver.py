from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class TextObserver(ABC):
  @abstractmethod
  def update_text(self, text):
    pass
