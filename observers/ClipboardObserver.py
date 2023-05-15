from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class ClipboardObserver(ABC):
  @abstractmethod
  def update_clipboard(self):
    pass
