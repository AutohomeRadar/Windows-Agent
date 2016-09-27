import logging
import os
import inspect
import g


def get_logger(logger_name='[PythonService]', dirpath=None):

    logger = logging.getLogger(logger_name)

    if dirpath is None:
        # dirpath = os.path.join(os.path.dirname(__file__), os.path.abspath('..'))
        dirpath = os.path.dirname(__file__)
        # dirpaht = "D:\"
    handler = logging.FileHandler(os.path.join(dirpath, "service.log"))

    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    if g.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.DEBUG)

    return logger


def init_log(path=None):
    if g.DEBUG:
        logging.basicConfig(filename=os.path.join(path, 'app.log'),level=logging.DEBUG, format='%(asctime)s %(filename)-12s %(levelname)-8s %(message)s')
    else:
        logging.basicConfig(filename=os.path.join(path, 'app.log'),level=logging.INFO, format='%(asctime)s %(filename)-12s %(levelname)-8s %(message)s')
