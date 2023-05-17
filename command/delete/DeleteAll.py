from copy import deepcopy

from models.Location import Location
from command.EditAction import EditAction
from consts.Cursor import X_ORIGIN, Y_ORIGIN
from consts.Observer import ObserverType

class DeleteAllAction(EditAction):
  def __init__(self, model) -> None:
    self.model = model

  def execute_do(self):
    self.previous_lines = deepcopy(self.model.lines)
    self.previous_cursor = deepcopy(self.model.cursor)

    self.model.lines = ['']
    self.model.cursor.set_location(Location(X_ORIGIN, Y_ORIGIN))

    print(self.model.lines)
    self.model.notify(ObserverType.TEXT)
    self.model.notify(ObserverType.CURSOR)

  def execute_undo(self):
    self.model.lines = self.previous_lines
    self.model.cursor = self.previous_cursor

    self.model.notify(ObserverType.TEXT)
    self.model.notify(ObserverType.CURSOR)
