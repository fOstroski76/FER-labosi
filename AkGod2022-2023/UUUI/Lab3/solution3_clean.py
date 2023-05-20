import argparse
import math
import copy

# class definitions

class ID3 :         

    def __init__(self) :

        pass


    def fit(self, matrix, startEntropy, classLabel) :
        
        level = 0
        runAlgorithm(matrix,startEntropy,classLabel,level, None, matrix)
        

    def predict (self,data_matrix, data_matrix_dict) :
        
        runPredictions(data_matrix, data_matrix_dict)
    
    class Node :

        def __init__(self,feature,level) :

            self.feature = feature
            self.level = level
            self.parentNode = None
            self.childNodes = list()
            self.isRoot = False
            self.isLeaf = False
            self.isXvalueOption = False
            self.theirMatrix = None
            self.isBigXValue = None
            self.isVerySpecial = None

        def __str__(self):
            if self.isLeaf == False :
                if self.isXvalueOption == False :
                    return str("{}:{}=".format(self.level,self.feature))

                else:
                    return str("{} ".format(self.feature))
            
            else :
                if self.isVerySpecial == None :
                    if self.isXvalueOption == True :
                        return str("{}").format(self.feature)
                    else :
                        return str("{}".format(self.feature[6:]))

                else :
                    return str("{} {}".format(self.feature,self.isVerySpecial))
        def printAttrs(self):

            print("Node:{} ,isRoot:{}, isLeaf:{}, isXvalueOption:{}, level:{}".format(self.feature,self.isRoot,self.isLeaf,self.isXvalueOption,self.level))

# method definitions 

def runAlgorithm( matrix,startEntropy,classLabel,level, previousNode, previousMatrix) :

    global globalObjectList
    global counterToDetermineRoot
    global maxDepth

    if level >= maxDepth : 
        previousNode.isLeaf = True
        return "Done"


    if (matrix == previousMatrix ) and level != 0:

        previousNode.isLeaf = True

        return "Done"

    
    resultFeature = argmax(data_matrix= matrix, startEntropy=startEntropy,classLabel= classLabel)
    
    resultNode = model.Node(resultFeature,level+1)
    resultNode.parentNode = previousNode
    resultNode.theirMatrix = matrix
    
    if previousNode != None :
        previousNode.childNodes.append(resultNode)

    if counterToDetermineRoot == 0 :
        resultNode.isRoot = True
        counterToDetermineRoot = 5

    if resultFeature.startswith("[END]:") :

        resultNode.isLeaf = True
        resultNode.parentNode = previousNode
        globalObjectList.append(resultNode)
        return "Done"
    
        
    possiblefeaturesOfResult = sorted(list(set(list(matrix[resultFeature][0].values()))))

    for feat  in possiblefeaturesOfResult :

        featureNode = model.Node(feat,level+2)
        featureNode.parentNode = resultNode
        featureNode.isXvalueOption = True
        featureNode.theirMatrix = matrix
        resultNode.childNodes.append(featureNode)

        
        yCountDict = dict()
        allYsList = matrix[classLabel][0]

        possibleYvalues = sorted(list(set(matrix[classLabel][0].values())))
        
        for y in possibleYvalues :
            yCountDict[y] = 0

        for elY in allYsList:
            
            if matrix[resultFeature][0][elY] == feat :
                yCountDict[allYsList[elY]] += 1
        
        featureEntropy = entropy(*yCountDict.values())
        
        
        runAlgorithm(reduceMatrix(matrix,feat,resultFeature),featureEntropy,classLabel,level + 1, featureNode, matrix)
        globalObjectList.append(featureNode)
        
    globalObjectList.append(resultNode)
        

def runPredictions(testDataMatrix, testdataMatrixDict) :

    global globalObjectList
    global test_ClassLabel
    global test_noOfLines
    global byDepth

    
    predictionsList = list()

    for line in testDataMatrix[1:] :
        rowDict = dict()
        for i in range(0, len(testDataMatrix[0].split(","))) :
            rowDict[testDataMatrix[0].split(",")[i]] = line.split(",")[i]
    
        open = list()
        visited = list()
        
    
        for obs in globalObjectList :
            if obs.isRoot == True :
                open.append(obs)

        
        nodeDFS(open[0],visited,predictionsList,rowDict,testdataMatrixDict)
        byDepth = 0

    
    print("[PREDICTIONS]:", end = ' ')

    for pred in predictionsList :
        print(pred, end= ' ') 

    toCompare = list(testdataMatrixDict[test_ClassLabel][0].values())
    calculateAccuracyAndConfMatrix(predictionsList,toCompare)


