import datetime
from abc import ABC, abstractmethod



class Logger(ABC):

    @abstractmethod
    def log_entry(self, info):
        pass

    def logging(self, info):
        self.log_entry(info)

        if (self.__loggerNext ==None):
            return
        else:
            self.__loggerNext.log(info)

class FileLogger(Logger):
    def __init__(self,__loggerNext,__logfilename):
        self.__logfile=open(__logfilename, "w")
        super().__init__(__loggerNext)

    def log_entry(self, info):
        self.__logfile.write(str(datetime.datetime.now())+": "+info \  +"\n")

class ConsoleLogger(Logger):
    def log_entry(self, info):
        print(str(datetime.datetime.now())+ ": " + info)

class DatabaseLogger(Logger):

    def __init__(self, __loggerNext,redis_client):
        self.__redis_client=redis_client
        super().__init__(__loggerNext)
    def log_entry(self, info):
        self.__redis_client.hset("logger",str(datetime.datetime.now()),info)