import tone_controller as tc
import keyboard
import numpy as np
import time
from Arduino_Serial import Arduino_Serial
from Argon_Serial import Argon_Serial
import Server
import pandas as pd
from ast import literal_eval
import matplotlib.pyplot as plt
import serial.tools.list_ports

fully_configured = 0
configure_msg = 0

channel1_array = [0.47, 0.95, 1.47]
channel2_array = [0.51, 1.05, 1.58]
channel3_array = [0.663, 1.06, 1.56] #1.68

phase_offset = [[32, 14, -3], [51, 11, 6], [54, 12, 9]]

case = 0
configured = 0

run_experiment = 0
experiment_complete = 0

# Keyboard globals
millis = lambda: int(round(time.time() * 1000))
prev_time = 0
update_flag = 0

# Setup the signal generator

# ================================================ Helper functions =====================================================
def connect_devices():
    ports = serial.tools.list_ports.comports()
    sensor_running = 0
    truth_running = 0

    # Check all the communication ports
    for p in ports:
        print(p.description)
        if p.description == "Argon CDC Mode":
            baud = 115200
            argon_serial = Argon_Serial(baud, p.device)
            #argon_serial.run()
            sensor_running = 1
        
        elif "ttyACM" in p.description or "Arduino" in p.description:
            baud = 9600
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

    return sensor_running

def load_settings():
    global channel1_array
    global channel2_array
    global channel3_array
    global phase_offset

    try:
        
        # Read in the previous settings from the previous run
        settings = pd.read_csv("settings.csv")
        print(settings)

        # Replace default settings with that of previous run
        channel1_array = settings.iloc[0][1:4].astype(float).to_list()
        channel2_array = settings.iloc[1][1:4].astype(float).to_list()
        channel3_array = settings.iloc[2][1:4].astype(float).to_list()
        phase_offset = phase_offset = settings.iloc[3][1:4].apply(literal_eval).to_list()

    except OSError:
        print("No preconfigured settings found. Using default settings..")

# Configure experimental using the keyboard
def configure(case):
    global prev_time
    global update_flag
    curr_time = millis()
    if curr_time - prev_time > tc.DELAY:
        update_flag = 1

    if update_flag == 1:
        # Channel 1:
        if keyboard.is_pressed('1'):
            # Amplitude
            if keyboard.is_pressed('up'):
                # Increase the value of the channel
                tc.channel_1 += tc.STEP
                if tc.channel_1 > tc.MAX_CHANNEL_VALUE:
                    tc.channel_1 = tc.MAX_CHANNEL_VALUE
                
                print("Channel 1 value: " + str(np.round(tc.channel_1, 3)))
                update_flag = 0
                prev_time = curr_time

            elif keyboard.is_pressed('down'):
                # Decrease the value of the channel
                tc.channel_1 -= tc.STEP
                if tc.channel_1 < tc.MIN_CHANNEL_VALUE:
                    tc.channel_1 = tc.MIN_CHANNEL_VALUE

                print("Channel 1 value: " + str(np.round(tc.channel_1, 3)))
                update_flag = 0
                prev_time = curr_time

            # Phase
            if keyboard.is_pressed('right'):
                # Shift the phase to the right
                tc.phase_1 += tc.STEP * 100
                print("Channel 1 phase: " + str(tc.phase_1))
                update_flag = 0
                prev_time = curr_time

            elif keyboard.is_pressed('left'):
                # Shift the phase to the left
                tc.phase_1 -= tc.STEP * 100
                print("Channel 1 phase: " + str(tc.phase_1))
                update_flag = 0
                prev_time = curr_time
            

        # Channel 2:
        elif keyboard.is_pressed('2'):
            # Amplitude
            if keyboard.is_pressed('up'):
                # Increase the value of the channel
                tc.channel_2 += tc.STEP
                if tc.channel_2 > tc.MAX_CHANNEL_VALUE:
                    tc.channel_2 = tc.MAX_CHANNEL_VALUE
                
                print("Channel 2 value: " + str(np.round(tc.channel_2, 3)))
                update_flag = 0
                prev_time = curr_time

            elif keyboard.is_pressed('down'):
                # Decrease the value of the channel
                tc.channel_2 -= tc.STEP
                if tc.channel_2 < tc.MIN_CHANNEL_VALUE:
                    tc.channel_2 = tc.MIN_CHANNEL_VALUE

                print("Channel 2 value: " + str(np.round(tc.channel_2, 3)))
                update_flag = 0
                prev_time = curr_time
            
            # Phase
            if keyboard.is_pressed('right'):
                # Shift the phase to the right
                tc.phase_2 += tc.STEP * 100
                print("Channel 2 phase: " + str(tc.phase_2))
                update_flag = 0
                prev_time = curr_time
                
            elif keyboard.is_pressed('left'):
                # Shift the phase to the left
                tc.phase_2 -= tc.STEP * 100
                print("Channel 2 phase: " + str(tc.phase_2))
                update_flag = 0
                prev_time = curr_time

        # Channel 3
        elif keyboard.is_pressed('3'):
            # Amplitude
            if keyboard.is_pressed('up'):
                # Increase the value of the channel
                tc.channel_3 += tc.STEP
                if tc.channel_3 > tc.MAX_CHANNEL_VALUE:
                    tc.channel_3 = tc.MAX_CHANNEL_VALUE
                
                print("Channel 3 value: " + str(np.round(tc.channel_3, 3)))
                update_flag = 0
                prev_time = curr_time

            elif keyboard.is_pressed('down'):
                # Decrease the value of the channel
                tc.channel_3 -= tc.STEP
                if tc.channel_3 < tc.MIN_CHANNEL_VALUE:
                    tc.channel_3 = tc.MIN_CHANNEL_VALUE

                print("Channel 3 value: " + str(np.round(tc.channel_3, 3)))
                update_flag = 0
                prev_time = curr_time

            # Phase
            if keyboard.is_pressed('right'):
                # Shift the phase to the right
                tc.phase_3 += tc.STEP * 100
                print("Channel 3 phase: " + str(tc.phase_3))
                update_flag = 0
                prev_time = curr_time
                
            elif keyboard.is_pressed('left'):
                # Shift the phase to the left
                tc.phase_3 -= tc.STEP * 200
                print("Channel 3 phase: " + str(tc.phase_3))
                update_flag = 0
                prev_time = curr_time

        elif keyboard.is_pressed('c') and keyboard.is_pressed('='):
            # Store the settings
            channel1_array[case] = tc.channel_1
            channel2_array[case] = tc.channel_2
            channel3_array[case] = tc.channel_3
            phase_offset[case][0] = tc.phase_1 + 120
            phase_offset[case][1] = tc.phase_2 - 120
            phase_offset[case][2] = tc.phase_3
            update_flag = 0
            
            prev_time = curr_time + 100
            return 1
    return 0

