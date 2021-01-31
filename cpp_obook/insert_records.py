import gzip
import umsgpack
import os
import random
from orderbook_helper import RtOrderbookWriter, RtOrderbookReader
import argparse


def run(path, orderbook, mode):
    for zipped_file in os.listdir():
        with gzip.open(zipped_file) as f:
            packed = f.read()
        updates = umsgpack.loads(packed)
        sorted_updates = sorted(updates, key=lambda s: s['seqnum'])
        if mode == 'update':
            insert_all_updates(sorted_updates, orderbook)
        elif mode == 'snapshot':
            insert_all_snapshots(sorted_updates, orderbook)


def insert_all_updates(updates, orderbook):
    for update in updates:
        insert_update(update, orderbook)
        snapped_bids = orderbook.snapshot_bids(100)
        snapped_asks = orderbook.snapped_asks(100)


def insert_all_snapshots(snapshots, orderbook):
    for snap in snapshots:
        orderbook.reset_bids()
        orderbook.reset_asks()
        insert_update(snap, orderbook)


def insert_update(update, orderbook):
    for price, quantity in update['asks'].items():
        orderbook.set_ask_quantity_at(price, quantity)
    for price, quantity in update['bids'].items():
        orderbook.set_bid_quantity_at(price, quantity)


if __name__ == '__main__':
    shm_name = '/shm' + str(random.random())
    writer = RtOrderbookWriter(shm_name)

    parser = argparse.ArgumentParser()
    parser.add_argument('record_dir', help='Directory in which records are stored')
    parser.add_argument('mode', help='Mode (orderbook updates or orderbook snapshots)')
    args = parser.parse_args()

    run(args.record_dir, writer, args.mode)