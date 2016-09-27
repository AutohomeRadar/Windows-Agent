"""
Collect Host's basic metric
Thanks to Feng_Qi a lot of code in this file was borrow from him.
"""
import psutil
import time
import json
import copy
import logging

from rpc.transfer import send_data_to_transfer
from utils import g

def collect():
    logging.debug('enter basic collect')
    push_interval = 60
    zh_decode = "gbk"

    time_now = int(time.time())
    payload = []
    data = {"endpoint": g.HOSTNAME, "metric": "", "timestamp": time_now,
            "step": push_interval, "value": "", "counterType": "", "tags": ""}

    cpu_status = psutil.cpu_times_percent()
    mem_status = psutil.virtual_memory()
    swap_status = psutil.swap_memory()
    disk_io_status = psutil.disk_io_counters(perdisk=True)
    net_io_status = psutil.net_io_counters(pernic=True)

    # agent alive
    data["metric"] = "agent.alive"
    data["value"] = 1
    data["counterType"] = "GAUGE"
    payload.append(copy.copy(data))

    logging.debug(cpu_status)
    data["metric"] = "cpu.user"
    data["value"] = cpu_status.user
    data["counterType"] = "GAUGE"
    payload.append(copy.copy(data))

    data["metric"] = "cpu.system"
    data["value"] = cpu_status.system
    payload.append(copy.copy(data))

    data["metric"] = "cpu.idle"
    data["value"] = cpu_status.idle
    payload.append(copy.copy(data))

    data["metric"] = "mem.memused.percent"
    data["value"] = mem_status.percent
    payload.append(copy.copy(data))

    data["metric"] = "mem.swapused.percent"
    data["value"] = swap_status.percent
    payload.append(copy.copy(data))

    disk_status = psutil.disk_partitions()
    for disk in disk_status:
        if 'cdrom' in disk.opts or disk.fstype == '':
            continue
        disk_info = psutil.disk_usage(disk.mountpoint)

        data["metric"] = "df.used.percent"
        data["value"] = disk_info.percent
        data["tags"] = "disk=" + disk.device.split(":")[0]
        payload.append(copy.copy(data))

        data["metric"] = "df.byte.total"
        data["value"] = disk_info.total
        payload.append(copy.copy(data))

        data["metric"] = "df.byte.used"
        data["value"] = disk_info.used
        payload.append(copy.copy(data))

        data["metric"] = "df.byte.free"
        data["value"] = disk_info.free
        payload.append(copy.copy(data))

    for key in disk_io_status:
        data["metric"] = "disk.io.read_count"
        data["value"] = disk_io_status[key].read_count
        data["tags"] = "device=" + key
        data["counterType"] = "COUNTER"
        payload.append(copy.copy(data))

        data["metric"] = "disk.io.write_count"
        data["value"] = disk_io_status[key].write_count
        payload.append(copy.copy(data))

        data["metric"] = "disk.io.read_bytes"
        data["value"] = disk_io_status[key].read_bytes
        payload.append(copy.copy(data))

        data["metric"] = "disk.io.write_bytes"
        data["value"] = disk_io_status[key].write_bytes
        payload.append(copy.copy(data))

        data["metric"] = "disk.io.read_time"
        data["value"] = disk_io_status[key].read_time
        payload.append(copy.copy(data))

        data["metric"] = "disk.io.write_time"
        data["value"] = disk_io_status[key].write_time
        payload.append(copy.copy(data))

    for key in net_io_status:
        if is_interface_ignore(key):
            continue

        data["metric"] = "net.if.in.mbits"
        data["value"] = net_io_status[key].bytes_recv * 8 / 100000
        data["tags"] = "interface=" + key.decode(zh_decode)
        payload.append(copy.copy(data))

        data["metric"] = "net.if.out.mbits"
        data["value"] = net_io_status[key].bytes_sent * 8 / 100000
        payload.append(copy.copy(data))

        data["metric"] = "net.if.in.packets"
        data["value"] = net_io_status[key].packets_recv
        payload.append(copy.copy(data))

        data["metric"] = "net.if.out.packets"
        data["value"] = net_io_status[key].packets_sent
        payload.append(copy.copy(data))

        data["metric"] = "net.if.in.error"
        data["value"] = net_io_status[key].errin
        payload.append(copy.copy(data))

        data["metric"] = "net.if.out.error"
        data["value"] = net_io_status[key].errout
        payload.append(copy.copy(data))

        data["metric"] = "net.if.in.drop"
        data["value"] = net_io_status[key].dropin
        payload.append(copy.copy(data))

        data["metric"] = "net.if.out.drop"
        data["value"] = net_io_status[key].dropout
        payload.append(copy.copy(data))
        logging.debug(payload)

        payload = filter(lambda x: x['metric'] not in g.IGNORE, payload)

    try:
        result = send_data_to_transfer(payload)
    except Exception as e:
        logging.error(e)
    else:
        logging.info(result)


def is_interface_ignore(key):
    """
    return if the inferface will ignore
    """

    for ignore_key in g.COLLECTOR['ifacePrefixIgnore']:
        if ignore_key in key.decode('gbk'):
            return True

def basic_collect(period):
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
