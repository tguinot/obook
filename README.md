
*Requires flask, zeromq, zerorpc, node.js, ccxws, pm2, postgresql, pg (node package for postgres)*

There are different components in this repository:
1. **Orderbook writer**: data structure for creating an orderbook SHM and inserting data inside.
2. **Orderbook reader**: data structure for reading an orderbook that already exists in SHM.
3. **Orderbook feeder**: Uses an Orderbook Writer and listens to an orderbook updates feed to insert data in orderbook.
3. **Live data service**: written in JS, listens to various exchanges in websocket and relays the data to zeroMQ sockets
4. **Orderbook service**: Creates Orderbook Feeders, communicates with Live data service and makes Orderbook Feeders to zeroMQ sockets for updates.
5. **Orderbook recorde**r service: Opens an existing orderbook in SHM and takes snapshots to insert in DB

**Make sure the following variables are defined in ENV**:

*export POSTGRES_DB_NAME=xxxxxxx*

*export POSTGRES_DB_HOST=xxxxxxx*

*export POSTGRES_DB_USER=xxxxxxx*

*export POSTGRES_DB_PASSWD=xxxxxxx*

*export POSTGRES_DB_PORT=xxxxxxx*


To start the live data service:

`bash start_live_data_service.sh`

To start the orderbook service (markets are defined in market_config.json):

`bash start_orderbook_service.sh`

To start the orderbook recorder service (markets are defined in the script itself):

`bash start_recording_orderbook.sh`

To visualize the services status:
`pm2 list`

Refer to pm2 documentation for further details about services management


In order to add an instrument to the live data service, it must be defined in `markets_config.json` using the following pattern:

`{
            "exchange": "BinanceUS",
            "id": "BTCUSDT",
            "base": "BTC",
            "quote": "USDT"
}`

The parameters for the live data service streams and the orderbook feeders must also be defined in database under the Service table:![Screen Shot 2021-03-02 at 10 12 56](https://user-images.githubusercontent.com/529902/109626077-5f2f7080-7b40-11eb-8638-ddf2eee493b7.jpg)

The SHM address of orderbook feeders will be rewritten automatically so the name at creation is irrelevant.

The exchange as well as both currencies used by the instrument must also be defined in database un der the currency and exchange tables.
