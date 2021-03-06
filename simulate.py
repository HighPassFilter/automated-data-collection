import tkinter as tk
from process_data_lib import process_data
from eval_data_lib import *
import matplotlib.pyplot as plt
import time
import pandas as pd
import threading

# Oscilloscope imports
from ds1054z import DS1054Z

# Sensor imports
from Server import sample_350_once

# Waveform generator imports
import argparse
import numpy as np
import sounddevice as sd
import time

# --------------------- Load the data from the samples collected ---------------------
# Default path
filename_default = "/home/alex/projectGreen/src/Important data"

# Select experiment
experiment = 5

# ======================================================== Experiment 1 ==============================================================
# Aim of the experiment:
# To collect data for three phase with varying current using the config 1 (wires in position: 2,3,4)

if experiment == 1:
    filename_experiment = filename_default + "/Three phase with varying current/"
    save_filename = "/home/alex/projectGreen/src/Server/samples/fully_balanced_3p_1A.csv"

    data_experiment_1 = pd.DataFrame()

    for j in range(1):
        print("")
        if j == 0:
            current_level = "low" # Options are low, med, high
            print("For low current:")
        if j == 1:
            current_level = "med"
            print("For medium current:")
        if j == 2:
            current_level = "high"
            print("For high current:")
        print("")

        # Load the data
        #filename = filename_experiment + current_level + "_current_3_phase"
        filename = "src/Server/samples/fully_balanced_3p_2A.csv"
        data_experiment_1 = pd.read_csv(filename)

        plot_all_data(data_experiment_1)

        # Save as csv files
        save_filename = filename_experiment + current_level + "_current_3_phase.csv"
        data_experiment_1.to_csv(save_filename)

# ======================================================== Experiment 2 =============================================================
# Aim of experiment:
# Analyse the precision/accuracy of the oscilloscope by comparing its measurements against that of the multimeter

# No code here
        
# ======================================================== Experiment 3 ==============================================================
# Aim of experiment:
# To collect data for very low single phase current

if experiment == 3:
    filename_experiment = filename_default + "/Single phase with varying low current/"
    save_filename = "/home/alex/projectGreen/src/Important data/"

    data_experiment_3 = pd.DataFrame()

    for j in range(3):
        print("")
        if j == 0:
            current_level = "low" # Options are low, med, high/home/alex/projectGreen/src/Important data/AirCond/nfTrial_00hh_00mm_08.030398ss_2021-01-29 11:08:09.487748.csv'
            print("For low current:")
        if j == 1:
            current_level = "med"
            print("For medium current:")
        if j == 2:
            current_level = "high"
            print("For high current:")
        print("")

        # Load the data
        filename = filename_experiment + "single_phase_" + current_level + "_current"
        data_experiment_3 = pd.read_csv(filename)

        plot_all_data(data_experiment_3)

        # Save as csv files
        save_filename = filename + ".csv"
        data_experiment_3.to_csv(save_filename)


# ======================================================== Experiment 4 ==============================================================
# Aim of experiment:
# To collect data for single phase in multiple positions with varying current (high, medium and low)

if experiment == 4:
    # Experiment settings
    filename_experiment = filename_default + "/Single phase multiple positions with varying current"
    save_filename = "/home/alex/projectGreen/src/Important data/Experiment_4_mag_sum.pkl"

    data_experiment_4 = pd.DataFrame()
    current_level = ""
    # Data select:
    for j in range(3):
        print("")
        if j == 0:
            current_level = "low" # Options are low, med, high
            print("For high current:")
        if j == 1:
            current_level = "med"
            print("For medium current:")
        if j == 2:
            current_level = "high"
            print("For low current:")
        print("")
        

        for iter in range(4):
            position_num = iter + 1
            filename = filename_experiment + "/pos" + str(position_num) + "_" + current_level + "_current"

            # --------------------------------- Process the data ---------------------------------
            # Rotate and remove the offset of the data
            data = pd.read_csv(filename)

            # Save raw data as csv
            save_filename = filename + ".csv"
            data.to_csv(save_filename)

            # plot_all_data(data)
            data = process_data(filename)

            # Fit a sine curve for all 14 sensors
            amp = pd.DataFrame()
            print_estimate = 0
            sum_x_axis = 0
            for i in range(14):
                data_select_string_x = "Sensor_" + str(i+1) + "_x"
                data_select_string_y = "Sensor_" + str(i+1) + "_y"

                data_select_x = data[data_select_string_x]
                data_select_y = data[data_select_string_y]

                param_x = sine_curve_fitting(data_select_x, freq_guess=0.4, phase_guess=0.5, print_estimate=print_estimate)
                param_y = sine_curve_fitting(data_select_y, freq_guess=0.4, phase_guess=0.5, print_estimate=print_estimate)

                amp.loc[i, data_select_string_x] = param_x[0]
                amp.loc[i, data_select_string_y] = param_y[0]

                sum_x_axis +=np.abs(param_x[0]) 
                
            #plot_amp(amp)
            data_experiment_4.loc[iter, current_level] = sum_x_axis
            print("Position " + str(position_num) + " completed")
    data_experiment_4.to_pickle(save_filename)

# ======================================================== Experiment 5 ===========================================================
# Aim of experiment:
# Obtain sets of 350 samples of data for 3 phase and single phase with different positions and current levels and phase 
if experiment == 5:
    
    # Configure the filepath for saving data
    filename_experiment = filename_default + "/round1"+ "/arduino_serialsingle_Alow.csv"
    filename_experiment = "/home/alex/projectGreen/src/Important data/round1/arduino_serial_three_med.csv"

    data_experiment_5 = pd.read_csv(filename_experiment)
    data_experiment_5.plot()
    data_experiment_5.plot(x='TS', y=data_experiment_5.columns[1:3], marker='.', subplots=True)
    plt.show()

    # Update the GUI            

# Save the data that has been rotated and its offset removed
#save_filename = '/home/alex/projectGreen/src/Server/samples/single_phase_0.1A_processed.csv'

#data.to_csv(save_filename)

# Plot the data
#gui_data_loader(data, 14)
#data.plot(y = ['Sensor_2_x', 'Sensor_2_y'])
#plt.show()

# GUI for displaying the readings
