import zerorpc
import threading
import zmq
import umsgpack
from pprint import pprint
import time
import os

class UniversalFeedListenner():
    def __init__(self, stream_addr, stream_port, exchange, update_type='trade', on_receive=None):
        super().__init__()
        self.exchange = exchange
        self.update_type = update_type
        self.stream_addr = stream_addr
        self.stream_port = stream_port
        self.on_receive = on_receive
        self.running = True
        self.setup_zmq()

    def run(self):
        self.subscribe()
        self.listen()

    def stop(self):
        self.running = False

    def setup_zmq(self):
        self.context = zmq.Context()
        self.zmq_socket = self.context.socket(zmq.SUB)

    def subscribe(self):
        print("Querying for connection details")
        #if self.update_type == 'trade':
        #    details = self.subscribe_trades(self.exchange, self.instrument)
        #elif self.update_type == 'orderbook':
        #    details = self.subscribe_orderbook(self.exchange, self.instrument)
        #print("Subscribing to relay details", details)
        self.zmq_socket.connect("tcp://{}:{}".format(self.stream_addr, self.stream_port))
        self.zmq_socket.setsockopt_string(zmq.SUBSCRIBE, "")

    def listen(self):
        print("Now listenning...")
        while self.running:
            update = umsgpack.loads(self.zmq_socket.recv(), raw=False)
            self.on_receive(update)
        print("Listenner stopping")
    