from copy import deepcopy

from command.EditAction import EditAction
from consts.Cursor import X_ORIGIN
from consts.Observer import ObserverType

class DeleteAfterAction(EditAction):
  def __init__(self, model) -> None:
    self.model = model

  def execute_do(self):
    self.previous_lines = deepcopy(self.model.lines)

    if self.model.selection_range.is_existing():
      self.model.delete_selection()
      return "error"

    cursor_normalized = self.model.cursor.normalized_location

    char_row = cursor_normalized.y
    char_position = cursor_normalized.x

    self.model.lines[char_row] = self.model.lines[char_row][:char_position] + self.model.lines[char_row][char_position + 1:]

    self.model.notify(ObserverType.TEXT)

  def execute_undo(self):
    self.model.lines = self.previous_lines

    self.model.notify(ObserverType.TEXT)
