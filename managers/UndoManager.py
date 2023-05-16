from typing import List
from command.EditAction import EditAction

class UndoManager:
  _instance = None

  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      cls._instance = super().__new__(cls, *args, **kwargs)
    return cls._instance

  def __init__(self) -> None:
    self.undo_stack: List[EditAction] = []
    self.redo_stack: List[EditAction] = []

    self.undo_observers = []
    self.redo_observers = []

  def undo(self):
    if len(self.undo_stack) > 0:
      action = self.undo_stack.pop()
      action.execute_undo()

      self.redo_stack.append(action)

  def redo(self):
    if len(self.redo_stack) > 0:
      action = self.redo_stack.pop()
      action.execute_do()

      self.undo_stack.append(action)

  def push(self, action: EditAction):
    self.redo_stack = []
    self.undo_stack.append(action)
