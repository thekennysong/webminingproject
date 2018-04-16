import sys
import random

def createSentFile(fileName):
    sentFile = open(fileName, 'w')

    for i in range(100):
        user = str(i)
        #pad user id with 0's up to 5 digits
        while(len(user) < 5):
            user = "0" + user
        curLine = user
        #generate random sentiments for movies
        for j in range(50):
            posSent = random.random()
            negSent = random.random()
            sent = posSent - negSent
            curLine += "|" + str(sent)
        sentFile.write(curLine+'\n')
    
    sentFile.close()

if(len(sys.argv) < 2):
    print("Please include name of output file. python createSampleFile.py outputFile.")
else:
    createSentFile(sys.argv[1])

        
