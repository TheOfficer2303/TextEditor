from typing import List

from models.Stack import Stack

from observers.Subject import Subject
from observers.ClipboardObserver import ClipboardObserver

class ClipboardStack(Stack, Subject):
  def __init__(self, attribute_name: str):
    super().__init__(attribute_name)
    self.observers: List[ClipboardObserver] = []

  def attach(self, observer: ClipboardObserver):
    self.observers.append(observer)

  def dettach(self, observer: ClipboardObserver):
    self.observers.remove(observer)

  def notify(self):
    for o in self.observers:
      o.update_clipboard()
