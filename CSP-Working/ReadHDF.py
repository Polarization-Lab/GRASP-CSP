# -*- coding: utf-8 -*-
"""
Read in HDF File
"""

import h5py
import FileProcessing_functions as p
import numpy as np
import os
import glob

datapath = 'C:/Users/Clarissa/Documents/AirMSPI/Bakersfield707_Data/'
os.chdir(datapath)
#f = h5py.File('AirMSPI_ER2_GRP_TERRAIN_20160707_193456Z_CA-Bakersfield_589F_F01_V006.hdf','r') 
#f1 = h5py.File('AirMSPI_ER2_GRP_TERRAIN_20160707_193736Z_CA-Bakersfield_000N_F01_V006.hdf','r') 

search_str = '*TERRAIN*.hdf'
files = np.array(glob.glob(search_str))

loop = -1
all_data = {'355':{},
            '380':{},
            '445':{},
            '470':{},
            '555':{},
            '660':{},
            '865':{}
            }

for f in files: 
    with h5py.File(f, 'r') as f:
        loop = loop+1
        #Path to wavelength channel data
        hdfpaths = ['/HDFEOS/GRIDS/355nm_band/Data Fields/',
                    '/HDFEOS/GRIDS/380nm_band/Data Fields/',
                    '/HDFEOS/GRIDS/445nm_band/Data Fields/',
                    '/HDFEOS/GRIDS/470nm_band/Data Fields/',
                    '/HDFEOS/GRIDS/555nm_band/Data Fields/',
                    '/HDFEOS/GRIDS/660nm_band/Data Fields/',
                    '/HDFEOS/GRIDS/865nm_band/Data Fields/']


        dataset_meas = 'I','IPOL','Q_meridian','U_meridian','Q_scatter','U_scatter','View_azimuth','View_zenith','Sun_azimuth','Sun_zenith'
        for path in hdfpaths:
            for key in all_data.keys():
                for dataset in dataset_meas: 
                    if dataset in f[path].keys():
                        if dataset not in all_data[key].keys(): 
                            all_data[key][dataset] = { (dataset + f'{loop}') : p.image_crop(f[path][dataset][()])}
                        else: 
                            all_data[key][dataset].update({(dataset + f'{loop}') : p.image_crop(f[path][dataset][()])})
    all_data['E0'+f"{loop}"] = f['/Channel_Information/Solar_irradiance_at_1_AU'][()]
    all_data['Sun_Distance'+f"{loop}"] = f['/HDFEOS/ADDITIONAL/FILE_ATTRIBUTES/'].attrs['Sun distance']
    all_data['Elevation'+f"{loop}"]= p.image_crop(f['/HDFEOS/GRIDS/Ancillary/Data Fields/Elevation/'][:])
    all_data['Lat'+f"{loop}"] = p.image_crop(f['/HDFEOS/GRIDS/Ancillary/Data Fields/Latitude/'][:])
    all_data['Long'+f"{loop}"] = p.image_crop(f['/HDFEOS/GRIDS/Ancillary/Data Fields/Longitude/'][:])
