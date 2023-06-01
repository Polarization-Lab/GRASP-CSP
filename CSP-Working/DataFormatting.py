# -*- coding: utf-8 -*-
"""
DataFormatting.py 
INPUT: AirMSPI .hdf files
OUTPUT: SDATA structured AirMSPI data products

This is a Python 3.9.13 code to read AirMSPI L1B2 data and 
format the data to perform aerosol retrievals using the 
Generalized Retrieval of Atmosphere and Surface Properties

Code Sections: 
I. User defined parameters
    a. Directories 
    b. Bounding box
    c. Region of interest
1. Data Curation
    a. Read in data via ReadAirMSPIData.py function
        a.i. Sort and Extract Data
        a.ii. Take Medians 
        a.iii. Return values for further processing
2. Geometry Reconciliation 
    a. Put AirMSPI measurements into GRASP geometry 
    b. Normalize radiances
3. Structure the data products according to the GRASP SDATA format 

More info on the GRASP geometry and sdata format can be found at grasp-open.com
and more info on this algoritm can be found in DeLeon et al. (202X)

Creation Date: 2022-08-05
Last Modified: 2023-03-29

by Michael J. Garay and Clarissa M. DeLeon
(Michael.J.Garay@jpl.nasa.gov, cdeleon@arizona.edu)
"""

#Import Packages#
import glob
import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
import time
from ReadAirMSPIData import main as read

#I. User defined parameters#
#Directories: path to AirMSPI data (datapath),
#path to output sdata files (outpath).
# datapath = "C:/Users/Clarissa/Documents/AirMSPI/Prescott/FIREX-AQ_8172019"
# outpath = "C:/Users/Clarissa/Documents/GitHub/GRASP-CSP/RetreivalExamples"
datapath = "C:/Users/ULTRASIP_1/Documents/Bakersfield707_Data/"
outpath = "C:/Users/ULTRASIP_1/Documents/GitHub/GRASP-CSP/RetrievalExamples/Bakersfield"


# Set the length of one measurement sequence of step-and-stare observations
# NOTE: This will typically be an odd number (9,7,5,...)
num_step = 5
    
# Set the index of the measurement sequence within the step-and-stare files
# NOTE: This is 0 for the first sequence in the directory, 1 for the second group, etc.
sequence_num = 0

#Channel indices 
num_int = 7 
num_pol = 3

#Set the bounding box dimensions that will correct for parallax 
# Set bounds for the image (USER INPUT)
#FIREX
# min_x = 1900
# max_x = 2200
# min_y = 1900
# max_y = 2200

# #Bakersfield
min_x = 1200
max_x = 1900
min_y = 1200
max_y = 1900


            
# Set bounds for ROI (USER INPUT)
# Note: These coordinates are RELATIVE to the overall bounding box set above
#FIREX
# roi_x1 = 120
# roi_x2 = 125
# roi_y1 = 105
# roi_y2 = 110
    
#Bakserfield
roi_x1 = 485
roi_x2 = 490
roi_y1 = 485
roi_y2 = 490

#Start the main code#
def main():  # Main code

# Angle Arrays
# ALL ANGLES IN RADIANS
    scat_median = np.zeros((num_step,num_int))  # Scattering angle
    vza_median = np.zeros((num_step,num_int))  # View zenith angle
    raz_median = np.zeros((num_step,num_int))  # Relative azimuth angle
    sza_median = np.zeros(num_step)  # Solar zenith angle (one per stare)

#Measurement Arrays   
    i_median = np.zeros((num_step,num_int))  # Intensity
    i_in_polar_median = np.zeros((num_step,num_pol))  # I in polarized bands
    q_median = np.zeros((num_step,num_pol))  # Q
    u_median = np.zeros((num_step,num_pol))  # U
    ipol_median = np.zeros((num_step,num_pol))  # Ipol
    dolp_median = np.zeros((num_step,num_pol))  # DoLP

#Section 1. Data Curation
#Variable Definitions
    """
    esd = earth sun distance
    E0 = solar irradiance
    elv = elevation
    lat/long = lattitude, longitude
    i = radiometric radiance
    view_zen/az = view zenith angle, view azimuth angle
    sun_zen/az = sun zenith angle, sun azimuth angle
    ipol = total polarized radiance
    qm = H/V polarized radiance reported from AirMSPI meridian plane
    um = 45/135 polarized radiance reported from AirMSPI meridian plane
    """
    date,time,target,esd,E0,elev,lat,long,i,view_zen,view_az,sun_zen,sun_az,ipol,qm,um=read(datapath,num_step,sequence_num,num_int,num_pol,min_x,min_y,max_x,max_y,roi_x1,roi_x2,roi_y1,roi_y2)
    print("view",view_az)
    print("sun",sun_az)
