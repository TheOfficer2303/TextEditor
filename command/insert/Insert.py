from copy import deepcopy

from command.EditAction import EditAction
from consts.Observer import ObserverType

class InsertAction(EditAction):
  def __init__(self, model, event, char) -> None:
    self.model = model
    self.event = event
    self.char = char

  def execute_do(self):
    if self.event is not None:
      if self.event.keysym == "Return":
        self.model.break_lines()
        self.model.notify(ObserverType.TEXT)
        return "error"
      if self.event.char == "" or not self.event.char.isalpha:
        return "error"

    self.previous_cursor = deepcopy(self.model.cursor)
    self.previous_lines = deepcopy(self.model.lines)

    char_to_insert = self.char if len(self.char) > 0 else self.event.char
    cursor_normalized = self.model.cursor.normalized_location

    char_row = cursor_normalized.y
    char_position = cursor_normalized.x

    old_string = self.model.lines[char_row]
    self.model.lines[char_row] = old_string[:char_position] + char_to_insert + old_string[char_position:]

    self.model.move_cursor_right(times=len(char_to_insert))
    self.model.notify(ObserverType.TEXT)

  def execute_undo(self):
    self.model.lines = self.previous_lines
    self.model.cursor = self.previous_cursor

    self.model.notify(ObserverType.TEXT)
    self.model.notify(ObserverType.CURSOR)
