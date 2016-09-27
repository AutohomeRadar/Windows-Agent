# jsonclient.py
# Simple JSONRPC client library created to work with Go servers
# Works with both Python 2.6+ and Python 3
# Copyright (c) 2011 Stephen Day, Bruce Eckel
# Distributed under the MIT Open-Source License:
# http://www.opensource.org/licenses/MIT
import json
import socket
import itertools
import logging

class JSONClient(object):
    '''
    jsonrpc client for py
    '''

    def __init__(self, addr):
        self.socket = socket.create_connection(addr)
        self.id_counter = itertools.count()

    def __del__(self):
        self.socket.close()

    def call(self, name, *params):
        request = dict(id=next(self.id_counter),
                       params=list(params),
                       method=name)
        self.socket.sendall(json.dumps(request).encode())

        # This must loop if resp is bigger than 4K
        response = self.socket.recv(4096)
        response = json.loads(response.decode())

        if response.get('id') != request.get('id'):
            raise Exception("expected id=%s, received id=%s: %s"
                            % (request.get('id'), response.get('id'),
                               response.get('error')))

        if response.get('error') is not None:
            raise Exception(response.get('error'))

        return response.get('result')
