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
import os
import random

def cluster(curUVs):
    #open the file assuming the data above is in a file called 'dataFile'
    #inFile = open(sys.argv[1],'r')
    #save the column/row headers (conditions/genes) into an array
    colHeaders = []
    rowHeaders = []
    dataMatrix = []

    # for user in curUVs:
    #     data = line.strip().split("|")
    #     rowHeaders.append(curUVs)
    #     dataMatrix.append([float(x) for x in data[1:]])

    for userId, ratings in curUVs.iteritems():
        rowHeaders.append(userId)
        dataMatrix.append(ratings)

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

    return (matrixOutput, [x for x in orderedRowHeaders])

def partition(k, file):
    k = int(k)
    files = []
    fold_file = "folds_%s/" % str(k)
    if not os.path.isdir(fold_file):
        os.mkdir(fold_file)
    for i in range(0,k):
       f = open(fold_file + "/review_fold_%s.txt" % str(i), "w")
       files.append(f)
    c = 0
    v = open(file, "r")
    for line in v:
        if line[0] == "u":
            continue
        if c == k:
            c = 0
            files[c].write(line)
            c += 1
        else:
            files[c].write(line)
            c += 1

def main():

    userVectors = {}
    movies = []


    inFile = open(sys.argv[1],'r')

    with open(sys.argv[1]) as f:
        line = f.readline()
        movies = line.strip().split("|")
        movies.pop(0)
    #save the column/row headers (conditions/genes) into an array
    
    colHeaders = inFile.next().strip().split()[1:]
    rowHeaders = []
    dataMatrix = []

    counter = 0
    for line in inFile:
        data = line.strip().split("|")      
        rowHeaders.append(data[0])
        ratings = [float(x) for x in data[1:]]
        dataMatrix.append(ratings)
    
        userVectors[rowHeaders[counter]] = ratings
        counter = counter + 1


    fold_num = 10

    partition(fold_num, sys.argv[1])

    fold_name = ""
    #' + str(fold_num) + '

    fold_file = "folds_" + str(fold_num) + "/review_fold_0.txt"

    curUVs = userVectors


    test = ['aa','bb','cc']
    # print 'range'
    # print range(test)

    userPredictions = {}
    f = open(fold_file, 'r')
    for userLine in f: #current fold
        user = userLine.strip().split("|")
        user = user.pop(0)
        listOfRatedMovies = []
        userPredictions[user] = []
        #print curUVs[user]
        movieIndex = 0
        # print 'users----'
        # print curUVs[user]
        # print 'users----'
        for movie in curUVs[user]:
            if(movie != 0.0):
                listOfRatedMovies.append(movieIndex)
            movieIndex = movieIndex + 1

        #print listOfRatedMovies
        #choose random movie to remove and note position of movie and original rating                           
        removedMovie = random.choice(listOfRatedMovies)
        #print removedMovie
        userPredictions[user].append(removedMovie) #the movie index
        userPredictions[user].append(curUVs[user][removedMovie]) #movie value

        #Once recorded, remove movie from test vectors
        curUVs[user][removedMovie] = 0.0

    cluster_results = cluster(curUVs)


    print '/*user predictions--------'
    print userPredictions
    print 'user predictions--------*/'

    # print 'cluster results---------'
    # print cluster_results
    # print 'cluster results---------'
    #     print curUVs

    cluster_nums = cluster_results[0]   
    cluster_ids = cluster_results[1] 

    


    foldFile = open(fold_file, 'r')
    for userLine in foldFile: 
        user = userLine.strip().split("|")
        user = user.pop(0)
        movieNeedingPrediction = userPredictions[user][0] #movieIndex

        finalCounter = 0
        for userId in cluster_ids:
            if user == userId:
                goldenIndex = finalCounter

            finalCounter = finalCounter + 1

        spread = 10 #indexes we'll look at in either direction of the movie direction





        #predictedRating = 
        #print movieNeedingPrediction




    # print userVectors
    # print rowHeaders
    # print dataMatrix
    # print movies

    
   
    #print ', '.join(rowHeaders)
   # print ', '.join(dataMatrix)






if __name__ == "__main__":
    main()