#Section 2. Polarimetric Coodinate System Reconciliation
#Per Equation (X) make stokes inputs [Q_i,U_i] for each wavelength
    for step in range(num_step):
        #470
        stokesin4 = np.array([[qm[step,0]], [um[step,0]]]) #Meridian plane      
        #660
        stokesin6 = np.array([[qm[step,1]], [um[step,1]]]) #Meridian
        #865
        stokesin8 = np.array([[qm[step,2]], [um[step,2]]]) #Meridian
        
        #Ug,m = -Uin
        qg_470 = stokesin4[0,0]
        ug_470 = -stokesin4[1,0]
        
        qg_660 = stokesin6[0,0]
        ug_660 = -stokesin6[1,0]
        
        qg_865 = stokesin8[0,0]
        ug_865 = -stokesin8[1,0]
        
        
        eqr_i_355 = np.pi*i[step,0]*esd**2/E0[step,0]  
        eqr_i_380 = np.pi*i[step,1]*esd**2/E0[step,1]  
        eqr_i_445 = np.pi*i[step,2]*esd**2/E0[step,2]  

        eqr_i_470 = np.pi*i[step,3]*esd**2/E0[step,3]  
        eqr_qg_470 = np.pi*qg_470*esd**2/E0[step,3]  
        eqr_ug_470 = np.pi*ug_470*esd**2/E0[step,3]  

        eqr_i_555 = np.pi*i[step,4]*esd**2/E0[step,4]  

        eqr_i_660 = np.pi*i[step,5]*esd**2/E0[step,5]  
        eqr_qg_660 = np.pi*qg_660*esd**2/E0[step,5]  
        eqr_ug_660 = np.pi*ug_660*esd**2/E0[step,5]  

        eqr_i_865 = np.pi*i[step,6]*esd**2/E0[step,6]  
        eqr_qg_865 = np.pi*qg_865*esd**2/E0[step,6]  
        eqr_ug_865 = np.pi*ug_865*esd**2/E0[step,6]  
        
#____________________________STORE THE DATA____________________________#

        loop = step        
        i_median[loop,0] = eqr_i_355
        i_median[loop,1] = eqr_i_380
        i_median[loop,2] = eqr_i_445
        i_median[loop,3] = eqr_i_470
        i_median[loop,4] = eqr_i_555
        i_median[loop,5] = eqr_i_660
        i_median[loop,6] = eqr_i_865
                
        
        # vza_median[loop,0] = view_zen[]
        # vza_median[loop,1] = vza_380
        # vza_median[loop,2] = vza_445
        # vza_median[loop,3] = vza_470
        # vza_median[loop,4] = vza_555
        # vza_median[loop,5] = vza_660
        # vza_median[loop,6] = vza_865


        # raz_median[loop,0] = raz_355
        # raz_median[loop,1] = raz_380
        # raz_median[loop,2] = raz_445
        # raz_median[loop,3] = raz_470
        # raz_median[loop,4] = raz_555
        # raz_median[loop,5] = raz_660
        # raz_median[loop,6] = raz_865
        
        
        q_median[loop,0] = eqr_qg_470
        q_median[loop,1] = eqr_qg_660
        q_median[loop,2] = eqr_qg_865
        
        u_median[loop,0] = eqr_ug_470
        u_median[loop,1] = eqr_ug_660
        u_median[loop,2] = eqr_ug_865
               
        
# Change to the output directory
    os.chdir(outpath) 
    
# Generate the base output file name
    outfile_base = "Bakersfield_Meridian_"

# Get the software version number to help track issues
    hold = os.path.basename(__file__)
    words = hold.split('_')
    temp = words[len(words)-1]  # Choose the last element
    hold = temp.split('.')
    vers = hold[0]
    
    outfile = outfile_base+"ALL"+".sdat"
        
    print("Saving: "+outfile)
    
# Open the output file

    outputFile = open(outfile, 'w')
        
# Write the sdat header information

    out_str = 'SDATA version 2.0\n'
    outputFile.write(out_str)
    out_str = '  1   1   1  : NX NY NT\n'
    outputFile.write(out_str)
    out_str = '\n'
    outputFile.write(out_str)
    
# Parse the date string into the correct format

    date = date[0]
    time = time[0]

    sdat_date = date[0:4]+'-'+date[4:6]+'-'+date[6:8]
   # print(sdat_date)
        
