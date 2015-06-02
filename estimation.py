import cv2
import numpy as np
import sys
import getopt
import os

#
# Read in an image file, errors out if we can't find the file
#
def readImage(filename, greyScale):
    img = cv2.imread(filename, greyScale)
    if img is None:
        print('Invalid image:' + filename)
        return None
    else:
        print('Image successfully read...' + filename)
        return img

#
#
#
def findTopandBottom(depthImg):
    top = None;
    btm = None;
    for i in range(depthImg.shape[0]):
        for j in range(depthImg.shape[1]):
            if top is None and depthImg.item(i, j) != 255:
                top = i
            if top is not None and depthImg.item(i, j) != 255:
                btm = i
    print "top found: " + str(top)
    print "bottom found: " + str(btm)
    return top, btm

def getSideviewShape(depthImg):
    top, btm = findTopandBottom(depthImg)
    sideview = []
    for i in range(top, btm+1):
        result = []
        for j in range(depthImg.shape[1]):
            if(depthImg.item(i, j) < 255):
                result.append(depthImg.item(i, j))
            #result = np.minimum(depthImg[i], 255)
        #print np.mean(result)
        sideview.append(np.mean(result))
            #z = depthImg[i][j > 254]
            #print np.mean(depthImg)
    return sideview
#
# Main parses argument list and runs the functions
#
def main():
    args, folder_name = getopt.getopt(sys.argv[1:],'', [''])
    args = dict(args)

    images = {}
    depth_list = os.listdir(folder_name[1])
    color_list = os.listdir(folder_name[0])
    #read our images and keep them in a tuple
    for img_name in depth_list:
        depth_img = readImage(folder_name[1] + '/' + img_name, 0)

        for name in color_list:
            if img_name in name:
                color_img_name = name
                break

        if color_img_name is not None:
            color_img = readImage(folder_name[0] + '/' + color_img_name, 1)
        images[img_name] = ((color_img, depth_img))

   # print len(images)
    #np.set_printoptions(threshold=np.nan)
    #print images['dornoosh7.bmp']
    sv = getSideviewShape(images['dornoosh7.bmp'][1])
    print len(sv[:len(sv)/2])

if __name__ == "__main__":
    main()