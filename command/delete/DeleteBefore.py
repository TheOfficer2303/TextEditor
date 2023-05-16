from copy import deepcopy

from command.EditAction import EditAction
from consts.Cursor import X_ORIGIN
from consts.Observer import ObserverType

class DeleteBeforeAction(EditAction):
  def __init__(self, model) -> None:
    self.model = model

  def execute_do(self):
    self.previous_lines = deepcopy(self.model.lines)
    self.previous_cursor = deepcopy(self.model.cursor)

    cursor_normalized = self.model.cursor.normalized_location

    char_row = cursor_normalized.y
    char_position = cursor_normalized.x

    if self.model.cursor.location.x == X_ORIGIN and not char_row == 0:
      self.model.move_cursor_right(times=len(self.model.lines[char_row - 1]) + 1)
      self.model.move_cursor_up()

    if self.model.selection_range.is_existing():
      self.model.delete_selection()
      return "error"

    if not char_position == 0:
      self.model.lines[char_row] = self.model.lines[char_row][:char_position - 1] + self.model.lines[char_row][char_position:]

    self.model.move_cursor_left()
    self.model.notify(ObserverType.TEXT)

  def execute_undo(self):
    self.model.lines = self.previous_lines
    self.model.cursor = self.previous_cursor

    self.model.notify(ObserverType.TEXT)
    self.model.notify(ObserverType.CURSOR)
