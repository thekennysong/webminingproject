"""cluster.py

Part 3 of group project. Clustering results from the sentiment analysis.

"""
import argparse

from numpy import vstack,array
from numpy.random import rand
from scipy import special, optimize
from scipy.cluster.vq import kmeans,vq
from pylab import plot,show
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, leaves_list
import numpy as np
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
import sys


def main():


#open the file assuming the data above is in a file called 'dataFile'
    inFile = open(sys.argv[1],'r')
    #save the column/row headers (conditions/genes) into an array
    colHeaders = inFile.next().strip().split()[1:]
    rowHeaders = []
    dataMatrix = []

    for line in inFile:
        data = line.strip().split("|")
        rowHeaders.append(data[0])
        dataMatrix.append([float(x) for x in data[1:]])

    #convert native data array into a numpy array
    dataMatrix = np.array(dataMatrix)
    distanceMatrix = pdist(dataMatrix,'euclidean')
    linkageMatrix = linkage(distanceMatrix)

    heatmapOrder = leaves_list(linkageMatrix)

    orderedDataMatrix = dataMatrix[heatmapOrder,:]
    rowHeaders = np.array(rowHeaders)
    orderedRowHeaders = rowHeaders[heatmapOrder]

    #output data for visualization in a browser with javascript/d3.js
    matrixOutput = []
    row = 0
    for rowData in orderedDataMatrix:
        col = 0
        rowOutput = []
        for colData in rowData:
            rowOutput.append([colData, row, col])
            col += 1
        matrixOutput.append(rowOutput)
        row += 1

    print 'var maxData = ' + str(np.amax(dataMatrix)) + ";"
    print 'var minData = ' + str(np.amin(dataMatrix)) + ";"
    print 'var data = ' + str(matrixOutput) + ";"
    print 'var cols = ' + str(colHeaders) + ";"
    print 'var rows = ' + str([x for x in orderedRowHeaders]) + ";"



if __name__ == "__main__":
    main()