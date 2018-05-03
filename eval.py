import sys

eval_count = 0
def main(evaluations):
    error1 = 0.5
    error2 = 0.25
    error3 = 0.1
    goodPredictions1 = 0
    goodPredictions2 = 0
    goodPredictions3 = 0
    samePolarity = 0
    avgSimilarity = 0.0
    for e in evaluations:
        #print(e)
        polarity = e[2]
        similarity = e[3]
        if similarity < error1:
            goodPredictions1 += 1
        if similarity < error2:
            goodPredictions2 += 1
        if similarity < error3:
            goodPredictions3 += 1
        if polarity == 1:
            samePolarity += 1
        avgSimilarity += similarity
    precision1 = goodPredictions1 / len(evaluations)
    precision2 = goodPredictions2 / len(evaluations)
    precision3 = goodPredictions3 / len(evaluations)
    polaritySimilarity = samePolarity / len(evaluations)
    avgSimilarity = avgSimilarity / len(evaluations)
    print("Precision with error bound (0.5): %s" % precision1)
    print("Precision with error bound (0.25): %s" % precision2)
    print("Precision with error bound (0.1): %s" % precision3)
    print("Precision on polarity: %s" % polaritySimilarity)
    print("Average similarity: %s" % avgSimilarity)
    #print(len(evaluations))


def evaluation(pVectors):
    evaluations = []
    for user in pVectors:
        # evaluation = [userID, movie, polarity, similarity]
        evaluation = []
        user, movie, originalRating, predictedRating = user[0], user[1], user[2], user[3]
        evaluation.append(user)
        evaluation.append(movie)
        originalRating, predictedRating = float(originalRating), float(predictedRating)
        if (originalRating > 0.0) and (predictedRating > 0.0):
            evaluation.append(1) 
        elif (originalRating < 0.0) and (predictedRating < 0.0):
            evaluation.append(1)
        else:
            evaluation.append(0)
        similarity = abs(originalRating - predictedRating)
        evaluation.append(float(similarity))
        evaluations.append(evaluation)
    return evaluations       

def getPredictionVectors(file):
    userPredictionVectors = []
    f = open(file, "r", encoding="utf-8")
    eval_count = 0
    for line in f:
        if line[0] == "f":
            continue
        #print(line)
        user = []
        user.append(line.split("|")[0])
        user.append(line.split("|")[1])
        user.append(line.split("|")[2])
        user.append(line.split("|")[3])
        userPredictionVectors.append(user)
        eval_count += 1
    #print(eval_count)
    return userPredictionVectors    

if __name__ == "__main__":
    predictionVectors = getPredictionVectors(sys.argv[1])
    evaluations = evaluation(predictionVectors)
    main(evaluations)