# Label generator
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

# Collect data from the truth and the sensor
def collect_data(arduino_serial, argon_serial, fileid, duration=2):
    saved = False
    sensor_collected = False
    truth_collected = False

    # Start collecting data from Arduino
    arduino_serial.p_main.send(1)
    # Start collecting data from the sensor
    argon_serial.p_main.send(1)

    # Wait x seconds
    time.sleep(duration)

    # Stop collecting data from Arduino
    arduino_serial.p_main.send(0)
    # Stop collecting data from the sensor
    argon_serial.p_main.send(0)

    while not saved:
        if argon_serial.p_main.poll():
            # Collect data from the sensors
            sensor_data = argon_serial.p_main.recv()
            
            if type(sensor_data) == list:
                print("\t\t\tData from sensors saved!")
                
                sensor_collected = True
                
        
        if arduino_serial.p_main.poll():
            ground_truth = arduino_serial.p_main.recv()

            if type(ground_truth) == list:
                print("\t\t\tData from truths saved!")
                ground_truth = pd.DataFrame(ground_truth, columns=["TS", "A", "B", "C"])
                truth_collected = True

        if sensor_collected and truth_collected:
            saved = True
            sensor_data.to_csv("/home/alex/projectGreen/src/Important data/round1/argon_serial_" + fileid + ".csv", index=False)

            # Rename the columns for truth data
            ground_truth.to_csv("/home/alex/projectGreen/src/Important data/round1/arduino_serial_" + fileid + ".csv", index=False)
            print("\t\t\tCurrent data collected")

    time.sleep(1)


# ========================================== Experiment =================================================
# setup the experiment

