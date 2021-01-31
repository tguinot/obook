import zerorpc
import umsgpack
import sys
import zmq


market = {
  'id': "BTC-PERP",
  'base': "BTC",
  'quote': "PERP",
}
# Socket to talk to server
context = zmq.Context()

socket = context.socket(zmq.SUB)

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")

port = c.subscribe_trades('FTX', market)
print("Subscribing to binance on port", port)

socket.connect("tcp://{}:{}".format("127.0.0.1", port))
socket.setsockopt_string(zmq.SUBSCRIBE, "")


while True:
  string = umsgpack.loads(socket.recv())
  print("Received:", string)