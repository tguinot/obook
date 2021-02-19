export ORDERBOOK_SERVICE_PORT=5000
echo "python3 -u orderbook_record_model.py $1 $2"
nohup bash -c "python3 -u orderbook_record_model.py $1 $2" > orderbook_recording.out 2>&1 &