import logging
import logging.handlers
import time

class Logger:

    def __init__(self)->None:
        self.logger = logging.getLogger('')
        self.setup_logging()

    def setup_logging(self)->None:
        #log format
        LogFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=LogFormat)

        #configure formater
        formatter = logging.Formatter(LogFormat)

        #configure console handler
        console = logging.StreamHandler()
        console.setFormatter(formatter)

        #configure Time
        log_file = 'logs/fastapi-reg.log'
        file = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight', backupCount=7)
        file.setFormatter(formatter)

        #add handlers
        self.logger.addHandler(console)
        self.logger.addHandler(file)


logger = Logger()