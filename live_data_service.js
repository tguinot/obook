const ccxws = require("ccxws");
var zerorpc = require("zerorpc");
var zmq = require("zeromq");
var msgpack = require('msgpack');
const { Sequelize, DataTypes } = require('sequelize');
var fs = require('fs');

const sequelize = new Sequelize(`postgres://${process.env.POSTGRES_DB_USER}:${process.env.POSTGRES_DB_PASSWD}@${process.env.POSTGRES_DB_HOST}:${process.env.POSTGRES_DB_PORT}/${process.env.POSTGRES_DB_NAME}`, {
    dialect: 'postgres',
    dialectOptions: {
        ssl: {
            require: true,
            rejectUnauthorized: false
        }
    }})
const markets_config = JSON.parse(fs.readFileSync('markets_config.json', 'utf8'));

const Service = sequelize.define('Service', {
    // Model attributes are defined here
    name: {
      type: DataTypes.STRING
    },
    id: { type: DataTypes.INTEGER, autoIncrement: true, primaryKey: true},
    port: { type: DataTypes.INTEGER, unique: true },
    address: {
        type: DataTypes.STRING
      },
    instrument: {
        type: DataTypes.STRING
    },
    exchange: {
        type: DataTypes.STRING,
      },

  }, {
    timestamps: false,
    tableName: 'service'
  });

(async () => {
    await sequelize.sync();
    own_service = await Service.findOne(
        {
            where: {
              name: 'LiveDataService',
              address: '127.0.0.1'
            }
          }
    );

    const supported_exchanges = ['Binance', 'FTX', 'Kraken'];

    var publish_socks = {}

    const exchanges_interfaces = {
        'Binance':  new ccxws.Binance(),
        'FTX':      new ccxws.Ftx(),
        'Kraken':   new ccxws.Kraken(),
    }

    function getRandomInt(max) {
        return Math.floor(Math.random() * Math.floor(max));
    }


    supported_exchanges.forEach(exchange_name =>  {
        exchanges_interfaces[exchange_name].on("trade", trade => {
            for (const [sock_name, publish] of Object.entries(publish_socks)) {
                if ("trade"+trade.exchange+trade.base+trade.quote == sock_name) {
                    publish_socks[sock_name]['sock'].send(msgpack.pack(trade));
                    break;
                }
            }
        });

        exchanges_interfaces[exchange_name].on("l2update", ob => {
            ob.server_received = Date.now()
            for (const [sock_name, publish] of Object.entries(publish_socks)) {
                if ("orderbook"+ob.exchange+ob.base+ob.quote == sock_name) {
                    //console.log("Sending update for", ob.exchange+ob.base+ob.quote) 
                    publish_socks[sock_name]['sock'].send(msgpack.pack(ob));
                    return;
                }
            }
            console.log("Unknown destination for", "orderbook"+ob.exchange+ob.base+ob.quote, "among", publish_socks);
        });
    })


    async function subscribe_to_orderbook(instrument) {
        exchange = instrument.exchange
        publish_name = "orderbook" + exchange+instrument.base+instrument.quote
        console.log("Starting orderbook subscription for", exchange, instrument)
        if (!publish_socks.hasOwnProperty(publish_name)) {
            console.log("Initializing socket", publish_name, 'by looking for', exchange, instrument.id)

            stream_details = await Service.findOne(
                {
                    where: {
                        name: 'OrderbookDataStream',
                        address: '127.0.0.1',
                        exchange: exchange,
                        instrument: instrument.id
                    }
                }
            );
            port = stream_details.dataValues.port
            publish_socks[publish_name] = {'sock': zmq.socket("pub"), 'port': port};
            publish_socks[publish_name]['sock'].bindSync("tcp://127.0.0.1:" + port);

            console.log("Created sock entry for", publish_name, "on port", port)
            console.log("Subscribing to instrument", instrument)
            exchanges_interfaces[exchange].subscribeLevel2Updates(instrument);
        }

    }

    for (const market of markets_config.all_markets) {
        console.log("Attempting to subscribe to market", market)
        await subscribe_to_orderbook(market)
    }

    var server = new zerorpc.Server({
        subscribe_trades: function(exchange, instrument, reply) {
            (async () => {
                socket_name = "trade"+exchange+instrument.base+instrument.quote

                if (!publish_socks.hasOwnProperty(socket_name)) {
                    console.log("Initializing socket")
                    stream_details = await Service.findOne(
                        {
                            where: {
                            name: 'TradeDataStream',
                            address: '127.0.0.1',
                            instrument: instrument.id,
                            exchange: exchange
                            }
                        }
                    );
                    port = stream_details.dataValues.port

                    publish_socks[socket_name] = {'sock': zmq.socket("pub"), 'port': port};
                    publish_socks[socket_name]['sock'].bindSync("tcp://127.0.0.1:" + port);

                    console.log("Created sock entry for", socket_name, "on port", port)
                    
                    exchanges_interfaces[exchange].subscribeTrades(instrument);
                }

                console.log("Sending back socket details", publish_socks[socket_name]['port'])
                reply(null, {addr: '127.0.0.1', port: publish_socks[socket_name]['port']});
            })();
        },

    });

    console.log("Service ready on "+own_service.dataValues.port);
    server.bind("tcp://127.0.0.1:"+own_service.dataValues.port);
    

})();



