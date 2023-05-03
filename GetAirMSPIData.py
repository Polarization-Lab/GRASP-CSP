# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 10:28:07 2023

@author: ULTRASIP_1
"""

import h5py
import ROI_functions as r

def getdata(f):


    channel355 = '/HDFEOS/GRIDS/355nm_band/Data Fields/';
    channel380 = '/HDFEOS/GRIDS/380nm_band/Data Fields/';
    channel445 = '/HDFEOS/GRIDS/445nm_band/Data Fields/';
    channel470 = '/HDFEOS/GRIDS/470nm_band/Data Fields/';
    channel555 = '/HDFEOS/GRIDS/555nm_band/Data Fields/';
    channel660 = '/HDFEOS/GRIDS/660nm_band/Data Fields/';
    channel865 = '/HDFEOS/GRIDS/865nm_band/Data Fields/';


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
        group8 = f['/HDFEOS/ADDITIONAL/FILE_ATTRIBUTES/']
        group9 = f['/Channel_Information/']
        
    
        # Create a structure to store the data
        data_structure = {
            '355_data': {},
            '380_data': {},
            '445_data': {},
            '470_data': {},
            '555_data': {},
            '660_data': {},
            '865_data': {},
            'E0':{}
            }
    
        dataset_name = 'I','IPOL','Q_meridian','U_meridian','Q_scatter','U_scatter','View_azimuth','View_zenith','Sun_azimuth','Sun_zenith',  'Solar_irradiance_at_1_AU'

        # Read the data from each group and store it in the structure
        for dataset_name in dataset_name:
            if dataset_name in group1: 
                data_structure['355_data'][dataset_name] = r.image_crop(group1[dataset_name][()])        
            if dataset_name in group2:
                data_structure['380_data'][dataset_name] = r.image_crop(group2[dataset_name][()])
            if dataset_name in group3:
                data_structure['445_data'][dataset_name] = r.image_crop(group3[dataset_name][()])
            if dataset_name in group4:
                data_structure['470_data'][dataset_name] = r.image_crop(group4[dataset_name][()])
            if dataset_name in group5:
                data_structure['555_data'][dataset_name] = r.image_crop(group5[dataset_name][()])
            if dataset_name in group6:
                data_structure['660_data'][dataset_name] = r.image_crop(group6[dataset_name][()])
            if dataset_name in group7:
                data_structure['865_data'][dataset_name] = r.image_crop(group7[dataset_name][()])  
            if dataset_name in group9:
                data_structure['E0'][dataset_name] = group9[dataset_name][()]
        #print('made it here')
        data_structure['Sun_Distance'] = f['/HDFEOS/ADDITIONAL/FILE_ATTRIBUTES/'].attrs['Sun distance']
        data_structure['Elevation']= r.image_crop(f['/HDFEOS/GRIDS/Ancillary/Data Fields/Elevation/'][:])
        data_structure['Lat'] = r.image_crop(f['/HDFEOS/GRIDS/Ancillary/Data Fields/Latitude/'][:])
        data_structure['Long'] = r.image_crop(f['/HDFEOS/GRIDS/Ancillary/Data Fields/Longitude/'][:])

        return(data_structure)


       

