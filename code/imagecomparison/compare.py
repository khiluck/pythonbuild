#!/usr/bin/env python3
import os
from os import listdir
import cv2
import numpy as np

dir_with_images = "img"

def mse_algorithm(original, duplicate):
    # Convert the images to grayscale
    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    duplicate = cv2.cvtColor(duplicate, cv2.COLOR_BGR2GRAY)
    h, w = original.shape
    diff = cv2.subtract(original, duplicate)
    err = np.sum(diff**2)
    mse = err/(float(h*w))
    return mse, diff

def check_similar_images(original, duplicate):
    # 1) Check if 2 images are equals
    if original.shape == duplicate.shape:
#        print("The images have same size and channels")
        difference = cv2.subtract(original, duplicate)
        b, g, r = cv2.split(difference)
        error, diff = mse_algorithm(original, duplicate)
        return error

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]

# This is the part of iteration
# Select current and previous element
def iter_in_pairs(iterable):
    for i in range(1, len(iterable)):
        yield (iterable[i-1], iterable[i])


# Process the filename to get date and time
# Cut extension and prefix
def file_proc(filename):
    tmp_filename = remove_prefix(os.path.splitext(filename)[0], "scr").split("-")
    file_date = tmp_filename[0].split("_")
    file_time = tmp_filename[1].split("_")
    return file_date, file_time

# Iterate through directories
directories = sorted(list([ name for name in os.listdir(dir_with_images) if os.path.isdir(os.path.join(dir_with_images, name)) ]))
for each_dir in directories:
    full_path_to_dir = os.path.join(dir_with_images, each_dir)
    # Select .png files from directory with images
    files = os.listdir(full_path_to_dir)
    png_files = sorted(list(filter(lambda f: f.endswith('.png'), files)))

    # Iterate through list of images and selec current and previous
    for prev, cur in iter_in_pairs(png_files):
        prev_np = cv2.imread(os.path.join(full_path_to_dir, prev))
        cur_np = cv2.imread(os.path.join(full_path_to_dir, cur))
        error = check_similar_images(prev_np, cur_np)
        prev_file_date, prev_file_time = file_proc(prev)
        cur_file_date, cur_file_time = file_proc(cur)
        print(f"PREV Date: {prev_file_date} and Time: {prev_file_time}")
        print(f"CUR Date: {cur_file_date} and Time: {cur_file_time}")
        if error > 0.01:
            print(f"Files {os.path.splitext(os.path.join(full_path_to_dir, prev))[0]} is similar to {os.path.join(full_path_to_dir, cur)} and error score is {error}")

        else:
            print(f"Files {os.path.splitext(os.path.join(full_path_to_dir, prev))[0]} is similar to {os.path.join(full_path_to_dir, cur)} and error score is {error}")