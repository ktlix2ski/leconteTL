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

# testing for individual images

image_path = "/home/kayatroyer/Desktop/Leconte/Test_Imgs/091823/IMG_1491.JPG"
image = Image.open(image_path)
exif_data = image.getexif()

# getting image data
print("Image Format:", image.format) 
print("Image Mode:", image.mode) 
print("Image Size:", image.size) 
print("Image Info:", exif_data.get(306))
        

#   graph of pixel data
# plt.plot(image.histogram())
# plt.xlabel('bands')
# plt.ylabel('count')
# plt.show()
