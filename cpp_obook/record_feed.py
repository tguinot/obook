from feed_recorder import Recorder

if __name__ == "__main__":
    market = {
        "id": "BTC/USD",
        "base": "BTC",
        "quote": "USD",
    }

    recorder = Recorder('127.0.0.1', '4242', 'FTX', market, record=True, record_time=100000, buffer_length=10, record_path='./')
    recorder.run()