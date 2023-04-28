# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 11:33:49 2023

INPUT: AirMSPI .hdf files
OUTPUT:AirMSPI data products for sdata input

This is a Python 3.9.13 code to read AirMSPI L1B2 data and 
format the data to perform aerosol retrievals using the 
Generalized Retrieval of Atmosphere and Surface Properties

Code Sections: 
Data products
    a. Load in Data
    b. Set ROI 
    c. Sort and Extract Data
    d. Take Medians 

INPUTS: 
    datapath: directory to .hdf files
    num_step: number of step and stare files in sequence
    sequence_num: Set the index of the sequence of step-and-stare files
                    NOTE: This is 0 for the first group in the directory, 1 for the second group, etc.
    num_rad: number of radiometric channels
    num_pol: number of polarimetric channels

OUTPUTS: 

"""
#_______________Import Packages_________________#
import glob
import h5py
import numpy as np
import os
import time

def main(datapath,num_step,sequence_num,num_int,num_pol,min_x,min_y,max_x,max_y,roi_x1,roi_x2,roi_y1,roi_y2):
    

    #Array Definitions
    wavelens = np.zeros((num_step,num_int))
    i = np.zeros((num_step,num_int))      
    view_zen = np.zeros((num_step,num_int))
    view_az = np.zeros((num_step,num_int))    
    ipol = np.zeros((num_step,num_pol))
    qm = np.zeros((num_step,num_pol))
    um = np.zeros((num_step,num_pol))
    
    sun_zen = np.zeros((num_step,num_int))
    sun_az = np.zeros((num_step,num_int))
    E0_values = np.zeros((num_step,num_int))

    esd = 0.0  # Earth-Sun distance (only need one)

    #Center point Arrays
    center_wave = np.zeros(num_int)  # Center wavelengths  
    center_pol = np.zeros(num_pol)  # Center wavelengths (polarized only)
    
    # Calculate the middle of the sequence
    mid_step = int(num_step/2)  
        
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
    sequence_files = file_list[sequence_num*5:sequence_num*5+num_step]
    
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
    
    for num_step in range(num_step):
        #print(num_step)
        inputName = sequence_files[num_step]
        f = h5py.File(inputName,'r')   
            
        channel355 = '/HDFEOS/GRIDS/355nm_band/Data Fields/';
        i_355 = np.median(np.flipud(f[channel355+'I/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])        
        vaz_355 = np.median(np.flipud(f[channel355+'View_azimuth/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])        
        vza_355 = np.median(np.flipud(f[channel355+'View_zenith/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])        
        saz_355 = np.median(np.flipud(f[channel355+'Sun_azimuth/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])        
        sza_355 = np.median(np.flipud(f[channel355+'Sun_zenith/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
            
        channel380 = '/HDFEOS/GRIDS/380nm_band/Data Fields/';
        i_380 = np.median(np.flipud(f[channel380+'I/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])          
        vaz_380 = np.median(np.flipud(f[channel380+'View_azimuth/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])        
        vza_380 = np.median(np.flipud(f[channel380+'View_zenith/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2]) 
        saz_380 = np.median(np.flipud(f[channel380+'Sun_azimuth/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])        
        sza_380 = np.median(np.flipud(f[channel380+'Sun_zenith/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
            
        channel445 = '/HDFEOS/GRIDS/445nm_band/Data Fields/';
        i_445 = np.median(np.flipud(f[channel445+'I/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
        vaz_445 = np.median(np.flipud(f[channel445+'View_azimuth/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])        
        vza_445 = np.median(np.flipud(f[channel445+'View_zenith/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2]) 
        saz_445 = np.median(np.flipud(f[channel445+'Sun_azimuth/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])        
        sza_445 = np.median(np.flipud(f[channel445+'Sun_zenith/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
            
        channel470 = '/HDFEOS/GRIDS/470nm_band/Data Fields/';
        i_470 = np.median(np.flipud(f[channel470+'I/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
        ipol_470 = np.median(np.flipud(f[channel470+'IPOL/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
        qm_470 = np.median(np.flipud(f[channel470+'Q_meridian/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
        um_470 = np.median(np.flipud(f[channel470+'U_meridian/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
        dolp_470 = np.median(np.flipud(f[channel470+'DOLP/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
            
        vaz_470 = np.median(np.flipud(f[channel470+'View_azimuth/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])        
        vza_470 = np.median(np.flipud(f[channel470+'View_zenith/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2]) 
        saz_470 = np.median(np.flipud(f[channel470+'Sun_azimuth/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])        
        sza_470 = np.median(np.flipud(f[channel470+'Sun_zenith/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
            
        channel555 = '/HDFEOS/GRIDS/555nm_band/Data Fields/';
        i_555 = np.median(np.flipud(f[channel555+'I/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
        vaz_555 = np.median(np.flipud(f[channel555+'View_azimuth/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])        
        vza_555 = np.median(np.flipud(f[channel555+'View_zenith/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2]) 
        saz_555 = np.median(np.flipud(f[channel555+'Sun_azimuth/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])        
        sza_555 = np.median(np.flipud(f[channel555+'Sun_zenith/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
            
        channel660 = '/HDFEOS/GRIDS/660nm_band/Data Fields/';
        i_660 = np.median(np.flipud(f[channel660+'I/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
        ipol_660 = np.median(np.flipud(f[channel660+'IPOL/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
        qm_660 = np.median(np.flipud(f[channel660+'Q_meridian/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
        um_660 = np.median(np.flipud(f[channel660+'U_meridian/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
        dolp_660 = np.median(np.flipud(f[channel660+'DOLP/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
            
        vaz_660 = np.median(np.flipud(f[channel660+'View_azimuth/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])        
        vza_660 = np.median(np.flipud(f[channel660+'View_zenith/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2]) 
        saz_660 = np.median(np.flipud(f[channel660+'Sun_azimuth/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])        
        sza_660 = np.median(np.flipud(f[channel660+'Sun_zenith/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
            
            
        channel865 = '/HDFEOS/GRIDS/865nm_band/Data Fields/';
        i_865 = np.median(np.flipud(f[channel865+'I/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
        ipol_865 = np.median(np.flipud(f[channel865+'IPOL/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
        qm_865 = np.median(np.flipud(f[channel865+'Q_meridian/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
        um_865 = np.median(np.flipud(f[channel865+'U_meridian/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
        dolp_865 = np.median(np.flipud(f[channel865+'DOLP/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
            
        vaz_865 = np.median(np.flipud(f[channel865+'View_azimuth/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])        
        vza_865 = np.median(np.flipud(f[channel865+'View_zenith/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2]) 
        saz_865 = np.median(np.flipud(f[channel865+'Sun_azimuth/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])        
        sza_865 = np.median(np.flipud(f[channel865+'Sun_zenith/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])
            
        # Get the Earth-Sun distance from the file attributes from the first file
        if(esd == 0.0):
            #print("GETTING EARTH-SUN DISTANCE")
            esd = f['/HDFEOS/ADDITIONAL/FILE_ATTRIBUTES/'].attrs['Sun distance']
                
            # Get the actual center wavelengths and E0 values
            center_raw = f['/Channel_Information/Center_wavelength/'][:]   
            E0_wave = f['/Channel_Information/Solar_irradiance_at_1_AU/'][:]
                
            # Get the actual center wavelengths and E0 values
            center_raw = f['/Channel_Information/Center_wavelength/'][:]       
            E0_wave = f['/Channel_Information/Solar_irradiance_at_1_AU/'][:]
            
            # Calculate the effective center wavelengths by appropriate averaging
            # NOTE: Essentially, for the radiometric only bands, the center wavelength is given in the
            #       file. For polarized bands, we average the three available bands.
                
            center_wave[0] = center_raw[0]  # 355 nm
            center_wave[1] = center_raw[1]  # 380 nm
            center_wave[2] = center_raw[2]  # 445 nm          
            center_wave[3] = (center_raw[3]+center_raw[4]+center_raw[5])/3.0 # 470 nm
            center_wave[4] = center_raw[6]  # 555 nm       
            center_wave[5] = (center_raw[7]+center_raw[8]+center_raw[9])/3.0 # 660 nm
            center_wave[6] = (center_raw[10]+center_raw[11]+center_raw[12])/3.0 # 865 nm
                
                
            center_pol[0] = center_wave[3]
            center_pol[1] = center_wave[5]
            center_pol[2] = center_wave[6]
                
        # Calculate the effective E0 values by appropriate averaging
        # NOTE: Essentially, for radiomentric only bands, the E0 is given in the
        #       file. For polarized bands, we average the E0's from the three available bands.
                
            E0_355 = E0_wave[0]  # 355 nm
            E0_380 = E0_wave[1]  # 380 nm
            E0_445 = E0_wave[2]  # 440 nm
            E0_470 = (E0_wave[3]+E0_wave[4]+E0_wave[5])/3.0 # 470 nm        
            E0_555 = E0_wave[6]  # 555 nm        
            E0_660 = (E0_wave[7]+E0_wave[8]+E0_wave[9])/3.0 # 660 nm
            E0_865 = (E0_wave[10]+E0_wave[11]+E0_wave[12])/3.0 # 865 nm       
                
            # Get the navigation information if this is the center acquisition
        if(num_step == mid_step): #latitude and longitude chosen from nadir of step and stare
            evel_coord = np.median(np.flipud(f['/HDFEOS/GRIDS/Ancillary/Data Fields/Elevation/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])   
            lat_coord = np.median(np.flipud(f['/HDFEOS/GRIDS/Ancillary/Data Fields/Elevation/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])   
            long_coord = np.median(np.flipud(f['/HDFEOS/GRIDS/Ancillary/Data Fields/Longitude/'][:][min_y:max_y,min_x:max_x])[roi_x1:roi_x2,roi_y1:roi_y2])   

            #____________________________STORE THE DATA____________________________#
        
        
        intensity = np.array([i_355,i_380,i_445,i_470,i_555,i_660,i_865])
        E0s = np.array([E0_355,E0_380,E0_445,E0_470,E0_555,E0_660,E0_865])
        ipols = np.array([ipol_470,ipol_660,ipol_865])
        qms = np.array([qm_470,qm_660,qm_865])
        ums = np.array([um_470,um_660,um_865])
        dolpms = np.array([dolp_470,dolp_660,dolp_865])
        
        
        vza = np.array([vza_355,vza_380,vza_445,vza_470,vza_555,vza_660,vza_865])
        vaz = np.array([vaz_355,vaz_380,vaz_445,vaz_470,vaz_555,vaz_660,vaz_865])
        
        sza = np.array([sza_355,sza_380,sza_445,sza_470,sza_555,sza_660,sza_865])
        saz = np.array([saz_355,saz_380,saz_445,saz_470,saz_555,saz_660,saz_865])
        
        for idx in range(num_int):        
            i[num_step,idx] = intensity[idx]
            view_zen[num_step,idx] = vza[idx] 
            view_az[num_step,idx] = vaz[idx] 
            sun_az[num_step,idx] = saz[idx] 
            sun_zen[num_step,idx] = sza[idx] 
            E0_values[num_step,idx] = E0s[idx]
        
        for indx in range(num_pol):
            ipol[num_step,indx] = ipols[indx]
            qm[num_step,indx] = qms[indx]
            um[num_step,indx] = ums[indx]

        f.close()
    print('Done reading files')
    return date_str,time_str,target_str,esd,E0_values,evel_coord,lat_coord,long_coord,i[:],view_zen[:],view_az[:],sun_zen[:],sun_az[:],ipol[:],qm[:],um[:]

### END MAIN FUNCTION