"""Play a sine signal."""
import argparse
import sys

import numpy as np
import sounddevice as sd
import keyboard
import time
from threading import Thread
import threading
start_idx = 0

# Initial channel value
channel_1 = 1
channel_2 = 1
channel_3 = 1

phase_1 = 0
phase_2 = 0
phase_3 = 0

MAX_CHANNEL_VALUE = 5
MIN_CHANNEL_VALUE = 0
STEP = 0.01
DELAY = 0 * 1000 # Seconds

class SignalGeneratorThread(Thread):
    def __init__(self):
        #self.process = Process(target=generate_waveform)
        #self.process.start()
        Thread.__init__(self)
        self._stop = threading.Event()
    def run(self):
        generate_waveform()

    def stop(self):
        self._stop.set()

def generate_waveform():
    global args
    global samplerate
    
    args = parser.parse_args(remaining)

    try:
        
        samplerate = sd.query_devices(args.device, 'output')['default_samplerate']

        with sd.OutputStream(device=args.device, channels=8, callback=callback,
                            samplerate=samplerate):
            print('#' * 86)
            print('\t\t\t\tSignal generator online')
            print('#' * 86)
            input()
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def callback(outdata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        global start_idx
        global channel_1
        global channel_2
        global channel_3
        global phase_1
        global phase_2
        global phase_3
        global samplerate
        global args

        t = (start_idx + np.arange(frames)) / samplerate
        t = t.reshape(-1, 1)
        x = np.array([channel_2,channel_3, channel_1,0,0,0,0,0])
        offset = np.deg2rad(np.array([phase_2 ,phase_3, phase_1,0,0,0,0,0]))
        outdata[:] = args.amplitude * np.sin(offset + 2 * np.pi * args.frequency * t) * x
        #print(outdata)
        start_idx += frames

# Retrieve arguments from the command line
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'frequency', nargs='?', metavar='FREQUENCY', type=float, default=20,
    help='frequency in Hz (default: %(default)s)')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='output device (numeric ID or substring)')
parser.add_argument(
    '-a', '--amplitude', type=float, default=0.2,
    help='amplitude (default: %(default)s)')


#signal = SignalGeneratorThread()
#signal.start()
