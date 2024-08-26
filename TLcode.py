#Code for making timelapse videos for Leconte Glacier in Alaska

# importing packages

import numpy as np
from numpy import asarray
from PIL import Image, ExifTags
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
folder_path = "/home/kayatroyer/leconteTL/Leconte/091823"
test_path = "/home/kayatroyer/leconteTL/Leconte/Mini_Test_Folder"
big_test = "/home/kayatroyer/Desktop/Leconte/bigminitest"
bleh_folder = "/home/kayatroyer/Desktop/Leconte/Test_notinorder"
output = "/home/kayatroyer/Desktop/Leconte/output_test"
drive_path = "/media/kayatroyer/BU_TLDRVid/TimeLapse/South/Canon/90D/092023"
        

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
            print(f"Skipping {image_path} DNE")
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
    return image_array[0]
            

vid_folder = "/home/kayatroyer/leconteTL/Leconte/video_folder/hopefuldrivetest2.mp4"


def create_timelapse(video_path, images_array, fps):
    "does not work for big folders"
    #image dimensions
    height, width, _ = images_array[0].shape
    
    #create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
    #write images to video
    for img in images_array:
        bgr_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        out.write(bgr_img)

    out.release()
    print("done, check video folder for timelapse video")
    
def get_orientation(image_path):
    """Gets the orientation from an image file."""
    image = Image.open(image_path)
    exif_data = image._getexif()
    if exif_data is not None:
        for tag, value in exif_data.items():
            if ExifTags.TAGS.get(tag) == 'Orientation':
                return value
    return 1

def collect_image_files(folder_path):
   image_files = []
    
   def recurse_dirs(current_path):
       print(f"Entering directory: {current_path}")  # Debug statement
       for entry in os.listdir(current_path):
           entry_path = os.path.join(current_path, entry)
           if os.path.isdir(entry_path):
               recurse_dirs(entry_path)
           elif entry.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
               print(f"Found image file: {entry_path}")  # Debug statement
               image_files.append(entry_path)
                
   recurse_dirs(folder_path)
   print(f"Total images collected: {len(image_files)}")  # Debug statement
   return image_files

def calculate_brightness(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Calculate the mean brightness
    return np.mean(gray)

def adjust_exposure(image, target_brightness, current_brightness):
    # Calculate the brightness ratio
    ratio = target_brightness / current_brightness
    # Adjust the image exposure
    return cv2.convertScaleAbs(image, alpha=ratio, beta=0)

def adjust_color_balance(image, alpha=1.0, beta=0.0):
    # Adjust the color balance to make the image less blue if necessary
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted_image


N_C1_061824 ="/media/kayatroyer/LC_TL_Win/July24Data/Timelapse/North/Canon1/061824"
vid_N_C1_061824 = "/home/kayatroyer/Desktop/Leconte/videos/vid_N_C1_061824.mp4"
    
def open_createTL(folder_path, video_out_path, fps):
    "combines folder_opening and create_timelapse so it dont crash (workingggg)"
    #timestamp writer is not working 
    
    #image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,f))]
    image_files = collect_image_files(folder_path)
    image_files.sort()
    total_images = len(image_files)
    print(f"Total images found: {total_images}")

    count = 0 
    batch = 100
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
    out = None
    initialized = False
    
    while count < total_images:
        img_array = []
        for i in range(count, min(count+batch, total_images)):
            img_path = image_files[i]
            try:
                orientation = get_orientation(img_path)
                image = Image.open(img_path).convert('RGB')
                exif_data = image.getexif()
                timestamp = exif_data.get(306)
                img = np.array(image)
            
                if img is not None:
                    bgr_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                   
                   # Rotate image 
                    if orientation == 3:
                       bgr_img = cv2.rotate(bgr_img, cv2.ROTATE_180)
                    elif orientation == 6:
                       bgr_img = cv2.rotate(bgr_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    elif orientation == 8:
                       bgr_img = cv2.rotate(bgr_img, cv2.ROTATE_90_CLOCKWISE)
                       
                    # Adjust exposure
                    #current_brightness = calculate_brightness(bgr_img)
                    #adjusted_img = adjust_exposure(bgr_img, target_brightness, current_brightness)
                   
                    if timestamp:
                        cv2.putText(bgr_img, timestamp, (150, 150), cv2.FONT_HERSHEY_PLAIN, 10, (0, 255, 0), 5, cv2.LINE_AA)               
                    #img_array.append(adjusted_img)
                    img_array.append(bgr_img)
            except Exception as e:
                    print(f"Error processing image {img_path}: {e}")
                
        if not initialized and img_array:
            height,width, _ = img_array[0].shape
            out = cv2.VideoWriter(video_out_path, fourcc, fps, (width, height))
            initialized = True
            
        for img in img_array:
            out.write(img)
        img_array.clear()
        count += batch
        print(f"Processed {min(count, total_images)} out of {total_images} images.")
        
    if out is not None:
        out.release()
    print("done, check video folder for timelapse video")    
        
    





























