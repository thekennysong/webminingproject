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
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np


def main():
    # raw_results  = open('sampleSentOutput.txt', 'w') 
    # print raw_results
    # raw_results.close()
    
    a = np.random.multivariate_normal([10, 0], [[3, 1], [1, 4]], size=[100,])
    b = np.random.multivariate_normal([0, 20], [[3, 1], [1, 4]], size=[50,])
    X = np.concatenate((a, b),)
    print X.shape  # 150 samples with 2 dimensions
    #plt.scatter(X[:,0], X[:,1])
    print X[:,0]
    print X[:,1]


    with open('out_rating_movies.txt', 'r') as file:
        # x = f.read()
        # x.replace('\n', ' ')
        # print x
        counter = 0 
       
        convertedList = []
        theList = [l.strip() for l in file]
        for user in theList:
            if(counter > 0):
                converted = user.split("|")
                converted.pop(0)
                converted = [float(i) for i in converted]
                #print(converted)
                converted = array(converted)
                convertedList.append(converted)
                counter = counter + 1
            else:
                template_line = user
                print template_line
                counter = counter + 1
                
        convertedList = array(convertedList)
        data = vstack(convertedList)

        
        #print data
        # Performs k-means on a set of observation vectors forming k
        # clusters. This yields a code book mapping centroids to codes and vice versa.
        # The k-means algorithm adjusts the centroids until sufficient progress cannot be made, i.e. the change in 
        # distortion since the last iteration is less than some threshold.
        # Parameters: 
        # obs : ndarray
        # Each row of the M by N array is an observation vector. The columns are the features seen during each observation. The features must be whitened first with the whiten function.

        # k_or_guess : int or ndarray
        # The number of centroids to generate. A code is assigned to each centroid, which is also the row index of the centroid in the code_book matrix generated.
        # The initial k centroids are chosen by randomly selecting observations from the observation matrix. Alternatively, passing a k by N array specifies the initial k centroids.

        # iter : int
        # The number of times to run k-means, returning the codebook with the lowest distortion. This argument is ignored if initial centroids are specified with an array for the k_or_guess paramter. This parameter does not represent the number of iterations of the k-means algorithm.

        centroids,_ = kmeans(data,50, 150)
        idx,distortion = vq(data, centroids)
        print distortion
        #print data[idx==0,0],data[idx==0,1]

        plot(data[idx==0,0],data[idx==0,1],'ob',
        data[idx==10,0],data[idx==1,1],'or',
        data[idx==2,0],data[idx==2,1],'og',
        data[idx==3,0],data[idx==3,1],'r+',
        data[idx==4,0],data[idx==4,1],'b+',
        data[idx==5,0],data[idx==5,1],'g+',
        data[idx==6,0],data[idx==6,1],'c+',
        data[idx==7,0],data[idx==7,1],'m+',
        data[idx==8,0],data[idx==8,1],'y+',
        data[idx==9,0],data[idx==9,1],'w+') # third cluster points
        plot(centroids[:,0],centroids[:,1],'sm',markersize=8)
        show()


if __name__ == "__main__":
    main()