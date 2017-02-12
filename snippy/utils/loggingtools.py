"""
Logging tools.
"""
import datetime
import glob
import logging
import os
from typing import Generic, Iterable
from snippy.settings import BASE_DIR

LOG_FORMAT_STANDARD = ("%(asctime)s %(levelname)s: "
                       "[%(filename)s:%(lineno)s, %(funcName)s()] "
                       "%(message)s")
TIME_FORMAT_STANDARD = "%Y-%m-%d %H:%M:%S"
LOG_DIR = os.path.join(BASE_DIR, "logs")


def get_logger(name, level: int=logging.INFO, filename: str=None,
               message_format: str=LOG_FORMAT_STANDARD,
               time_format: str=TIME_FORMAT_STANDARD):
    """Returns a logger instance.

    :param name: Module name
    :type name: str
    :param level: Logging level
    :type level: int
    :param filename: Output filename
    :type filename: str
    :param message_format: Message format
    :type message_format: str
    :param time_format: Timestamp format
    :type time_format: str
    """
    datestamp = datetime.date.today().strftime("%Y%m%d")

    if filename is None:
        filename = "{0}_{1}.log".format(name, datestamp)
    else:
        filename += "_{0}.log".format(datestamp)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    filepath = os.path.join(LOG_DIR, filename)
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    file_handler = logging.FileHandler(filepath)
    file_handler.setLevel(level)
    formatter = logging.Formatter(message_format, time_format)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def cleanup_logs(retention_days: int=30,
                 file_exts: Iterable(Generic(str))=(".log", )):
    """Clean up log files for a given retention period.

    :param retention_days: Days to retain log files
    :type retention_days: int
    :param file_exts: Log file extensions
    :type file_exts: list(str)
    """
    logger = get_logger('loggingtools', logging.DEBUG)
    filepaths = []
    for file_ext in file_exts:
        filepaths.extend(glob.glob("*{0}".format(file_ext)))

    today = datetime.date.today()
    for filepath in filepaths:
        date = _get_date_from_filepath(filepath)
        if today - date > datetime.timedelta(days=retention_days):
            os.remove(filepath)
            logger.debug("Removed %s", filepath)


def _get_date_from_filepath(filepath):
    return (datetime.datetime.strptime(_get_datestamp_from_filepath(filepath),
                                       "%Y%m%d"))


def _get_datestamp_from_filepath(filepath):
    return filepath[-10:-4]
