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

    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
#        print("The images are completely Equal")
#        cv2.imshow('difference', difference)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()
        error, diff = mse_algorithm(original, duplicate)
        cv2.imshow("difference", diff)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return True, error
    else:
#        print("But they are not Equal")
        error, diff = mse_algorithm(original, duplicate)
#        print("Image matching Error between the two images:",error)
        cv2.imshow("difference", diff)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return False, error

# This is the part of iteration
# Select current and previous element
def iter_in_pairs(iterable):
    for i in range(1, len(iterable)):
        yield (iterable[i-1], iterable[i])

# Select .png files from directory with images
files = os.listdir(dir_with_images)
png_files = sorted(list(filter(lambda f: f.endswith('.png'), files)))

# Iterate through list of images and selec current and previous
for prev, cur in iter_in_pairs(png_files):
    prev_np = cv2.imread(os.path.join(dir_with_images, prev))
    cur_np = cv2.imread(os.path.join(dir_with_images, cur))
    result, error = check_similar_images(prev_np, cur_np)
    if result == True:
        print(f"Files {os.path.join(dir_with_images, prev)} is similar to {os.path.join(dir_with_images, cur)} and error score is {error}")
    else:
        print(f"Files {os.path.join(dir_with_images, prev)} is similar to {os.path.join(dir_with_images, cur)} and error score is {error}")