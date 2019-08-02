import numpy as np
import matplotlib.pylab as plt
import os, sys
from PIL import Image
import glob

outputFile = open("Scaling_Results.txt", "w")
# simple function to calculate the average of a list
def getListAverage(list):
    numElements = 0
    sum = 0
    for i in list:
        if(i != 0):
            sum += i
            numElements += 1
    return sum / numElements

def getScaling(heatmap, groundTruth):
    # scale_avg = []
    scale = []
    numElements = 0

    # Cropping both images
    width, height = heatmap.size
    area = (width * .48, height * .95, width * .51, height * .97)
    cropped_img = heatmap.crop(area)
    cropped_Truth = groundTruth.crop(area)
    pix_val = list(cropped_img.getdata())
    ground_pix = list(cropped_Truth.getdata())

    # Compare pixel by pixel and store to later calculate the average. Divide ground_pix by 256 to get an 8 bit value
    for i in range(len(ground_pix)):
        if(ground_pix[i] != 0):
            ground_pix[i] = ground_pix[i] / 256
            scale.append(pix_val[i] / ground_pix[i])
            numElements += 1
    return scale

# Simple function that simply outputs the data in a way that can be read in a text file
def writeScaleToFile(scale, heatName, truthName):
    outputFile.write("Heatmap: " + heatName
    + "GroundTruth: " + truthName + " Scaling: "
    + str(getListAverage(scale)) + "\n")

    outputFile.write("\n")


# Basically the main of the program
fileList = glob.glob('Images/*.png')
groundTruths = glob.glob('disp_noc_0/*.png')

for truth in groundTruths:
    groundTruth = Image.open(truth)
    truthName = groundTruth.filename
    for image in fileList:
        heatMap = Image.open(image)
        heatName = heatMap.filename
        heatMap = heatMap.convert('L')
        scale = getScaling(heatMap, groundTruth)
        writeScaleToFile(scale, heatName, truthName)
