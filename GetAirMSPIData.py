"""
Created on Fri Apr 28 10:28:07 2023

@author: ULTRASIP_1
"""

import h5py
import ROI_functions as r
import numpy as np

def getdata(f,num_step,data):


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

        
    
        dataset_names = 'I','IPOL','Q_meridian','U_meridian','Q_scatter','U_scatter','View_azimuth','View_zenith','Sun_azimuth','Sun_zenith'

           # Loop over the groups and check if the dataset name exists
        for group in [group1, group2, group3, group4, group5, group6, group7]:
            wave = group.name.split("/")[3][0:5]
            #print(wave)
            data_key = f"{wave}/{num_step}"
            data[data_key] = {}
            for dataset_name in dataset_names:
                if dataset_name in group:
            # If the dataset name exists in the group, save the data under the same key as a subset labeled as dataset_name
                    data[data_key][dataset_name] = r.image_crop(group[dataset_name][()])
        data['E0'+f"{num_step}"] = f['/Channel_Information/Solar_irradiance_at_1_AU'][()]
        data['Sun_Distance'+f"{num_step}"] = f['/HDFEOS/ADDITIONAL/FILE_ATTRIBUTES/'].attrs['Sun distance']
        data['Elevation'+f"{num_step}"]= r.image_crop(f['/HDFEOS/GRIDS/Ancillary/Data Fields/Elevation/'][:])
        data['Lat'+f"{num_step}"] = r.image_crop(f['/HDFEOS/GRIDS/Ancillary/Data Fields/Latitude/'][:])
        data['Long'+f"{num_step}"] = r.image_crop(f['/HDFEOS/GRIDS/Ancillary/Data Fields/Longitude/'][:])

    return(data)


       

