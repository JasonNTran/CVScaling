import numpy as np
import matplotlib.pylab as plt
import os, sys
from PIL import Image
import glob

outputFile = open("Scaling_Results.txt", "w")
def getListAverage(list):
    numElements = 0
    sum = 0
    for i in list:
        if(i != 0):
            sum += i
            numElements += 1
    return sum / numElements

def getScaling(heatmap, groundTruth):
    scale_avg = []
    scale = []
    numElements = 0

    width, height = heatmap.size
    area = (width * .48, height * .93, width * .51, height * .95)
    cropped_img = heatmap.crop(area)
    cropped_Truth = groundTruth.crop(area)
    pix_val = list(cropped_img.getdata())
    ground_pix = list(cropped_Truth.getdata())

    for i in range(len(ground_pix)):
        ground_pix[i] = ground_pix[i] / 256
    scale_avg.append(getListAverage(pix_val) / getListAverage(ground_pix))

    for i in range(len(ground_pix)):
        if(ground_pix[i] != 0):
            scale.append(pix_val[i] / ground_pix[i])
            numElements += 1
    scale_avg.append(scale)
    return scale_avg

def writeScaleToFile(scale, heatName, truthName):
    outputFile.write("Average of heatmap -" +  heatName
    + "- divide by average of ground truth -"
    + truthName + "-: " + str(scale.pop(0)) + "\n")

    outputFile.write("Average of every individual pixel of heatmap -" + heatName
    + "- divided by ground truth-" + truthName + "-: "
    + str(getListAverage(scale.pop())) + "\n")

    outputFile.write("\n")



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
