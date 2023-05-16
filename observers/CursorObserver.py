from dataclasses import dataclass
from abc import ABC, abstractmethod
from models.Cursor import Cursor


@dataclass
class CursorObserver(ABC):
  @abstractmethod
  def update_cursor_location(self, cursor: Cursor):
    pass
