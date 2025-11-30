import datetime
from abc import ABC, abstractmethod

class Logger(ABC):

    @abstractmethod
    def log_entry(self, info):
        pass

    def logging(self, info):
        
        self.log_entry(info)

        if (self.logger_Next ==None):
            return
        else:
            self.logger_Next.log(info)

    def __init__(self,_logger_Next):
        self.logger_Next = _logger_Next

class FileLogger(Logger):
    def __init__(self,_logger_Next,log_filename):
        self.__logfile=open(log_filename, "a+")
        super().__init__(_logger_Next)

    def log_entry(self, info):
       self.__logfile.write(str(datetime.datetime.now()) + ": " + info \
                              + "\n")

class ConsoleLogger(Logger):
    def log_entry(self, info):
        print(str(datetime.datetime.now())+ ": " + info)

class DatabaseLogger(Logger):

    def __init__(self, _logger_Next,redis_client):
        self.__redis_client=redis_client
        super().__init__(_logger_Next)
    def log_entry(self, info):
        self.__redis_client.hset("logger",str(datetime.datetime.now()),info)