"""
    script to evenly partition vector file k times
"""
import sys
import os

"""
    creates a directory 'folds_k' and places k vector txt files in it.
    
    ex output (k=3)
        folds_3/review_fold_0.txt
        folds_3/review_fold_0.txt
        folds_3/review_fold_0.txt
"""
def partition(k, file):
    k = int(k)
    files = []
    fold_file = "folds_%s/" % str(k)
    if not os.path.isdir(fold_file):
        os.mkdir(fold_file)
    for i in range(0,k):
       f = open(fold_file + "/review_fold_%s.txt" % str(i), "w", encoding="utf-8")
       files.append(f)
    c = 0
    v = open(file, "r", encoding="utf-8")
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
    

"""
    run with $python fold.py k file
    k = number of partitions desired
    file = vector file to be partitioned 
"""
if __name__ == "__main__":
    k = sys.argv[1]
    read_file = sys.argv[2]
    partition(k, read_file)