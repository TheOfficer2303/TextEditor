from typing import List

from observers.Subject import Subject
from observers.ClipboardObserver import ClipboardObserver

class ClipboardStack(Subject):
  def __init__(self, attribute_name: str):
    setattr(self, attribute_name, [])
    self.items = getattr(self, attribute_name)
    self.observers: List[ClipboardObserver] = []

  def is_empty(self):
    return len(self.items) == 0

  def push(self, item):
    self.items.append(item)
    self.notify()

  def pop(self):
    if not self.is_empty():
      item = self.items.pop()
      self.notify()
      return item
    else:
      return

  def peek(self):
    if not self.is_empty():
        return self.items[-1]
    else:
        return

  def size(self):
    return len(self.items)

  def clear(self):
    self.items = []

  def attach(self, observer):
    self.observers.append(observer)

  def dettach(self, observer: ClipboardObserver):
    self.observers.remove(observer)

  def notify(self):
    for o in self.observers:
      o.update_clipboard()
