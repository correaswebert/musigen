import logging
from colorlog import ColoredFormatter


class Logger:

    APP_LOGGER_NAME = "musigen_logger"

    FILE_LOGFORMAT = (
        "%(asctime)s | "
        "%(levelname)-8s | "
        "%(module)10s | "
        "%(message)s"
    )

    STREAM_LOGFORMAT = (
        "%(log_color)s%(levelname)-8s%(reset)s | "
        "%(module)10s | "
        "%(log_color)s%(lineno)3d%(reset)s | "
        "%(log_color)s%(message)s%(reset)s"
    )

    def __init__(self):
        self.logger = logging.getLogger(Logger.APP_LOGGER_NAME)
        logging.root.setLevel("DEBUG")
        self.logger.handlers.clear()

    def add_file_handler(self, filename: str, log_level: str = "WARNING"):
        f_formatter = logging.Formatter(self.FILE_LOGFORMAT)
        self.file_handler = logging.FileHandler(filename)
        self.file_handler.setFormatter(f_formatter)
        self.file_handler.setLevel(log_level)
        self.logger.addHandler(self.file_handler)

    def add_stream_handler(self, log_level: str = "DEBUG"):
        s_formatter = ColoredFormatter(self.STREAM_LOGFORMAT)
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(s_formatter)
        self.stream_handler.setLevel(log_level)
        self.logger.addHandler(self.stream_handler)
    
    @staticmethod
    def get_logger() -> logging.Logger:
        return logging.getLogger(Logger.APP_LOGGER_NAME)