# Parse the time string into the correct format

    sdat_time = time[0:2]+':'+time[2:4]+':'+time[4:7]
   # print(sdat_time)
        
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

    out_str = out_str+'{:19.8f}'.format(long)  # Longitude
    out_str = out_str+'{:18.8f}'.format(lat)  # Latitude
    out_str = out_str+'{:17.8f}'.format(elev) # Elevation

    out_str = out_str+'      100.000000'  # Percent of land
    out_str = out_str+'{:16d}'.format(num_int)  # Number of wavelengths (nwl)
    
  ## SET UP THE WAVELENGTH AND MEASUREMENT INFORMATION
  
    #Wavelengths in microns
    out_str = out_str+'{:17.9f}'.format(355/1000)
    out_str = out_str+'{:17.9f}'.format(380/1000)
    out_str = out_str+'{:17.9f}'.format(445/1000)
    out_str = out_str+'{:17.9f}'.format(470/1000)
    out_str = out_str+'{:17.9f}'.format(555/1000)
    out_str = out_str+'{:17.9f}'.format(660/1000)
    out_str = out_str+'{:17.9f}'.format(865/1000)
                                        
  
    #Number of measurements for each wavelength
    out_str = out_str+'{:12d}'.format(1)
    out_str = out_str+'{:12d}'.format(1) # 1 measurement per wavelength
    out_str = out_str+'{:12d}'.format(1)
    out_str = out_str+'{:12d}'.format(3)
    out_str = out_str+'{:12d}'.format(1)
    out_str = out_str+'{:12d}'.format(3)
    out_str = out_str+'{:12d}'.format(3)
    
    #Measurement type of each measurement
    #e.g. 42 is Q - each type has sequence_num values
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
    
    #Number of measurements of each type per wavelength
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
    
    #Angles for each measurement 
    # Solar zenith angle per wavelength
    # NOTE: This is per wavelength rather than per measurement (probably because of 
    #       AERONET), so we take the average solar zenith angle, although this
    #       varies from measurement to measurement from AirMSPI

    for loop in range(num_int):
        out_str = out_str+'{:16.8f}'.format(sun_zen[0])
        
    # View zenith angle per measurement per wavelength
    for outer in range(6):
        for inner in range(step): 
            out_str = out_str+'{:16.8f}'.format(view_zen[inner,outer])

    for outer in range(6):
        for inner in range(step): 
            out_str = out_str+'{:16.8f}'.format(view_zen[inner,outer])
    for inner in range(step):
        out_str = out_str+'{:16.8f}'.format(view_zen[inner,6])
    
    #Measurment values in order
    #41 for 355,380,445,470
    for outer in [0,1,2]:  # Loop over wavelengths
        for inner in range(num_step):  # Loop over measurements
            out_str = out_str+'{:16.8f}'.format(i_median[inner,outer])
    
    for outer in [3]:  # Loop over wavelengths
       for inner in range(num_step):  # Loop over measurements
           out_str = out_str+'{:16.8f}'.format(i_median[inner,outer])  # I
       # for inner in range(num_step):  # Loop over measurements
       #     out_str = out_str+'{:16.8f}'.format(i_in_polar_median[inner,0])  # Ipol
       for inner in range(num_step):  # Loop over measurements
           out_str = out_str+'{:16.8f}'.format(q_median[inner,0])  # Q
       for inner in range(num_step):  # Loop over measurements
           out_str = out_str+'{:16.8f}'.format(u_median[inner,0])  # U

    for outer in [4]:  # Loop over wavelengths
       for inner in range(num_step):  # Loop over measurements
                out_str = out_str+'{:16.8f}'.format(i_median[inner,outer])

    for outer in [5]:  # Loop over wavelengths
        for inner in range(num_step):  # Loop over measurements
            out_str = out_str+'{:16.8f}'.format(i_median[inner,outer])  # I
        for inner in range(num_step):  # Loop over measurements
            out_str = out_str+'{:16.8f}'.format(q_median[inner,1])  # Q
        for inner in range(num_step):  # Loop over measurements
            out_str = out_str+'{:16.8f}'.format(u_median[inner,1])  # U


    for outer in [6]:  # Loop over wavelengths
        for inner in range(num_step):  # Loop over measurements
            out_str = out_str+'{:16.8f}'.format(i_median[inner,outer])  # I
        for inner in range(num_step):  # Loop over measurements
            out_str = out_str+'{:16.8f}'.format(q_median[inner,2])  # Q
        for inner in range(num_step):  # Loop over measurements
            out_str = out_str+'{:16.8f}'.format(u_median[inner,2])  # U
    
    
## ADDITIONAL PARAMETERS- unused so set to zero

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

        
### END MAIN FUNCTION
if __name__ == '__main__':
     main()
