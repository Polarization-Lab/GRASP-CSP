# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 10:28:07 2023

@author: ULTRASIP_1
"""
import glob
import h5py
import numpy as np
import os


sequence_num = 0
num_step = 5

datapath = "C:/Users/ULTRASIP_1/Documents/Prescott817_Data/"

# Change directory to the datapath
os.chdir(datapath)

# Get the list of files in the directory
# NOTE: Python returns the files in a strange order, so they will need to be sorted by time
#Search for files with the correct names
search_str = '*TERRAIN*.hdf'
file_list = np.array(glob.glob(search_str))
dum_list = glob.glob(search_str)
raw_list = np.array(dum_list)

# Get the number of files    
num_files = len(file_list)
        
# Check the number of files against the index to only read one measurement sequence
#print("AirMSPI Files Found: ",num_files)
sequence_files = file_list[(sequence_num*5):(sequence_num*5)+num_step]

channel355 = '/HDFEOS/GRIDS/355nm_band/Data Fields/';
channel380 = '/HDFEOS/GRIDS/380nm_band/Data Fields/';
channel445 = '/HDFEOS/GRIDS/445nm_band/Data Fields/';
channel470 = '/HDFEOS/GRIDS/470nm_band/Data Fields/';
channel555 = '/HDFEOS/GRIDS/555nm_band/Data Fields/';
channel660 = '/HDFEOS/GRIDS/660nm_band/Data Fields/';
channel865 = '/HDFEOS/GRIDS/865nm_band/Data Fields/';



inputName = sequence_files[num_step-1]
f = h5py.File(inputName,'r')  

# Open the HDF file
with f as f:
    # Get a reference to the group containing the data you want to read
    group1 = f[channel355]
    group2 = f[channel380]
    group3 = f[channel445]
    group4 = f[channel470]
    group5 = f[channel555]
    group6 = f[channel660]
    group7 = f[channel865]

    
    # Create a structure to store the data
    data_structure = {
        '355_data': {},
        '380_data': {},
        '445_data': {},
        '470_data': {},
        '555_data': {},
        '660_data': {},
        '865_data': {}
    }
    
    dataset_name = 'I','IPOL','Q_meridian','U_meridian','Q_scatter','U_scatter','View_azimuth','View_zenith','Sun_azimuth','Sun_zenith'

    # Read the data from each group and store it in the structure
    for dataset_name in dataset_name:
        if dataset_name in group1: 
            data_structure['355_data'][dataset_name] = group1[dataset_name][()]         
        if dataset_name in group2:
            data_structure['380_data'][dataset_name] = group2[dataset_name][()]
        if dataset_name in group3:
            data_structure['445_data'][dataset_name] = group3[dataset_name][()]
        if dataset_name in group4:
            data_structure['470_data'][dataset_name] = group4[dataset_name][()]
        if dataset_name in group5:
            data_structure['555_data'][dataset_name] = group5[dataset_name][()]
        if dataset_name in group6:
            data_structure['660_data'][dataset_name] = group6[dataset_name][()]
        if dataset_name in group7:
            data_structure['865_data'][dataset_name] = group7[dataset_name][()]



       

