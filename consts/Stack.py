from enum import Enum

class StackState(Enum):
  EMPTY = 1
  NOT_EMPTY = 2

class StackType(Enum):
  REDO = 1
  UNDO = 2
