import zerorpc
import threading
import zmq
import umsgpack
from pprint import pprint
import time
import os

class UniversalFeedListenner(zerorpc.Client):
    def __init__(self, relayer_addr, relayer_port, exchange, instrument, update_type='trade', on_receive=None):
        super().__init__()
        self.exchange = exchange
        self.update_type = update_type
        self.instrument = instrument
        print("Connecting to", f"tcp://{relayer_addr}:{relayer_port}")
        self.connect(f"tcp://{relayer_addr}:{relayer_port}")
        self.on_receive = on_receive
        self.setup_zmq()

    def run(self):
        self.subscribe()
        self.listen_thread  = threading.Thread(target=self.listen, args=())
        self.listen_thread.start()
        return self.listen_thread

    def setup_zmq(self):
        self.context = zmq.Context()
        self.zmq_socket = self.context.socket(zmq.SUB)

    def subscribe(self):
        print("Querying for connection details")
        if self.update_type == 'trade':
            details = self.subscribe_trades(self.exchange, self.instrument)
        elif self.update_type == 'orderbook':
            details = self.subscribe_orderbook(self.exchange, self.instrument)
        print("Subscribing to relay details", details)
        self.zmq_socket.connect("tcp://{}:{}".format(details['addr'], details['port']))
        self.zmq_socket.setsockopt_string(zmq.SUBSCRIBE, "")

    def listen(self):
        print("Now listenning...")
        while True:
            update = umsgpack.loads(self.zmq_socket.recv(), raw=False)
            self.on_receive(update)
            time.sleep(0.002)
    