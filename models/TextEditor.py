from tkinter import Tk, Widget, INSERT
from models.Location import Location

from models.TextEditorModel import TextEditorModel
import consts.Cursor as Cursor

from observers.CursorObserver import CursorObserver

class TextEditor(CursorObserver):
  def __init__(self, window: Tk, model: TextEditorModel) -> None:
    self._init_model(model)
    self._init_window(window)
    self.cursor = self._show_cursor()


  def _init_window(self, window: Tk):
    self.window = window
    self.window.bind('<Right>', self.model.move_cursor_right)
    self.window.bind('<Left>', self.model.move_cursor_left)
    self.window.bind('<Up>', self.model.move_cursor_up)
    self.window.bind('<Down>', self.model.move_cursor_down)


  def _init_model(self, model: TextEditorModel):
    self.model = model
    model.attach(self)

  def show_text(self):
    text_opts = {
      "font": ("Courier New", 16)
    }

    options = {
      "text": self.model.lines,
      "anchor": "w",
      "font": ("Courier New", 16)
    }
    
    base_widget = Widget(self.window, "label", options)

    text_widget = Widget(self.window, "text", text_opts)
    text_widget.tk.call(text_widget._w, 'insert', "0.0", "ABCD8")

    count = text_widget.tk.call(text_widget._w, 'count', '-chars', '1.0', 'end')
    print(count)

    text_widget.configure(state='disabled')

    text_widget.place(x=0, y=0)

    base_widget.place(x=0, y=0)

  def _show_cursor(self):
    options = {
      "height": Cursor.HEIGHT,
      "width": Cursor.WIDTH,
      "bg": Cursor.COLOR,
    }

    cursor = Widget(self.window, "frame", options)
    cursor.place(x=self.model.cursor_location.x, y=self.model.cursor_location.y)
    cursor.lift()

    return cursor

  def update_cursor_location(self, location: Location):
    self.cursor.place(x=location.x, y=location.y)
    self.cursor.lift()
