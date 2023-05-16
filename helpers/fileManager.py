from tkinter import filedialog as fd
from models.TextEditorModel import TextEditorModel

files = [('All Files', '*.*'),
         ('Python Files', '*.py'),
         ('Text Document', '*.txt')]

def save_file(self):
  file = fd.asksaveasfile(filetypes = files, defaultextension = files)

  with open(file.name, 'w') as file:
    for line in self.model.lines:
      file.write(line + '\n')

def open_file(self):
  file = fd.askopenfilename(filetypes=files, defaultextension = '.txt')

  with open(file, 'r') as f:
    lines = ""
    for line in f:
      lines += line

    model = TextEditorModel(lines)
    self._init_model(model)
    self.update_text()

def exit_file(self):
  self.window.destroy()
