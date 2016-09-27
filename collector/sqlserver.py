import socket
import time
import logging
import winstats

from helpers import get_service_alive_info
from rpc.transfer import send_data_to_transfer
from utils import g

COUNTERS = [
    (r'\Processor Information(_Total)\% Processor Time',
     'processor_info.total.processor_time',
     'GAUGE'),
    (r'\PhysicalDisk(_Total)\Avg. Disk Queue Length',
     'physical_disk.total.avg.disk_queue_length',
     'GAUGE'),
    (r'\PhysicalDisk(_Total)\Avg. Disk Read Queue Length',
     'physical_disk.total.avg.disk_read_queue_length',
     'GAUGE'),
    (r'\PhysicalDisk(_Total)\Avg. Disk sec/Read',
     'physical_disk.total.avg.disk_sec_per_read',
     'GAUGE'),
    (r'\PhysicalDisk(_Total)\Disk Read Bytes/sec',
     'physical_disk.total.avg.disk_read_bytes_per_sec',
     'GAUGE'),
    (r'\PhysicalDisk(_Total)\Avg. Disk Write Queue Length',
     'physical_disk.total.avg.disk_write_queue_length',
     'GAUGE'),
    (r'\PhysicalDisk(_Total)\Avg. Disk sec/Write',
     'physical_disk.total.avg.disk_sec_per_write',
     'GAUGE'),
    (r'\PhysicalDisk(_Total)\Disk Write Bytes/sec',
     'physical_disk.total.avg.disk_write_bytes_per_sec',
     'GAUGE'),
    (r'\Process(sqlservr)\% Privileged Time',
     'proc.sqlservr.privileged_time',
     'GAUGE'),
    (r'\Process(sqlservr#1)\% Processor Time',
     'proc.sqlservr.1.processor_time',
     'GAUGE'),
    (r'\SQLServer:SQL Statistics\Batch Requests/sec',
     'sqlserver.sql_statistics.batch_rps',
     'GAUGE'),
    (r'\SQLServer:Buffer Manager\Buffer cache hit ratio',
     'sqlserver.buffer_manager.buffer_cache_hit_ratio',
     'GAUGE'),
    (r'\SQLServer:SQL Statistics\SQL Compilations/sec',
     'sqlserver.sql_statistics.sql_compilations_per_sec',
     'GAUGE'),
    (r'\SQLServer:Buffer Manager\Database pages',
     'sql_server.buffer_manager.database_pages',
     'GAUGE'),
    (r'\SQLServer:Databases(_Total)\Data File(s) Size (KB)',
     'sqlserver.databases.total.data_file_size',
     'GAUGE'),
    (r'\SQLServer:Access Methods\Full Scans/sec',
     'sqlserver.access_methods.full_sacans_per_sec',
     'GAUGE'),
    (r'\SQLServer:Buffer Manager\Lazy writes/sec',
     'sqlserver.buffer_manager.lazy_writes_per_sec',
     'GAUGE'),
    (r'\SQLServer:Locks(_Total)\Lock Waits/sec',
     'sqlserver.locks.lock_waits_per_sec',
     'GAUGE'),
    (r'\SQLServer:Databases(_Total)\Log File(s) Size (KB)',
     'sqlserver.databases.total.log_file_size',
     'GAUGE'),
    (r'\SQLAgent:Jobs(_Total)\Failed jobs',
     'sqlagent.jobs.total.failed_jobs',
     'GAUGE'),
    (r'\SQLServer:General Statistics\User Connections',
     'sqlserver.general_statistics.user_connections',
     'GAUGE'),
    (r'\SQLServer:Locks(_Total)\Number of Deadlocks/sec',
     'sqlserver.locks.total.number_of_deadlocks_per_sec',
     'GAUGE'),
    (r'\SQLServer:Buffer Manager\Page Life Expectancy',
     'sqlserver.buffer_manager.page_life_expectancy',
     'GAUGE'),
    (r'\SQLServer:SQL Statistics\SQL Re-Compilations/sec',
     'sqlserver.sql_statistics.sql_re_complilations_per_sec',
     'GAUGE'),
    (r'\SQLServer:Buffer Manager\Total Pages',
     'sqlserver.buffer_manager.total_pages',
     'GAUGE'),
    (r'\SQLServer:Memory Manager\Target Server Memory (KB)',
     'sqlserver.memory_manager.target_server_memory',
     'GAUGE'),
    (r'\SQLServer:Memory Manager\Total Server Memory (KB)',
     'sqlserver.memory_manager.total_server_memory',
     'GAUGE'),
    (r'\SQLServer:Databases(_Total)\Transactions/sec',
     'sqlserver.databases.total.transactions_per_sec',
     'GAUGE'),
]

SERVICES = [('MSDtsServer', 'MSDtsServer.alive'),
            ('ReportServer', 'ReportServer.alive'),
            ('SQLServerAgent', 'SQLServerAgent.alive'),
            ('SQLBrowser', 'SQLBrowser.alive'),
            ('MSSQLSERVER', 'MSSQLSERVER.alive')]


def collect():
    """
    collect sqlserver metric
    """
    logging.debug("enter sqlserver collect")
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
            'metric': 'sqlserver.{}'.format(metric),
            'endpoint': hostname,
            'timestamp': timestamp,
            'step': step,
            'value': value,
            'counterType': vtype,
            'tags': tags
        }
        logging.debug("metric: %s, value: %s" % (metric_dict['metric'], value))
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
        logging.debug("metric: %s, value: %s" %
                     (metric_dict['metric'], is_alive))
        data.append(metric_dict)

    try:
        result = send_data_to_transfer(data)
    except Exception as e:
        logging.error(e)
    else:
        logging.info(result)


def sqlserver_collect(period):
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
