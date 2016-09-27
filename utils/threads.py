import threading
import logging

from api.http import app
from collector.basic import basic_collect
from collector.iis import iis_collect
from collector.sqlserver import sqlserver_collect
from collector.reporter import status_report


run_period = 60

class APIThread(threading.Thread):
    '''
    http service thread
    '''

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print "Starting " + self.name
        # Get lock to synchronize threads
        #print_time(self.name, self.counter, 3)
        # Free lock to release next thread
        app.run(port=1988)


class BasicCollectThread(threading.Thread):
    """
    collect basic metric of windows
    """

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        logging.debug("Starting " + self.name)
        basic_collect(run_period)


class IISCollectThread(threading.Thread):
    """
    collect basic metric of windows
    """

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        logging.debug("Starting " + self.name)
        iis_collect(run_period)


class SQLServerCollectThread(threading.Thread):
    """
    collect basic metric of windows
    """

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        logging.debug("Starting " + self.name)
        sqlserver_collect(run_period)


class StatusReportThread(threading.Thread):
    """
    collect basic metric of windows
    """

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        logging.debug("Starting " + self.name)
        status_report(run_period)

ThreadLock = threading.Lock()
Threads = []
