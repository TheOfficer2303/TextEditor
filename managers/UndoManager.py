from typing import List
from command.EditAction import EditAction
from observers.UndoStackObservers.RedoStackObserver import RedoStackObserver
from observers.UndoStackObservers.UndoStackObserver import UndoStackObserver
from consts.Stack import StackState, StackType

class UndoManager:
  _instance = None

  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      cls._instance = super().__new__(cls, *args, **kwargs)
    return cls._instance

  def __init__(self) -> None:
    self.undo_stack: List[EditAction] = []
    self.redo_stack: List[EditAction] = []

    self.undo_observers: List[UndoStackObserver] = []
    self.redo_observers: List[RedoStackObserver] = []

  def undo(self):
    if len(self.undo_stack) > 0:
      action = self.undo_stack.pop()
      action.execute_undo()

      if len(self.undo_stack) == 0:
        self.notify_undo(StackState.EMPTY)

      self.redo_stack.append(action)
      self.notify_redo(StackState.NOT_EMPTY)
    else:
      self.notify_undo(StackState.NOT_EMPTY)

  def redo(self):
    if len(self.redo_stack) > 0:
      action = self.redo_stack.pop()
      action.execute_do()

      if len(self.redo_stack) == 0:
        self.notify_redo(StackState.EMPTY)

      self.undo_stack.append(action)
      self.notify_undo(StackState.NOT_EMPTY)
    else:
      self.notify_redo(StackState.NOT_EMPTY)

  def push(self, action: EditAction):
    self.redo_stack = []
    self.undo_stack.append(action)

    self.notify_redo(StackState.EMPTY)
    self.notify_undo(StackState.NOT_EMPTY)


  #UNDO OBSERVERS

  def attach_undo(self, o: UndoStackObserver):
    self.undo_observers.append(o)

  def detach_undo(self, o: UndoStackObserver):
    self.undo_observers.remove(o)

  def notify_undo(self, state: StackState):
    for o in self.undo_observers:
      if state == StackState.EMPTY:
        o.stack_empty(StackType.UNDO)
      else:
        o.stack_not_empty(StackType.UNDO)

  #REDO OBSERVERS
  def attach_redo(self, o: RedoStackObserver):
    self.redo_observers.append(o)

  def detach_redo(self, o: RedoStackObserver):
    self.redo_observers.remove(o)

  def notify_redo(self, state: StackState):
    for o in self.redo_observers:
      if state == StackState.EMPTY:
        o.stack_empty(StackType.REDO)
      else:
        o.stack_not_empty(StackType.REDO)
