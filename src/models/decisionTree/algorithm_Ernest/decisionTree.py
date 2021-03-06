#!/usr/bin/python3

import csv
import pandas as pd
import math
import API_Ernest
import pickle

filename = './data/data_Ernest/trainData_holdOut_Ernest.csv'
dataSet = pd.read_csv(filename)

predictfeature = 'Attrition'
entireAttrSet = API_Ernest.attrSetGenerate(dataSet)
decisionTree = {}

def treeGenerate(dataSet, decisionTree) :
    print('create new node')
    ent_attrition = API_Ernest.entD(dataSet, 'Attrition')

    global entireAttrSet

    dataSet = dataSet.reset_index(drop=True) 

    df = dataSet.copy()
    currentAttrSet = API_Ernest.attrSetGenerate(df)

    ifSame = API_Ernest.ifSameClass(dataSet, predictfeature)
    if ifSame :
        decisionTree[predictfeature] = ifSame 
        return

    if (len(currentAttrSet) == 0 or API_Ernest.ifAllClassSame(dataSet)) :
        
        featureClass = API_Ernest.getClass(dataSet, predictfeature)
        decisionTree[predictfeature] = featureClass

    #compute every feature and get best one
    gain = 0
    gain_ratio = 0
    bestFeature = ''
    bestBoundary = 0

    print('Current Function: find best feature')
    for index in dataSet.columns :
        if index != 'Attrition' :
            gainDic_feature = API_Ernest.getGainDicByFeature(dataSet, index, ent_attrition, 'Attrition', entireAttrSet)
            print('Current feature', index)
            print('Gain',gainDic_feature['gain'])


            if gainDic_feature['gain'] > gain :
                gain = gainDic_feature['gain']
                bestFeature = index
                if bestFeature == 'YearsSinceLastPromotion' :
                    print(gainDic_feature)
                if gainDic_feature['continuous'] :
                    bestBoundary = gainDic_feature['bestBoundary'] 
    
    decisionTree[bestFeature] = {}

    if (entireAttrSet[bestFeature]['ifContinuous']) :
            decisionTree[bestFeature]['>='+ str(bestBoundary)]= {}
            decisionTree[bestFeature]['<'+ str(bestBoundary)]= {}
            subDataBig = dataSet.loc[dataSet[bestFeature] >= bestBoundary ]
            subDataSmall = dataSet.loc[dataSet[bestFeature] < bestBoundary ]
            del subDataBig[bestFeature]
            del subDataSmall[bestFeature]
         
            if (len(subDataBig) == 0) :
                featureClass = API_Ernest.getClass(dataSet, predictfeature)
                decisionTree[bestFeature]['>='+ str(bestBoundary)][predictfeature] = featureClass
            else :
                treeGenerate(subDataBig, decisionTree[bestFeature]['>='+ str(bestBoundary)])
            if (len(subDataSmall) == 0) :
                featureClass = API_Ernest.getClass(dataSet, predictfeature)
                decisionTree[bestFeature]['<'+ str(bestBoundary)][predictfeature] = featureClass
            else :
                treeGenerate(subDataSmall, decisionTree[bestFeature]['<'+ str(bestBoundary)])

    else :
        for index in entireAttrSet[bestFeature]['Attribution'] :
            decisionTree[bestFeature][index] = {}
            subData = dataSet.loc[dataSet[bestFeature] == index ]
            del subData[bestFeature]
            
            if (len(subData) == 0) :

                featureClass = API_Ernest.getClass(dataSet, predictfeature)
                decisionTree[bestFeature][index][predictfeature] = featureClass
            else :
                treeGenerate(subData, decisionTree[bestFeature][index])

    return decisionTree
    
decisionTree = treeGenerate(dataSet, decisionTree)
#print(decisionTree)

#print(type(entireAttrSet['BusinessTravel']) )
#print(dataSet.loc[dataSet['MonthlyRate'] <=100000]) 
#print(dataSet['Department'])

 
pickle.dump(decisionTree, open("./models/decisionTree_Ernest", "wb"))
 
#print(obj2)


