# -*- coding: utf-8 -*-
"""
Functions
"""

import glob
import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
import time
from matplotlib import patches


def calculate_dolp(stokesparam):

    #I = stokesparam[0]
    Q = stokesparam[0]
    U = stokesparam[1]
    dolp = ((Q**2 + U**2)**(1/2)) #/I
    return dolp

def image_crop(a):
        #np.clip(a, 0, None, out=a)
        a[a == -999] = np.nan
        mid_row = a.shape[0] // 2
        mid_col = a.shape[1] // 2
        start_row = mid_row - 262
        end_row = mid_row + 262
        start_col = mid_col - 262
        end_col = mid_col + 262
        
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


def  choose_roi(image): 
            std_dev = calculate_std(image)
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
        
def format_directory():
    
    directory_path = input("Enter the directory path: ")
    # Remove trailing slashes
    directory_path = directory_path.rstrip(os.path.sep)

    # Normalize path separators
    directory_path = os.path.normpath(directory_path)

    # Replace backslashes with forward slashes
    directory_path = directory_path.replace('\\', '/')

    # Format the directory path as a raw string literal
    formatted_directory_path = r"{}".format(directory_path)

    return formatted_directory_path


def load_hdf_files(folder_path, group_size,idx):
    # Get a list of HDF file paths in the folder
    file_paths = glob.glob(os.path.join(folder_path, '*.hdf'))

    # Sort file paths based on date and time in the file name
    sorted_file_paths = sorted(file_paths, key=lambda x: (os.path.basename(x).split('_')[5][0:8], os.path.basename(x).split('_')[5][8:14]))

    # Load files in groups of the specified size
    groups = [sorted_file_paths[i:i+group_size] for i in range(0, len(sorted_file_paths), group_size)]

    # Choose one group to use
    selected_group = groups[idx]  # Change the index to select a different group

    return selected_group
