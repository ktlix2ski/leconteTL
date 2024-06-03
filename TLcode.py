#Code for making timelapse videos for Leconte Glacier in Alaska

# importing packages

import numpy as np
from numpy import asarray
from PIL import Image
from PIL.ExifTags import TAGS
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from datetime import datetime
import shutil
import cv2
import imageio


# INDIVIDUAL IMAGE TESTING 

image_path = "/home/kayatroyer/Desktop/Leconte/Mini_Test_Folder/IMG_1701.JPG"
img = Image.open(image_path)

# PRINTING IMAGE DATA
def process_image(image_path):
    image = Image.open(image_path)
    exif_data = image.getexif()
    file_size = os.path.getsize(image_path)
    width, height = image.size
    print("IMAGE NAME:", os.path.basename(image_path))
   # print("Image Format:", image.format) 
   # print("Image Mode:", image.mode) 
    print("Image Size:", image.size) 
    print("Image Info:", exif_data.get(306))
    print("File Size",file_size/(1e12), "TB")
    print("Total Pixels in Image:", width*height)
  #  print("Image Resolution:")
    

def image_timestamp(image_path):
    "ONLY PRINTS TIMESTAMP, NO ADDITIONAL DATA"
    image = Image.open(image_path)
    exif_data = image.getexif()
    print(os.path.basename(image_path),"Captured at:", exif_data.get(306))    
    
    

# INPUT IMAGE FOLDER PATHS
folder_path = "/home/kayatroyer/Desktop/Leconte/091823"
test_path = "/home/kayatroyer/leconteTL/Leconte/Mini_Test_Folder"
big_test = "/home/kayatroyer/Desktop/Leconte/bigminitest"
bleh_folder = "/home/kayatroyer/Desktop/Leconte/Test_notinorder"
output = "/home/kayatroyer/Desktop/Leconte/output_test"
        

def process_folder(folder_path):
    "PRINTS DATA FOR EACH IMAGE IN FOLDER (working)"
    failed_files =[]
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,f))]
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        if os.path.exists(image_path):
            try:
                process_image(image_path)
            except Exception as e:
                print(f"Failed to process {image_path}: {e}")
                failed_files.append(image_path)
        else:
            print(f"Skipping {image_path} as it does not exist")
            failed_files.append(image_path)
    print("FAILED TO PROCESS FOLLOWING FILES:")
    for failed_file in failed_files:
        print(failed_file)


def capture_times(folder_path):
    "PRINTS IMAGE TIMESTAMP (working)"
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,f))]
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image_timestamp(image_path)
        
def folder_opening(folder_path):
    empty = []
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,f))]
    for image_file in image_files:
        full_image_path = os.path.join(folder_path, image_file)
        #print(full_image_path)
        try:
            image = Image.open(full_image_path).convert('RGB')
            image = np.array(image)
            empty.append(image)
        except Exception as e:
            print(f"Error opening {full_image_path}: {e}")
    image_array = np.array(empty)
    return image_array
            
img_array = folder_opening(test_path)

vid_folder = "/home/kayatroyer/leconteTL/Leconte/video_folder/test_video2.mp4"


def create_timelapse(video_path, images_array, fps):
    #image dimensions
    height, width, _ = images_array[0].shape
    
    #create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Change codec as needed (e.g., 'XVID' for .avi format)
    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
    #write images to video
    for img in images_array:
        bgr_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        out.write(bgr_img)

    out.release()
    print("done, check video folder for timelapse video")
    
    
#WORKS FOR SMALL FOLDERS RN BUT CRASHES WITH BIG ONES

