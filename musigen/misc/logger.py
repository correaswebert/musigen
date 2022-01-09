import logging
from colorlog import ColoredFormatter
import client.globals as g


F_LOGFORMAT = "%(levelname)-8s | %(module)20s | %(lineno)3d | %(message)s"
C_LOGFORMAT = "%(log_color)s%(levelname)-8s%(reset)s | %(module)20s | %(log_color)s%(lineno)3d%(reset)s | %(log_color)s%(message)s%(reset)s"


f_formatter = logging.Formatter(F_LOGFORMAT)
c_formatter = ColoredFormatter(C_LOGFORMAT)

file = logging.FileHandler("file.log")
file.setFormatter(f_formatter)

stream = logging.StreamHandler()
stream.setFormatter(c_formatter)

log = logging.getLogger("root")
log.addHandler(file)


def init_logger():
    if g.LOG_LEVEL not in g.VALID_LOG_LEVELS:
        g.LOG_LEVEL = "WARNING"
    logging.root.setLevel(g.LOG_LEVEL)
    file.setLevel(g.LOG_LEVEL)
    stream.setLevel(g.LOG_LEVEL)

    if not g.SHOW_PROGRESS:
        log.addHandler(stream)


if __name__ == "__main__":
    log.warning("This is a warning!")
    log.debug("This is a debugging message.")
