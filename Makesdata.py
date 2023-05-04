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
    #picklepath = "C:/Users/Clarissa/Documents/GitHub/GRASP-CSP/RetrievalExamples/FIREX1"
    outpath = "C:/Users/ULTRASIP_1/Documents/ULTRASIP/AirMSPI_FIREXAQ/Retrievals/May423/FIREX1"
    os.chdir(picklepath)
    ref_plane = 'meridian'
    
    # open the pickle file for reading
    with open('FIREX1.pickle', 'rb') as f:
        # load the object from the pickle file
        data_dict = pickle.load(f)

# Change to the output directory
    os.chdir(outpath) 
    
# Generate the base output file name
    outfile_base = f'Rotfrom{ref_plane}'
    
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

    # for group_name in data_dict.keys():
    #     if 'nm/0' in group_name:
    #         out_str = out_str + ' ' + str(int(group_name[0:3])/1000)
            
    out_str = out_str +  str(0.355100000)
    out_str = out_str + ' ' + str(0.377200000)
    out_str = out_str + ' ' + str(0.443300000)
    out_str = out_str + ' ' + str(0.469100000)
    out_str = out_str + ' ' + str(0.553500000)
    out_str = out_str + ' ' + str(0.659133333)
    out_str = out_str + ' ' + str(0.863700000)
       

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
        if 'nm/0' in group_name:
            wave = group_name.split("/")[0]
            num = group_name.split('/')[1]
            out_str = out_str + ' ' + str(data_dict[f"{wave}/{num}"]['Sun_zenith_med'])
            print(data_dict[f"{wave}/{num}"]['Sun_zenith_med'])

            
    #view_zenith angles
    for group_name in data_dict.keys():
        if '355nm/4' in group_name:
            wave = group_name.split("/")[0]
            num = group_name.split('/')[1]
            print(num)
            for meas in range(int(num)+1):
                print(f"{wave}/{meas}")
                out_str = out_str + ' ' + str(data_dict[f"{wave}/{meas}"]['View_zenith_med'])
                print(data_dict[f"{wave}/{meas}"]['View_zenith_med'])
        if '380nm/4' in group_name:
          wave = group_name.split("/")[0]
          num = group_name.split('/')[1]
          print(num)
          for meas in range(int(num)+1):
              print(f"{wave}/{meas}")
              out_str = out_str + ' ' + str(data_dict[f"{wave}/{meas}"]['View_zenith_med'])
              print(data_dict[f"{wave}/{meas}"]['View_zenith_med'])
        if '445nm/4' in group_name:
         wave = group_name.split("/")[0]
         num = group_name.split('/')[1]
         print(num)
         for meas in range(int(num)+1):
             print(f"{wave}/{meas}")
             out_str = out_str + ' ' + str(data_dict[f"{wave}/{meas}"]['View_zenith_med'])
             print(data_dict[f"{wave}/{meas}"]['View_zenith_med'])
        if '470nm/4' in group_name:
            wave = group_name.split("/")[0]
            num = group_name.split('/')[1]
            print(num)
            for i in range(3):
                for meas in range(int(num)+1):
                    print(f"{wave}/{meas}")
                    out_str = out_str + ' ' + str(data_dict[f"{wave}/{meas}"]['View_zenith_med'])
                    print(data_dict[f"{wave}/{meas}"]['View_zenith_med'])
        if '555nm/4' in group_name:
            wave = group_name.split("/")[0]
            num = group_name.split('/')[1]
            print(num)
            for meas in range(int(num)+1):
                print(f"{wave}/{meas}")
                out_str = out_str + ' ' + str(data_dict[f"{wave}/{meas}"]['View_zenith_med'])
                print(data_dict[f"{wave}/{meas}"]['View_zenith_med'])
        if '660nm/4' in group_name:
            wave = group_name.split("/")[0]
            num = group_name.split('/')[1]
            print(num)
            for i in range(3):
                for meas in range(int(num)+1):
                    print(f"{wave}/{meas}")
                    out_str = out_str + ' ' + str(data_dict[f"{wave}/{meas}"]['View_zenith_med'])
                    print(data_dict[f"{wave}/{meas}"]['View_zenith_med'])
        if '865nm/4' in group_name:
            wave = group_name.split("/")[0]
            num = group_name.split('/')[1]
            print(num)
            for i in range(3):
                for meas in range(int(num)+1):
                    print(f"{wave}/{meas}")
                    out_str = out_str + ' ' + str(data_dict[f"{wave}/{meas}"]['View_zenith_med'])
                    print(data_dict[f"{wave}/{meas}"]['View_zenith_med'])
   
    #relative azimuth
    n=0
    for group_name in data_dict.keys():
        if '355nm/4' in group_name:
            wave = group_name.split("/")[0]
            num = group_name.split('/')[1]
            print(num)
            for meas in range(int(num)+1):
                num = group_name.split('/')[1]
                saz = data_dict[f"{wave}/{meas}"]['Sun_azimuth_med']
                vaz = data_dict[f"{wave}/{meas}"]["View_azimuth_med"]
                if saz >= 180: 
                    saz = saz - 180
                else:
                    saz = saz + 180
                # calculate the difference
                raz = saz - vaz
                if raz < 0:
                    raz = raz + 360     
                out_str = out_str + ' ' + str(raz)
                n=n+1
        if '380nm/4' in group_name:
          wave = group_name.split("/")[0]
          num = group_name.split('/')[1]
          print(num)
          for meas in range(int(num)+1):
              num = group_name.split('/')[1]
              saz = data_dict[f"{wave}/{meas}"]['Sun_azimuth_med']
              vaz = data_dict[f"{wave}/{meas}"]["View_azimuth_med"]
              if saz >= 180: 
                  saz = saz - 180
              else:
                  saz = saz + 180          
              # calculate the difference
              raz = saz - vaz
              if raz < 0:
                  raz = raz + 360     
              out_str = out_str + ' ' + str(raz)
              n=n+1
        if '445nm/4' in group_name:
         wave = group_name.split("/")[0]
         num = group_name.split('/')[1]
         print(num)
         for meas in range(int(num)+1):
             num = group_name.split('/')[1]
             saz = data_dict[f"{wave}/{meas}"]['Sun_azimuth_med']
             vaz = data_dict[f"{wave}/{meas}"]["View_azimuth_med"]
             if saz >= 180: 
                 saz = saz - 180
             else:
                saz = saz + 180         
             # calculate the difference
             raz = saz - vaz
             if raz < 0:
                 raz = raz + 360     
             out_str = out_str + ' ' + str(raz)
             n=n+1
        if '470nm/4' in group_name:
            wave = group_name.split("/")[0]
            num = group_name.split('/')[1]
            for i in range(3):
                print(i)
                for meas in range(int(num)+1):
                    num = group_name.split('/')[1]
                    saz = data_dict[f"{wave}/{meas}"]['Sun_azimuth_med']
                    vaz = data_dict[f"{wave}/{meas}"]["View_azimuth_med"]
                if saz >= 180: 
                    saz = saz - 180
                else:
                    saz = saz + 180                
                    # calculate the difference
                    raz = saz - vaz
                if raz < 0:
                    raz = raz + 360     
                out_str = out_str + ' ' + str(raz)
                n=n+1
        if '555nm/4' in group_name:
            wave = group_name.split("/")[0]
            num = group_name.split('/')[1]
            print(num)
            for meas in range(int(num)+1):
                num = group_name.split('/')[1]
                saz = data_dict[f"{wave}/{meas}"]['Sun_azimuth_med']
                vaz = data_dict[f"{wave}/{meas}"]["View_azimuth_med"]
                if saz >= 180: 
                    saz = saz - 180
                else:
                    saz = saz + 180
                # calculate the difference
                raz = saz - vaz
                if raz < 0:
                    raz = raz + 360     
                out_str = out_str + ' ' + str(raz)
                n=n+1
        if '660nm/4' in group_name:
            wave = group_name.split("/")[0]
            num = group_name.split('/')[1]
            print(num)
            for i in range(3):
                for meas in range(int(num)+1):
                    num = group_name.split('/')[1]
                    saz = data_dict[f"{wave}/{meas}"]['Sun_azimuth_med']
                    vaz = data_dict[f"{wave}/{meas}"]["View_azimuth_med"]
                    if saz >= 180: 
                        saz = saz - 180
                    else:
                        saz = saz + 180
                    # calculate the difference
                    raz = saz - vaz
                    if raz < 0:
                        raz = raz + 360     
                    out_str = out_str + ' ' + str(raz)
                    n=n+1
        if '865nm/4' in group_name:
            wave = group_name.split("/")[0]
            num = group_name.split('/')[1]
            for i in range(3):
                for meas in range(int(num)+1):
                    num = group_name.split('/')[1]
                    saz = data_dict[f"{wave}/{meas}"]['Sun_azimuth_med']
                    vaz = data_dict[f"{wave}/{meas}"]["View_azimuth_med"]
                    if saz >= 180: 
                        saz = saz - 180
                    else:
                        saz = saz + 180
                    # calculate the difference
                    raz = saz - vaz
                    print(raz)
                    if raz < 0:
                        raz = raz + 360     
                    out_str = out_str + ' ' + str(raz)
                    n=n+1
    print(n)


    
    #Measurements for each wavelength
    for key in data_dict.keys():
        if '355' in key:
            first_subkey = next(iter(data_dict[key]))
            I_med = data_dict[key][first_subkey]
            out_str = out_str + ' ' + str(I_med)
    for key in data_dict.keys():
        if '380' in key:
            first_subkey = next(iter(data_dict[key]))
            I_med = data_dict[key][first_subkey]
            out_str = out_str + ' ' + str(I_med)
            
    for key in data_dict.keys():
        if '445' in key:
            first_subkey = next(iter(data_dict[key]))
            I_med = data_dict[key][first_subkey]
            out_str = out_str + ' ' + str(I_med)
            
    for key in data_dict.keys():
        if '470' in key:
            first_subkey = next(iter(data_dict[key]))
            second_subkey = list(data_dict[key])[1]
            I_med = data_dict[key][first_subkey]
            out_str = out_str + ' ' + str(I_med)
            
    for key in data_dict.keys():
        if '470' in key:
            if 'meridian' in ref_plane:
                Q_med = data_dict[key]['Q_meridian_med']
            if 'scattering' in ref_plane: 
                Q_med = -data_dict[key]['Q_scatter_med']
            out_str = out_str + ' ' + str(Q_med)
            
    for key in data_dict.keys():
        if '470' in key:
            if 'meridian' in ref_plane:
                U_med = data_dict[key]['U_meridian_med']
            if 'scattering' in ref_plane: 
                U_med = -data_dict[key]['U_scatter_med']
            out_str = out_str + ' ' + str(U_med)
                
    for key in data_dict.keys():
        if '555' in key:
            first_subkey = next(iter(data_dict[key]))
            I_med = data_dict[key][first_subkey]
            out_str = out_str + ' ' + str(I_med)
    
    for key in data_dict.keys():
        if '660' in key:
            first_subkey = next(iter(data_dict[key]))
            second_subkey = list(data_dict[key])[1]
            I_med = data_dict[key][first_subkey]
            out_str = out_str + ' ' + str(I_med)
            
    for key in data_dict.keys():
        if '660' in key:
            if 'meridian' in ref_plane:
                Q_med = data_dict[key]['Q_meridian_med']
            if 'scattering' in ref_plane: 
                Q_med = -data_dict[key]['Q_scatter_med']
            out_str = out_str + ' ' + str(Q_med)
            
    for key in data_dict.keys():
        if '660' in key:
            if 'meridian' in ref_plane:
                U_med = data_dict[key]['U_meridian_med']
            if 'scattering' in ref_plane: 
                U_med = -data_dict[key]['U_scatter_med']
            out_str = out_str + ' ' + str(U_med)
                
    for key in data_dict.keys():
        if '865' in key:
            first_subkey = next(iter(data_dict[key]))
            second_subkey = list(data_dict[key])[1]
            I_med = data_dict[key][first_subkey]
            out_str = out_str + ' ' + str(I_med)
            
    for key in data_dict.keys():
        if '865' in key:
            if 'meridian' in ref_plane:
                Q_med = data_dict[key]['Q_meridian_med']
            if 'scattering' in ref_plane: 
                Q_med = -data_dict[key]['Q_scatter_med']
            out_str = out_str + ' ' + str(Q_med)
            
    for key in data_dict.keys():
        if '865' in key:
            if 'meridian' in ref_plane:
                U_med = data_dict[key]['U_meridian_med']
            if 'scattering' in ref_plane: 
                U_med = -data_dict[key]['U_scatter_med']
            out_str = out_str + ' ' + str(U_med)
        
