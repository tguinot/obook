from feed_recorder import Recorder
from models import init_db

if __name__ == "__main__":
    market = {
        "id": "BTC/USD",
        "base": "BTC",
        "quote": "USD",
    }
    init_db("other_db.db")
    recorder = Recorder('127.0.0.1', '4242', 'FTX', market, record=True, record_time=1000000, buffer_length=10, record_path='./')
    
    recorder.run()