import random
import socket
import itertools
import logging

from client import JSONClient
from utils import g

hbs_rpc_clients = {}


class HBSJSONClient(JSONClient):

    def __init__(self, addr):
        super(HBSJSONClient, self).__init__(addr)
        self.addr = addr

    def insure_conn(self):
        """
        insure tcp connection is alive, if not alive or client
        is None create a new tcp connection. Becouse there is not 
        any method like Ping, so I use Agent.TrustableIps instead.
        Args:
            addr (JSONClient): client which can send rpc request
        Returns:
            JSONClient with given addr
        """
        try:
            res = self.call('Agent.TrustableIps', None)
        except Exception as e:
            logging.error(e)
        else:
            return

        logging.info("hbs lose connection...")
        for i in range(3):    
            logging.info("hbs rpc client trying reconnect. times: %s" % i)
            try:
                self.socket = socket.create_connection(self.addr)
            except Exception as e:
                logging.error(e)
            else:
                logging.info("hbs rpc client trying reconnect success! ")
                break


def init_rpc_client(addr_and_port):
    """
     init tcp client
    """
    addr, port = addr_and_port.split(':')
    addr_tuple = (addr, int(port))
    logging.info('make tcp connection --> addr: %s port: %s' % (addr, port))
    hbs_rpc_clients[addr_and_port] = HBSJSONClient(addr_tuple)
    return hbs_rpc_clients[addr_and_port]


def get_hbs_rpc_client(addr):
    """
    return transfer rpc client with given address
    """
    hbs_rpc_client = hbs_rpc_clients.get(addr)
    if hbs_rpc_client is not None:
        hbs_rpc_client.insure_conn()
    else:
        logging.info('not connect to hbs %s, connecting' % addr)
        hbs_rpc_client = init_rpc_client(addr)
    return hbs_rpc_client


def report_status_to_hbs(data):
    """
    send formated data to transfer via rpc
    Args:
        data (dict): {}
    """
    addr = g.HEARTBEAT['addr']

    rpc = get_hbs_rpc_client(addr)
    for i in range(3):
        try:
            res = rpc.call('Agent.ReportStatus', data)
        except Exception as e:
            logging.warn("call (%s) Agent.ReportStatus failure, times: %s -> msg: %s" %
                        (addr, i, e))
            continue
        return res
    logging.error("report_status_to_hbs %s to hbs (%s) failure" % (data, addr))
