from liborderbook.orderbook_helper import RtOrderbookReader
from db_inquirer import DatabaseQuerier

class ResilientOrderbookReader(RtOrderbookReader):

    def __init__(self, exchange, instrument):
        self.exchange, self.instrument = exchange, instrument
        shm = self.get_orderbook_shm()
        self.shm = shm
        super().__init__(shm)

    def get_orderbook_shm(self):
        db_service_interface = DatabaseQuerier('127.0.0.1', 5678)
        orderbook_details = db_service_interface.find_service('OrderbookFeeder', instrument=self.instrument, exchange=self.exchange) 
        #orderbook_details = Service.get((Service.name == 'OrderbookFeeder') & (Service.exchange == self.exchange) & (Service.instrument == self.instrument))
        db_service_interface.close()
        return orderbook_details.get('address')

    def refresh_orderbook(self):
        shm = self.get_orderbook_shm()
        self.shm = shm
        super().init_shm(shm)