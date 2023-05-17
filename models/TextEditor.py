from tkinter import Tk, Widget

from iterators.AllLines import AllLinesIterator
from iterators.RangeLines import RangeIterator

from managers.UndoManager import UndoManager

from models.StatusBar import StatusBar
from models.TextEditorModel import TextEditorModel
from models.ClipboardStack import ClipboardStack
from models.Cursor import Cursor as CursorModel

import consts.Cursor as Cursor
from consts.Stack import StackType
from consts.Observer import ObserverType

from observers.CursorObserver import CursorObserver
from observers.TextObserver import TextObserver
from observers.ClipboardObserver import ClipboardObserver
from observers.UndoStackObservers.RedoStackObserver import RedoStackObserver
from observers.UndoStackObservers.UndoStackObserver import UndoStackObserver

from helpers.setupMenu import setup_menu
from helpers.fileManager import save_file, open_file, exit_file

class TextEditor(ClipboardObserver, CursorObserver, TextObserver, UndoStackObserver, RedoStackObserver):
  def __init__(self, window: Tk, model: TextEditorModel) -> None:
    self.clipboard = ClipboardStack("texts")
    self.undo_manager = UndoManager()

    self._init_model(model)
    self._init_window(window)
    self._init_status_bar()
    self._init_actions()

    self.cursor = self._show_cursor()

    setup_menu(self)
    self.show_text()

  def _init_window(self, window: Tk):
    self.window = window
    self._bind_cursor_keys()
    self._bind_text_editing_keys()
    self._bind_clipboard_keys()
    self._bind_undo_manager_keys()

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

  def _bind_undo_manager_keys(self):
    self.window.bind('<Control-z>', self._undo)
    self.window.bind('<Control-y>', self._redo)


  def _init_model(self, model: TextEditorModel):
    self.model = model
    model.attach(self, ObserverType.CURSOR)
    model.attach(self, ObserverType.TEXT)

    self.clipboard.attach(self)
    self.undo_manager.attach_redo(self)
    self.undo_manager.attach_undo(self)

  def _init_status_bar(self):
    self.status_bar = StatusBar(self.window)
    self.model.attach(self.status_bar, ObserverType.CURSOR)
    self.model.attach(self.status_bar, ObserverType.TEXT)

  def _init_actions(self):
    self.cut_action_active = False
    self.copy_action_active = False
    self.paste_action_active = False
    self.paste_take_action_active = False
    self.undo_action_active = False
    self.redo_action_active = False
    self.delete_selection_action_active = False

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
    all_lines_iter = AllLinesIterator(self.model.lines)
    for line in all_lines_iter:
      text_widget.tk.call(text_widget._w, 'insert', f"{all_lines_iter.current + 1}.0", line + '\n')


  def _show_cursor(self):
    options = {
      "height": Cursor.HEIGHT,
      "width": Cursor.WIDTH,
      "bg": Cursor.COLOR,
    }

    cursor = Widget(self.window, "frame", options)
    cursor.place(x=self.model.cursor.location.x, y=self.model.cursor.location.y)
    cursor.lift()

    return cursor


  def _copy_to_clipboard(self, event=None):
    if self.model.selection_range.is_existing():
      text = self.model.get_text_in_selection()
      self.clipboard.push(text)


  def _cut_to_clipboard(self, event=None):
    self._copy_to_clipboard(None)
    self.model.delete_selection()


  def _paste_from_clipboard(self, event=None):
    text = self.clipboard.peek()
    self.model.insert_text(text)
    self.model.unselect()


  def _paste_and_remove_from_clipboard(self, event=None):
    self._paste_from_clipboard(None)
    self.clipboard.pop()

  def _undo(self, event=None):
    self.undo_manager.undo()

  def _redo(self, event=None):
    self.undo_manager.redo()


  def update_cursor_location(self, cursor: CursorModel):
    self.cursor.place(x=cursor.location.x, y=cursor.location.y)
    self.cursor.lift()


  def update_text(self, text=None):
    self.text.configure(state='normal')
    self._update_all_lines()

    self.copy_action_active, self.cut_action_active, self.delete_selection_action_active = False, False, False
    if self.model.selection_range.is_existing():
      self.copy_action_active, self.cut_action_active, self.delete_selection_action_active = True, True, True

      start = self._create_tag_start_location()
      end = self._create_tag_end_location()

      self.text.tk.call(self.text._w, 'tag', 'add', 'bg', start, end)
      self.text.tk.call(self.text._w, 'tag', 'configure', 'bg', '-background', 'orange')

    setup_menu(self)
    self.text.configure(state='disabled')


  def update_clipboard(self):
    if self.clipboard.is_empty():
      self.paste_action_active, self.paste_take_action_active = False, False
    else:
      self.paste_action_active, self.paste_take_action_active = True, True

    setup_menu(self)

  def stack_empty(self, stack_type: StackType):
    if stack_type == StackType.UNDO:
      self.undo_action_active = False
    else:
      self.redo_action_active = False

    setup_menu(self)

  def stack_not_empty(self, stack_type: StackType):
    if stack_type == StackType.UNDO:
      self.undo_action_active = True
    else:
      self.redo_action_active = True

    setup_menu(self)

  def _update_all_lines(self):
    all_lines_iter = AllLinesIterator(self.model.lines)
    for line in all_lines_iter:
      if self.text.tk.call(self.text._w, 'count', '-lines', '1.0', 'end') < len(self.model.lines):
        self.text.tk.call(self.text._w, 'insert', f"{all_lines_iter.current }.0", line + '\n')
        print(self.text.tk.call(self.text._w, 'count', '-lines', '1.0', 'end'))
      else:
        self.text.tk.call(self.text._w, 'replace', f"{all_lines_iter.current }.0", f"{all_lines_iter.current }.end",  line)


  def _create_tag_start_location(self):
    row = self.model.selection_range.start.y + 1
    column = self.model.selection_range.start.x

    return f"{row}.{column}"


  def _create_tag_end_location(self):
    row = self.model.selection_range.end.y + 1
    column = self.model.selection_range.end.x

    return f"{row}.{column}"


  def _delete_selection(self):
    return self.model.delete_selection()

  def _move_to_start(self):
    self.model.move_cursor_to_origin_x()
    self.model.move_cursor_to_origin_y()

  def _move_to_end(self):
    self.model.move_cursor_to_end()

  def _save_file(self):
    save_file(self)

  def _open_file(self):
    open_file(self)

  def _exit_file(self):
    exit_file(self)
