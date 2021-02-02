const ccxws = require("ccxws");
var zerorpc = require("zerorpc");
var zmq = require("zeromq");
var msgpack = require('msgpack');

const supported_exchanges = ['Binance'];
var exchanges_interfaces = {};

supported_exchanges.forEach(exchange_name =>  {
    exchanges_interfaces[exchange_name] = new ccxws.Binance();

    exchanges_interfaces[exchange_name].on("trade", trade => {
        console.log("Received trade")
        for (const [sock_name, publish] of Object.entries(publish_socks)) {
            if ("trade"+trade.exchange+trade.base+trade.quote == sock_name) {
                console.log("Redirecting trade of", sock_name)
                publish_socks[sock_name]['sock'].send(msgpack.pack(trade));
                break;
            }
        }
    });

    exchanges_interfaces[exchange_name].on("l2snapshot", ob => {
        // console.log("Received ob update", ob)
        for (const [sock_name, publish] of Object.entries(publish_socks)) {
            if ("orderbook"+ob.exchange+ob.base+ob.quote == sock_name) {
                console.log("Redirecting ob update of", sock_name)
                publish_socks[sock_name]['sock'].send(msgpack.pack(ob));
                break;
            } else {
                console.log("Unknown destination for", "orderbook"+ob.exchange+ob.base+ob.quote, "only know", sock_name)
            }
        }
    });
})

var publish_socks = {}

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

var server = new zerorpc.Server({
    subscribe_trades: function(exchange, instrument, reply) {
        socket_name = "trade"+exchange+instrument.base+instrument.quote

        if (!publish_socks.hasOwnProperty(socket_name)) {
            console.log("Initializing socket")
            port = 5500 + getRandomInt(200)

            publish_socks[socket_name] = {'sock': zmq.socket("pub"), 'port': port};
            publish_socks[socket_name]['sock'].bindSync("tcp://127.0.0.1:" + port);

            console.log("Created sock entry for", socket_name, "on port", port)
            
            exchanges_interfaces[exchange].subscribeTrades(instrument);
        }

        console.log("Sending back socket details", publish_socks[socket_name]['port'])

        reply(null, {addr: '127.0.0.1', port: publish_socks[socket_name]['port']});
    },

    subscribe_orderbook: function(exchange, instrument, reply) {
        socket_name = "orderbook" + exchange+instrument.base+instrument.quote

        if (!publish_socks.hasOwnProperty(socket_name)) {
            console.log("Initializing socket", socket_name)
            port = 5500 + getRandomInt(200)

            publish_socks[socket_name] = {'sock': zmq.socket("pub"), 'port': port};
            publish_socks[socket_name]['sock'].bindSync("tcp://127.0.0.1:" + port);

            console.log("Created sock entry for", socket_name, "on port", port)
            
            exchanges_interfaces[exchange].subscribeLevel2Snapshots(instrument);
        }

        console.log("Sending back socket details", publish_socks[socket_name]['port'])

        reply(null, {addr: '127.0.0.1', port: publish_socks[socket_name]['port']});
    }
});

console.log("Service ready on 4242");

server.bind("tcp://127.0.0.1:4242");
