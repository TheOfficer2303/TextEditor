import tkinter as tk

root = tk.Tk()

text = tk.Text(root, height=5, width=30)
text.pack()

# Insert some text into the widget
text.insert("1.0", "Hello, World!\nHow are you today?")

# Get the coordinates of the first 'o' character
char_coords = text.bbox("1.5")

print("The coordinates of the first 'o' character are:", char_coords)

root.mainloop()
