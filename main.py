import tkinter as tk
from models.TextEditorModel import TextEditorModel
from models.TextEditor import TextEditor

new_window = tk.Tk()
model = TextEditorModel("ABC\nDASDSA")
editor = TextEditor(new_window, model)
editor.show_text()

# keep the window displaying
new_window.mainloop()
