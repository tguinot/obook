from multiprocessing import Process, Lock, Value
import os
import random
import time
from orderbook_helper import RtOrderbookWriter
from orderbook_helper import RtOrderbookReader


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(num, shm_name, name):
    counter = 1
    obr = RtOrderbookReader(shm_name)
    info('In Child bids are')
    print('Child hello', name, obr.snapshot_bids(10))
    num.value = 1
    print("Waiting for updates")
    while num.value < 9000000:
        if num.value > counter:
            print('Orderbook is sound:', obr.is_sound())
            counter += 1

if __name__ == '__main__':
    num = Value('d', 0.0)
    shm_name = '/shm' + str(random.random())
    writer = RtOrderbookWriter(shm_name)
    writer.set_quantity_at(True, 56, 10, 31000, 1)
    info('In parent OK writer')
    # Lock A
    p = Process(target=f, args=(num, shm_name, 'bob',))
    p.start()
    time.sleep(0.5)
    while num.value < 1:
        pass
    for i in range(9000000):
        price_rand = int(30000 + random.random() * 10)
        qty_rand = int(1 + random.random() * 5)
        writer.set_quantity_at(True, qty_rand, 10, price_rand, 1)
        #print("Finished parent update")
        num.value += 1

    # Update orderbook
    # Release lock, expect child to acquire and read orderbook 

    
    p.join()
    print("Joined child")