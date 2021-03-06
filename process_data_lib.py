import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

# Created by Alex
pi = math.pi
sensor_diameter = 0.033
sensor_radius = sensor_diameter/2
num_sensors = 14

# Helper function to rotate 2D vectors by a desired angle
# vector: A list of two arrays containing [x,y]
# angle: desired angle to rotate the data
# Returns the transformed vector or list of vectors
def rotate(vector, angle):
    theta = angle

    # Rotates the data for each reading
    # Assumes that x and y are of equal length
    for i in range(len(vector[0])):

        #print("Theta = " + str(np.degrees(theta)))
        #print("Vector = " + str(vector))
        rotation_vector = [vector[0][i], vector[1][i]]
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))

        rotation = np.dot(rotation_vector, R)
        vector[0][i] = rotation[0]
        vector[1][i] = rotation[1]
    return vector

# The main function responsible for rotating all data from a file by a desired angle
def rotate_data(data, angle):

    # Rotate the data for each sensor
    for i in range(num_sensors):
        # Collect XY data for each sensor
        x_i = "Sensor_" + str(i+1) + "_x"
        y_i = "Sensor_" + str(i+1) + "_y"
        data_array = [data[x_i].values, data[y_i].values]

        # Rotate the data
        rotated_data = rotate(data_array, angle)


        # Update the data with the rotated data
        data[x_i] = rotated_data[0]
        data[y_i] = rotated_data[1]

    return data

def remove_offset_xy(data):
    for i in range(num_sensors):
        x_i = "Sensor_" + str(i+1) + "_x"
        y_i = "Sensor_" + str(i+1) + "_y"
        data_x = data[x_i]
        data_y = data[y_i]
        data[x_i] = data_x - np.mean(data_x)
        data[y_i] = data_y - np.mean(data_y)
    return data

def process_data(filename):
    angle = 150
    # Read in the data from the file
    data = pd.read_csv(filename)
    # Remove the offset in the sensor data
    data = remove_offset_xy(data)
    # Rotate the data by degrees
    data = rotate_data(data, angle)
    # Convert the data from bit to gauss
    data = convert_to_gauss(data)
    return data

def convert_to_gauss(data):
    gauss_per_bit = 4 / 32768 # May need to subtract this by 1 to account for zero term
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            data.iloc[i,j] = data.iloc[i,j] * gauss_per_bit

    return data

