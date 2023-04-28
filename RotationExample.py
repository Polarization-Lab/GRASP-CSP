# -*- coding: utf-8 -*-
"""
Rotation example following the methods of Section 4.2.1 
and detailed in Appendix B of DeLeon et al. XXXX.. 
"""
#Import Libraries 
import glob
import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
import time

#Data Point from Table B.4
# #478F Datapoint
qm = -0.028720994
um = -0.003678653
qs = -0.028884614
us = -0.0021799933
vaz = 340.60052
vza = 49.187294
saz = 335.1774
sza = 13.95994




#Define vectors 
#Zenith 
z= np.array([0, 0, 1]);
i = np.array([np.cos(np.radians(saz))*np.sin(np.radians(sza)), -np.sin(np.radians(saz))*np.sin(np.radians(sza)), -np.cos(np.radians(sza))]); #illumination vec,flip sign of sza
k = np.array([np.cos(np.radians(vaz))*np.sin(np.radians(vza)), -np.sin(np.radians(vaz))*np.sin(np.radians(vza)), np.cos(np.radians(vza))]);

# #Illumination Vector 
# i = np.array([np.cos(np.radians(phi_i))*np.sin(np.radians(theta_i)), -np.sin(np.radians(phi_i))*np.sin(np.radians(theta_i)), -np.cos(np.radians(theta_i))]); 
# #View vector in direction of photon travel
# k = np.array([np.cos(np.radians(phi_v))*np.sin(np.radians(theta_v)), -np.sin(np.radians(phi_v))*np.sin(np.radians(theta_v)), np.cos(np.radians(theta_v))]); 

#Define input stokes
stokesin = np.array([[qm], [um]]) #Meridian
stokesins = np.array([[qs], [us]]) #Scattering

#----------------Rotation from AirMSPI Scattering to GRASP Meridian---------#
#Normal vectors from refernce plane Eqns B.1 and B.2
n_m = np.cross(z,k)/np.linalg.norm(np.cross(z,k))
n_s = np.cross(i,k)/np.linalg.norm(np.cross(i,k))

#Horizontal vectors via Eqn 3 for both 
h_i = np.cross(k,n_s)/np.linalg.norm(np.cross(k,n_s))
h_o = np.cross(k,n_m)/np.linalg.norm(np.cross(k,n_m))

#Vertical vectors found from horizontal vectors 
v_i = np.cross(k,h_i)/np.linalg.norm(np.cross(k,h_i))
v_o = np.cross(k,h_o)/np.linalg.norm(np.cross(k,h_o))

#Input and output bases according to Eqn 5. 
O_in = np.stack((h_i,v_i,k),axis=1);
O_out = np.stack((h_o,v_o,k),axis=1);

#Rotation Matrix according to Eqn 6.
r_alpha = O_out.T@(O_in)

#Solve for alpha via Eqn 7. 
alpha = np.arctan2(-r_alpha[0,1],r_alpha[0,0]);  

#Final rotation according to Eqn 4. 
rotationmatrix = np.array([[np.cos(2*alpha),-np.sin(2*alpha)],[np.sin(2*alpha),np.cos(2*alpha)]]);
#Should match Q,U from the meridional plane
stokesout = rotationmatrix@stokesins

print(stokesout.T, '=', stokesin.T,'?')

