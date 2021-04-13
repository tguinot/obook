
from peewee import *
from decimal import Decimal
import datetime
import os
from pprint import pprint
from playhouse.postgres_ext import *

db = PostgresqlExtDatabase(os.environ.get('POSTGRES_DB_NAME'), user=os.environ.get('POSTGRES_DB_USER'), host=os.environ.get('POSTGRES_DB_HOST'), password=os.environ.get('POSTGRES_DB_PASSWD'), port=os.environ.get('POSTGRES_DB_PORT'), sslmode='require')
services_db = PostgresqlExtDatabase(os.environ.get('POSTGRES_SERVICES_DB_NAME'), user=os.environ.get('POSTGRES_SERVICES_DB_USER'), host=os.environ.get('POSTGRES_SERVICES_DB_HOST'), password=os.environ.get('POSTGRES_SERVICES_DB_PASSWD'), port=os.environ.get('POSTGRES_SERVICES_DB_PORT'), sslmode='require')


class Exchange(Model):
    name = CharField(unique=True)
    id = AutoField()

    class Meta:
        database = db


class Service(Model):
    address = CharField(null=True)
    exchange = CharField(null=True)
    instrument = CharField(null=True)
    name = CharField(null=True)
    port = IntegerField(null=True, unique=True)

    class Meta:
        table_name = 'service'
        database = services_db


class Currency(Model):
    name = CharField(unique=True)
    id = AutoField()

    class Meta:
        database = db


class Instrument(Model):
    id = AutoField()
    base = ForeignKeyField(Currency)
    quote = ForeignKeyField(Currency)
    exchange_name = CharField(null=True)
    name = CharField(null=True)
    kind = CharField(null=True)

    class Meta:
        database = db


class OrderbookRecord(Model):
    id = AutoField()
    base = ForeignKeyField(Currency)
    quote = ForeignKeyField(Currency)
    bid_sizes = ArrayField(DecimalField, {"max_digits": 19, "decimal_places": 12, "auto_round": True})
    bid_prices = ArrayField(DecimalField, {"max_digits": 19, "decimal_places": 12, "auto_round": True})
    ask_sizes = ArrayField(DecimalField, {"max_digits": 19, "decimal_places": 12, "auto_round": True})
    ask_prices = ArrayField(DecimalField, {"max_digits": 19, "decimal_places": 12, "auto_round": True})
    exchange = ForeignKeyField(Exchange)
    kind = CharField(null=True)
    timestamp = DateTimeField()

    class Meta:
        database = db


class OrderbookUpdate(Model):
    id = AutoField()
    side = BooleanField()
    base = ForeignKeyField(Currency)
    quote = ForeignKeyField(Currency)
    exchange = ForeignKeyField(Exchange)
    timestamp = DateTimeField()
    price = DecimalField()
    size = DecimalField()

    class Meta:
        database = db


db.connect()
services_db.connect()

#db.create_tables([Exchange, Currency, OrderbookRecord, Service, Instrument])

##ftx = Exchange(name="FTX")
#ftx.save()

# ftx = Exchange(name="Binance")
# ftx.save()

#binanceus = Exchange(name="BinanceUS")
#binanceus.save()

#usd = Currency(name="USD")
#usd.save()

# usdt = Currency(name="USDT")
# usdt.save()

#btc = Currency(name="BTC")
#btc.save()

#eth = Currency(name="ETH")
#eth.save()

# eth = Currency.get(Currency.name == 'ETH')

# ftx = Exchange.get(Exchange.name == 'FTX')
# btc = Currency.get(Currency.name == 'BTC')
# usd = Currency.get(Currency.name == 'USD')

# btcusd_ftx = Instrument(base=btc, quote=usd, name='BTC/USD', exchange_name='FTX', kind='spot')
# btcusd_ftx.save()
# btcusd_binanceus = Instrument(base=btc, quote=usd, name='BTCUSD', exchange_name='BinanceUS', kind='spot')
# btcusd_binanceus.save()
# btcusd_ccxt = Instrument(base=btc, quote=usd, name='BTC/USD', exchange_name='ccxt', kind='spot')
# btcusd_ccxt.save()
        
# ethusd_ftx = Instrument(base=eth, quote=usd, name='ETH/USD', exchange_name='FTX', kind='spot')
# ethusd_ftx.save()
# ethusd_binanceus = Instrument(base=eth, quote=usd, name='ETHUSD', exchange_name='BinanceUS', kind='spot')
# ethusd_binanceus.save()
# ethusd_ccxt = Instrument(base=eth, quote=usd, name='ETH/USD', exchange_name='ccxt', kind='spot')
# ethusd_ccxt.save()

# btcperp_ftx = Instrument(base=btc, quote=usd, name='BTC-PERP', exchange_name='FTX', kind='perpetual_futures')
# btcperp_ftx.save()
# btcperp_ccxt = Instrument(base=btc, quote=usd, name='BTC-PERP', exchange_name='ccxt', kind='perpetual_futures')
# btcperp_ccxt.save()

# orderbook_service_d = Service(name='LiveDataService', port=4242, address='127.0.0.1', instrument='ALL', exchange='ALL')
# orderbook_service_d.save()

# orderbook_service_e = Service(name='OrderbookDataStream', port=5090, address='127.0.0.1', instrument='BTC/USD', exchange='FTX')
# orderbook_service_e.save()
# orderbook_service_f = Service(name='OrderbookDataStream', port=5091, address='127.0.0.1', instrument='ETH/USD', exchange='FTX')
# orderbook_service_f.save()
# orderbook_service_g = Service(name='OrderbookDataStream', port=5092, address='127.0.0.1', instrument='BTCUSD', exchange='BinanceUS')
# orderbook_service_g.save()
# orderbook_service_h = Service(name='OrderbookDataStream', port=5093, address='127.0.0.1', instrument='ETHUSD', exchange='BinanceUS')
# orderbook_service_h.save()
#orderbook_service_h = Service(name='OrderbookDataStream', port=5098, address='127.0.0.1', instrument='BTC-PERP', exchange='FTX')
#orderbook_service_h.save()



# orderbook_feeder = Service(name='OrderbookFeeder', port=0, address='/shm_xyz', instrument='BTCUSD', exchange='BinanceUS')
# orderbook_feeder.save()
#orderbook_feeder = Service(name='OrderbookFeeder', port=4, address='/shm_rty', instrument='BTC-PERP', exchange='FTX')
#orderbook_feeder.save()
# orderbook_feeder = Service(name='OrderbookFeeder', port=1, address='/shm_abc', instrument='ETHUSD', exchange='BinanceUS')
# orderbook_feeder.save()
# orderbook_feeder = Service(name='OrderbookFeeder', port=2, address='/shm_hyu', instrument='BTC/USD', exchange='FTX')
# orderbook_feeder.save()
# orderbook_feeder = Service(name='OrderbookFeeder', port=3, address='/shm_koi', instrument='ETH/USD', exchange='FTX')
# orderbook_feeder.save()

#oms = Service(name='OMS Service', port=4477, address='127.0.0.1', instrument='ALL', exchange='ALL')
#oms.save()



#timestamp = datetime.datetime.now()
#record = OrderbookRecord(base=btc, quote=usd, exchange=ftx, side=True, timestamp=timestamp, ask_prices=[Decimal("50011.34"), Decimal("50014.54")], ask_sizes=[Decimal("11.42"), Decimal("10.98")], bid_prices=[Decimal("50001.34"), Decimal("50004.54")], bid_sizes=[Decimal("1.42"), Decimal("0.98")])
#record.save()

