from rtlsdr import *
import requests
from time import sleep
from os.path import exists
import json
import websocket
import rel

DEFAULT_ALIAS = 'Virtual Robot'
DEFAULT_ID_STORAGE_PATH = './id'
PROD_ROBOT_POST_URL = 'https://jamming-587.herokuapp.com/robot'
PROD_POST_URL = 'https://jamming-587.herokuapp.com/measurement'
DEFAULT_WS_URL = 'ws://localhost:3000/robot/ws'
DEFAULT_ROBOT_POST_URL = 'http://localhost:3000/robot'
DEFAULT_POST_URL = 'http://localhost:3000/measurement'
DEFAULT_LAT_LONG = (39.75035755631502, -105.22396087646484)
DEFAULT_SAMPLE_WIDTH = 256 * 1024
DEFAULT_SAMPLE_RATE = 2.4e6
DEFAULT_FREQUENCY = 95e6
DEFAULT_GAIN = 4
DEFAULT_SLEEP = 1

class Radio():
    def __init__(self, sample_rate, center_freq, gain, url, sample_width) -> None:
        self.sdr = RtlSdr()
        self.sdr.sample_rate = sample_rate
        self.sdr.center_freq = center_freq
        self.sdr.gain = gain
        self.sample_width = sample_width
        self.url = url
        self.lat = None
        self.long = None

    # Returns an array of all samples.
    def take_samples(self):
        return self.sdr.read_samples(self.sample_width)

    # Returns one RSSI measurement across all samples.
    def take_average_measurement(self):
        samples = self.sdr.read_samples(self.sample_width)
        total = 0.0
        for sample in samples:
            total += sample
        return total / float(self.sample_width)

    def close(self):
        self.sdr.close()

    def set_coordinates(self, lat, long):
        self.lat = lat
        self.long = long

class GPS():
    def __init__(self) -> None:
        pass

    def measure_coordinates(self):
        return DEFAULT_LAT_LONG

class Robot():
    def __init__(self, alias, websocket_url) -> None:
        if (exists(DEFAULT_ID_STORAGE_PATH)):
            file = open(DEFAULT_ID_STORAGE_PATH, 'r')
            self.id = file.readline().strip()
        else:
            try:
                result = requests.post(DEFAULT_ROBOT_POST_URL, json={'alias': alias})
                if (int(result.status_code) != 200):
                    print("Robot initialization failed. Connection to the server could not be established.")
                    return
                id = result.json()                
                if (id is not None):
                    file = open('./id', 'w+')
                    file.write(id)
                    self.id = id
                
            except Exception as e:
                print(f'An error was encountered in setting up the robot. Please restart the device: {e}')
                return

    def get_id(self):
        return self.id

def post_measurement(self, measurement, lat, long):
    if (lat is None):
        lat = DEFAULT_LAT_LONG[0]
    if (long is None):
        long = DEFAULT_LAT_LONG[1]
    result = requests.post(self.url, data={'lat': lat, 'long': long, 'intensity': measurement})
    return result

def on_ws_message(robot, ws, message):
    print(message)

def on_error(ws, error):
    print(f'Web socket initialization error: {error}')

def on_close(ws, close_status, close_message):
    print("The web socket was closed.")

def on_open(ws):
    print("Websocket connection successful!")

def create_websocket(websocket_url):
    try:
        websocket.enableTrace(True)
        ws = websocket.WebSocket()
        ws.connect(websocket_url)
        return ws
    except Exception as e:
        print(f'Error configuring web socket connection: {e}')

def main():
    robot = Robot(DEFAULT_ALIAS, DEFAULT_WS_URL)
    radio = Radio(DEFAULT_SAMPLE_RATE, DEFAULT_FREQUENCY, DEFAULT_GAIN, DEFAULT_POST_URL, DEFAULT_SAMPLE_WIDTH)
    gps = GPS()
    ws = create_websocket(f'{DEFAULT_WS_URL}/{robot.get_id()}')
    # ws.send("Hello!")
    # ws.close()

    terminal_condition = False

    while not terminal_condition:
        incoming = json.loads(ws.recv())
        # gps_measurement = gps.measure_coordinates()
        # rssi_measurement = radio.take_average_measurement()
        # post_measurement(rssi_measurement, gps_measurement[0], gps_measurement[1])
        ws.send(json.dumps({'message':'request_position_update'}))
        sleep(DEFAULT_SLEEP)

try:
    main()
except Exception as error:
    print(error)