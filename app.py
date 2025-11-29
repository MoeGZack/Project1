import configparser
import redis
from logger import *

class App():
    __instance = None

    def __new__(cls):
        if (cls.__instance is None):
            cls.__instance = super(App, cls).__new__(cls)
            cls.__instance.setup()

        return cls.__instance
    
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
        
        # Setup Logging
        self.loggers=None
        #Console Logger Initizalization
        if config["Logging"]["console"]=="True":
            self.loggers=ConsoleLogger(self.loggers)
        #Fle Logger Wraps Console Logger
        if config["Logging"]["file"]=="True":
            self.__logfilename=config["Logging"]["__logfilename"]
            self.loggers=FileLogger(self.loggers,self.__logfilename)
        #DB wraps what is existing
        if config["Logging"].get("database","FALSE")=="True":
            self.loggers=DatabaseLogger(self.loggers,self.redis_client)
    
    def logging(self,Info):
        if self.loggers is None:
            return
        else:
            self.loggers.logging(Info)
            
    

    
               
