import time
import logging

from rpc.hbs import report_status_to_hbs
from utils import g


def report():
    """
    report status info to hbs
    """
    data = {
        "Hostname": g.HOSTNAME,
        "IP": g.IP,
        "AgentVersion": g.VERSION,
        "PluginVersion": "plugin not enabled"
    }
    logging.debug(data)

    try:
        res = report_status_to_hbs(data)
    except Exception as e:
        logging.error(e, exc_info=True)
    logging.info("report to hbs --> %s" % res)


def status_report(period):
    logging.debug('prepare collect basic data')
    while True:
        try:
            report()
        except Exception as e:
            logging.error(e, exc_info=True)
        time.sleep(period)
