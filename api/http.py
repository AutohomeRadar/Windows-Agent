import logging
import json

from flask import Flask, request
from guppy import hpy

from utils import g
from rpc.transfer import get_transfer_rpc_client

app = Flask(__name__)


@app.route("/health")
def hello():
    return "ok"


@app.route("/v1/push", methods=['POST'])
def process_push_data():
    logging.info('push data here')
    try:
        payload = request.get_json()
        logging.debug("payloads: %s" % payload)
        addrs = g.TRANSFER['addrs']
        logging.info(addrs)
        rpc = get_transfer_rpc_client(addrs)
        logging.debug('rpc client initialized')
    except Exception as e:
        logging.error(e)
    result = rpc.call('Transfer.Update', payload)
    logging.info(result)
    return result['Message']

@app.route("/debug/memory/usage")
def memory_usage():
    logging.info("fuck")
    h = hpy()
    result = str(h.heap()).replace("\n", "<br>")
    return result
