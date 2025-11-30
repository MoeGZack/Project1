from app import *
from Missionreport import *
import tkinter as tk
from tkinter import ttk

class View:

    def PythonGUI(self):

        self.root = tk.Tk()
        self.root.title("Mission Control")
        self.root.geometry("700x450")


        self.missionLbl = ttk.Label(self.root, text="Mission Control Panel", font=("Helvetica", 16))
        self.missionLbl.place(x=225, y=10)

        self.RetrieveMissionbtn = ttk.Button(self.root, text="Retrieve Missions")
        self.RetrieveMissionbtn.place(x=50, y=50)
        self.GenerateBtn = ttk.Button(self.root, text="Generate Report")
        self.GenerateBtn.place(x=375, y=50)
       
        ttk.Label(self.root, text="Select Mission:").place(x=50, y=100)

        self.MissionList = tk.Listbox(self.root, height=12,width=50)
        self.MissionList.place(x=50, y=130)

        ttk.Label(self.root, text="Mission Report:").place(x=375, y=100)

        self.MissionReport= tk.Text(self.root, height=12,width=50)
        self.MissionReport.place(x=375, y=130)
       
        self.StatusLbl = ttk.Label(self.root, text="Status: —")
        self.StatusLbl.place(x=50, y=400)
class Controller:
    def __init__(self, view, model):
        self.__view = view
        self.__model = model
    
        
    def run(self):
        self.__view.PythonGUI()
        self.__view.RetrieveMissionbtn.config(command=self.generate_MissionList)
        self.__view.GenerateBtn.config(command=self.generate_Report)
        self.update_status()
        self.__view.root.mainloop()   
    
    def generate_MissionList(self):
        keys = self.__model.list_mission_keys()

        n = self.__view.MissionList
        n.delete(0, tk.END)

        if not keys:
            self.__view.StatusLbl.config(text="Status: No Missions found.")
            return
        
        for key in keys:
            n.insert(tk.END, key)
        self.__view.StatusLbl.config(text=f"Status: Retrieved {len(keys)} Missions.")

    def generate_Report(self):
        Selection=self.__view.MissionList.curselection()

        if not Selection:
            self.__view.StatusLbl.config(text="Status: Please Select Mission.")
            return
        
        MissionKey=self.__view.MissionList.get(Selection[0])

        self.__view.StatusLbl.config(text=f"Status: Mission Report generated {MissionKey}")

    def update_status(self):
        stat = self.__model.health()   
        Db_Api_status =(bool(stat["db_ok"]), bool(stat["api_ok"]))
       
        match Db_Api_status:      
            case (True, True):
                txt = "Status: Connected (DB Good, API Good)"
            case (True, False):
                txt = "Status: Partial (DB Good, API Bad)"
            case (False, True):
                txt = "Status: Partial (DB Bad, API Good)"
            case _:
                txt = "Status: Disconnected (DB Bad, API Bad)"
        self.__view.StatusLbl.config(text=txt)
        
class Model:
    
    def __init__(self):
        self.app=App()
        self.redis=self.app.redis_client

    def list_mission_keys(self):
        return list(self.redis.keys(match="Mission:*"))
    
    def get_mission_data(self, key):
        mission=self.redis.json().get(key)
        if not mission:
            return None
        n1=mission["nodes"][0]
        n2=mission["nodes"][1]

        return {
            "start_coords":[n1["x"],n1["y"]],
            "end_coords":[n2["x"],n2["y"]],
        }
    def health(self):
        db_ok=True
        api_ok=True
        try:
            self.redis.ping()
        except redis.exceptions.ConnectionError:
            db_ok=False
        api_ok=getattr(self.app,"ors_Client")  
        return{"db_ok":db_ok,"api_ok":api_ok}
    
    

    
