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

image_path = "/home/kayatroyer/Desktop/Leconte/Test_Imgs/091823/IMG_1491.JPG"
image = Image.open(image_path)
exif_data = image.getexif()
file_size = os.path.getsize(image_path)

# getting image data
print("Image Format:", image.format) 
print("Image Mode:", image.mode) 
print("Image Size:", image.size) 
print("Image Info:", exif_data.get(306))
print("File Size",file_size/(1e12), "TB")
        

#   graph of pixel data
# plt.plot(image.histogram())
# plt.xlabel('bands')
# plt.ylabel('count')
# plt.show()

# taking in a folder of images
folder_path = "/home/kayatroyer/Desktop/Leconte/091823"
image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,f))]



#folder_data = folder_path.getexif()

# image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,f))]
# for file_name in image_files:
#     try:
#         image = Image.open(os.path.join(folder_path, file_name))
#         image.show()
#     except IOError:
#         print(f"unable to open {file_name}")

#folder = Image.open(folder_path)
# folder_data = folder.getexif()
