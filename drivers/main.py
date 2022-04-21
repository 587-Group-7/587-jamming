from pylab import *
from rtlsdr import *
import requests
from time import sleep
from os.path import exists
import json

DEFAULT_ALIAS = 'Virtual Robot'
DEFAULT_ID_STORAGE_PATH = './id'
DEFAULT_ROBOT_POST_URL = 'https://jamming-587.herokuapp.com/robot'
DEFAULT_POST_URL = 'https://jamming-587.herokuapp.com/measurement'
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
    def __init__(self, alias) -> None:
        if (exists(DEFAULT_ID_STORAGE_PATH)):
            file = open(DEFAULT_ID_STORAGE_PATH, 'r')
            self.id = file.readline().strip()
        else:
            try:
                result = requests.post(DEFAULT_ROBOT_POST_URL, json={'alias': alias})
                print(result.json())
            except Exception as e:
                print(e)

def post_measurement(self, measurement, lat, long):
    if (lat is None):
        lat = DEFAULT_LAT_LONG[0]
    if (long is None):
        long = DEFAULT_LAT_LONG[1]
    result = requests.post(self.url, data={'lat': lat, 'long': long, 'intensity': measurement})
    return result

def main():
    robot = Robot(DEFAULT_ALIAS)
    return
    radio = Radio(DEFAULT_SAMPLE_RATE, DEFAULT_FREQUENCY, DEFAULT_GAIN, DEFAULT_POST_URL, DEFAULT_SAMPLE_WIDTH)
    gps = GPS()

    terminal_condition = False

    while not terminal_condition:
        gps_measurement = gps.measure_coordinates()
        rssi_measurement = radio.take_average_measurement()
        post_measurement(rssi_measurement, gps_measurement[0], gps_measurement[1])
        sleep(DEFAULT_SLEEP)

try:
    main()
except Exception as error:
    print(error)