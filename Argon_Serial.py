import serial
import time
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process, Pipe 
millis = lambda: int(round(time.time() * 1000))
'''
Note:   Argon Serial and Arduino Serial are very similar classes which can be combined. The main differences are in 
        the way that they collect, store and command data from the devices. If they are combined, the function who_are_you()
        in experiment_interface can be integrated to automatically identify the devices on the serial ports.
'''

raw_sensor = [[],[]]
prev_value =0

class Argon_Serial():
    def __init__(self, baud, port):
        self.ser = serial.Serial(port, baud)
        command_stream(self.ser, False)
        self.p_main, self.p_process = Pipe()
        self.process = Process(target=stream_sensor_data, args=(self.p_process, self.ser,))
        print("Sensor data collector initiated")

    def run(self):
        self.process.start()
        if self.process.is_alive():
            print("Starting sensor data collector..\n")

    def stop(self):
        print("Shutting down collector..")
        command_stream(self.ser, False)
        self.process.terminate()
        if self.process.is_alive():
            print("Sensor data collector shutdown success\n")

# Return the data to main processes
def stream_sensor_data(p_process, ser):
    global raw_sensor
    global prev_value

    # Initialise variables
    stream_on = 0 
    collect_data = 0
    save_data = 0

    # Process loop for sensor sampling
    
    while True:
        if p_process.poll():
            collect_data = p_process.recv()
        if collect_data == 1:
            if stream_on == 0:
                command_stream(ser, True)
            
            #for i in range(2000):
            while True:
                if p_process.poll():
                    break
                collect_sensor_data(ser)
                if len(raw_sensor[1]) - prev_value >= 10000:
                    print(len(raw_sensor[1]))
                    prev_value = len(raw_sensor[1])
                
            save_data = 1


        # Return the sensor collected
        elif collect_data == 0 and save_data == 1:
            command_stream(ser, False)
            p_process.send(format_data(raw_sensor))
            #print("Data returned - Sensor")
            raw_sensor = [[],[]]
            ser.flushInput()
            save_data = 0

def format_data(raw_sensor):
    sensor = [[] for i in range(14 * 3 + 1)]
    
    for data in raw_sensor[1]:
        # Fill up the data list
        for sensor_num in range(14):
            if data[0] == sensor_num:
                # For sensor with data
                for i in range(3):
                    sensor[sensor_num*3+i+1].append(int.from_bytes([data[i*2+1], data[i*2+2]], byteorder="little", signed=True))
                    
            else:
                # For sensor without data
                for i in range(3):
                    sensor[sensor_num*3+i+1].append("")
    sensor[0] = raw_sensor[0]
    return sensor

def command_stream(ser, status=False):
    global stream_on
    if status == True:
        ser.write(bytes(b'1'))
        stream_on = 1
    elif status == False:
        ser.write(bytes(b'0'))
        stream_on = 0

    time.sleep(0.1)

def collect_sensor_data(ser):
    global raw_sensor
    # Collect one set of data
    if ser.in_waiting > 0:
        raw_sensor[1].append(ser.read(7))
        
        # Timestamp the data
        timestamp = datetime.datetime.now()
        raw_sensor[0].append(timestamp)



'''

ser = serial.Serial("/dev/ttyACM0", 115200)
#ser.write(bytes(b'ON'))
command_stream(ser, False)
time.sleep(1)
command_stream(ser, True)
timetaken = []

for i in range(2000):
    collect_sensor_data(ser)



sensor[0] = raw_sensor[0]
sensor = np.array(sensor)
sensor = sensor.T
df = pd.DataFrame(sensor)
df.to_csv("Testing.csv")
command_stream(ser, False)

'''


