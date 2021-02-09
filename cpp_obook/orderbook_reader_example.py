import os
from pprint import pprint
import time
from orderbook_helper import RtOrderbookReader
import requests
import umsgpack

orderbook_service_port = os.environ.get("ORDERBOOK_SERVICE_PORT")

# First we ask the orderbook service to start listenning to orderbook updates and fill itself
status = umsgpack.loads(requests.get('http://localhost:{}/start_listenning'.format(orderbook_service_port)).content, raw=False)
print("Orderbook service status:", status)

# Wait for enough exchange data to arrive... 
time.sleep(3)

# Then we request to know the location of the data in shared memory so we can open it
orderbooks_details = umsgpack.loads(requests.get('http://localhost:{}/shm'.format(orderbook_service_port)).content, raw=False)

# Now that we know the locations of orderbooks in SHM we can create orderbook readers to read them
# The hardcoded maximum size of orderbook is 400 (there are 200 bids and asks)
for exchange, instrument, shm_path in orderbooks_details:
    reader = RtOrderbookReader(shm_path)
    print(f"\nCreated reader for orderbook {exchange}:{instrument} located at {shm_path}")

    print("Top 3 Bids are:")
    pprint(reader.snapshot_bids(3))

    print("Top 3 Asks are:")
    pprint(reader.snapshot_asks(3))