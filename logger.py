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

class Debug(Logger):
    def __init__(self,_logger_Next,log_filename):
        self.__logfile=open(log_filename, "a+")
        super().__init__(_logger_Next)

    def level(self):
        return "DEBUG"

    def log_entry(self, info):
       self.__logfile.write(
           f"[DEBUG]{str(datetime.datetime.now())}: {info} \n"
        )
class Success(Logger):
    def __init__(self,_logger_Next,log_filename):
        self.__logfile=open(log_filename, "a+")
        super().__init__(_logger_Next)

    def level(self):
        return "SUCCESS"

    def log_entry(self, info):
       self.__logfile.write(
           f"[SUCCESS]{str(datetime.datetime.now())}: {info} \n"
        )

class Crtical(Logger):
    def __init__(self,_logger_Next,log_filename):
        self.__logfile=open(log_filename, "a+")
        super().__init__(_logger_Next)

    def level(self):
        return "CRITICAL"

    def log_entry(self, info):
       self.__logfile.write(
           f"[CRITICAL]{str(datetime.datetime.now())}: {info} \n"
        )