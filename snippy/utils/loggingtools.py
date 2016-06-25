import datetime
import glob
import logging
import os

LOG_FORMAT_STANDARD = ("%(asctime)s %(levelname)s: "
                       "[%(filename)s:%(lineno)s, %(funcName)s()] "
                       "%(message)s")
TIME_FORMAT_STANDARD = "%Y-%m-%d %H:%M:%S"
LOG_DIR = os.path.join("snippy", "logs")

def get_logger(name, level=logging.INFO, filename=None,
               message_format=LOG_FORMAT_STANDARD,
               time_format=TIME_FORMAT_STANDARD):
    datestamp = datetime.date.today().strftime("%Y%m%d")

    if filename is None:
        filename = "{0}_{1}.log".format(name, datestamp)
    else:
        filename += "_{0}.log".format(datestamp)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    filepath = os.path.join(LOG_DIR, filename)
    file_handler = logging.FileHandler(filepath)
    file_handler.setLevel(level)
    formatter = logging.Formatter(message_format, time_format)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

def cleanup_logs(retention_days=30, file_exts=(".log", )):
    logger = get_logger('loggingtools', logging.DEBUG)
    filepaths = []
    for file_ext in file_exts:
        filepaths.extend(glob.glob("*{0}".format(file_ext)))

    today = datetime.date.today()
    for filepath in filepaths:
        date = _get_date_from_filename(filepath)
        if today - date > datetime.timedelta(days=retention_days):
            os.remove(filepath)
            logger.debug("Removed {0}".format(filepath))

def _get_date_from_filename(filename):
    return (datetime.datetime.strptime(_get_datestamp_from_filename(filepath),
                                       "%Y%m%d"))

def _get_datestamp_from_filename(filename):
    return filename[-10:-4]