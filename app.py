import configparser
import redis
import requests

class App():
    
    def setup(self):
        # Load configuration from config.cfg
        config = configparser.ConfigParser()
        config.read('config.cfg')
    # Initialize Redis connection
        self.redis_client = redis.Redis(
            host=config["Database"]["host"],
            port=config["Database"]["port"],
            password=config["Database"]["password"],
            decode_responses=True)
     # Test the connection
        self.redis_client.ping()
        print("Connected to Redis successfully!")

        #Retrieve API 
        self.api_key = config["OpenRouteAPI"]["api_key"]
        self.test_api_Connection()
        
    # Retrieve Information within DB
    def getMissionData(self, key):
        
        keys=list(self.redis_client.scan_iter())
        value=self.redis_client.json().get(key)
        if not keys:
            print("No keys found in Redis.")
        else:
            print(f"Keys in Redis: {keys}")
            print(f"Value for '{key}': {value}")

    def test_api_Connection(self):
        mission = self.redis_client.json().get("Mission2")
        if not mission or "nodes" not in mission or len(mission["nodes"]) < 2:
            print("Mission2 missing or incomplete.")
            return

        n1, n2 = mission["nodes"][0], mission["nodes"][1]
        start = f"{float(n1['x']):.6f},{float(n1['y']):.6f}"
        end   = f"{float(n2['x']):.6f},{float(n2['y']):.6f}"

        url = "https://api.openrouteservice.org/v2/directions/driving-car"
        params = {"api_key": self.api_key, "start": start, "end": end}
            

        result = requests.get(url, params=params, timeout=15)

        if result.status_code != 200:
            print("API request failed with status code:", result.status_code)
            return
           
        try:
            data=result.json()
            route=data["features"][0]["properties"]["segments"][0]
            distance_km=route["distance"] / 1000  
            duration_min=route["duration"] / 60  
            print(f"Distance: {distance_km:.2f} km")
            print(f"Duration: {duration_min:.2f} minutes")  

        except (KeyError, IndexError):
                print("Error parsing API response:")
               
if __name__ == "__main__":
    app = App()
    app.setup()
    app.getMissionData("Mission2")