import pyaudio
import aubio
import numpy as np
import time
from neopixel import *
import random
import thread


CHUNK_SIZE = 4096*2
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
WIN_S = CHUNK_SIZE * 2
HOP_S = WIN_S // 2

LED_COUNT = 150
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 5  # DMA channel to use for generating signal (try 5)
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP = ws.WS2811_STRIP_GRB  # Strip type and colour ordering
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest


def light(brightness):
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS,
                              LED_CHANNEL,
                              LED_STRIP)
    strip.begin()
    adjusted_brightness = round(brightness, 0)*3
    print "adjusted brightness: %s " % adjusted_brightness
    if (adjusted_brightness <15) :
        strip.setBrightness(0)
        strip.show()
        return
    elif (adjusted_brightness > 255):
        adjusted_brightness = 255

    strip.setBrightness(int(adjusted_brightness))

    for i in range(0, strip.numPixels(), 1):
        strip.setPixelColor(i, Color( int(adjusted_brightness), int(adjusted_brightness) , int(adjusted_brightness)))
        # time.sleep(10 / 1000.0)
    strip.show()
class AudioInput:
    p = pyaudio.PyAudio()
    energy = 0.00
    frequency = 0.00

    def __init__(self):
        pass

    def start_recording(self):
        print 'recording'
        stream = self.p.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK_SIZE)
        pitcher = self.create_pitcher()


        while True:
            try:
                data = stream.read(CHUNK_SIZE)
                samples = np.fromstring(data, dtype=aubio.float_type)
                frequency = pitcher(samples)[0]
                energy = np.sum(samples ** 2) / len(samples)
                print("{:10.4f} {:10.4f}".format(frequency * 4, energy * 25000))
                thread.start_new_thread(light, (energy *25000,))
                # time.sleep(.2)
            except IOError as e:
                self.start_recording()


    def create_pitcher(self):
        pitcher = aubio.pitch("default", WIN_S, HOP_S, RATE)
        pitcher.set_unit("Hz")
        pitcher.set_silence(-40)
        return pitcher


