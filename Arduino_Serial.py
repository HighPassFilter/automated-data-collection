import serial
import pandas as pd
import matplotlib.pyplot as plt
import time
import datetime
from multiprocessing import Process, Pipe

class Arduino_Serial():
    def __init__(self, baud, port):
        self.ser = serial.Serial(port, baud)
        command_stream(self.ser, False)
        self.p_main, self.p_process = Pipe()
        self.process = Process(target=stream_ground_truth, args=(self.p_process, self.ser,))
        print("Ground truth collector initiated")

    def run(self):
        self.process.start()
        if self.process.is_alive():
            print("Starting ground truth collector..\n")

    def stop(self):
        print("Shutting down collector..")
        command_stream(self.ser, False)
        self.process.terminate()
        if self.process.is_alive():
            print("Ground truth collector shutdown success\n")

def stream_ground_truth(p_process, ser):
    # Initialise variables
    stream_on = 0
    save_data = 0
    truth = []
    collect_data = 0
    
    # Process loop for truth streaming
    while True:
        
        if p_process.poll():
            collect_data = p_process.recv()
        if collect_data == 1:
            if stream_on == 0:
                command_stream(ser, True)
            truth.append(collect_ground_truth(ser))
            
            save_data = 1

        # Return the data to main process
        elif save_data == 1 and collect_data == 0:
            command_stream(ser, False)
            save_data = 0
            p_process.send(truth)
            #print("Data returned - Truth")

            # Reset the data array
            truth = []
            ser.flushInput()

def command_stream(ser, status=False):
    global stream_on
    if status == True:
        ser.write(bytes(b'1'))
        stream_on = 1
    elif status == False:
        ser.write(bytes(b'0'))
        stream_on = 0

    time.sleep(0.1)

def collect_ground_truth(ser):
    # Obtain data from Arduino
    data = ser.readline()
    # Record the time of arrival of serial data
    timestamp = datetime.datetime.now()

    # Extract channel values of serial input
    data = str(data).replace("\\n", "").replace("b'", "").replace("'", "").replace("\\r", "").split(' ')
    ground_truth = []
    if not '' in data and len(data) == 3:
        ground_truth = [timestamp, int(data[0]) / 1023 * 3.3, int(data[1]) / 1023 * 3.3, int(data[2])/ 1023 * 3.3]
        #print(ground_truth)
    return ground_truth



'''
ser = serial.Serial("/dev/ttyACM0", 9600)
#ser.write(bytes(b'OFF\n'))
#ser.write(bytes(b'ON\n'))
timetaken = []
command_stream(ser, False)
command_stream(ser, True)
for i in range(200):
    print(collect_ground_truth(ser))

command_stream(ser, False)
#ser.write(bytes(b'OFF\n'))
'''

    

        


        


        
    

            
                

    


'''
data = []
for i in range(10000):
    data.append(collect_ground_truth(ser))
    

store = pd.DataFrame(data)
store.plot()
plt.show()
'''

    





    

