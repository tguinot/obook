
*Requires flask, zeromq, zerorpc, node.js, ccxws, pm2, postgresql, pg (node package for postgres)*

There are different components in this repository:
1. **Orderbook writer**: data structure for creating an orderbook SHM and inserting data inside.
2. **Orderbook reader**: data structure for reading an orderbook that already exists in SHM.
3. **Orderbook feeder**: Uses an Orderbook Writer and listens to an orderbook updates feed to insert data in orderbook.
3. **Live data service**: written in JS, listens to various exchanges in websocket and relays the data to zeroMQ sockets
4. **Orderbook service**: Creates Orderbook Feeders, communicates with Live data service and makes Orderbook Feeders to zeroMQ sockets for updates.
5. **Orderbook recorde**r service: Opens an existing orderbook in SHM and takes snapshots to insert in DB

**Make sure the following variables are defined in ENV**:

export POSTGRES_DB_NAME=xxxxxxx
export POSTGRES_DB_HOST=xxxxxxx
export POSTGRES_DB_USER=xxxxxxx
export POSTGRES_DB_PASSWD=xxxxxxx
export POSTGRES_DB_PORT=xxxxxxx

To start the live data service:

`bash start_live_data_service.sh`

To start the orderbook service (markets are defined in market_config.py):

`bash start_orderbook_service.sh`

To start the orderbook recorder service (markets are defined in the script itself):

`bash start_recording_orderbook.sh`
