from app import *

class MissionReport:
    def __init__(self, model):
        self.model = model
        self.app = App()
        self.client = self.app.ors_Client


    def generate_report(self, mission_key):
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

        #duration="Durations in secs: {}\n".format(matrix['durations'])
        #distance="Distances in m: {}".format(matrix['distances'])

        duration=matrix['durations'][0][1]  # Duration from start to end
        distance=matrix['distances'][0][1]  # Distance from start to end

        #Mission Report Structure
        Report=[
            f"Mission Report:{mission_key}\n\n",

            f"Start Location: {start}\n",
            f"End Location: {end}\n",
            f"Distance: {distance:.2f}m\n",
            f"Duration: {duration:.2f}s\n"
        ]
        return Report