Python orderbook software, for cryptocurrency trading.

Requires flask, zerorpc, zeromq, node.js, ccxws


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


