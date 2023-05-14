from typing import List

from models.LocationRange import LocationRange
from models.Location import Location

from observers.Subject import Subject
from observers.CursorObserver import CursorObserver
from observers.TextObserver import TextObserver

import consts.Cursor as Cursor
from consts.Observer import ObserverType

class TextEditorModel(Subject):
  def __init__(self, text: str):
    self.lines = self._break_text(text)

    range_start = Location(0, 0)
    range_end = Location(0, 0)
    self.selection_range = LocationRange(range_start, range_end)

    self.cursor_location = Location(Cursor.X_ORIGIN, Cursor.Y_ORIGIN)

    self.cursor_observers: List[CursorObserver] = []
    self.text_observers: List[TextObserver] = []


  def _break_text(self, text: str):
    brokenText = text.split("\n")
    return brokenText


  def _move_cursor(self, axis, direction="backwards", times=1):
    if axis == "x":
      self._move_cursor_x(direction, times)
    elif axis == "y":
      self._move_cursor_y(direction, times)

    self.notify(ObserverType.CURSOR)


  def _move_cursor_x(self, direction: str, times=1):
    move = Cursor.X_JUMP * times

    if direction == "forwards":
        self.cursor_location.x += move
    elif self.cursor_location.x - move > 0:
      self.cursor_location.x -= move
    else:
      self.cursor_location.x = Cursor.X_ORIGIN

  def _move_cursor_y(self, direction: str, times=1):
    move = Cursor.Y_JUMP * times
    if direction == "forwards":
      self.cursor_location.y += move
    elif self.cursor_location.y - move > 0:
      self.cursor_location.y -= move
    else:
      self.cursor_location.y = Cursor.Y_ORIGIN


  # CURSOR METHODS
  def move_cursor_right(self, event=None, times=1):
    self._move_cursor("x", "forwards", times=times)

  def move_cursor_left(self, event=None, times=1):
    self._move_cursor("x", times=times)

  def move_cursor_down(self, event=None, times=1):
    self._move_cursor("y", "forwards", times=times)

  def move_cursor_up(self, event=None, times=1):
    self._move_cursor("y", times=times)


  # TEXT METHODS
  def delete_before(self, event=None):
    char_row = int(self.cursor_location.y / Cursor.Y_JUMP)
    char_position = int(self.cursor_location.x / Cursor.X_JUMP)

    if self.cursor_location.x == Cursor.X_ORIGIN:
      self.move_cursor_right(times=len(self.lines[char_row - 1]) + 1)
      self.move_cursor_up()

    if self.selection_range.is_existing():
      self.delete_selection()
      return

    self.lines[char_row] = self.lines[char_row][:char_position - 1] + self.lines[char_row][char_position:]

    self.move_cursor_left()
    self.notify(ObserverType.TEXT)


  def delete_after(self, event=None):
    if self.selection_range.is_existing():
      self.delete_selection()
      return

    char_row = int(self.cursor_location.y / Cursor.Y_JUMP)
    char_position = int(self.cursor_location.x / Cursor.X_JUMP)

    self.lines[char_row] = self.lines[char_row][:char_position] + self.lines[char_row][char_position + 1:]

    self.notify(ObserverType.TEXT)


  def delete_selection(self):
    for y in range(self.selection_range.end.y + len(self.lines) - self.selection_range.start.y):
      if y != self.selection_range.end.y:
        continue
      self.lines[y] = self.lines[y][:self.selection_range.start.x] + self.lines[y][self.selection_range.end.x:]

    self.move_cursor_left(times=self.selection_range.x_range())
    self.selection_range.reset()
    self.notify(ObserverType.TEXT)


  def update_selection_range(self, event):
    cursor_normalized = self._cursor_location_normalized()
    print('normalized', cursor_normalized)
    if event.keysym == 'Right':
      if self.selection_range.is_existing():
        self.selection_range.end.x += 1
      else:
        self.selection_range.start.x = cursor_normalized.x
        self.selection_range.start.y = cursor_normalized.y

        self.selection_range.end.x = self.selection_range.start.x + 1
        self.selection_range.end.y = cursor_normalized.y

      self.move_cursor_right()

    elif event.keysym == 'Left':
      if self.selection_range.is_existing():
        self.selection_range.end.x -= 1
      self.move_cursor_left()

    self.notify(ObserverType.TEXT)


  def attach(self, observer, obs_type: ObserverType):
    if obs_type == ObserverType.CURSOR:
      self.cursor_observers.append(observer)
    elif obs_type == ObserverType.TEXT:
      self.text_observers.append(observer)

  def dettach(self, observer, obs_type: ObserverType):
    if obs_type == ObserverType.CURSOR:
      self.cursor_observers.remove(observer)
    elif obs_type == ObserverType.TEXT:
      self.text_observers.remove(observer)

  def notify(self, obs_type: ObserverType):
    if obs_type == ObserverType.CURSOR:
      for o in self.cursor_observers:
        o.update_cursor_location(self.cursor_location)

    elif obs_type == ObserverType.TEXT:
      for o in self.text_observers:
        o.update_text()


  def _cursor_location_normalized(self):
    return Location(int(self.cursor_location.x / Cursor.X_JUMP), int(self.cursor_location.y / Cursor.Y_JUMP))
