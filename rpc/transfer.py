import random
import socket
import itertools
import logging

from client import JSONClient
from utils import g

transfer_rpc_clients = {}

class TransferJSONClient(JSONClient):

    def __init__(self, addr):
        super(TransferJSONClient, self).__init__(addr)
        self.addr = addr

    def insure_conn(self):
        """
        insure tcp connection is alive, if not alive or client
        is None create a new tcp connection.
        Args:
            addr (JSONClient): client which can send rpc request
        Returns:
            JSONClient with given addr
        """
        for _ in range(3):
            try:
                self.call('Transfer.Ping', None)
            except Exception as e:
                logging.error(e)
                logging.error("lose connection to transfer, prepare to rebuild")
                self.socket = socket.create_connection(self.addr)
            break


def init_rpc_client(addr_and_port):
    """
     init tcp client
    """
    addr, port = addr_and_port.split(':')
    addr_tuple = (addr, int(port))
    logging.info('make tcp connection --> addr: %s port: %s' % (addr, port))
    transfer_rpc_clients[addr_and_port] = TransferJSONClient(addr_tuple)
    return transfer_rpc_clients[addr_and_port]


def get_transfer_rpc_client(addr):
    """
    return transfer rpc client with given address
    """
    transfer_rpc_client = transfer_rpc_clients.get(addr)
    if transfer_rpc_client is not None:
        transfer_rpc_client.insure_conn()
    else:
        transfer_rpc_client = init_rpc_client(addr)
    return transfer_rpc_client


def send_data_to_transfer(data):
    """
    send formated data to transfer via rpc, select transfer randomly and every 
    transfer will retry 3 times if failure
    Args:
        data (list of dict): [{}, {}, ...]
    """
    addrs = g.TRANSFER['addrs']
    logging.debug(addrs)
    random.shuffle(addrs)
    for addr in addrs:
        call_success = False
        rpc = get_transfer_rpc_client(addr)
        for i in range(3):
            try:
                res = rpc.call('Transfer.Update', data)
            except Exception as e:
                logging.warn("call (%s) Transfer.update failure, times: %s -> msg: %s" %
                            (addr, i, e))
                continue
            call_success = True
            return res
        if not call_success:
            logging.error("send data %s to transfer (%s) failure" %
                         (data, addr))
