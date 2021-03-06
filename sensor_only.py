import keyboard as ky
import time
import datetime
from Arduino_Serial import Arduino_Serial
from Argon_Serial import Argon_Serial
import serial.tools.list_ports
import numpy as np
import pandas as pd
import os.path

minutes = 10
timeout = minutes * 60
def column_name_generator():
    k = 1
    axis = [".x", ".y", ".z"]
    column_names = []
    for i in range(2):
        for j in range(7):

            if i == 0:
                H = "H1." # Right board

                for l in range(3):
                    column_names.append(H + str(8-k) + axis[l])
            else:
                H = "H2." # Left board

                for l in range(3):
                    column_names.append(H + str(k) + axis[l])
    
            k += 1
        k = 1
    return column_names

def create_column_arr():
    column_names = column_name_generator()

    # Create empty array
    column_arr = []

    # Populate dictionary
    column_arr.append("TS")
    for i in range(42):
        column_arr.append(column_names[i])

    return column_arr


def connect_devices():
    ports = serial.tools.list_ports.comports()
    sensor_running = 0
    truth_running = 0

    # Check all the communication ports
    for p in ports:
        if p.description == "Argon CDC Mode":
            baud = 115200
            print("Argon detected!")
            argon_serial = Argon_Serial(baud, p.device)
            #argon_serial.run()
            sensor_running = 1
        
        elif "ttyACM" in p.description or "Arduino" in p.description:
            baud = 9600
            print("Arduino detected!")
            arduino_serial = Arduino_Serial(baud, p.device)
            #arduino_serial.run()
            truth_running = 1

    if sensor_running == 0 and truth_running == 0:
        print("Argon and Arduino not detected")
        return ([],[])
    elif sensor_running == 1 and truth_running == 0:
        return (argon_serial, [])
    elif sensor_running == 0 and truth_running == 1:
        return ([], arduino_serial)
    else:
        return(argon_serial, arduino_serial)

def save_data(argon_serial, timeout_flag=False):
    
    time.sleep(0.2)
    #arduino_serial.p_main.send(0)
    argon_serial.p_main.send(0)
    
    sensor_data = argon_serial.p_main.recv()
    print("Data collected!")
    sensor_data = np.array(sensor_data)
    sensor_data = sensor_data.T
    sensor_data = pd.DataFrame(sensor_data, columns=create_column_arr())

    # Obtain the duration of the data collection
    df = pd.to_datetime(sensor_data["TS"])
    duration_string = str((df.tail(1) - df[0]).iloc[0])
    duration_string = duration_string.split(" ")[2].split(":")
    duration = duration_string[0] + "hh_" + duration_string[1] + "mm_" + duration_string[2] + "ss"

    # Prepare file location
    main_path = "/home/alex/projectGreen/src/Important data/"
    appliance = ""
    file_location = ""

    if timeout_flag:
        file_location = main_path + "Sensor"
        appliance = "AirCond"
    else:
        # Obtain the unique name from the user
        print("Please key in the name of the electrical appliance that you're collecting data from (e.g. AirCond):")
        appliance = input()

        print("Please key in folder name:")
        folder_name = input()
        file_location = main_path + folder_name

    # Check if folder name is there
    if not os.path.exists(file_location):
        os.umask(0)
        os.mkdir(file_location)
            
    # Save file
    filename = file_location + "/" + appliance + "_" + duration + "_" + date + ".csv"
    sensor_data.to_csv(filename, index=False)

    print("File saved")
    print("Press n and ""="" to start collecting data again")
    sensor_data = ""

# Auto detect for Argon
argon_serial, arduino_serial = connect_devices()
argon_serial.run()

prev_datetime = datetime.datetime.now()
curr_datetime = datetime.datetime.now()
timer = False

while True:
    if timer:
        curr_datetime = datetime.datetime.now()

    if ky.is_pressed("n") and ky.is_pressed("="):
        time.sleep(0.2)
        print("Collecting data..")
        argon_serial.p_main.send(1)

        # Obtain the datetime
        date = str(datetime.datetime.now())
        
        # Start the timer
        timer = True

    elif ky.is_pressed("f") and ky.is_pressed("="):
        save_data(argon_serial)

    elif (curr_datetime - prev_datetime).total_seconds() > timeout:
        # Timeout and save data
        print("TIMEOUT")
        prev_datetime = datetime.datetime.now()
        save_data(argon_serial ,True)
    
        # Start collecting more data
        print("Collecting data..")
        argon_serial.p_main.send(1)

        # Obtain the datetime
        date = str(datetime.datetime.now())