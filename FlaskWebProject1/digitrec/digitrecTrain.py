# -*- coding: utf-8 -*-
"""
Created on Sat Jan 07 22:27:58 2017

@author: yuwan
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from spyre import server
import Imp


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
    
def KNN(pixels, n=5, verbose=False):
    a = Imp.np.array(pixels)
    sim = trainData.dot(a)
    sortResult = Imp.np.argsort(sim)
    
    if verbose:
        Imp.plt.imshow(a.reshape((28,28)))
        for i in reversed(list(sortResult[-n:])):
            print(sim[i], trainTarget[i])
            Imp.plt.figure()
            Imp.plt.imshow(trainData[i].reshape((28,28)))
    
    return int(Imp.sp.stats.mode([trainTarget[i] for i in reversed(list(sortResult[-n:]))])[0][0])


mnist = Imp.sk.datasets.fetch_mldata('MNIST original', data_home=r"d:\temp\skdata")
trainData, testData, trainTarget, testTarget = Imp.sk.cross_validation.train_test_split(mnist.data, mnist.target, test_size=0.1, random_state=1)
trainData = trainData > 200
testData = testData > 200

#Imp.plt.hist(trainData.reshape((50000*784,)))

clf = Imp.sk.linear_model.LogisticRegression(tol=1., C=0.01)
clf.fit(trainData, trainTarget)
print("accuracy: %s" % Imp.sk.metrics.accuracy_score(testTarget, clf.predict(testData)))

classCoefs = [list(classCoef) for classCoef in clf.coef_]
classBiases = list(clf.intercept_)

#pred = [Imp.np.argmax(Predict(classCoefs, classBiases, row)) for row in testData]
#print("accuracy: %s" % Imp.sk.metrics.accuracy_score(testTarget, pred))
# accuracy: 0.8715
#
#with open(r"model.py", "w") as outF:
#    outF.write("classCoefs = %s\n" % repr(classCoefs))
#    outF.write("classBiases = %s\n" % repr(classBiases))

    
            

idealTarget = []
lrPred = []
knn5Pred = []
knn1Pred = []
images = []
for no, line in enumerate(open(r"d:\temp\TestWebApp\FlaskWebProject1\digitrec\data.tsv")):
    target, image = line.split("\t")
    image = eval(image)
    target = int(target)
    #Imp.plt.figure()
    #Imp.plt.imshow(Imp.np.array(image).reshape((28,28)))
    
    idealTarget.append(target)
    
    lrPred0 = Imp.np.argmax(Predict(classCoefs, classBiases, image))
    knn5Pred0 = KNN(image, n=5, verbose=False)
    knn1Pred0 = KNN(image, n=1)
    lrPred.append(lrPred0)
    knn5Pred.append(knn5Pred0)
    knn1Pred.append(knn1Pred0)
    images.append(image)


print("n: %s" % (no+1))
print("LR accuracy: %s" % Imp.sk.metrics.accuracy_score(idealTarget, lrPred))   
print("KNN5 accuracy: %s" % Imp.sk.metrics.accuracy_score(idealTarget, knn5Pred))   
print("KNN1 accuracy: %s" % Imp.sk.metrics.accuracy_score(idealTarget, knn1Pred))   

lrWrongIndices = []
for no, (lrPred0, knn5Pred0, knn1Pred0, idealTarget0) in enumerate(zip(lrPred, knn5Pred, knn1Pred, idealTarget)):
    if lrPred0 != idealTarget0:
        lrWrongIndices.append(no)



class UnderstandLRWrongPred(server.App):
    title = "Understand LR Wrong Prediction"
    inputs = [{ "type":"dropdown",
               "label":"wrong prediction index",
               "options" : [{"label": str(wrongIndex), "value": str(wrongIndex)} for wrongIndex in lrWrongIndices],
               "key":"wrongIndex",
                "action_id":"update_data"}]

    controls = [{   "type" : "hidden",
                    "id" : "update_data"}]

    outputs = [{"type":"html",
                 "id":"html",
                 "control_id" : "update_data"
                },
                {"type":"plot",
                 "id": "plot",
                 "control_id" : "update_data"
                }
            ]

    def getHTML(self, params):
        idx = int(params["wrongIndex"])        
        return "Label: %s, LR Pred: %s, KNN5 Pred: %s" % (idealTarget[idx], lrPred[idx], knn5Pred[idx])
        
    def getPlot(self, params):
        idx = int(params["wrongIndex"])        
        
        pixels = images[idx]
        n = 5
        
        a = Imp.np.array(pixels)
        sim = trainData.dot(a)
        sortResult = Imp.np.argsort(sim)
        
        fig = Imp.plt.figure(figsize=(12,8))
        Imp.plt.subplot(251)
        
        Imp.plt.imshow(a.reshape((28,28)))
        Imp.plt.title("Original graph")
        
        for figNo, idx in enumerate(sortResult[-n:]):
                Imp.plt.subplot(2, 5, figNo+6)
                Imp.plt.imshow(trainData[idx].reshape((28,28)))
                Imp.plt.title("label: %s" % trainTarget[idx])

        
        return fig

app = UnderstandLRWrongPred()
app.launch()


