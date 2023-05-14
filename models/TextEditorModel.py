from typing import List

from models.LocationRange import LocationRange
from models.Location import Location

from observers.Subject import Subject
from observers.CursorObserver import CursorObserver

import consts.Cursor as Cursor

class TextEditorModel(Subject):
  def __init__(self, text: str):
    self.lines = self._break_text(text)

    range_start = Location(0, 0)
    range_end = Location(0, 0)
    self.selection_range = LocationRange(range_start, range_end)

    self.cursor_location = Location(Cursor.X_ORIGIN, Cursor.Y_ORIGIN)

    self.cursor_observers: List[CursorObserver] = []

  def _break_text(self, text: str):
    brokenText = text.split("\n")
    return brokenText


  def _move_cursor(self, axis, direction="backwards"):
    if axis == "x":
      self._move_cursor_x(direction)
    elif axis == "y":
      self._move_cursor_y(direction)

    self.notify()


  def _move_cursor_x(self, direction: str):
    if direction == "forwards":
        self.cursor_location.x += Cursor.X_JUMP
    elif self.cursor_location.x - Cursor.X_JUMP > 0:
      self.cursor_location.x -= Cursor.X_JUMP
    else:
      self.cursor_location.x = Cursor.X_ORIGIN

  def _move_cursor_y(self, direction: str):
    if direction == "forwards":
      self.cursor_location.y += Cursor.Y_JUMP
    elif self.cursor_location.y - Cursor.Y_JUMP > 0:
      self.cursor_location.y -= Cursor.Y_JUMP
    else:
      self.cursor_location.y = Cursor.Y_ORIGIN


  def move_cursor_right(self, event):
    self._move_cursor("x", "forwards")

  def move_cursor_left(self, event):
    self._move_cursor("x")

  def move_cursor_down(self, event):
    self._move_cursor("y", "forwards")

  def move_cursor_up(self, event):
    self._move_cursor("y")


  def attach(self, observer):
    self.cursor_observers.append(observer)

  def dettach(self, observer):
    self.cursor_observers.remove(observer)

  def notify(self):
    for o in self.cursor_observers:
      o.update_cursor_location(self.cursor_location)