## ADDITIONAL PARAMETERS
# NOTE: This is kludgy and GRASP seems to run without this being entirely correct

    out_str = out_str+'       0.00000000'  # Ground parameter (wave 1)
    out_str = out_str+'       0.00000000'  # Ground parameter (wave 2)
    out_str = out_str+'       0.00000000'  # Ground parameter (wave 3)
    out_str = out_str+'       0.00000000'  # Ground parameter (wave 4)
    out_str = out_str+'       0.00000000'  # Ground parameter (wave 5)
    out_str = out_str+'       0.00000000'  # Ground parameter (wave 6)
    out_str = out_str+'       0.00000000'  # Ground parameter (wave 7)
    out_str = out_str+'       0'  # Gas parameter (wave 1)
    out_str = out_str+'       0'  # Gas parameter (wave 2)
    out_str = out_str+'       0'  # Gas parameter (wave 3)
    out_str = out_str+'       0'  # Gas parameter (wave 4)
    out_str = out_str+'       0'  # Gas parameter (wave 5)
    out_str = out_str+'       0'  # Gas parameter (wave 6)
    out_str = out_str+'       0'  # Gas parameter (wave 7)
    out_str = out_str+'       0'  # Covariance matrix (wave 1)
    out_str = out_str+'       0'  # Covariance matrix (wave 2)
    out_str = out_str+'       0'  # Covariance matrix (wave 3)
    out_str = out_str+'       0'  # Covariance matrix (wave 4)
    out_str = out_str+'       0'  # Covariance matrix (wave 5)
    out_str = out_str+'       0'  # Covariance matrix (wave 6)
    out_str = out_str+'       0'  # Covariance matrix (wave 7)
    out_str = out_str+'       0'  # Vertical profile (wave 1)
    out_str = out_str+'       0'  # Vertical profile (wave 2)
    out_str = out_str+'       0'  # Vertical profile (wave 3)
    out_str = out_str+'       0'  # Vertical profile (wave 4)
    out_str = out_str+'       0'  # Vertical profile (wave 5)
    out_str = out_str+'       0'  # Vertical profile (wave 6)
    out_str = out_str+'       0'  # Vertical profile (wave 7)
    out_str = out_str+'       0'  # (Dummy) (wave 1)
    out_str = out_str+'       0'  # (Dummy) (wave 2)
    out_str = out_str+'       0'  # (Dummy) (wave 3)
    out_str = out_str+'       0'  # (Dummy) (wave 4)
    out_str = out_str+'       0'  # (Dummy) (wave 5)
    out_str = out_str+'       0'  # (Dummy) (wave 6)
    out_str = out_str+'       0'  # (Dummy) (wave 7)
    out_str = out_str+'       0'  # (Extra Dummy) (wave 1)
    out_str = out_str+'       0'  # (Extra Dummy) (wave 2)
    out_str = out_str+'       0'  # (Extra Dummy) (wave 3)
    out_str = out_str+'       0'  # (Extra Dummy) (wave 4)
    out_str = out_str+'       0'  # (Extra Dummy) (wave 5)
    out_str = out_str+'       0'  # (Extra Dummy) (wave 6)
    out_str = out_str+'       0'  # (Extra Dummy) (wave 7)
    out_str = out_str+'       0'  # (Extra Dummy) (wave 1)
    out_str = out_str+'       0'  # (Extra Dummy) (wave 2)
    out_str = out_str+'       0'  # (Extra Dummy) (wave 3)
    out_str = out_str+'       0'  # (Extra Dummy) (wave 4)
    out_str = out_str+'       0'  # (Extra Dummy) (wave 5)
    out_str = out_str+'       0'  # (Extra Dummy) (wave 6)
    out_str = out_str+'       0'  # (Extra Dummy) (wave 7)
                   
# Endline
       
    out_str = out_str+'\n'

# Write out the line
     
    outputFile.write(out_str)

# Close the output file

    outputFile.close()                     
            
        
    return out_str, data_dict
    
# ### END MAIN FUNCTION
### END MAIN FUNCTION
if __name__ == '__main__':
     outstr, data  = main()