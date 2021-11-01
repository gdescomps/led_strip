from __future__ import print_function
from __future__ import division

import platform
import numpy as np
# import config

UDP_IP = "192.168.1.42"
UDP_PORT = 7777
N_PIXELS = 60

# ESP8266 uses WiFi communication
# if config.DEVICE == 'esp8266':
import socket
_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# _gamma = np.load(config.GAMMA_TABLE_PATH)
"""Gamma lookup table used for nonlinear brightness correction"""

# _prev_pixels = np.tile(253, (3, N_PIXELS))
# """Pixel values that were most recently displayed on the LED strip"""

# _is_python_2 = int(platform.python_version_tuple()[0]) == 2

def _update_esp8266(pixels):
    """Sends UDP packets to ESP8266 to update LED strip values

    The ESP8266 will receive and decode the packets to determine what values
    to display on the LED strip. The communication protocol supports LED strips
    with a maximum of 256 LEDs.

    The packet encoding scheme is:
        |i|r|g|b|
    where
        i (0 to 255): Index of LED to change (zero-based)
        r (0 to 255): Red value of LED
        g (0 to 255): Green value of LED
        b (0 to 255): Blue value of LED
    """
    # global pixels, _prev_pixels
    # Truncate values and cast to integer
    pixels = np.clip(pixels, 0, 255).astype(int)
    # Optionally apply gamma correc tio
    # p = _gamma[pixels] if config.SOFTWARE_GAMMA_CORRECTION else np.copy(pixels)
    p = np.copy(pixels)
    MAX_PIXELS_PER_PACKET = 126
    # Pixel indices
    idx = range(pixels.shape[1])
    idx = [i for i in idx]
    n_packets = len(idx) // MAX_PIXELS_PER_PACKET + 1
    idx = np.array_split(idx, n_packets)
    for packet_indices in idx:
        m = []
        for i in packet_indices:
                m.append(i)  # Index of pixel to change
                m.append(p[0][i])  # Pixel red value
                m.append(p[1][i])  # Pixel green value
                m.append(p[2][i])  # Pixel blue value
        m = bytes(m)
        _sock.sendto(m, (UDP_IP, UDP_PORT))

def update(pixels):
    """Updates the LED strip values"""
    _update_esp8266(pixels)

class Hub():
    def __init__(self, host, port) -> None:
        self._host = host
        self._port = port

    def set_color(self, r, g, b):

        pixels = np.tile(1, (3, N_PIXELS))
        """Pixel values for the LED strip"""

        # Turn all pixels off
        pixels *= 0

        pixels[0,:] = r
        pixels[1,:] = g
        pixels[2,:] = b

        # print(pixels)
        update(pixels)

    def turn_on(self):
        self.set_color(100,20,0)

    def turn_off(self):
        self.set_color(0,0,0)
