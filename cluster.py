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
    # raw_results  = open('sampleSentOutput.txt', 'w') 
    # print raw_results
    # raw_results.close()
    
    # a = np.random.multivariate_normal([10, 0], [[3, 1], [1, 4]], size=[100,])
    # b = np.random.multivariate_normal([0, 20], [[3, 1], [1, 4]], size=[50,])
    # X = np.concatenate((a, b),)
    # #print X.shape  # 150 samples with 2 dimensions
    # # plt.scatter(X[:,0], X[:,1])
    # # plt.show()
    # # print X[:,0]
    # # print X[:,1]


    # Z = linkage(X, 'ward')

    # c, coph_dists = cophenet(Z, pdist(X))

    # print Z[:20]

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
    distanceMatrix = pdist(dataMatrix)
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

    # with open('out_rating_movies.txt', 'r') as file:
    #     # x = f.read()
    #     # x.replace('\n', ' ')
    #     # print x
    #     counter = 0 
       
    #     convertedList = []
    #     theList = [l.strip() for l in file]
    #     for user in theList:
    #         if(counter > 0):
    #             converted = user.split("|")
    #             converted.pop(0)
    #             converted = [float(i) for i in converted]
    #             #print(converted)
    #             converted = array(converted)
    #             convertedList.append(converted)
    #             counter = counter + 1
    #         else:
    #             template_line = user
    #             #print template_line
    #             counter = counter + 1
                
    #     convertedList = array(convertedList)
    #     data = vstack(convertedList)





if __name__ == "__main__":
    main()