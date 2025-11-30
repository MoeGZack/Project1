from app import *
### API call using OpenRouteService
### Mission Report used to calculate Route Distance and time in a Mission
### Output is Sent to View
class MissionReport:
    def __init__(self, model):
        self.model = model
        self.app = App()
        self.client = self.app.ors_Client


    def create_report(self, mission_key):
        App().logSucess("Generating Mission Report:"+str(mission_key))
        mission_data = self.model.get_mission_data(mission_key)
        if not mission_data:
            return "No data found for the selected mission."

        start=mission_data["start_coords"]
        end=mission_data["end_coords"]

        matrix = self.client.distance_matrix(
            locations=[start,end],
            profile='driving-car',
            metrics=['distance', 'duration'],
            validate=False,
        )

        #OpenSource returns a full distanc matrix for all coordiante pairs
        #We Make our Mission nodes by 2 coordinates. ORS returns a 2x2
        duration=matrix['durations'][0][1]  
        distance=matrix['distances'][0][1]  

        #Mission Report Structure
        Report=[
            f"Mission Report:{mission_key}\n\n",

            f"Start Location: {start}\n",
            f"End Location: {end}\n",
            f"Distance: {distance:.2f}m\n",
            f"Duration: {duration:.2f}s\n"
        ]
        
        return "\n".join(Report)