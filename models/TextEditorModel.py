from typing import List

from models.LocationRange import LocationRange
from models.Location import Location
from models.Cursor import Cursor

from observers.Subject import Subject
from observers.CursorObserver import CursorObserver
from observers.TextObserver import TextObserver

from consts.Observer import ObserverType
from consts.Cursor import X_ORIGIN, Y_ORIGIN, X_JUMP, Y_JUMP

class TextEditorModel(Subject):
  def __init__(self, text: str):
    self.lines = self._break_text(text)

    range_start = Location(0, 0)
    range_end = Location(0, 0)
    self.selection_range = LocationRange(range_start, range_end)

    self.cursor = Cursor(X_ORIGIN, Y_ORIGIN)

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


  def _move_cursor_to(self, location: Location):
    self.cursor.set_location(location)
    self.notify(ObserverType.CURSOR)


  def _move_cursor_x(self, direction: str, times=1):
    move = X_JUMP * times

    if direction == "forwards":
      self.cursor.increase_x(move)
    elif self.cursor.location.x - move > 0:
      self.cursor.decrease_x(move)
    else:
      self.cursor.location.x = X_ORIGIN

  def _move_cursor_y(self, direction: str, times=1):
    move = Y_JUMP * times
    if direction == "forwards":
      self.cursor.increase_y(move)
    elif self.cursor.location.y - move > 0:
      self.cursor.decrease_y(move)
    else:
      self.cursor.location.y = Y_ORIGIN


  # CURSOR METHODS
  def move_cursor_right(self, event=None, times=1):
    if not self.cursor.normalized_location.x == len(self.lines[self.cursor.normalized_location.y]):
      self._move_cursor("x", "forwards", times=times)

  def move_cursor_left(self, event=None, times=1):
    self._move_cursor("x", times=times)

  def move_cursor_down(self, event=None, times=1):
    if not self.cursor.normalized_location.y == len(self.lines) - 1:
      self._move_cursor("y", "forwards", times=times)

  def move_cursor_up(self, event=None, times=1):
    self._move_cursor("y", times=times)

  def move_cursor_to_origin_x(self):
    self._move_cursor_to(Location(X_ORIGIN, self.cursor.location.y))

  def move_cursor_to_origin_y(self):
    self._move_cursor_to(Location(self.cursor.location.x, Y_ORIGIN))

  def move_cursor_to_end(self):
    last_row = self.lines[-1]
    position = (len(last_row)) * X_JUMP

    last_row_position = len(self.lines) - 1

    self._move_cursor_to(Location(position, last_row_position * Y_JUMP + Y_ORIGIN))


  # TEXT METHODS
  def insert(self, event, char=""):
    if event is not None:
      if event.keysym == "Return":
        self.break_lines()
        self.notify(ObserverType.TEXT)
        return

      if event.char == "" or not event.char.isalpha:
        return

    char_to_insert = char if len(char) > 0 else event.char
    cursor_normalized = self.cursor.normalized_location

    char_row = cursor_normalized.y
    char_position = cursor_normalized.x

    old_string = self.lines[char_row]
    self.lines[char_row] = old_string[:char_position] + char_to_insert + old_string[char_position:]

    self.move_cursor_right(times=len(char_to_insert))
    self.notify(ObserverType.TEXT)


  def insert_text(self, text: str):
    for char in text:
      self.insert(None, char)


  def break_lines(self):
    cursor_normalized = self.cursor.normalized_location

    char_row = cursor_normalized.y
    char_position = cursor_normalized.x

    chars_to_new_line = self.lines[char_row][char_position:]
    self.lines[char_row] = self.lines[char_row][:char_position]
    self.lines.insert(char_row + 1, chars_to_new_line)

    self.move_cursor_down()
    self.move_cursor_to_origin_x()


  # DELETE METHODS
  def delete_before(self, event=None):
    cursor_normalized = self.cursor.normalized_location

    char_row = cursor_normalized.y
    char_position = cursor_normalized.x

    if self.cursor.location.x == X_ORIGIN:
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

    cursor_normalized = self.cursor.normalized_location

    char_row = cursor_normalized.y
    char_position = cursor_normalized.x

    self.lines[char_row] = self.lines[char_row][:char_position] + self.lines[char_row][char_position + 1:]

    self.notify(ObserverType.TEXT)


  def delete_selection(self):
    for y in range(self.selection_range.end.y + len(self.lines) - self.selection_range.start.y):
      if y != self.selection_range.end.y:
        continue
      self.lines[y] = self.lines[y][:self.selection_range.start.x] + self.lines[y][self.selection_range.end.x:]

    cursor_normalized = self.cursor.normalized_location

    move_steps = self.selection_range.x_range() if cursor_normalized.x == self.selection_range.end.x else 0
    self.move_cursor_left(times=move_steps)
    self.unselect()


  def update_selection_range(self, event):
    cursor_normalized = self.cursor.normalized_location

    if event.keysym == 'Right':
      if self.selection_range.is_existing():
        if cursor_normalized.x == self.selection_range.end.x:
          self.selection_range.end.x += 1
        elif cursor_normalized.x == self.selection_range.start.x:
          self.selection_range.start.x += 1

      else:
        self.selection_range.start.x = cursor_normalized.x
        self.selection_range.start.y = cursor_normalized.y

        self.selection_range.end.x = self.selection_range.start.x + 1
        self.selection_range.end.y = cursor_normalized.y

      self.move_cursor_right()

    elif event.keysym == 'Left':
      if self.selection_range.is_existing():
        if cursor_normalized.x == self.selection_range.start.x:
          self.selection_range.start.x -= 1
        elif cursor_normalized.x == self.selection_range.end.x:
          self.selection_range.end.x -= 1
      else:
        print("TU SAM")
        self.selection_range.start.x = cursor_normalized.x - 1
        self.selection_range.start.y = cursor_normalized.y

        self.selection_range.end.x = self.selection_range.start.x + 1
        self.selection_range.end.y = cursor_normalized.y
        print("Cursor", cursor_normalized)
        print("selection", self.selection_range)
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
        o.update_cursor_location(self.cursor)

    elif obs_type == ObserverType.TEXT:
      for o in self.text_observers:
        o.update_text(self.lines)


  def get_text_in_selection(self):
    if self.selection_range.is_existing():
      row = self.selection_range.start.y
      first_char_position = self.selection_range.start.x
      last_char_position = self.selection_range.end.x

      return self.lines[row][first_char_position:last_char_position]


  def unselect(self):
    self.selection_range.reset()
    self.notify(ObserverType.TEXT)
