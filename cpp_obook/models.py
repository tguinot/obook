
from peewee import *
from decimal import Decimal
import datetime
from pprint import pprint
from playhouse.postgres_ext import *

# db = SqliteDatabase('qlabs_trading.db')
db = PostgresqlExtDatabase('nmezfpnr', user='nmezfpnr', host='dumbo.db.elephantsql.com', password='r5B7YHZr2sL08f7yc0e3QcLdaD4amB0t')


class Exchange(Model):
    name = CharField(unique=True)
    id = AutoField()

    class Meta:
        database = db


class Currency(Model):
    name = CharField(unique=True)
    id = AutoField()

    class Meta:
        database = db


class OrderbookRecord(Model):
    id = AutoField()
    base = ForeignKeyField(Currency)
    quote = ForeignKeyField(Currency)
    side =  BooleanField()
    sizes = ArrayField(DecimalField)
    prices = ArrayField(DecimalField)
    exchange = ForeignKeyField(Exchange)
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
db.create_tables([Exchange, Currency, OrderbookRecord])

# ftx = Exchange(name="FTX")
# ftx.save()

# usd = Currency(name="USD")
# usd.save()

# btc = Currency(name="BTC")
# btc.save()

# timestamp = datetime.datetime.now()
# record = OrderbookRecord(base=btc, quote=usd, exchange=ftx, side=True, timestamp=timestamp, prices=[Decimal("50001.34"), Decimal("50004.54")], sizes=[Decimal("1.42"), Decimal("0.98")])
# record.save()

