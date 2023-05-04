# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 11:40:27 2023

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
    datapath = "C:/Users/Clarissa/Documents/AirMSPI/Prescott/FIREX-AQ_8172019"
    outpath = "C:/Users/Clarissa/Documents/GitHub/GRASP-CSP/RetrievalExamples/FIREX1"
    #datapath = "C:/Users/ULTRASIP_1/Documents/Bakersfield707_Data/"
    #outpath = "C:/Users/ULTRASIP_1/Documents/GitHub/GRASP-CSP/RetrievalExamples/Bakersfield"

    # Change directory to the datapath
    os.chdir(datapath)

    # Set the length of one measurement sequence of step-and-stare observations
    # NOTE: This will typically be an odd number (9,7,5,...)
    num_step = 5
        
    # Set the index of the measurement sequence within the step-and-stare files
    # NOTE: This is 0 for the first sequence in the directory, 1 for the second group, etc.
    sequence_num = 0
    
    #Channel indices 
    num_int = 7 
    num_pol = 3
    
    #Define empty dictionaries 
    
    medians_dict = {}
    datastructure = {}

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
    
    for num_step in range(num_step):
        i = 0 + num_step
        print(num_step,i)
        
        #get data structures 
        inputName = sequence_files[num_step]
        f = h5py.File(inputName,'r')         
        
        data =  gd.getdata(f,num_step,datastructure)
        
        
        
          #find ROI using first file and 660 nm data point 
        if i == 0:
              img = data['660nm/0']['I']
              img = r.image_crop(img)
              roi_x, roi_y = r.choose_roi(img)
              medians_dict['Sun_distance'] = data['Sun_Distance'+ f"{num_step}"]
              medians_dict['E0'] = data['E0'+ f"{num_step}"]
              medians_dict['Elevation'] =  r.calculate_median(data['Elevation0'])[roi_x,roi_y]
              medians_dict['Lat'] =  r.calculate_median(data['Lat0'])[roi_x,roi_y]
              medians_dict['Long'] =  r.calculate_median(data['Long0'])[roi_x,roi_y]
              medians_dict['Date'] = date_str[0]
              medians_dict['Time'] = time_str[0]
              medians_dict['Target'] = target_str[0]
              medians_dict['ROI Coordinates'] = {   
                  'x': roi_x,
                  'y': roi_y
                  }

    for key in data.keys():
        if 'nm' in key:
            # Initialize a temporary dictionary to hold the median and std values
            temp_dict = {}
    
            # Loop over each subkey (i.e., 'I', 'Q', 'U', etc.)
            for subkey in data[key].keys():
                print(subkey)
                # Calculate the median and std of the values for this subkey
                median_val = r.calculate_median(data[key][subkey])[roi_x,roi_y]
                std_val = r.calculate_std(data[key][subkey])[roi_x,roi_y]
                    
                # Add the median and std values to the temporary dictionary
                temp_dict[subkey + '_med'] = median_val
                temp_dict[subkey + '_std'] = std_val
    
            # Add the temporary dictionary to the output dictionary, using the same key
            medians_dict[key] = temp_dict
        
    return outpath, data,medians_dict
        
### END MAIN FUNCTION
if __name__ == '__main__':
     outpath, data_product, medians  = main()
     
     # Open a file in binary mode and write the dictionary to it using pickle
     os.chdir(outpath)
     with open('FIREX1.pickle', 'wb') as f:
         pickle.dump(medians, f)
     