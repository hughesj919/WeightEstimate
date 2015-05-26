import cv2
import numpy as np
import sys
import getopt
import os

#
# Read in an image file, errors out if we can't find the file
#
def readImage(filename):
    img = cv2.imread(filename, 0)
    if img is None:
        print('Invalid image:' + filename)
        return None
    else:
        print('Image successfully read...')
        return img

#
# Main parses argument list and runs the functions
#
def main():
    args, folder_name = getopt.getopt(sys.argv[1:],'', [''])
    args = dict(args)

    images = []
    depth_list = os.listdir(folder_name[1])
    color_list = os.listdir(folder_name[0])
    #read our images and keep them in a tuple
    for img_name in depth_list:
        depth_img = readImage(folder_name[1] + '/' + img_name)

        for name in color_list:
            if img_name in name:
                color_img_name = name
                break

        if color_img_name is not None:
            color_img = readImage(folder_name[0] + '/' + color_img_name)
        images.append((color_img, depth_img))

    print len(images)

if __name__ == "__main__":
    main()