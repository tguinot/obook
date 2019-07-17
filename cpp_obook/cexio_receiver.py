from exchange_receiver import ExchangeInterface
from inspect import currentframe as code_here
import json
import datetime
import time
from decimal import Decimal
import yaml
import hmac
import hashlib

class CexioInterface(ExchangeInterface):
    def __init__(self, currencies, key, secret, g_logger, subscriptions=None, order_manager=None, mode='listenner', no_orders_query=False, on_orderbook_update=None, on_ignite=None):
        self.wss_address = "wss://ws.cex.io/ws/"
        self.exchange = 'cexio'
        self.on_orderbook_update = on_orderbook_update
        super(CexioInterface, self).__init__(currencies, key, secret, g_logger, subscriptions, order_manager, mode, no_orders_query, on_ignite=on_ignite)

    def setup_order_functions(self):
        self.response_actions_map = {
                              "ping": self.send_pong,
                              "pong": self.update_connection,
                              "connected": self.update_connection,
                              "disconnecting": self.update_connection,
                              "md_update": self.queue_orderbook_update,
                              "auth": self.update_auth_status,
                              "order-book-subscribe": self.queue_orderbook_update,
                              "order-book-unsubscribe": self.update_subscriptions}


    def queue_orderbook_update(self, msg):
        self.log_debug(code_here(),"Raw orderbook update msg {}".format(msg))
        msg_data = self.parse_msg_data(msg)
        if 'error' in msg_data:
            self.log_error(code_here(),"Error while getting orderbook: {}".format(msg_data['error']))
        else:
            update_data = self.parse_orderbook_data(msg)
            timestamp = update_data['timestamp']
            if timestamp not in self.pending_orderbook_updates:
                self.pending_orderbook_updates[timestamp] = []
            self.pending_orderbook_updates[timestamp].append(update_data)
        return True


    def process_orderbook_updates(self):
        print("Starting updates processor")
        while self.websock:
            milli_wait = 0
            self.log_debug(code_here(),"Nb of orderbook updates waiting: {}".format(len(self.pending_orderbook_updates)))
            while not self.pending_orderbook_updates or ((len(self.pending_orderbook_updates) <10) and (milli_wait<100)):
                time.sleep(0.0005)
                milli_wait += 1
            try:
                oldest_update_time = min(self.pending_orderbook_updates.keys())
                self.log_debug(code_here(),"Processing update: {} out of {}".format(oldest_update_time, str(self.pending_orderbook_updates)))
                #print("Processing update: {} out of {}".format(oldest_update_time, str(self.pending_orderbook_updates)))
                for update in self.pending_orderbook_updates[oldest_update_time]:
                    self.update_orderbook_data(update)
                del self.pending_orderbook_updates[oldest_update_time]
            except BaseException as exe:
                print("Failed to process update: {}".format(str(exe)))
                #print("Processing update: {} out of {}".format(oldest_update_time, str(self.pending_orderbook_updates)))
                self.log_error(code_here(), "Failed to process update: {}".format(str(exe)))


    def update_orderbook_data(self, orderbook_data):
        old_bidorders, old_askorders = self.bid_orders, self.ask_orders
        self.log_debug(code_here(),"Update content is {}".format(str(orderbook_data)))
        self.log_debug(code_here(),"Updating limits according to {} : {} out of {}".format(orderbook_data['timestamp'], old_bidorders, old_askorders))
        if orderbook_data['bids']:
            for update in json.loads(orderbook_data['bids'], parse_int=Decimal, parse_float=Decimal):
                price, size = update[0], update[1]
                self.on_orderbook_update(True, size, price)

        if orderbook_data['asks']:
            for update in json.loads(orderbook_data['asks'], parse_int=Decimal, parse_float=Decimal):
                price, size = update[0], update[1]
                self.on_orderbook_update(False, size, price)

        if self.ask_orders and self.bid_orders and (min(self.ask_orders.keys()) < max(self.bid_orders.keys())):
            self.log_error(code_here(), "Crossing is {} VS {}".format(min(self.ask_orders.keys()), max(self.bid_orders.keys())))
            self.log_error(code_here(), "Keys are {} VS {}".format(self.ask_orders.keys(), self.bid_orders.keys()))
            self.log_error(code_here(), "Crossing detected! orderbooks are: \n bid: {} \n ask: {}".format(str(self.bid_orders), str(self.ask_orders)))
            self.log_error(code_here(), "Previous orderbooks were: \n bid: {} \n ask: {}".format(str(old_bidorders), str(old_askorders)))
            self.log_error(code_here(), "Type of orderbooks are {} {}".format(type(self.ask_orders), type(self.bid_orders)))

        self.archive[orderbook_data['timestamp']] = orderbook_data
        return True


    def generate_order_book_sub_msg(self,  oid, currencies):
        subscribe_msg = {
                          "e": "order-book-subscribe",
                          "data": {
                          "pair": [
                                currencies[:3],
                                currencies[3:]
                                ],
                                "subscribe": True,
                                "depth": 4
                          },
                          "oid": str(oid)
                        }
        return subscribe_msg

    def get_message_oid(self, message):
        return message.get('oid')


    def get_message_type(self, msg):
        return msg.get('e')

    def auth_request(self, key, secret):
        timestamp, signature = self.create_signature(key, secret)
        return json.dumps({'e': 'auth',
                           'auth': {'key': key, 'signature': signature, 'timestamp': timestamp,},
                           'oid': 'auth', })

    def generate_ticker_msg(self):
        subscribe_msg = {
                        "e": "subscribe",
                        "rooms": [
                                "tickers"
                                ]
                        }
        return subscribe_msg

    def is_auth_established(self, msg):
        self.log_info(code_here(),"Auth is:" + str(msg))
        if msg['e']=='auth':
            return True
        else:
            return False

    def create_signature(self, key, secret):  # (string key, string secret)
        timestamp = int(datetime.datetime.now().timestamp())  # UNIX timestamp in seconds
        string = "{}{}".format(timestamp, key)
        return timestamp, hmac.new(secret.encode(), string.encode(), hashlib.sha256).hexdigest()

    def parse_msg_data(self, msg):
        msg_data = msg['data']
        return msg_data

    def parse_tickupdate_data(self, msg, currencies, logger=None):
        result = msg['data']
        if result['symbol1'] != currencies[:3] or result['symbol2'] != currencies[3:]:
            self.log_info(code_here(),result['symbol1'] +' vs ' + currencies[:3] + ' & ' + result['symbol2'] + ' vs ' + currencies[3:])
            return None
        result['price'] = float(result['price'])
        return result

    def parse_ticker_data(self, msg):
        result = msg['data']
        result['timestamp'] = float(result['timestamp'])
        result['last'] = float(result['last'])
        return result

    def parse_orderbook_data(self, msg):
        result = msg['data']
        result['bids'] = str(result['bids']) if result['bids'] else None
        result['asks'] = str(result['asks']) if result['asks'] else None
        time_string = result.get('time') or result.get('timestamp')
        result['timestamp'] = float(time_string) if time_string else None
        return result

    def parse_open_order_msg(self, msg):
        return msg['data']

    def parse_subscription_msg(self, msg, logger=None):
        self.log_info(code_here(),"Received subscription message {}".format(str(msg)))
        if 'pair' not in msg['data']:
            self.log_info(code_here(),"Subs msg is {}".format(str(msg)))
            return None
        else:
            return msg['e'], msg['data']['pair']
