import os
from pprint import pprint
from orderbook_helper import RtOrderbookReader
import requests
import umsgpack


orderbook_service_port = os.environ.get("SHM_PORT")

orderbooks_details = umsgpack.loads(requests.get('http://localhost:{}/shm'.format(orderbook_service_port)).content, raw=False)

all_readers = []

for exchange, instrument, shm_path in orderbooks_details:
    all_readers.append(RtOrderbookReader(shm_path))
    print(f"Created reader for orderbook {exchange}:{instrument} located at {shm_path}")
    print("Bids are:")
    pprint(all_readers[-1].snapshot_bids())
    print("Asks are:")
    pprint(all_readers[-1].snapshot_asks())