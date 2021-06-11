from liborderbook.orderbook_helper import RtOrderbookReader
from local_models import Service

class ResilientOrderbookReader(RtOrderbookReader):

    def __init__(self, exchange, instrument, db_interface=None):
        # if not db_interface:
        #     self.db_service_interface = DatabaseQuerier('127.0.0.1', 5678)
        # else:
        #     self.db_service_interface = db_interface
        self.exchange, self.instrument = exchange, instrument
        shm = self.get_orderbook_shm()
        self.shm = shm
        print(f"Initialising resilient orderbook reader for {exchange} {instrument} on SHM {shm}")
        super().__init__(shm)

    def get_orderbook_shm(self):
        #orderbook_details = self.db_service_interface.find_service('OrderbookFeeder', instrument=self.instrument, exchange=self.exchange) 
        orderbook_details = Service.get((Service.name == 'OrderbookFeeder') & (Service.exchange == self.exchange) & (Service.instrument == self.instrument))
        return orderbook_details.address

    def refresh_orderbook(self):
        shm = self.get_orderbook_shm()
        self.shm = shm
        super().init_shm(shm)