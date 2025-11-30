import configparser
import redis
from logger import *
import openrouteservice as ors

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
    
    
        #Retrieve API 
        self.ors_Client = ors.Client(key=config["OpenRouteAPI"]["api_key"])

        # Setup Logging
        self.loggersCritical=None
        self.loggersSuccess=None
        self.loggersDebug=None

        if config["Logging"]["Debug"]=="true":
            self.log_filename=config["Logging"]["log_filename"]
            self.loggersDebug=Debug(self.loggersDebug,self.log_filename) 

        if config["Logging"]["Success"]=="true":
            self.log_filename=config["Logging"]["log_filename"]
            self.loggersSuccess=Success(self.loggersSuccess,self.log_filename) 

        if config["Logging"]["Crtical"]=="true":
            self.log_filename=config["Logging"]["log_filename"]
            self.loggersCritical=Crtical(self.loggersCritical,self.log_filename)     

    #Logging Chain of Responsibility
    def logSucess(self,Info):
        if self.loggersSuccess is None:
            return
        else:
            self.loggersSuccess.logging(Info)

    def logCritical(self,Info):

        if self.loggersCritical is None:
            return
        else :
            self.loggersCritical.logging(Info)

    def logDebug(self,Info):
        if self.loggersDebug is None:
            return
        else:
            self.loggersDebug.logging(Info)

    
               
