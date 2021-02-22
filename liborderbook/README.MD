## A shared memory orderbook

This software, written in Python and C++ aims to provide a real-time orderbook for cryptocurrency trading.

| Feature | Motivation |
| ---- | --- |
| **Written in C++**| Allow fast insertion/deletion from websocket/FIX feeds |
| **Python Wrapped**| Allow integration with projects based on Python trading libraries such as exchange APIs or Zipline/CCXT |
| **Residing in Shared memory (SHM)**| Allow multiprocess, independant, service-based running logic |
| **Rationals-based**| Allow better precision than floats and doubles, and easy Python interfacing |



Build instructions:

1. `cmake .`
2. `make orderbook_wrapper`



