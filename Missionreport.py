from matplotlib.pylab import matrix
from app import *

class MissionReport:
    def __init__(self, model):
        self.model = model
        self.app = App()
        self.client = self.app.ors.Client


    def generate_report(self, mission_key):
        mission_data = self.model.get_mission_data(mission_key)
        if not mission_data:
            return "No data found for the selected mission."

        start=mission_data["start_coords"]
        end=mission_data["end_coords"]
        client=App().osrs_Client

        matrix = client.distance_matrix(
            locations=[start,end],
            profile='driving-car',
            metrics=['distance', 'duration'],
            validate=False,
        )

        duration="Durations in secs: {}\n".format(matrix['durations'])
        distance="Distances in m: {}".format(matrix['distances'])

        #Mission Report Structure
        Report=[
            f"Mission Report:{mission_key}",

            f"Start Location: {start}",
            f"End Location: {end}",
            f"Distance: {distance}",
            f"Duration: {duration}"
        ]
        return Report