import configparser
import redis


class App():
    
    def setup(self):
        # Load configuration from config.cfg
        config = configparser.ConfigParser()
        config.read('config.cfg')

        # Retrieve Redis connection details from the configuration file
        redis_host = config.get('Database', 'host')
        redis_port = config.getint('Database', 'port')
        redis_password = config.get('Database', 'password')

        # Initialize Redis connection
        self.redis_client = redis.Redis(
            host=config["Database"]["host"],
            port=config["Database"]["port"],
            password=config["Database"]["password"],
            decode_responses=True)
        
        # Test the connection
        self.redis_client.ping()
        print("Redis connection details:")
        print(f"Host: {config['Database']['host']}")
        print(f"Port: {config['Database']['port']}")
        print("Connected to Redis successfully!")
        #Retrieve Information within DB

        
    # Retrieve Information within DB
    def getMissionData(self, key):
        
        keys=list(self.redis_client.scan_iter())
        value=self.redis_client.json().get(key)
        if not keys:
            print("No keys found in Redis.")
        else:
         print(f"Keys in Redis: {keys}")
         print(f"Value for '{key}': {value}")
               
if __name__ == "__main__":
        app = App()
        app.setup()
        app.getMissionData("Mission1") # Example key to retrieve mission data
