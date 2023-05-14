from dataclasses import dataclass
from models.Location import Location

class LocationRange:
  def __init__(self, start: Location, end: Location) -> None:
    self.start = start
    self.end = end


  def __repr__(self) -> str:
    return f"{self.start} {self.end}"

  def is_existing(self):
    if self.start.x - self.end.x != 0:
      return True
    elif self.start.y - self.end.y != 0:
      return True

    return False


  def x_range(self):
    return self.end.x - self.start.x

  def y_range(self):
    return self.end.y - self.start.y


  def reset(self):
    self.start.x = 0
    self.end.x = 0
    self.start.y = 0
    self.end.y = 0
