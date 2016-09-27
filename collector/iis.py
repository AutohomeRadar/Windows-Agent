import json
import socket
import time
import logging

import winstats
from helpers import get_service_alive_info
from utils import g
from rpc.transfer import send_data_to_transfer

# counters
COUNTERS = [
    (r'\ASP.NET\Application Restarts',
     'asp.net.application.restarts',
     'GAUGE'),
    (r'\ASP.NET\Requests Current',
     'asp.net.requests.current',
     'GAUGE'),
    (r'\ASP.NET\Request Execution Time',
     'asp.net.request_execution_time',
     'GAUGE'),
    (r'\ASP.NET Applications(__Total__)\Requests/Sec',
     'asp.net.applications.total.rps',
     'GAUGE'),
    (r'\ASP.NET\Requests Queued',
     'asp.net.request_queued',
     'GAUGE'),
    (r'\ASP.NET\Request Wait Time',
     'asp.net.request_wait_time',
     'GAUGE'),
    (r'\ASP.NET Applications(__Total__)\Errors Total',
     'asp.net.applications.total.errors',
     'GAUGE'),
    (r'\ASP.NET\Worker Process Restarts',
     'asp.net.worker_process_restarts',
     'GAUGE'),
    (r'\Web Service(_Total)\Current Anonymous Users',
     'web_service.current_anonymous_users',
     'GAUGE'),
    (r'\Web Service(_Total)\Current Connections',
     'web_service.current_connections',
     'GAUGE'),
    (r'\Web Service(_Total)\Current NonAnonymous Users',
     'web_service.total.current_nonanonymous_users',
     'GAUGE'),
    (r'\Web Service(_Total)\Total Get Requests',
     'web_service.total_get_reqeusts',
     'GAUGE'),
    (r'\Web Service(_Total)\Total Head Requests',
     'web_service.total.total_head_requests',
     'GAUGE'),
    (r'\Web Service(_Total)\Total Post Requests',
     'web_service.total_post_requests',
     'GAUGE'),
]

# services
SERVICES = [('W3SVC', 'service.alive')]

def collect():
    """
    collect iis metric
    """
    timestamp = int(time.time())
    hostname = g.HOSTNAME
    tags = ''
    data = []
    step = 60

    for counter, metric, vtype in COUNTERS:
        try:
            counter_value = winstats.get_perf_data(counter, delay=100)
        except Exception as e:
            logging.debug(e)
            continue
        value = counter_value[0]

        metric_dict = {
            'metric': 'iis.{}'.format(metric),
            'endpoint': hostname,
            'timestamp': timestamp,
            'step': step,
            'value': value,
            'counterType': vtype,
            'tags': tags
        }
        logging.debug("%s: %s" % (metric_dict['metric'], value))
        data.append(metric_dict)

    for srv, metric in SERVICES:
        try:
            is_alive = get_service_alive_info(srv)
        except Exception as e:
            logging.debug(e)
            continue
        metric_dict = {
            'metric': metric,
            'endpoint': hostname,
            'timestamp': timestamp,
            'step': step,
            'value': is_alive,
            'counterType': 'GAUGE',
            'tags': tags
        }
        logging.debug("isalive: %s" % is_alive)
        logging.debug("metrics: %s" % metric_dict['metric'])
        data.append(metric_dict)

    try:
        result = send_data_to_transfer(data)
    except Exception as e:
        logging.error(e, exc_info=True)
    else:
        logging.info(result)


def iis_collect(period):
    """
    deadloop to collect data periodically
    :params: `period` is the seconds of collecting circle
    """
    logging.debug('prepare collect basic data')
    while True:
        try:
            collect()
        except Exception as e:
            logging.error(e, exc_info=True)
        time.sleep(period)
