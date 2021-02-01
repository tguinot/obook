import zerorpc
import threading
import zmq
import umsgpack
import time
import os

class UniversalFeedListenner(zerorpc.Client):
    def __init__(self, addr, zmq_port, relayer_port, markets, on_orderbook_update=None, on_trade_update=None):
        super().__init__()
        self.markets = markets
        self.connect(f"tcp://{addr}:{relayer_port}")
        self.on_orderbook_update = on_orderbook_update
        self.on_trade_update = on_trade_update
        self.setup_zmq()

    def run(self):
        self.subscribe()
        self.listen_thread  = threading.Thread(target=self.listen, args=())
        self.listen_thread.start()

    def setup_zmq(self):
        self.context = zmq.Context()
        self.zmq_socket = self.context.socket(zmq.SUB)

    def subscribe(self):
        for market in self.markets:
            port = self.subscribe_orderbook('FTX', market)
            print("Subscribing to orderbook on port", port)
            self.zmq_socket.connect("tcp://{}:{}".format("127.0.0.1", self.zmq_port))
            self.zmq_socket.setsockopt_string(zmq.SUBSCRIBE, "")

    def listen(self):
        while True:
            string = umsgpack.loads(self.zmq_socket.recv())
            print("Received:", string)
    