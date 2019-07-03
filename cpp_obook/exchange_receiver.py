import hmac
import datetime
from concurrent.futures import ThreadPoolExecutor
import hashlib
from inspect import currentframe as code_here
import yaml
import random
from collections import OrderedDict
import logging
import traceback
import configparser
import websocket
import _thread as thread
from trade_logger import l_info
import threading
import requests
import time
import json

class ExchangeInterface():
    def __init__(self, currencies, key, secret, g_logger, subscriptions=None, order_manager=None, mode='listenner', no_orders_query=False, conf_file='interface.ini'):
        self.logger = g_logger
        # Initialise list rather than variable
        self.currencies = currencies
        self.user_id = 'my_user_id'
        self.key = key
        self.mode = mode
        self.authenticated = False
        self.no_orders_query = no_orders_query
        self.connected = False
        self.balance = {}
        self.config = configparser.ConfigParser()
        self.config.read(conf_file)
        self.bid, self.ask, self.trade_price = None, None, None
        self.secret =secret
        self.archive = {}
        self.latest_balance = {}
        self.error_messages = []
        self.bid_orders, self.ask_orders = {}, {}
        self.discarded_messages = []
        self.messages_to_process = {}
        self.subscriptions = {}
        self.subscriptions_todo = subscriptions if subscriptions else []
        self.failed_treated_msgs = []
        self.pending_orders = []
        self.sendformat_currencies = currencies[:3] + ':' + currencies[3:]
        self.expected_responses = {}
        self.oid = int(time.time())
        self.threads = {}
        self.nonce = int(time.time()/2+1331242423481)
        # Initialse dict instead of variable ?
        self.sub_functions = {'orderbook':  self.subscribe_orderbook,
                              'ticker':     self.subscribe_ticker,
                              'balance':    self.subscribe_balance,
                              }
        self.setup_order_functions()

    def startup(self):
        threading.Thread(target=self.recvd_message_processor).start()
        self.ignite()
        threading.Thread(target=self.process_orderbook_updates).start()
        threading.Thread(target=self.keep_connection_sanity).start()
        while True:
            time.sleep(3600)

    def log_info(self, frame, msg):
        self.logger.info(msg + ' - ' + l_info(frame))

    def log_debug(self, frame, msg):
        self.logger.debug(msg + ' - ' + l_info(frame))

    def log_error(self, frame, msg):
        self.logger.error(msg + ' - ' + l_info(frame))

    def setup_websocket(self):
        websocket.enableTrace(True)
        self.auth_msg = self.auth_request(self.key, self.secret)
        self.websock = websocket.WebSocketApp(self.wss_address,
                              on_message = self.on_message,
                              on_error = self.on_error,
                              on_close = self.on_close,
                              on_open = self.on_open,
                              header=['Origin: https://cex.io'])
        print("New websocket object created")
        self.websock.run_forever()

    def update_auth_status(self, msg):
        print("CHECKING AUTHENTICATION")
        self.authenticated = self.is_auth_established(msg)
        if not self.authenticated:
           print("NOT AUTHED")
        else:
            print("SUCCESSFULLY AUTHED")
        return self.authenticated

    def get_live_thread_number(self):
        count = 0
        for t in self.threads["websock"]:
            if t.is_alive():
                count += 1
        if "auth" in self.threads:
            for t in self.threads["auth"]:
                if t.is_alive():
                    count += 1
        return count

    def ignite(self):
        self.pending_orderbook_updates = {}
        self.log_info(code_here(),"Igniting, instanciating new orderbooks")
        self.bid_orders, self.ask_orders = {}, {}
        if "websock" not in self.threads:
            self.threads["websock"] = []
        self.threads["websock"].append(threading.Thread(target=self.setup_websocket))
        self.threads["websock"][-1].start()
        self.lets_listen = True
        print("There are {} threads or {} active threads".format(self.get_live_thread_number(), threading.activeCount()))
    

    def get_bid_ask_tradeprice(self):
        return self.bid, self.ask, self.trade_price

    def on_message(self, message):
        timestamp = time.time()
        message = yaml.safe_load(message)
        print("Received message: " + str(message))
        self.log_debug(code_here(),"Received message: " + str(message))
        if not self.is_msg_ok(message):
            self.log_info(code_here(),"Message is NOT ok!")
            self.error_messages.append(message)
        elif not self.is_msg_expected(message):
            self.log_info(code_here(),"Message is unexpected, ditching!")
            self.discarded_messages.append(message)
        else:
            self.messages_to_process[timestamp] = message
            self.log_info(code_here(),"Length of messages waiting to process: {}".format(len(self.messages_to_process)))

    def on_error(self, error):
        self.log_info(code_here(),str(error))

    def on_close(self):
        print("ON CLOSE CALLED")
        time.sleep(10)
        self.reset_connection()

    def reset_connection(self):
        print("RESET CALLED")       
        self.websock = None
        self.log_info(code_here(),"### closed ###")
        self.lets_listen = False
        time.sleep(0.5)
        self.ignite()

    def is_msg_ok(self, msg):
        if 'ok' in msg:
            return (True if msg.get('ok') == 'ok' else False)
        return True

    def keep_connection_sanity(self):
        while True:
            time.sleep(1.1)

    def authenticate(self):
        print("BEGINNING OF AUTH...")
        time.sleep(1.6)
        trials = 0
        self.websock.send(self.auth_msg)
        print("SENT AUTH MESSAGE")
        time.sleep(1.6)
        while not self.authenticated:
            print("WAITING FOR AUTH...")
            time.sleep(1)
            trials += 1
            if trials >= 100:
                exit()
        print("STARTING SUBSCRIPTIONS")
        self.perform_subscriptions()
        print("FINISHED AUTH")

    def on_open(self):
        if "auth" not in self.threads:
            self.threads["auth"] = []
        self.threads["auth"].append(threading.Thread(target=self.authenticate))
        self.threads["auth"][-1].start()


    def perform_subscriptions(self):
        for idx, sub in enumerate(self.subscriptions_todo):
            print("PERFORMING SUBSCRIPTION {}".format(idx))
            self.sub_functions[sub]()

    #Check parsing beforehand is done right
    def is_msg_expected(self, message):
        oid = self.get_message_oid(message)
        if oid and oid not in self.expected_responses:
            return False
        else:
            return True

    def sort_message(self, message):
        action_to_perform = self.response_actions_map[self.get_message_type(message)]
        return action_to_perform

    def get_new_oid(self):
        self.oid += 1
        return self.oid

    def generate_nonce(self):
        self.nonce += 1
        return self.nonce

    def treat_message(self, msg):
        if self.get_message_type(msg) not in self.response_actions_map:
            self.log_info(code_here(),"{} IS NOT IN {}".format(self.get_message_type(msg), self.response_actions_map.keys()))
            func = self.pass_on_message
        else:
            func = self.response_actions_map[self.get_message_type(msg)]
        try:
            result = func(msg)
        except BaseException as exe:
            self.log_error(code_here(),"Treament function excepted: {}".format(str(exe)))
            self.log_error(code_here(),"Stack trace is: \n {}".format(traceback.format_exc()))
            result = None
        finally:
            return result

    def recvd_message_processor(self):
        pool = ThreadPoolExecutor(13)
        future_results = []

        while True:
            while not self.messages_to_process:
                time.sleep(0.00001)
            self.log_info(code_here(),"Just doing my job...")
            while self.messages_to_process:
                oldest_time = min(self.messages_to_process.keys())
                msg = self.messages_to_process[oldest_time]
                try:
                    self.log_debug(code_here(),"message is :" + str(msg) + " type: " + str(type(msg)))
                    msg_future = pool.submit(self.treat_message, (msg))
                    future_results.append(msg_future)
                    if oldest_time in self.messages_to_process:
                        del self.messages_to_process[oldest_time]
                    self.log_debug(code_here(),"Remaining length of messages waiting to process: {}".format(len(self.messages_to_process)))
                except BaseException as exe:
                    self.log_error(code_here(),str(exe))

            finished_treatments = (r for r in future_results if r.done())

            for treated in finished_treatments:
                treatment_results = treated.result()
                try:
                    if treatment_results:
                        future_results.remove(treated)
                    else:
                        self.failed_treated_msgs.append(treated)
                        print("Failed to treat message: ", str(treated))
                        self.logger.critical("Failed to treat message: " + str(treated))
                        return -1
                except TypeError as e:
                    self.log_info(code_here(),"EXECEPTION HERE:" + str(e))

    # move to exchange library
    def is_connection_established(self, msg):
        return (True if self.get_message_type(msg) == 'connected' else False)

    def pass_on_message(self, msg):
        self.log_info(code_here(),"ignoring msg: {}".format(msg))
        return True

    def update_connection(self, msg):
        self.connected = self.is_connection_established(msg)
        if self.connected:
            self.log_info(code_here(),"WE ARE CONNECTED")

        #self.update_shm('connection', self.connected)
        return True

    def update_subscriptions(self, msg):
        subscription_type, status = self.parse_subscription_msg(msg)
        self.subscriptions[subscription_type] = status
        return True

    def update_ticker_data(self, msg):
        ticker_data = self.parse_tickupdate_data(msg, self.currencies)
        self.log_info(code_here(),"ticker data is: " + str(ticker_data))
        if ticker_data:
            self.update_shm('trade_price', ticker_data['price'])
            self.trade_price = ticker_data['price']
            self.archive[time.ctime()] = ticker_data
        return True


    def subscribe_balance(self):
        if "balance" in self.threads:
            if self.threads["balance"].is_alive():
                return
        self.threads["balance"] = threading.Thread(target=self.check_balance)
        self.threads["balance"].start()

    def check_balance(self):
        while True:
            time.sleep(int(random.random()*10) + 5)
            self.query_balance()
            time.sleep(int(random.random()*10) + 5)

    def send_msg(self, msg):
        try:
            self.websock.send(msg)
        except:
            time.sleep(5)
            self.send_msg(msg)

    def send_pong(self, msg):
        print("##### Sending pong #####")
        self.log_info(code_here(),"##### Sending pong #####")
        self.send_msg(json.dumps({"e": "pong"}))
        return True

    def prepare_all_shms(self):
        self.data_shms, self.flags_shms = {}, {}

        if self.mode != 'listenner':
            return True

        for shm_name, shm_type in data_shms_details:
            path_pattern = path_prefix + shm_name
            self.data_shms[shm_name] = ShmObject(path_pattern.format(self.currencies), shm_type)
            path_pattern = path_pattern+'ready'
            self.flags_shms[shm_name] = ShmObject(path_pattern.format(self.currencies), 'integer')

        [self.flags_shms[key].set_variable(1) for key in self.flags_shms]

    def update_shm(self, target_name, input_val):
        if self.mode != 'listenner':
            return True
        self.data_shms[target_name].set_variable(input_val)
        self.flags_shms[target_name].increment(1)
        self.log_info(code_here(),"Updated {} SHM with value: {}".format(target_name, input_val))


    def subscribe_ticker(self):
        subscribe_msg = self.generate_ticker_msg()
        self.send_msg(json.dumps(subscribe_msg))

    def subscribe_orderbook(self):
        oid = self.get_new_oid()
        subscribe_msg = self.generate_order_book_sub_msg(oid, self.currencies)
        self.send_msg(json.dumps(subscribe_msg))
        self.expected_responses[str(oid)] = subscribe_msg