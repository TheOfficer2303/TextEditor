import tkinter as tk
from models.Cursor import Cursor
from observers.CursorObserver import CursorObserver
from observers.TextObserver import TextObserver

class StatusBar(CursorObserver, TextObserver):
  def __init__(self, window):
    self.frame = tk.Frame(window)
    self.frame.pack(side = tk.BOTTOM)
    self.frame.lift()

    self.cursor_label = tk.Label(self.frame, text=f"x: 0, y: 0")
    self.cursor_label.pack(side=tk.BOTTOM)

    self.lines_label = tk.Label(self.frame, text="lines: 1")
    self.lines_label.pack(side=tk.RIGHT)

  def update_cursor_location(self, cursor: Cursor):
    self.cursor_label.config(text=f"x: {cursor.normalized_location.x}, y: {cursor.normalized_location.y}")

  def update_text(self, text: list):
    self.lines_label.config(text=f"lines: {len(text)}")
