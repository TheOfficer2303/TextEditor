from copy import deepcopy

from command.EditAction import EditAction
from consts.Cursor import X_ORIGIN
from consts.Observer import ObserverType

class DeleteSelectionAction(EditAction):
  def __init__(self, model) -> None:
    self.model = model

  def execute_do(self):
    self.previous_lines = deepcopy(self.model.lines)
    self.previous_cursor = deepcopy(self.model.cursor)
    self.previous_selection = deepcopy(self.model.selection_range)

    for y in range(self.model.selection_range.end.y + len(self.model.lines) - self.model.selection_range.start.y):
      if y != self.model.selection_range.end.y:
        continue
      self.model.lines[y] = self.model.lines[y][:self.model.selection_range.start.x] + self.model.lines[y][self.model.selection_range.end.x:]

    cursor_normalized = self.model.cursor.normalized_location

    move_steps = self.model.selection_range.x_range() if cursor_normalized.x == self.model.selection_range.end.x else 0
    self.model.move_cursor_left(times=move_steps)
    self.model.unselect()

  def execute_undo(self):
    self.model.lines = self.previous_lines
    self.model.cursor = self.previous_cursor
    self.model.selection_range = self.previous_selection

    self.model.notify(ObserverType.TEXT)
    self.model.notify(ObserverType.CURSOR)