def nodeDFS ( node, visited,predictionsList, rowDict, testdataMatrixDict) :

    global byDepth
    
    if node.level > maxDepth :
    
        byDepth = 1
        predictionsList.append(str(returnMostCommonY(reduceMatrix(node.theirMatrix,node.feature,node.parentNode.feature),test_ClassLabel)))
        return str(returnMostCommonY(node.theirMatrix,test_ClassLabel))
    
    if node.isXvalueOption == False : # weather, humidity , etc..
        
        visited.append(node)
        if node.isLeaf == False :
            for child in node.childNodes :
                
                if child.feature in set(list(testdataMatrixDict[node.feature][0].values())) :
                    if child.feature in rowDict.values() :
                        for key in rowDict.keys() :
                           
                            if rowDict[key] == child.feature and child not in visited and key == child.parentNode.feature :
                                nodeDFS(child,visited,predictionsList, rowDict,testdataMatrixDict)
                                

                elif child.feature not in set(list(testdataMatrixDict[node.feature][0].values())) :
                    
                    if byDepth != 1 :
                        predictionsList.append(str(returnMostCommonY(child.theirMatrix,test_ClassLabel)))
                    return str(returnMostCommonY(child.theirMatrix,test_ClassLabel))
                         

        elif node.isLeaf == True and str(node) in set(list(testdataMatrixDict[test_ClassLabel][0].values())) :  # neki y
        
            predictionsList.append(str(node))
            return str(node)

        elif node.isLeaf == True :
            
            predictionsList.append(str(returnMostCommonY(node.theirMatrix,test_ClassLabel)))
            return str(returnMostCommonY(node.theirMatrix,test_ClassLabel))
        
    elif node.isXvalueOption == True :

        visited.append(node)

        for child in node.childNodes :

            if child not in visited :
                nodeDFS(child,visited,predictionsList,rowDict,testdataMatrixDict)
                return


def calculateAccuracyAndConfMatrix( predictions, original) :

    accuCounter = 0
    possibleVals = sorted(list(set(original)))
    ConfMatrix = dict() 

    for i in range(len(possibleVals)) :
        for j in range(len(possibleVals)) :
            ConfMatrix[tuple((possibleVals[i],possibleVals[j]))] = 0

    for el1, el2 in zip(predictions, original) :

        if el1 == el2 :
            accuCounter += 1

        else:
            pass

        ConfMatrix[(el1,el2)] += 1
    
    print(" ")
    print("[ACCURACY]: {}".format('{:.5f}'.format(accuCounter/len(original))))
    print(" ")
    print("[CONFUSION_MATRIX]:")

    rows = sorted(set(label[0] for label in ConfMatrix.keys()))
    columns = sorted(set(label[1] for label in ConfMatrix.keys()))

   
    for column in columns:
        for row in rows:
            print(ConfMatrix.get((row, column), 0), end=' ')
        print()


def entropy (*args) :   #log2 entropy

    sum = 0
    result = 0
    for arg in args :

        sum = sum + arg

    for arg in args :

        var = arg / sum

        if var != 0 :
            result = result + (var * math.log2(var))

        else :
            result = result + 0

    return  abs(round(result,4))


def argmax (data_matrix, startEntropy, classLabel) : 
        
        if startEntropy == 0 :
            allYs = list(data_matrix[classLabel][0].values()) # they are all the same
        
            return "[END]:{}".format(allYs[0])
            
        featureRatiosSaved = dict()
        

        for key in data_matrix.keys() :

            possibleFeatures = sorted(list(set(data_matrix[key][0].values())))

            featureRatios = dict()

            for featureValue in possibleFeatures :
                featureRatios[featureValue] = list(data_matrix[key][0].values()).count(featureValue)
                
            featureRatiosSaved[key] = featureRatios


        allYsList = data_matrix[classLabel][0]
        
        possibleYs = set(data_matrix[classLabel][0].values())
    
        informationGains = dict()

        for el in featureRatiosSaved.keys() :
            
            entropies = dict()
            
            
            for el2 in featureRatiosSaved[el] :
                
                tempPosYdict = dict()
                for elem in possibleYs :
                    tempPosYdict[elem] = 0

                for el3 in allYsList :                    

                    if data_matrix[el][0][el3] == el2 :
                        tempPosYdict[allYsList[el3]] += 1

                
                tempTuple = ((sum(tempPosYdict.values())),el2)
                entropies[tempTuple] = entropy(*tempPosYdict.values())
            
            
            tempSuma = 0
            for element in entropies :
                tempSuma += ((element[0] / len(allYsList)) * entropies[element])
            informationGain = startEntropy - tempSuma

            if informationGain != 0 :

                formattedInformationGain = f"{informationGain : .4f}"
                informationGains[el] = formattedInformationGain

            
        informationGains.__delitem__(classLabel)

        maxUinfo = -100

        for key in informationGains.keys() :
            if float(informationGains[key]) > float(maxUinfo) :
                maxUinfo = informationGains[key]

        sviSmaxom = list()
        for key in informationGains.keys() :
            if float(informationGains[key]) == float(maxUinfo) :
                sviSmaxom.append(key)
        
        minAlph = sviSmaxom[0]
        for el in sviSmaxom :
            if el < minAlph :
                minAlph = el

        maxIG = minAlph

        return maxIG

    

