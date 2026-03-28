clear
python komunikacja.py &
PID=$!

sleep 2
python client.py

kill -- $PID