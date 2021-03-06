import math

# compute Entropy
def entD (dataSet, feature) :
    values = dataSet[feature].value_counts(normalize=True)
    sum = 0
    for i in values :
        sum += i* math.log2(i)
    sum = -sum
    return sum


# compute gain and IV, return a Dict
def getGainDicByFeature(dataSet, feature, entDValue, entD_feature,entireAttrSet) :

    valuesRateList = dataSet[feature].value_counts(normalize=True)
    num = len(valuesRateList)
    valuesList = dataSet[feature]

    attiData = []
    entList = []
    entSum = 0
    sum = 0
    IV = 0

    # Use dichotomy to handle continuous discrete attributes
    # Judge whether it is a continuous value

    #print(entireAttrSet[feature])
    #print(isinstance( entireAttrSet['Department'],dict) )
    if( entireAttrSet[feature]['ifContinuous']) :
        dict = _getGainDicByFeatureInContinuous(dataSet, feature, entDValue, entD_feature )
        return dict
    else :
        for i in range(num) :
            attiData.append(dataSet[dataSet[feature] == valuesRateList.index[i] ])
            entList.append (entD (attiData[i], entD_feature))
            entSum += valuesRateList[valuesRateList.index[i]] * entList[i]

            ratio = valuesRateList[valuesRateList.index[i]]
            sum += ratio * math.log2(ratio)

        IV = -sum
        gain = entDValue - entSum
        return {'gain':gain, 'IV':IV, 'continuous': False}


def attrSetGenerate (dataSet) :
    #print('current Function: attrSetGenerate') 

    attrSet = {}
    ent_attrition = entD(dataSet, 'Attrition')
    for index in dataSet.columns :
        if index!='Attrition' :
            #print('current Feature: ',index)
            
            attrSet[index] = {}
            valuesList = dataSet[index]
            valuesRateList = dataSet[index].value_counts(normalize=True)
            num = len(valuesRateList)
            #print(valuesList.index[0])
            #Judge whether it is a continuous value
            if( len(valuesRateList) >=15 and str(valuesList[valuesList.index[0]]).isdigit()) :
                #dict = _getGainDicByFeatureInContinuous(dataSet, index, ent_attrition, 'Attrition')
                #attrSet[index] = {'bestBoundary': dict['bestBoundary']} 
                attrSet[index] = {'ifContinuous':True}

            else :
                attrSet[index]['Attribution'] = []
                for i in range(num) :
                    attrSet[index]['Attribution'].append(valuesRateList.index[i])
                    #print(valuesRateList.index[i])
                    attrSet[index]['ifContinuous'] = False

    #print(attrSet)
    return attrSet
    

def _getGainDicByFeatureInContinuous (dataSet, feature, entDValue, entD_feature) :
    #order
    orderedDataSet = dataSet.sort_values(by=feature)
    orderedValuesList = orderedDataSet[feature].reset_index(drop=True)

    bestBoundary = ( orderedValuesList[0] + orderedValuesList[1] ) / 2
    bestGain = 0
    IV = 0
    bestI = 0

    ListNum = len(dataSet)

    #Loops get the best demarcation
    for i in range(ListNum) :
        P = (i+1)/ListNum
        attiData = []
        entList = []

        attiData.append(orderedDataSet[0:i+1])
        attiData.append(orderedDataSet[i+1:])

        entList.append( entD( attiData[0], entD_feature ))
        entList.append( entD( attiData[1], entD_feature ))

        entSum = P * entList[0] + (1-P) * entList[1]
        gain = entDValue - entSum

        if gain >= bestGain :
            bestGain = gain
            bestBoundary = ( orderedValuesList[i] + orderedValuesList[i+1] ) / 2;
            bestI = i
            IV = -(P* math.log2(P) + (1-P) * math.log2(1 - P))

    return {'gain': bestGain, 'IV':IV, 'continuous': True, 'bestBoundary': bestBoundary, 'bestI':bestI}


def ifSameClass(dataSet, feature) :

    valuesRateList = dataSet[feature].value_counts(normalize=True)

    if (len(valuesRateList) == 1):
        return valuesRateList.index[0]
    else :
        return 0

def ifAllClassSame(dataSet) :
    df2 = dataSet.copy()
    del df2['Attrition']
    for index in df2.columns :
        values = df2[index].value_counts(normalize=True)
        if(len(values) != 1) :
            return 0 

    return 1

def getClass(dataSet, predictfeature) :
     
    bestClass = ''
    bestRate = 0
    valuesRateList = dataSet[predictfeature].value_counts(normalize=True)
    
    for i in range(len(valuesRateList)) :
        if valuesRateList[valuesRateList.index[i]] > bestRate :
            bestClass = valuesRateList.index[i]
            bestRate = valuesRateList[valuesRateList.index[i]]

    return bestClass







