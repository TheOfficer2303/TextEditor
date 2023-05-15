import tkinter as tk
from models.TextEditorModel import TextEditorModel
from models.TextEditor import TextEditor

new_window = tk.Tk()
new_window.geometry("1000x500")

model = TextEditorModel("abc\n123\n321\ncba\nASDASDASD")
editor = TextEditor(new_window, model)
editor.show_text()

# keep the window displaying
new_window.mainloop()
