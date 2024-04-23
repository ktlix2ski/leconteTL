#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 15:10:17 2024

@author: kayatroyer
"""
# importing packages

import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
import matplotlib.pyplot as plt
import os

# testing for individual images

image_path = "C:\Users\ktlix\OneDrive\Desktop\Glaciology_Research_Work\Code_Test_Images\IMG_9286.JPG"

# prints image data 
def process_image(image_path):
    image = Image.open(image_path)
    exif_data = image.getexif()
    file_size = os.path.getsize(image_path)
    print("Image Format:", image.format) 
    print("Image Mode:", image.mode) 
    print("Image Size:", image.size) 
    print("Image Info:", exif_data.get(306))
    print("File Size",file_size/(1e12), "TB")
    
# prints just the timestamp and no additional data
def image_timestamp(image_path):
    image = Image.open(image_path)
    exif_data = image.getexif()
    print(os.path.basename(image_path),"Captured at:", exif_data.get(306))    

#   graph of pixel data
# plt.plot(image.histogram())
# plt.xlabel('bands')
# plt.ylabel('count')
# plt.show()

#taking in a folder of images
#folder_path = "/home/kayatroyer/Desktop/Leconte/091823"
#test_path = "C:\Users\ktlix\OneDrive\Desktop\Glaciology_Research_Work\Code_Test_Images"
#fuck_folder = "/home/kayatroyer/Desktop/Leconte/Test_notinorder"

def process_folder(folder_path):
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,f))]
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        process_image(image_path)

# prints the time each image in the folder was taken 
def capture_times(folder_path):
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,f))]
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image_timestamp(image_path)
        
# organizes the images in te folder by date and time (idk if this is working)
def organize_images(folder_path):
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,f))]
    image_paths_with_timestamps = []

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        timestamp = image_timestamp(image_path)
        if timestamp:
            image_paths_with_timestamps.append((image_path, timestamp))

# Sort images by timestamp
sorted_image_paths = sorted(image_paths_with_timestamps, key=lambda x: x[1])

# Print sorted image paths
for image_path, timestamp in sorted_image_paths:
    print(f"Image: {image_path}, Timestamp: {timestamp}")       
