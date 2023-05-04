# -*- coding: utf-8 -*-
"""
Created on Wed May  3 14:38:24 2023

@author: ULTRASIP_1
"""

#Import Packages#
import glob
import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
import time
import GetAirMSPIData as gd
import ROI_functions as r
import pickle


def main():
    #I. User defined parameters#
    #Directories: path to AirMSPI data (datapath),
    #path to output sdata files (outpath).
    #datapath = "C:/Users/Clarissa/Documents/AirMSPI/Prescott/FIREX-AQ_8172019"
    #outpath = "C:/Users/Clarissa/Documents/GitHub/GRASP-CSP/RetrievalExamples/FIREX2"
    datapath = "C:/Users/ULTRASIP_1/Documents/Bakersfield707_Data/"
    outpath = "C:/Users/ULTRASIP_1/Documents/GitHub/GRASP-CSP/RetrievalExamples/Bakersfield"

    # Change directory to the datapath
    os.chdir(datapath)

    # Set the length of one measurement sequence of step-and-stare observations
    # NOTE: This will typically be an odd number (9,7,5,...)
    num_step = 2
        
    # Set the index of the measurement sequence within the step-and-stare files
    # NOTE: This is 0 for the first sequence in the directory, 1 for the second group, etc.
    sequence_num = 0
    
    #Channel indices 
    num_int = 7 
    num_pol = 3
    
    medians_dict = {}

# Get the list of files in the directory
    # NOTE: Python returns the files in a strange order, so they will need to be sorted by time
    #Search for files with the correct names
    search_str = '*TERRAIN*.hdf'
    file_list = np.array(glob.glob(search_str))
    dum_list = glob.glob(search_str)
    raw_list = np.array(dum_list)
    
    # Get the number of files    
    num_files = len(file_list)
    #print(num_files)       
    # Check the number of files against the index to only read one measurement sequence
    #print("AirMSPI Files Found: ",num_files)
    sequence_files = file_list[(sequence_num*5):(sequence_num*5)+num_step]
    #print(len(sequence_files))
    
    # Loop through files within the sequence and sort by time (HHMMSS)
    # and extract date and target name
    #Filenaming strings 
    #Measurement time as an integer
    time_raw = np.zeros((num_files),dtype=int) 
        
    #Time, Date, and Target Name as a string
    time_str_raw = []  
    date_str_raw = []  
    target_str_raw = [] 

    #Start the for loop
    for loop in range(num_files):
            #print('hi')
    # Select appropriate file

            this_file = raw_list[loop]

    # Parse the filename to get information
        
            words = this_file.split('_')
            
            date_str_raw.append(words[4])
            time_str_raw.append(words[5])  # This will retain the "Z" designation
            target_str_raw.append(words[6])
            
            temp = words[5]
            hold = temp.split('Z')
            time_hhmmss = int(hold[0])
            time_raw[loop] = time_hhmmss

    # Convert data to numpy arrays

            date_str = np.array(date_str_raw)
            time_str = np.array(time_str_raw)
            target_str = np.array(target_str_raw)
    #print(date_str)
    datastructure = {}
    for num_step in range(num_step):
        print(num_step)
        
        #get data structures 
        inputName = sequence_files[num_step]
        f = h5py.File(inputName,'r')         
        
        data =  gd.getdata(f,num_step,datastructure)
        
    return data
### END MAIN FUNCTION
if __name__ == '__main__':
     data_products  = main()