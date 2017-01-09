# -*- coding: utf-8 -*-
"""
Created on Sat Jan 07 22:46:44 2017

@author: yuwan
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math
import sys
import os
import os.path


def GetProgPath():
    return os.path.dirname(__main__.__file__)
    
sys.path.append(os.path.split(os.path.realpath(__file__))[0])


from model import *

def Predict(sample):
    scoreList = []
    for i in range(len(classCoefs)):
        classCoef = classCoefs[i]
        classBias = classBiases[i]
        score = sum(pixel * coef for (pixel, coef) in zip(sample, classCoef)) + classBias
        scoreList.append(math.exp(score))
    sumScore = sum(scoreList)
    scoreList = [unnormScore/sumScore for unnormScore in scoreList]
    return scoreList



    

