export FLASK_APP=orderbook_feeder.py
export INSTRUMENT='ETHBTC'
export EXCHANGES='cexio binance'

flask run --port=5001 

