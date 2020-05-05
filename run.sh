cd SensorParser
gnome-terminal -x python3 sensor_parser.py &
cd ../REST
gnome-terminal -x python3 server.py &
cd ../PWA
npm run dev
