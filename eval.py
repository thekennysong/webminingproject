import sys

def main(evaluations, originalVectors):
    error1 = 0.5
    error2 = 0.25
    error2 = 0.1
    goodPredictions1 = 0
    goodPredictions2 = 0
    goodPredictions3 = 0
    samePolarity = 0
    avgSimilarity = 0.0
    for e in evaluations:
        if similarity < error1:
            goodPredictions1 += 1
        if similarity < error2:
            goodPredictions2 += 1
        if similarity < error3:
            goodPredictions3 += 1
        if e[2] == 1:
            samePolarity += 1
        avgSimilarity += e[3]
    baseSize = 0
    f = open(originalVectors, "r", encoding="utf-8")
    for line in f:
        baseSize+=1
    precision1 = goodPredictions1 / baseSize
    precision2 = goodPredictions2 / baseSize
    precision3 = goodPredictions3 / baseSize
    polaritySimilarity = samePolarity / baseSize
    avgSimilarity = avgSimilarity / len(evaluations)
    print("Precision with error bound (0.5): %s" % precision1)
    print("Precision with error bound (0.25): %s" % precision2)
    print("Precision with error bound (0.1): %s" % precision3)
    print("Precision on polarity: %s" % polaritySimilarity)
    print("Average similarity: %s" % avgSimilarity)


def evaluation(pVectors):
    for user in pVectors:
        # evaluation = [userID, movie, polarity, similarity]
        evaluation = []
        user, movie, originalRating, predictedRating = pVectors[0], pVectors[1], pVectors[2], pVectors[3]
        evaluation.append(user)
        evaluation.append(movie)
        if originalRating and predictedRating > 0.0:
            evaluation.append(1) 
        elif originalRating and predictedRating < 0.0:
            evaluation.append(1)
        else:
            evaluation.append(0)
        similarity = abs(originalRating - predictedRating)
        evaluation.append(similarity)
    return evaluations        

def getVectors(file):
    userVectors = []
    movies = {}
    with open(file, "r", encoding="utf-8"):
        i = 0
        for line in file:
            userVectors.append(line)
    return userVectors

def getPredictionVectors(file):
    userPredictionVectors = []
    with open(file, "r", encoding="utf-8"):
        for line in file:
            user = []
            user.append(line.split("|")[0])
            user.append(line.split("|")[1])
            user.append(line.split("|")[2])
            user.append(line.split("|")[3])
            userPredictionVectors.append(user)
    return userPredictionVectors    

if __name__ == "__main__":
    originalVectors = getVectors(sys.argv[1])
    predictionVectors = getPredictionVectors(sys.argv[2])
    evaluations = evaluations(predictionVectors)
    main(evaluations, originalVectors)