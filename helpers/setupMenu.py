from tkinter import Menu
from consts.Menu import FILE_MENU, EDIT_MENU

def setup_menu(self):
  self.menubar = Menu(self.window)

  setup_file_menu(self)
  setup_edit_menu(self)

  self.window.config(menu = self.menubar)


def setup_file_menu(self):
  self.file_menu = Menu(self.menubar, tearoff=0)
  for option in FILE_MENU:
    command = f"_{option['command']}_file"
    self.file_menu.add_command(label=option["label"], command=getattr(self, command))

  self.menubar.add_cascade(label = "File", menu = self.file_menu)

def setup_edit_menu(self):
  self.edit_menu = Menu(self.menubar, tearoff=0)
  for option in EDIT_MENU:
    state = "normal" if getattr(self, f"{option['state']}_action_active") else "disabled"
    self.edit_menu.add_command(label=option["label"],
                               command=getattr(self, option["command"]),
                               state=state)

  self.edit_menu.add_command(label="Delete Selection", command=self._delete_selection)

  self.menubar.add_cascade(label = "Edit", menu = self.edit_menu)

def setup_move_menu(self):
  self.move_menu = Menu(self.menubar, tearoff=0)
