const ccxws = require("ccxws");
var zerorpc = require("zerorpc");
var zmq = require("zeromq");
var msgpack = require('msgpack');

var exchanges_interfaces = {};

exchanges_interfaces['FTX'] = new ccxws.Ftx();
exchanges_interfaces['FTX'].on("trade", trade => {
    console.log("Received trade")
    for (const [sock_name, publish] of Object.entries(publish_socks)) {
        if (trade.exchange+trade.base+trade.quote == sock_name) {
            console.log("Redirecting trade of", sock_name)
            publish_socks[sock_name]['sock'].send(msgpack.pack(trade));
            break;
        }
    }
});

var publish_socks = {}

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

var server = new zerorpc.Server({
    subscribe_trades: function(exchange, instrument, reply) {
        socket_name = exchange+instrument.base+instrument.quote

        if (!publish_socks.hasOwnProperty(socket_name)) {
            console.log("Initializing socket")
            port = 5500 + getRandomInt(200)

            publish_socks[socket_name] = {'sock': zmq.socket("pub"), 'port': port};
            publish_socks[socket_name]['sock'].bindSync("tcp://127.0.0.1:" + port);

            console.log("Created sock entry for", socket_name, "on port", port)
            
            exchanges_interfaces[exchange].subscribeTrades(instrument);
        }

        console.log("Sending back socket details", publish_socks[socket_name]['port'])

        reply(null, publish_socks[socket_name]['port']);
    }
});

console.log("Service ready");

server.bind("tcp://0.0.0.0:4242");
