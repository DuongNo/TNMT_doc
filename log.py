import logging
import os
from datetime import date

class LoggingDebug:
    def __init__(self,path_log):
        self.path_log = path_log
        self.month, self.year = self.current_date()
        self.log_folder = os.path.join(self.path_log, self.year)
        isExist = os.path.exists(self.log_folder)
        print("self.log_folder = ",self.log_folder)
        if not isExist:
            os.mkdir(self.log_folder)
        fileName = self.month + "_" + self.year + ".log"
        log_file = os.path.join(self.log_folder, fileName)

        self.logger = logging.getLogger(LoggingDebug.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.fileHandler = logging.FileHandler(log_file,mode='a')  
        self.fileHandler.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        self.fileHandler.setFormatter(self.formatter) 
        self.logger.addHandler(self.fileHandler)
    
    def checkFileName(self):
        month, year = self.current_date()
        if self.year != year:
            self.log_folder = os.path.join(self.path_log, year)
            isExist = os.path.exists(self.log_folder)
            if not isExist:
                os.mkdir(self.log_folder)            
            self.logger.removeHandler(self.fileHandler)     
            fileName = month + "_" + year + ".log"
            log_file = os.path.join(self.log_folder, fileName)
           
            self.fileHandler = logging.FileHandler(log_file,mode='a')
            self.fileHandler.setLevel(logging.DEBUG)
            self.formatter = logging.Formatter('%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
            self.fileHandler.setFormatter(self.formatter)
            self.logger.addHandler(self.fileHandler)
            self.year = year
        elif self.month != month:
            self.logger.removeHandler(self.fileHandler)     
            fileName = month + "_" + year + ".txt"
            log_file = os.path.join(self.log_folder, fileName)

            self.fileHandler = logging.FileHandler(log_file,mode='a')
            self.fileHandler.setLevel(logging.DEBUG)
            self.formatter = logging.Formatter('%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
            self.fileHandler.setFormatter(self.formatter)
            self.logger.addHandler(self.fileHandler)
            self.month = month

    def debug(self, message):
        self.checkFileName()
        self.logger.debug(message)

    def info(self, message):
        self.checkFileName()
        self.logger.info(message)

    def warning(self, message):
        self.checkFileName()
        self.logger.warning(message)
    
    def error(self, message):
        self.checkFileName()
        self.logger.error(message)
        
    def critical(self, message):
        self.checkFileName()
        self.logger.critical(message)

    def exception(self, message):
        self.checkFileName()
        self.logger.exception(message)

    def current_date(self):
        t1 = date.today().strftime("%m %Y")
        #print("t1 =", t1)
        month = t1[0:2]
        year = t1[3:7]
        #print("month = ",month)
        #print("year = ",year)
        return month, year

    # link guider https://docs.python.org/3/howto/logging.html#what-happens-if-no-configuration-is-provided
    def testLog(self):
        logger = logging.getLogger(LoggingDebug.__name__)   
        fileHandler = logging.FileHandler("demo.log",mode='a')
        fileHandler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        logger.debug('debug message')
        logger.info('info message')
        logger.warning('warn message')
        logger.error('error message')
        logger.critical('critical message')
        logger.exception("this exception")
        fileHandler2 = logging.FileHandler("/home/duongpa/project/chatbot/travel/logs/demo2.log",mode='a')
        logger.addHandler(fileHandler2)
        logger.removeHandler(fileHandler)
        logger.info('info message 2')
        logger.debug('debug message')
        logger.info('info message')
        logger.warning('warn message')
        logger.error('error message')
        logger.critical('critical message')
    
if __name__ == "__main__":
    demo = LoggingDebug("./logs")
    #demo.testLog()
    demo.info("this if file name")