from tkinter import Tk, Widget

from models.TextEditorModel import TextEditorModel
from models.ClipboardStack import ClipboardStack

import consts.Cursor as Cursor
from consts.Observer import ObserverType

from observers.CursorObserver import CursorObserver
from observers.TextObserver import TextObserver

class TextEditor(CursorObserver, TextObserver):
  def __init__(self, window: Tk, model: TextEditorModel) -> None:
    self._init_model(model)
    self._init_window(window)
    self.cursor = self._show_cursor()
    self.clipboard = ClipboardStack("texts")

  def _init_window(self, window: Tk):
    self.window = window
    self._bind_cursor_keys()
    self._bind_text_editing_keys()
    self._bind_clipboard_keys()

  def _bind_cursor_keys(self):
    self.window.bind('<Right>', self.model.move_cursor_right)
    self.window.bind('<Left>', self.model.move_cursor_left)
    self.window.bind('<Up>', self.model.move_cursor_up)
    self.window.bind('<Down>', self.model.move_cursor_down)

  def _bind_text_editing_keys(self):
    self.window.bind('<BackSpace>', self.model.delete_before)
    self.window.bind('<Delete>', self.model.delete_after)

    self.window.bind('<Shift-Right>', self.model.update_selection_range)
    self.window.bind('<Shift-Left>', self.model.update_selection_range)

    self.window.bind('<KeyPress>', self.model.insert)

  def _bind_clipboard_keys(self):
    self.window.bind('<Control-c>', self._copy_to_clipboard)
    self.window.bind('<Control-x>', self._cut_to_clipboard)
    self.window.bind('<Control-v>', self._paste_from_clipboard)
    self.window.bind('<Control-Shift-V>', self._paste_and_remove_from_clipboard)


  def _init_model(self, model: TextEditorModel):
    self.model = model
    model.attach(self, ObserverType.CURSOR)
    model.attach(self, ObserverType.TEXT)


  def show_text(self):
    text_opts = {
      "font": ("Courier New", 24)
    }

    text_widget = Widget(self.window, "text", text_opts)
    self._show_all_lines(text_widget)

    text_widget.configure(state='disabled')

    text_widget.place(x=0, y=0)
    self.cursor.lift()

    self.text = text_widget


  def _show_all_lines(self, text_widget: Widget):
    for index, line in enumerate(self.model.lines):
      text_widget.tk.call(text_widget._w, 'insert', f"{index + 1}.0", line + '\n')


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


  def _copy_to_clipboard(self, event):
    if self.model.selection_range.is_existing():
      text = self.model.get_text_in_selection()
      self.clipboard.push(text)


  def _cut_to_clipboard(self, event):
    self._copy_to_clipboard(None)
    self.model.delete_selection()


  def _paste_from_clipboard(self, event):
    text = self.clipboard.peek()
    self.model.insert_text(text)
    self.model.unselect()


  def _paste_and_remove_from_clipboard(self, event):
    print("I work")
    self._paste_from_clipboard(None)
    self.clipboard.pop()

  def update_cursor_location(self):
    self.cursor.place(x=self.model.cursor_location.x, y=self.model.cursor_location.y)
    self.cursor.lift()


  def update_text(self):
    self.text.configure(state='normal')
    self._update_all_lines()

    if self.model.selection_range.is_existing():
      start = self._create_tag_start_location()
      end = self._create_tag_end_location()

      self.text.tk.call(self.text._w, 'tag', 'add', 'bg', start, end)
      self.text.tk.call(self.text._w, 'tag', 'configure', 'bg', '-background', 'orange')

    self.text.configure(state='disabled')


  def _update_all_lines(self):
    for index, line in enumerate(self.model.lines):
      if self.text.tk.call(self.text._w, 'count', '-lines', '1.0', 'end') < len(self.model.lines):
        self.text.tk.call(self.text._w, 'insert', f"{index + 1}.0", line + '\n')
        print(self.text.tk.call(self.text._w, 'count', '-lines', '1.0', 'end'))
      else:
        self.text.tk.call(self.text._w, 'replace', f"{index + 1}.0", f"{index + 1}.end",  line)


  def _create_tag_start_location(self):
    row = self.model.selection_range.start.y + 1
    column = self.model.selection_range.start.x

    return f"{row}.{column}"


  def _create_tag_end_location(self):
    row = self.model.selection_range.end.y + 1
    column = self.model.selection_range.end.x

    return f"{row}.{column}"
