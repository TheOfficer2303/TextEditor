from dataclasses import dataclass
from abc import ABC, abstractmethod

from models.Location import Location

@dataclass
class CursorObserver(ABC):
  @abstractmethod
  def update_cursor_location(self):
    pass
