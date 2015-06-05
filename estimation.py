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
# Read and return raw depth data
#
def readRawDepthInfo(filename):
    f = None
    x = None
    try:
        f = open(filename, 'r')
    except:
        print("Could not retrieve raw depth file: " + filename)
    if f is not None:
        x = np.zeros((480, 640))
        count = 0
        lines = f.readlines()
        for line in lines:
            elements = [int(i) for i in line.split('\t') if i != '\n']
            #print len(elements)
            #print type(elements[0])
            x[count,:] = elements
            count+=1
    return x

#
# Finds the leftmost and rightmost column of the human
#
def findLeftandRight(depthImg):
    left = None;
    right = None;
    for i in range(depthImg.shape[1]):
        for j in range(depthImg.shape[0]):
            if left is None and depthImg.item(j, i) != 255:
                left = i
            if left is not None and depthImg.item(j, i) != 255:
                right = i
    print "left found: " + str(left)
    print "right found: " + str(right)
    return left, right


#
# Finds the top and bottom row of the human
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

def getSideviewShape(depthImg, top, btm):
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
    raw_depth_list = os.listdir(folder_name[2])
    #read our images and keep them in a tuple
    for img_name in depth_list:
        depth_img = readImage(folder_name[1] + '/' + img_name, 0)

        for name in color_list:
            if img_name in name:
                color_img_name = name
                break

        if color_img_name is not None:
            color_img = readImage(folder_name[0] + '/' + color_img_name, 1)


        fname, ext = os.path.splitext(img_name)
        raw_depth_name = folder_name[2] + '/' + fname + ".txt"
        raw_depth = readRawDepthInfo(raw_depth_name)
        if raw_depth is not None:
            images[img_name] = ([color_img, depth_img, raw_depth])

    print len(images)
    #np.set_printoptions(threshold=np.nan)
    #print images['dornoosh7.bmp']

    #sv = getSideviewShape(images['dornoosh7.bmp'][1])

   # findLeftandRight(images['dornoosh7.bmp'][1])
    #print len(sv[:len(sv)/2])


    l, r = findLeftandRight(images['dornoosh7.bmp'][1])
    t, b = findTopandBottom(images['dornoosh7.bmp'][1])
    sv = getSideviewShape(images['dornoosh7.bmp'][1], t, b)

    leftCol = images['dornoosh7.bmp'][2][:,[l]]
    rightCol = images['dornoosh7.bmp'][2][:,[r]]
    topRow = images['dornoosh7.bmp'][2][t,:]
    bottomRow = images['dornoosh7.bmp'][2][b,:]
    print np.amin(leftCol[np.nonzero(leftCol)])
    print np.amin(rightCol[np.nonzero(rightCol)])
    print np.amin(topRow[np.nonzero(topRow)])
    print np.amin(bottomRow[np.nonzero(bottomRow)])


if __name__ == "__main__":
    main()