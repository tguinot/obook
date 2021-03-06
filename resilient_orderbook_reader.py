from liborderbook.orderbook_helper import RtOrderbookReader
from models import OrderbookRecord, Currency, Exchange, Service

class ResilientOrderbookReader(RtOrderbookReader):

    def __init__(self, exchange, instrument):
        self.exchange, self.instrument = exchange, instrument
        shm = self.get_orderbook_shm()
        self.shm = shm
        super().__init__(shm)

    def get_orderbook_shm(self):
        orderbook_details = Service.get((Service.name == 'OrderbookFeeder') & (Service.exchange == self.exchange) & (Service.instrument == self.instrument))
        return orderbook_details.address

    def refresh_orderbook(self):
        shm = self.get_orderbook_shm()
        self.shm = shm
        super().init_shm(shm)