def reduceMatrix( inputMatrix, reducingValue, resultFeature) :

    matrix_copy = copy.deepcopy(inputMatrix)
    matrixCopy_copy = copy.deepcopy(matrix_copy)
    indexesToNotRemove = list()

    for ele in matrix_copy:
        
        if ele == resultFeature:

            rowsByColumn = matrix_copy[ele][0]
            
            for elem in rowsByColumn.keys() :
                
                if rowsByColumn[elem] == reducingValue :
                    indexesToNotRemove.append(elem)

    
    for ele in matrix_copy :
        rowsByColumn = matrix_copy[ele][0]
        rowsByColumnCopy = matrixCopy_copy[ele][0]

        for key in rowsByColumn.keys() :
            if key not in indexesToNotRemove :
                rowsByColumnCopy[key] = None


    for ele in list(matrixCopy_copy.values()):
        tempDict = ele[0]
        tempDict = {key: value for key, value in tempDict.items() if value is not None}
        ele[0] = tempDict
        
    return matrixCopy_copy


def returnMostCommonY( inputMatrix, classLabel) :

    ySdict = inputMatrix[classLabel][0]
    diffValues = sorted(list(set(ySdict.values())))
    countDict = dict()

    for el in diffValues :
        countDict[el] = 0
    
    for el in ySdict.values() :
        countDict[el] += 1
    
    max = -100
    for el in countDict.values() :
        if el > max :
            max = el
    
    sviSMaxValue = list()
    for el in countDict.keys() :
        if countDict[el] == max :
            sviSMaxValue.append(el)
    
    minAlph = sviSMaxValue[0]
    for el in sviSMaxValue :
        if el < minAlph :
            minAlph = el

    return minAlph


# parsing input
parser = argparse.ArgumentParser()

parser.add_argument('file_dirs',nargs='+')

args = parser.parse_args()

try :
    maxDepth =int(args.file_dirs[2])

except (IndexError) :

    maxDepth = 10000



if args.file_dirs :

    with open(args.file_dirs[0],'r') as data :  # train dataset

        header = list()
        stored_data = list()
        matrix = dict()
        classCounter = 0
        noOfLines = 0 

        for line in data :
            stored_data.append(line.strip())
            noOfLines += 1

        for el in stored_data[0].split(",") :
            header.append(el)
            classCounter += 1

        #print("Header:",header)
        classLabel = header[-1]
        print("[CL] : ",classLabel)

        for i in range(0, classCounter) :
            
            tempColumn = list()
            tempDict = dict()
            for j in range(0, noOfLines) :
                if j != 0 :
                    tempDict[j] = stored_data[j].split(",")[i]
                
            tempColumn.append(tempDict)
            #print(tempColumn)

            matrix[header[i]] = tempColumn    


        possibleClassLabelValues = sorted(list(set(matrix[classLabel][0].values())))
        
        ratiosOfValues = dict()
        for value in possibleClassLabelValues :
            ratiosOfValues[value] = (list(matrix[classLabel][0].values()).count(value))

        
    with open(args.file_dirs[1],'r') as test_data :  # prediction dataset

        stored_test_data = list()
        test_header = list()
        test_matrix = dict()
        test_classCounter = 0
        test_noOfLines = 0 

        for line in test_data :
            stored_test_data.append(line.strip())
            test_noOfLines += 1


        for el in stored_test_data[0].split(",") :
            test_header.append(el)
            test_classCounter += 1
        
        test_ClassLabel = test_header[-1]


        for i in range(0, test_classCounter) :
            
            tempTestColumn = list()
            tempTestDict = dict()
            for j in range(0, test_noOfLines) :
                if j != 0 :
                    tempTestDict[j] = stored_test_data[j].split(",")[i]
                
            tempTestColumn.append(tempTestDict)
            
            test_matrix[test_header[i]] = tempTestColumn 
        

print(" ")
print("[CATEGORIES_COUNT] : ",classCounter)
print("[ROW_COUNT] : ",noOfLines)

print(" ")

byDepth = 0

globalObjectList = list()
counterToDetermineRoot = 0
startLevel = 1
model = ID3()
model.fit(matrix= matrix, startEntropy= entropy(*ratiosOfValues.values()), classLabel= classLabel)

print("[BRANCHES]:")

if maxDepth == 10000 :
    for obj in globalObjectList:
        if obj.isLeaf == True :
            path = list()
            path.append(obj)
            
            while obj.parentNode != None :
                    
                    obj = obj.parentNode
                    path.append(obj)

            pathway = "".join(str(node) for node in reversed(path))
            print(pathway)

else:
    for obj in globalObjectList:
        if obj.level == maxDepth + 1 :
            obj.isLeaf = True
            valjue = reduceMatrix(obj.theirMatrix,obj.feature,obj.parentNode.feature)
            valjue2 = returnMostCommonY(valjue,classLabel)
            obj.isVerySpecial = valjue2
                        
        else :
            obj.isLeaf = False
    
    for obj in globalObjectList:
        if obj.isLeaf == True :
            path2 = list()
            path2.append(obj)

            while obj.parentNode != None:
                obj = obj.parentNode 
                
                path2.append(obj)
            pathway2 = "".join(str(node) for node in reversed(path2))
            print(pathway2)
            
print(" ")

model.predict(stored_test_data,test_matrix)

