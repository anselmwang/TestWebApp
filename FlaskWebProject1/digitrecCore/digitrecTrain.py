# -*- coding: utf-8 -*-
"""
Created on Sat Jan 07 22:27:58 2017

@author: yuwan
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import Imp



#digits = Imp.sk.datasets.load_digits()
#
#data = digits.images.reshape((digits.images.shape[0], -1))
#data = data > 8
#target = digits.target
#trainData = data[：1700]
#trainTarget = target[:1700]
#testData = data[1700:]
#testTarget = target[1700:]

mnist = Imp.sk.datasets.fetch_mldata('MNIST original', data_home=r"d:\temp\skdata")
trainData, testData, trainTarget, testTarget = Imp.sk.cross_validation.train_test_split(mnist.data, mnist.target, test_size=0.1, random_state=1)
trainData = trainData > 100
testData = testData > 100

#Imp.plt.hist(trainData.reshape((50000*784,)))

clf = Imp.sk.linear_model.LogisticRegression(tol=0.1)
clf.fit(trainData, trainTarget)

print("accuracy: %s" % Imp.sk.metrics.accuracy_score(testTarget, clf.predict(testData)))

classCoefs = [list(classCoef) for classCoef in clf.coef_]
classBiases = list(clf.intercept_)

import math
def Predict(classCoefs, classBiases, sample):
    scoreList = []
    for i in range(len(classCoefs)):
        classCoef = classCoefs[i]
        classBias = classBiases[i]
        score = sum(pixel * coef for (pixel, coef) in zip(sample, classCoef)) + classBias
        scoreList.append(math.exp(score))
    sumScore = sum(scoreList)
    scoreList = [unnormScore/sumScore for unnormScore in scoreList]
    return scoreList


#print(Predict(classCoefs, classBiases, data[1]))
#print(clf.predict_proba(data[1]))

#print(repr(classCoefs))
#print(repr(classBiases))
pred = [Imp.np.argmax(Predict(classCoefs, classBiases, row)) for row in testData]
print("accuracy: %s" % Imp.sk.metrics.accuracy_score(testTarget, pred))
# accuracy: 0.8715

with open(r"model.py", "w") as outF:
    outF.write("classCoefs = %s\n" % repr(classCoefs))
    outF.write("classBiases = %s\n" % repr(classBiases))
