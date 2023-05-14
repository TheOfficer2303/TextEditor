from dataclasses import dataclass
from models.Location import Location

class LocationRange:
  def __init__(self, start: Location, end: Location) -> None:
    self.range_start_location = start
    self.range_end_location = end
