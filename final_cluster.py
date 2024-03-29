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
from scipy.spatial.distance import pdist
import sys
import os
import random
from scipy.cluster import hierarchy

def cluster(curUVs, numClusts, userIds):
    #open the file assuming the data above is in a file called 'dataFile'
    #inFile = open(sys.argv[1],'r')
    #save the column/row headers (conditions/genes) into an array
    colHeaders = []
    rowHeaders = []
    dataMatrix = []

    Xclust = hierarchy.fclusterdata(curUVs, numClusts, 'maxclust')

    clusters = {}
    userCluster = {}

    for i in range(len(Xclust)):
        if Xclust[i] not in clusters:
            clusters[int(Xclust[i])] = []
        clusters[int(Xclust[i])].append(userIds[i])
        userCluster[userIds[i]] = int(Xclust[i])


    return clusters,userCluster

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
    for foldIndex in range(0,10):
        fold_file = "folds_" + str(fold_num) + "/review_fold_" + str(foldIndex) + ".txt"

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
      
            for movie in curUVs[user]:
                if(movie != 0.0):
                    #if movieIndex in listOfRatedMovies != True:
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

        
        userIds = []
        vectors = []
        for userId, ratings in curUVs.iteritems():
            userIds.append(userId)
            vectors.append(ratings)   


        # # #Hierarchal clustering with the total number of users/10 for the number of clusters
        numClusts = len(userIds)/100



        cluster_results,user_cluster = cluster(vectors, numClusts, userIds)
        #print cluster_results

        foldFile = open(fold_file, 'r')


        for userLine in foldFile: 
         
            user = userLine.strip().split("|")
            user = user.pop(0)
            movieNeedingPrediction = userPredictions[user][0] #movieIndex

            userGroupClusterIndex = 0
            #theUserGroup = []
            finalCounter = 0

            clusterUsersIds = cluster_results[user_cluster[user]]

            clusteredRatings = []


            for gUser in clusterUsersIds:            
                needMovieRating = curUVs[gUser][movieNeedingPrediction]
                if(needMovieRating > 0):
                    clusteredRatings.append(needMovieRating)

            if len(clusteredRatings) == 0:
                clusterId = user_cluster[user]
                surroundingClusters = cluster_results[clusterId] 
                incrementer = 0
                while(len(clusteredRatings) == 0):
                    for x in range(0,incrementer):
                        if(clusterId+x < len(cluster_results)):
                           
                            surroundingCluster = cluster_results[clusterId + x]
                        
                            for scUser in surroundingCluster:
                                needMovieRating = curUVs[scUser][movieNeedingPrediction]
                                if(needMovieRating > 0):
                                    clusteredRatings.append(needMovieRating)

                    if len(clusteredRatings) == 0:
                        for x in range(0,incrementer):
                            if(clusterId > incrementer):
                                surroundingCluster = cluster_results[clusterId - x]
                                
                                for scUser in surroundingCluster:
                                    needMovieRating = curUVs[scUser][movieNeedingPrediction]
                                    if(needMovieRating > 0):
                                        clusteredRatings.append(needMovieRating)
                    incrementer = incrementer + 1

            predictedRating = sum(clusteredRatings)/len(clusteredRatings)

            userPredictions[user].append(predictedRating)


        print fold_file    

        for final in userPredictions:
                print final + "|" + movies[userPredictions[final][0]] + "|" + str(userPredictions[final][1])+ "|" + str(userPredictions[final][2])





if __name__ == "__main__":
    main()