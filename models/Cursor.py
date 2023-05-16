from models.Location import Location
from consts.Cursor import X_JUMP, Y_JUMP

class Cursor:
  def __init__(self, x, y) -> None:
    self.location = Location(x, y)
    self.normalized_location = Location(0, 0)

  def set_location(self, location: Location):
    self.location = location
    self.normalized_location.x = int(self.location.x / X_JUMP)
    self.normalized_location.y = int(self.location.y / Y_JUMP)

  def increase_x(self, times=1):
    self.location.x += 1 * times
    self.normalized_location.x = int(self.location.x / X_JUMP)

  def decrease_x(self, times=1):
    self.location.x -= 1 * times
    self.normalized_location.x = int(self.location.x / X_JUMP)

  def increase_y(self, times=1):
    self.location.y += 1 * times
    self.normalized_location.y = int(self.location.y / Y_JUMP)

  def decrease_y(self, times=1):
    self.location.y -= 1 * times
    self.normalized_location.y = int(self.location.y / Y_JUMP)
