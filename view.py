import tkinter as tk
from tkinter import ttk


window =tk.Tk()
choices=["A,V,X,D,E,S"]
window.geometry=('300x300')
DROPDOWN=ttk.Combobox(window,values=choices)
DROPDOWN.pack()

window.mainloop()

