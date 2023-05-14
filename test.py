import tkinter as tk

root = tk.Tk()

text_widget = tk.Text(root)
text_widget.pack()

# Insert some text into the widget
text_widget.insert(tk.END, "This is some text")

# Add a tag to the text
text_widget.tag_add("bg", "1.0", "1.5")

# Configure the tag with a background color
text_widget.tag_configure("bg", background="orange")

root.mainloop()
