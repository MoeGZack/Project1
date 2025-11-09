from app import *
from report import *
from time import time
import tkinter as tk
from tkinter import ttk

class View:

    def PythonGUI(self):
        self.root = tk.Tk()
        self.root.title("Mission Control")
        self.root.geometry("800x600")
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.RetrieveMissionbtn = ttk.Button(self.frame, text="Retrieve Mission Data")
        self.RetrieveMissionbtn.pack(pady=10)
        self.missionLbl = ttk.Label(self.frame, text="Mission Control Panel", font=("Helvetica", 16))
        self.missionLbl.pack(pady=10)
        self.MissionSelect = ttk.Label(self.frame, text="Select Mission:")
        self.MissionSelect.pack(pady=5)
        self.GenerateBtn = ttk.Button(self.frame, text="Generate Report")
        self.GenerateBtn.pack(pady=20)

    def Mainpage(self):
        self.RetrieveMissionbtn

    def MissionSelect(self):
        self.MissionSelect

    def generate_report(self):
        self.GenerateBtn()


class Controller:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view

    def run(self):
        self.__view.PythonGUI()
        if self.__view.RetrieveMissionbtn:
            
    

    def generate_MissionList(self):
        pass
        
class Model:
    def __init__(self):
        pass



