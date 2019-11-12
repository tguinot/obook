from orderbook_helper import RtOrderbookWriter, RtOrderbookReader

obw = RtOrderbookWriter("/shmtotesteyur")

obw.set_quantity_at(True, 13, 1, 60, 1, 2)
obw.set_quantity_at(True, 23, 1, 60, 1, 3)

obw.set_quantity_at(True, 22, 1, 75, 1, 3)
obw.set_quantity_at(True, 6, 1, 75, 1, 2)

obw.set_quantity_at(True, 11, 1, 67, 1, 4)
obw.set_quantity_at(True, 4, 1, 67, 1, 5)
obw.set_quantity_at(True, 30, 1, 67, 1, 6)
obw.set_quantity_at(True, 24, 1, 67, 1, 7)
obw.set_quantity_at(True, 0, 1, 67, 1, 7)

obr = RtOrderbookReader("/shmtotesteyur")

obr.snapshot_bids(10)