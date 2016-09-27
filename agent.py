import socket
import time
import json
import os
import logging

import pythoncom
import win32serviceutil
import win32service
import win32event
import servicemanager

from utils.log import get_logger, init_log
from utils.threads import (APIThread, BasicCollectThread, IISCollectThread,
                           SQLServerCollectThread, StatusReportThread)
from utils import g


class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "OpenFalconAgent"
    _svc_display_name_ = "Open Falcon Windows Agent"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.isAlive = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.isAlive = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.isAlive = True
        # Create new threads
        self.main()

    def main(self):

        current_path = os.path.dirname(os.path.abspath(__file__))
        cfg_file = os.path.join(current_path, 'cfg.json')

        try:
            with open(cfg_file) as confile:
                config = json.load(confile)
        except Exception as e:
            logging.error(e)
		
        g.HOSTNAME = config['hostname']
        g.DEBUG = config['debug']
        g.IP = config['ip']
        g.HEARTBEAT = config['heartbeat']
        g.TRANSFER = config['transfer']
        g.HTTP = config['http']
        g.COLLECTOR = config['collector']
        g.IGNORE = config['ignore']

        init_log(current_path)

        logging.info('starting api thread....')
        api_thread = APIThread(1, "HTTPThread", 1)
        api_thread.start()

        logging.info('starting basic metric collecting thread....')
        basic_thread_collect = BasicCollectThread(2, "BasicCollectThread", 1)
        basic_thread_collect.start()

        logging.info('starting iis metric collecting thread....')
        iis_thread_collect = IISCollectThread(3, "IISCollectThread", 1)
        iis_thread_collect.start()

        logging.info('starting sqlserver metric collecting thread....')
        sqlserver_thread_collect = SQLServerCollectThread(
            4, "SQLServerCollectThread", 1)
        sqlserver_thread_collect.start()

        logging.info('starting status reporting thread....')
        status_report_thread = StatusReportThread(
            5, "StatusReportThread", 1)
        status_report_thread.start()

        while self.isAlive:
            time.sleep(60)
        logging.error('end of main, should never going to here')


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
