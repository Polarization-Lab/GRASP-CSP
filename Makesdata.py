# -*- coding: utf-8 -*-
"""
Created on Wed May  3 09:55:12 2023

@author: ULTRASIP_1
"""

#Import Packages#
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle

def main(): 
    
    picklepath = "C:/Users/ULTRASIP_1/Documents/GitHub/GRASP-CSP/RetrievalExamples/FIREX1"   
    outpath = picklepath
    os.chdir(picklepath)
    ref_plane = 'meridian'
    
    # open the pickle file for reading
    with open('FIREX1.pickle', 'rb') as f:
        # load the object from the pickle file
        data_dict = pickle.load(f)

# Change to the output directory
    os.chdir(outpath) 
    
# Generate the base output file name
    outfile_base = 'RotfromScat'
    
# Generate an output file name

    outfile = outfile_base+".sdat"
        
    print()
    print("Saving: "+outfile)
    
    outputFile = open(outfile, 'w')

# Get the software version number to help track issues
    hold = os.path.basename(__file__)
    words = hold.split('_')
    temp = words[len(words)-1]  # Choose the last element
    hold = temp.split('.')
    vers = hold[0]
    
# Write the sdat header information

    out_str = 'SDATA version 2.0\n'
    outputFile.write(out_str)
    out_str = '  1   1   1  : NX NY NT\n'
    outputFile.write(out_str)
    out_str = '\n'
    outputFile.write(out_str)

# Parse the date string into the correct format

    sdat_date = data_dict['Date'][:]
    print(sdat_date)
        
# Parse the time string into the correct format

    sdat_time =  data_dict['Time'][:]
    print(sdat_time)
        
# Write out the data header line

    out_str = '  1   '+sdat_date+'T'+sdat_time
    out_str = out_str+'       70000.00   0   1   : NPIXELS  TIMESTAMP  HEIGHT_OBS(m)  NSURF  IFGAS    1\n'
    outputFile.write(out_str)
    
# Generate content for sdat (single line)

    out_str = '           1'  # x-coordinate (ix)
    out_str = out_str+'           1'  # y-coordinate (iy)
    out_str = out_str+'           1'  # Cloud Flag (0=cloud, 1=clear)
    out_str = out_str+'           1'  # Pixel column in grid (icol)
    out_str = out_str+'           1'  # Pixel line in grid (row)

    out_str = out_str+'{:19.8f}'.format(data_dict['Long'])  # Longitude
    out_str = out_str+'{:18.8f}'.format(data_dict['Lat'])  # Latitude
    out_str = out_str+'{:17.8f}'.format(data_dict['Elevation']) # Elevation

    out_str = out_str+'      100.000000'  # Percent of land
    out_str = out_str+'{:16d}'.format(7)  # Number of wavelengths (nwl)
    
  ## SET UP THE WAVELENGTH AND MEASUREMENT INFORMATION
        
# Loop through wavelengths

    for group_name in data_dict.keys():
        if '_data/I/' in group_name:
            out_str = out_str + ' ' + str(int(group_name[0:3])/1000)
       

# for loop in range(num_intensity):
    out_str = out_str+'{:12d}'.format(1)
    out_str = out_str+'{:12d}'.format(1) # 1 measurement per wavelength
    out_str = out_str+'{:12d}'.format(1)
    out_str = out_str+'{:12d}'.format(3)
    out_str = out_str+'{:12d}'.format(1)
    out_str = out_str+'{:12d}'.format(3)
    out_str = out_str+'{:12d}'.format(3)

# Loop over the measurement types per wavelength
# NOTE: Values can be found in the GRASP documentation in Table 4.5
#       41 = Normalized radiance (I = rad*pi/E0) - GRASP calls normalized (reduced) radiance

    out_str = out_str+'{:12d}'.format(41)
    out_str = out_str+'{:12d}'.format(41)
    out_str = out_str+'{:12d}'.format(41)
    out_str = out_str+'{:12d}'.format(41)
    out_str = out_str+'{:12d}'.format(42)
    out_str = out_str+'{:12d}'.format(43)
    out_str = out_str+'{:12d}'.format(41)
    out_str = out_str+'{:12d}'.format(41)
    out_str = out_str+'{:12d}'.format(42)
    out_str = out_str+'{:12d}'.format(43)
    out_str = out_str+'{:12d}'.format(41)
    out_str = out_str+'{:12d}'.format(42)
    out_str = out_str+'{:12d}'.format(43)
    
    #Number of measurements per measurement type - number of images in sequence
    num_step = 5

    out_str = out_str+'{:12d}'.format(num_step)
    out_str = out_str+'{:12d}'.format(num_step)
    out_str = out_str+'{:12d}'.format(num_step)
    out_str = out_str+'{:12d}'.format(num_step)
    out_str = out_str+'{:12d}'.format(num_step)
    out_str = out_str+'{:12d}'.format(num_step)
    out_str = out_str+'{:12d}'.format(num_step)
    out_str = out_str+'{:12d}'.format(num_step)
    out_str = out_str+'{:12d}'.format(num_step)
    out_str = out_str+'{:12d}'.format(num_step)
    out_str = out_str+'{:12d}'.format(num_step)
    out_str = out_str+'{:12d}'.format(num_step)
    out_str = out_str+'{:12d}'.format(num_step)
    
    #sun_zenith angles
    for group_name in data_dict.keys():
        if 'Sun_zenith/' in group_name:
            out_str = out_str + ' ' + str(data_dict[group_name]['median'])
            
    #view_zenith angles
    for group_name in data_dict.keys():
        if 'View_zenith/' in group_name:
            out_str = out_str + ' ' + str(data_dict[group_name]['median'])
    
    #relative azimuth
    for group_name in data_dict.keys():
        # check if the key contains "Sun_azimuth"
        if "/Sun_azimuth/0" in group_name:
            # get the corresponding value for the key
            saz = data_dict[group_name]['median']
            # extract the number from the key string
            wave = group_name.split("/")[0]
            num = 0
            print(wave,num)
            # construct the corresponding view azimuth key
            vaz_gname = f"{wave}/View_azimuth/{num}"
            # get the corresponding view azimuth value
            vaz = data_dict[vaz_gname]['median']
            # calculate the difference
            raz = saz - vaz
            if raz < 0:
                raz = raz + 360
                
            out_str = out_str + ' ' + str(raz)
    
    #Measurements for each wavelength
    for group_name in data_dict.keys():
        if "355_data" in group_name: 
            print(group_name)
            
        
        
    return out_str
    
# ### END MAIN FUNCTION
### END MAIN FUNCTION
if __name__ == '__main__':
     outstr  = main()