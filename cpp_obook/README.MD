## A shared memory orderbook

This software, written in Python and C++ aims to provide a real-time orderbook for cryptocurrency trading.

| Feature | Motivation |
| ---- | --- |
| **Written in C++**| Allow fast insertion/deletion from websocket/FIX feeds |
| **Python Wrapped**| Allow integration with projects based on Python trading libraries such as exchange APIs or Zipline/CCXT |
| **Residing in Shared memory (SHM)**| Allow multiprocess, independant, service-based running logic |
| **Rationals-based**| Allow better precision than floats and doubles, and easy Python interfacing |


Requires flask, zerorpc, zeromq, node.js, ccxws

There are different components in this repository:
1. Orderbook writer: data structure for creating an orderbook SHM and inserting data inside.
2. Orderbook reader: data structure for reading an orderbook that already exists in SHM.
3. Orderbook Feeder: Uses an Orderbook Writer and listens to an orderbook updates feed to insert data in orderbook.
3. Live data service: written in JS, listens to various exchanges in websocket and relays the data to zeroMQ sockets
4. Orderbook service: Creates Orderbook Feeders, communicates with Live data service and makes Orderbook Feeders to zeroMQ sockets for updates.



Build instructions:

1. `cmake .`
2. `cd build/ && make orderbook_wrapper`


Usage instructions:

1. Start the live data service:

`node live_data_service.js`

2. Start the orderbook service (markets must be defined in markets_config.py):

`export FLASK_APP=start_orderbook_service && flask run`

3. Run the example (default FLASK port is 5000 but it can be changed):

`export ORDERBOOK_SERVICE_PORT=5000 && python3 orderbook_reader_example.py`


