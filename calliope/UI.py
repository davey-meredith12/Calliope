#from code documentation for tkinter
import tkinter as tk
from tkinter import ttk

spacing: int = 10
length: int = 500
topStart: int = 40
leftStart: int = 1

root = tk.Tk()
root.title("frame name")
#make the window expand to fill the screen
root.state("zoomed")
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=1)

#create canvas and fill with lines
note_canvas = tk.Canvas(frm, background="white", width=500, height=100)
note_canvas.grid(column=0, row=2)
for i in range(5):
    x0: float = leftStart
    y0: float = topStart + (i-1)*spacing
    x1 = x0 + length
    y1 = y0
    note_canvas.create_line(x0, y0, x1, y1)
note_canvas.create_line(15, 15, 30, 30)
root.mainloop()






# root = tk.Tk()
# root.title("Window Name")
#
# frame = tk.Frame(root)
# frame.pack(fill = "both", expand = True)
#
# button = tk.Button(frame, text = "button", pady = 5)
#
# root.mainloop()