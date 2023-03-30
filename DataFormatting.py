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
datapath = "C:/Users/Clarissa/Documents/AirMSPI/Prescott/FIREX-AQ_8172019"
outpath = "C:/Users/Clarissa/Documents/GitHub/GRASP-CSP/RetreivalExamples"

# Set the length of one measurement sequence of step-and-stare observations
# NOTE: This will typically be an odd number (9,7,5,...)
num_step = 5
    
# Set the index of the measurement sequence within the step-and-stare files
# NOTE: This is 0 for the first sequence in the directory, 1 for the second group, etc.
sequence_num = 0

#Set the bounding box dimensions that will correct for parallax 
# Set bounds for the image (USER INPUT)
#FIREX
min_x = 1900
max_x = 2200
min_y = 1900
max_y = 2200

# #Bakersfield
# min_x = 1200
# max_x = 1900
# min_y = 1200
# max_y = 1900


            
# Set bounds for ROI (USER INPUT)
# Note: These coordinates are RELATIVE to the overall bounding box set above
#FIREX
roi_x1 = 120
roi_x2 = 125
roi_y1 = 105
roi_y2 = 110
    
#Bakserfield
# roi_x1 = 485
# roi_x2 = 490
# roi_y1 = 485
# roi_y2 = 490

#Start the main code#
def main():  # Main code

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
    esd,E0,elv,lat,long,i,view_zen,view_az,sun_zen,sun_az,ipol,qm,um=read(datapath,num_step,sequence_num,min_x,min_y,max_x,max_y,roi_x1,roi_x2,roi_y1,roi_y2)
    #print(qm[:])
#Section 2. Polarimetric Coodinate System Reconciliation
#Per Equation (X) make stokes inputs [Q_i,U_i] for each wavelength
    for step in range(num_step):
        #470
        stokesin4 = np.array([[qm[step,0]], [um[step,0]]]) #Meridian plane      
        #660
        stokesin6 = np.array([[qm[step,1]], [um[step,1]]]) #Meridian
        #865
        stokesin8 = np.array([[qm[step,2]], [um[step,2]]]) #Meridian
        

### END MAIN FUNCTION
if __name__ == '__main__':
     main()
