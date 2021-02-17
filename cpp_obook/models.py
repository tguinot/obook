
from peewee import *

db = SqliteDatabase('qlabs_trading.db')

class OrderbookEntryUpdate(Model):
    side = CharField()
    base = CharField()
    quote = CharField()
    exchange = CharField()
    timestamp = DateTimeField()
    price = DecimalField()
    size = DecimalField()

    class Meta:
        database = db # This model uses the "people.db" database.