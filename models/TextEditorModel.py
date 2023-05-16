from typing import List

from command.delete.DeleteBefore import DeleteBeforeAction
from command.delete.DeleteAfter import DeleteAfterAction
from command.delete.DeleteSelection import DeleteSelectionAction
from command.insert.Insert import InsertAction
from managers.UndoManager import UndoManager

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

    self.undo_manager = UndoManager()


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
    action = InsertAction(self, event, char)
    error = action.execute_do()

    if not error:
      self.undo_manager.push(action)


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
    action = DeleteBeforeAction(self)
    error = action.execute_do()

    if not error:
      self.undo_manager.push(action)


  def delete_after(self, event=None):
    action = DeleteAfterAction(self)
    error = action.execute_do()

    if not error:
      self.undo_manager.push(action)



  def delete_selection(self):
    action = DeleteSelectionAction(self)
    action.execute_do()
    self.undo_manager.push(action)


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
        self.selection_range.start.x = cursor_normalized.x - 1
        self.selection_range.start.y = cursor_normalized.y

        self.selection_range.end.x = self.selection_range.start.x + 1
        self.selection_range.end.y = cursor_normalized.y
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
