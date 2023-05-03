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
    # datapath = "C:/Users/Clarissa/Documents/AirMSPI/Prescott/FIREX-AQ_8172019"
    # outpath = "C:/Users/Clarissa/Documents/GitHub/GRASP-CSP/RetreivalExamples"
    datapath = "C:/Users/ULTRASIP_1/Documents/Bakersfield707_Data/"
    outpath = "C:/Users/ULTRASIP_1/Documents/GitHub/GRASP-CSP/RetrievalExamples/Bakersfield"

    # Change directory to the datapath
    os.chdir(datapath)

    # Set the length of one measurement sequence of step-and-stare observations
    # NOTE: This will typically be an odd number (9,7,5,...)
    num_step = 1
        
    # Set the index of the measurement sequence within the step-and-stare files
    # NOTE: This is 0 for the first sequence in the directory, 1 for the second group, etc.
    sequence_num = 0
    
    #Channel indices 
    num_int = 7 
    num_pol = 3

# Get the list of files in the directory
    # NOTE: Python returns the files in a strange order, so they will need to be sorted by time
    #Search for files with the correct names
    search_str = '*TERRAIN*.hdf'
    file_list = np.array(glob.glob(search_str))
    dum_list = glob.glob(search_str)
    raw_list = np.array(dum_list)
    
    # Get the number of files    
    num_files = len(file_list)
    print(num_files)       
    # Check the number of files against the index to only read one measurement sequence
    #print("AirMSPI Files Found: ",num_files)
    sequence_files = file_list[(sequence_num*5):(sequence_num*5)+num_step]
    print(len(sequence_files))
    
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
            print('hi')
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
    
    for num_step in range(5):
        i = 0 + num_step
        print(num_step,i)
        
        #get data structures 
        inputName = sequence_files[num_step]
        f = h5py.File(inputName,'r')         
        
        data =  gd.getdata(f)
        
        medians_dict = {}
        
        #find ROI using first file and 660 nm data point 
        if i == 0:
            img = data['660_data']['I']
            img = r.image_crop(img)
            roi_x, roi_y = r.choose_roi(img)
            medians_dict['Sun_distance' + f"{num_step}"] = data['Sun_Distance']
            medians_dict['E0' + f"{num_step}"] = data['E0']
            medians_dict['Elevation'] =  r.calculate_median(data['Elevation'])[roi_x,roi_y]
            medians_dict['Lat'] =  r.calculate_median(data['Lat'])[roi_x,roi_y]
            medians_dict['Long'] =  r.calculate_median(data['Long'])[roi_x,roi_y]
            medians_dict['Date'] = date_str
            medians_dict['Time'] = time_str
            medians_dict['Target'] = target_str
            medians_dict['ROI Coordinates'] = {   
                'x': roi_x,
                'y': roi_y
                }

        
        print(data.keys())
        keys_to_exclude = ['Sun_Distance', 'E0','Elevation', 'Lat', 'Long']


        for group_name in data.keys():
            print(group_name)
            if group_name not in keys_to_exclude:
                for dataset_name in data[group_name].keys():
                # if dataset_name not in keys_to_exclude:
                    print(dataset_name)
                    #if isinstance(data[group_name][dataset_name], list):
                    dataset_median = r.calculate_median(data[group_name][dataset_name])
                    dataset_stdev = r.calculate_std(data[group_name][dataset_name])

                    medians_dict[f"{group_name}/{dataset_name}/{num_step}"] = {
                        'median': dataset_median[roi_x,roi_y],
                        'stdev': dataset_stdev[roi_x,roi_y]
                        }
               
        
    return outpath, medians_dict
        
### END MAIN FUNCTION
if __name__ == '__main__':
     outpath, data_products  = main()
     
     # Open a file in binary mode and write the dictionary to it using pickle
     os.chdir(outpath)
     with open('Bakersfield0707.pickle', 'wb') as f:
         pickle.dump(data_products, f)
     