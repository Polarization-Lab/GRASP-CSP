# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 10:09:33 2023

@author: ULTRASIP_1
"""

# Import packages

import glob
import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
import time
from matplotlib import patches



def image_crop(a):
        #np.clip(a, 0, None, out=a)
        a[a == -999] = np.nan
        mid_row = a.shape[0] // 2
        mid_col = a.shape[1] // 2
        start_row = mid_row - 524
        end_row = mid_row + 524
        start_col = mid_col - 524
        end_col = mid_col + 524
        
        a = a[start_row:end_row, start_col:end_col]
        return a


def calculate_std(image):
# Define the size of the regions we'll calculate the standard deviation for
    region_size = 5

    # Calculate the standard deviation over the regions
    std_dev = np.zeros_like(image)
    for i in range(region_size//2, image.shape[0] - region_size//2):
        for j in range(region_size//2, image.shape[1] - region_size//2):
            std_dev[i,j] = np.std(image[i-region_size//2:i+region_size//2+1, j-region_size//2:j+region_size//2+1])

    return std_dev

def calculate_median(image):
# Define the size of the regions we'll calculate the standard deviation for
    region_size = 5

    # Calculate the standard deviation over the regions
    median_img = np.zeros_like(image)
    for i in range(region_size//2, image.shape[0] - region_size//2):
        for j in range(region_size//2, image.shape[1] - region_size//2):
            median_img[i,j] = np.median(image[i-region_size//2:i+region_size//2+1, j-region_size//2:j+region_size//2+1])

    return median_img

def  choose_roi(image): 
            std_dev = calculate_std(image)
            med_img = calculate_median(image)
    # Plot the original image and the standard deviation image side by side
            fig, ax = plt.subplots(1,2,  figsize=(16, 8))
            ax[0].imshow(image , cmap = 'gray')
            ax[0].set_title('Original Image')
            ax[0].axis('off')
            im = ax[1].imshow(std_dev, cmap = 'jet')
            ax[1].set_title('Standard Deviation')
            ax[1].grid(True)
            cbar = fig.colorbar(im, ax = ax[1], fraction = 0.046, pad=0.04)
            
            plt.show()

        # Prompt the user to choose a region
            x = int(input('Enter x-coordinate of region: '))
            y = int(input('Enter y-coordinate of region: '))

          
            # Create a new figure with 1 row and 2 columns
            fig, axs = plt.subplots(1, 2, figsize=(16, 8))

        # Plot the original image with the selected region of interest highlighted
            axs[0].imshow(image, cmap='gray')
            axs[0].add_patch(patches.Rectangle((x, y), 5, 5, linewidth=5, edgecolor='w', facecolor='none'))
            axs[0].set_title('Selected Region of Interest')

            # Plot the standard deviation image with the selected region of interest highlighted
            im = axs[1].imshow(std_dev, cmap='jet')
            axs[1].add_patch(patches.Rectangle((x, y),5,5,linewidth=5, edgecolor='w', facecolor='none'))
            axs[1].set_title('Standard Deviation with Selected Region of Interest')
            cbar = fig.colorbar(im, ax=axs[1], fraction=0.046, pad=0.04)

        # Show the plot
            plt.show()
            
            
            return x,y