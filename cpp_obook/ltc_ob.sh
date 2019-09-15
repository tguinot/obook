export FLASK_APP=orderbook_feeder.py
export INSTRUMENT='LTCBTC'
export EXCHANGES='cexio binance'

flask run --port=5002