while experiment_complete == 0:
    # Check and ask if you want to reload previous settings

    if fully_configured != 1:
        # ---------------------------- Configure channel settings ----------------------------------------
        if configure_msg == 0:
            
            # Try and load previous settings
            #load_settings()

            # Connect to Arduino and Argon
            argon_serial, arduino_serial = connect_devices()
            #argon_serial.run()
            #arduino_serial.run()

            # Start the waveform generator
            signal = tc.SignalGeneratorThread()
            signal.start()

            print("Please configure Experiment 5 based on your choice of current level and phase")
            print("Press c to confirm settings and run experiments")
            configure_msg = 1
            time.sleep(1)

        # Configure the channel settings for low current
        if case == 0:
            print("Configuring for low current..")

            # Use the previous settings
            tc.channel_1 = channel1_array[case]
            tc.channel_2 = channel2_array[case]
            tc.channel_3 = channel3_array[case]

            tc.phase_1 = -120 + phase_offset[case][0]
            tc.phase_2 = 120 + phase_offset[case][1]
            tc.phase_3 = 0 + phase_offset[case][2]

            # Use the keyboard to control the current and phase
            while configured == 0:
                time.sleep(0.1)
                configured = configure(case)
            
            configured = 0
            print("\nLow current configured\n")
            case = 1
            
        # Configure the channel settings for medium current
        elif case == 1:
            print("Configuring for medium current..")

            # Use the previous settings
            tc.channel_1 = channel1_array[case]
            tc.channel_2 = channel2_array[case]
            tc.channel_3 = channel3_array[case]
            
            # Phase change for current difference
            tc.phase_1 = -120 + phase_offset[case][0]
            tc.phase_2 = 120 + phase_offset[case][1]
            tc.phase_3 = 0 + phase_offset[case][2]

            # Swap the phase
            #tc.phase_1 = 120 + phase_offset[0]
            #tc.phase_2 = -120 + phase_offset[1]
            #tc.phase_3 = 0 + phase_offset[2]

            # Use the keyboard to control the current and phase
            while configured == 0:
                time.sleep(0.1)
                configured = configure(case)
            
            configured = 0
            print("\nMedium current configured\n")

            case = 2

        # Configure the channel settings for high current
        else:
            print("Configuring for high current..")

            # Use the previous settings
            tc.channel_1 = channel1_array[case]
            tc.channel_2 = channel2_array[case]
            tc.channel_3 = channel3_array[case]

            # Phase change for current difference
            tc.phase_1 = -120 + phase_offset[case][0]
            tc.phase_2 = 120 + phase_offset[case][1]
            tc.phase_3 = 0 + phase_offset[case][2]

            # Swap the phase
            #tc.phase_1 = 0 + phase_offset[0]
            #tc.phase_2 = 120 + phase_offset[1]
            #tc.phase_3 = -120 + phase_offset[2]
            # Use the keyboard to control the current and phase
            while configured == 0:
                time.sleep(0.1)
                configured = configure(case)
            
            configured = 0

            
            print("\nHigh current configured\n")

            # Inform user about current settings used in experiment
            fully_configured = 1
            
            print("-"*29 + "Experiment fully configured" + "-"*29 + "\n")

            # Save the experiment settings to a file
            print("Current settings:")
            settings = [channel1_array, channel2_array, channel3_array, phase_offset]
            settings = pd.DataFrame(settings, columns=["Low", "Med", "High"], index=["Channel_1", "Channel_2", "Channel_3", "Phase_offset"])
            print(settings)
            settings_filename = "settings.csv"
            settings.to_csv(settings_filename)
            run_experiment = 1

            time.sleep(0.5)
    
    elif run_experiment == 1:
        # ------------------------------------------- Run the experiment ----------------------------------------------
        print("")
        print("Running experiment..")
        fileid = ["low", "med", "high"]
        single = ["A", "B", "C"]

        # Set the channel value
        tc.channel_1 = 0
        tc.channel_2 = 0
        tc.channel_3 = 0
        duration = 2 # CHANGE YOUR DURATION HERE

        # Collect zero current data
        collect_data(arduino_serial, argon_serial, "zero", duration)
        
        # Do for each current level
        for i in range(len(channel1_array)):
            print("FOR CURRENT " + str(i+1) + ":")
            
            # Collect each single phase data for current configuration
            for k in range(3):
                print("\t\tcollecting single phase data for channel " + str(k+1))
                if k == 0:
                    # Set the channel value
                    tc.channel_1 = channel1_array[i]
                    tc.channel_2 = 0
                    tc.channel_3 = 0

                    collect_data(arduino_serial, argon_serial, "single_"+ single[k] + "_" + fileid[i], duration)
                    
                elif k == 1:
                    # Set the channel value
                    tc.channel_1 = 0
                    tc.channel_2 = channel2_array[i]
                    tc.channel_3 = 0

                    collect_data(arduino_serial, argon_serial, "single_" + single[k] + "_" + fileid[i], duration)

                elif k == 2:
                    # Set the channel value
                    tc.channel_1 = 0
                    tc.channel_2 = 0
                    tc.channel_3 = channel3_array[i]

                    collect_data(arduino_serial, argon_serial, "single_" + single[k] + "_" + fileid[i], duration)

            # Collect the three phase data
            # Set the channel value
            tc.channel_1 = channel1_array[i]
            tc.channel_2 = channel2_array[i]
            tc.channel_3 = channel3_array[i]

            collect_data(arduino_serial, argon_serial, "three_" + fileid[i], duration)
        
        run_experiment = 0

    else:
        experiment_complete = 1

        time.sleep(3)
        arduino_serial.stop()
        argon_serial.stop()

        print("")
        print("#" * 84)
        print("\t\t\t\tExperiment complete")
        print("#" * 84)
        print("")
        

'''
    # Do for each phase permutation (For 3 phase -> Permutations  = 6)
                for j in range(6):
                    print("\tfor phase permutation " + str(j+1) + ":")
'''

''' For merging
    arg = pd.read_csv('argon_serial_single_A_high.csv', parse_dates=['TS'])
ard = pd.read_csv('arduino_serial_single_A_high.csv', parse_dates=['TS'])ard[['A', 'B', 'C']] = ard[['A', 'B', 'C']] * 500.0 / 3.2ar = arg.append(ard).sort_values(by=['TS'])ard.plot(x='TS', y=ard.columns[1:], marker='.', figsize=(50.0, 30.0))
arg.plot(x='TS', y=arg.columns[1:], marker='.', figsize=(50.0, 30.0))ar.plot(x='TS', y=ar.columns[1:], marker='.', figsize=(50.0, 30.0))
'''