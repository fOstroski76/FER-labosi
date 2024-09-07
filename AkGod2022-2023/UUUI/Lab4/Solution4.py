import argparse
import numpy as np
import NeuralNet as NN
import copy
import random


def evaluatePopulation(population, input_Xs, input_Ys) :
    
    errors = []

    for neuNet in population :

        computed_Ys = neuNet.forward_advance(input_Xs)
        #print("comp. ys:",computed_Ys)
        error = NN.calculateError(computed_Ys,input_Ys)
        errors.append(error)
        #print("error:",error)
        neuNet.fitnessScore = neuNet.calculateFitness(error)
    
    sortedErrors = sorted(errors)

    return sortedErrors[0]


def selectParents(population, conf, inputDim) :

    parent1 = NN.NeuralNetwork(conf,inputDim)
    parent2 = NN.NeuralNetwork(conf,inputDim)
    fitnessSum = 0
    for neuNet in population :
        fitnessSum += neuNet.fitnessScore
    
    randomNumber1 = np.random.uniform(0,1)
    threshhold = 0

    for candidateNeuNet in population :
        threshhold += candidateNeuNet.fitnessScore / fitnessSum

        if randomNumber1 < threshhold :
            parent1 = copy.deepcopy(candidateNeuNet)
            break

    randomNumber2 = np.random.uniform(0,1)
    threshhold2 = 0

    for candidateNeuNet in population :
        threshhold2 += candidateNeuNet.fitnessScore / fitnessSum

        if randomNumber2 < threshhold2 :
            
            parent2 = copy.deepcopy(candidateNeuNet)

            if parent1 != parent2 :
                break
    
    return tuple((parent1,parent2))


def crossover(parent1, parent2,conf,inputDim) :

    child1 = NN.NeuralNetwork(conf,inputDim)
    child2 = NN.NeuralNetwork(conf,inputDim)

    childrenWeights = []
    childrenBiases = []

    for wP1, wP2 in zip(parent1.weightsMatrix, parent2.weightsMatrix) :
        #print("parent1:{}   parent2:{}".format(parent1.weightsMatrix,parent2.weightsMatrix))
        child1.weightsMatrix.append(np.add(wP1,wP2) / 2)
        child2.weightsMatrix.append(np.add(wP1,wP2) / 2)

        #print("ch1weights:",child1.weightsMatrix)
        #print("ch2weights",child2.weightsMatrix)

    for bP1, bP2 in zip(parent1.biasesMatrix, parent2.biasesMatrix) :
        child1.biasesMatrix.append(np.add(bP1,bP2) / 2)
        child2.biasesMatrix.append(np.add(bP1,bP2) / 2)

        
    child1 = copy.deepcopy(child2)
    #child1.addNNCalculatedValues(childrenWeights,childrenBiases)
    #child2.addNNCalculatedValues(childrenWeights,childrenBiases)

    #print("Kreirao djecu")

    return child1, child2


def mutate(child, p, K) :

    for i in range(len(child.weightsMatrix)) :

        for weight in child.weightsMatrix[i] :

            if random.random()  < (p) :
                weight += np.random.normal(loc=0,scale=K) 

    #print("mutirao!")
    for i in range(len(child.biasesMatrix)) :
        for bias in child.biasesMatrix[i] :
            if random.random() < (p) :
                bias += np.random.normal(loc=0,scale=K)

# parsing the input

parser = argparse.ArgumentParser()

parser.add_argument('--popsize',type=int)
parser.add_argument('--elitism',type=int)
parser.add_argument('--p',type=float)
parser.add_argument('--K',type=float)
parser.add_argument('--iter',type=int)
parser.add_argument('--train',type=str)
parser.add_argument('--test',type=str)
parser.add_argument('--nn',type=str,help="Define the neural network type.",choices=['5s', '20s', '5s5s'])

args = parser.parse_args()

#print(args)

if args.train and args.test:

    with open(args.train,'r') as trainData :
        contentsTrain = trainData.readlines()
        #print(contents)

        noOfRows = 0
        """ print("Train:")
        for line in contentsTrain :
            line = line.strip()
            noOfRows += 1
            print(line) """

        
        columnNo = len(contentsTrain[0].strip().split(','))
        noOfRows -= 1
        #print(columnNo)
        #print(noOfRows)
        inputX = list()
        inputY = list()
        for i in range(columnNo -1) :
            temparr = list()

            for line in contentsTrain :
                line = line.strip()
                if line != contentsTrain[0].strip() :
                    temparr.append(line.split(',')[i])

            inputX.append(temparr)
        
        inputXasNParray = np.array(inputX,dtype=float)

        #print(inputXasNParray)

        for line in contentsTrain :
            line = line.strip()
            if line != contentsTrain[0].strip() :
                inputY.append(line.split(',')[-1])
                       
        inputYasNParray = np.array(inputY,dtype=float)

        #print(inputYasNParray)

        #entity = NN.NeuralNetwork(args.nn, columnNo - 1)
        #entity.generateRandomNNValues()
    
    with open(args.test,'r') as testData :
        contentsTest = testData.readlines()

        """print("Test:")
        for line in contentsTest :
            line = line.strip()
            print(line)
        #print(contentsTest) """

        inputXtest = list()
        inputYtest = list()
        for i in range(columnNo -1) :
            temparr2 = list()

            for line in contentsTest :
                line = line.strip()
                if line != contentsTest[0].strip() :
                    temparr2.append(line.split(',')[i])

            inputXtest.append(temparr2)
        
        inputXasNParrayTest = np.array(inputXtest,dtype=float)

        #print(inputXasNParray)

        for line in contentsTest :
            line = line.strip()
            if line != contentsTest[0].strip() :
                inputYtest.append(line.split(',')[-1])
                       
        inputYasNParrayTest = np.array(inputYtest,dtype=float)

        #print(inputYasNParrayTest)

    
    # genetic algorithm 

    start_population = NN.createNewPopulation(args.popsize, args.nn, columnNo - 1)
    evalResult = evaluatePopulation(start_population, inputXasNParray, inputYasNParray)

    elites = list()
    sortedPopulation = sorted(start_population, reverse= True)

    for i in range(args.elitism) :
        elites.append(sortedPopulation[i])
    
    for i in range (1, args.iter + 1) :
        
        evalResult = evaluatePopulation(start_population, inputXasNParray, inputYasNParray)

        if i == 1 :
            print("[Train error @0]: {}".format(evalResult))

        if i % 2000 == 0 :
            print("[Train error @{}]: {}".format(i, evalResult))

        new_population = list()
        
        for el in elites :
            new_population.append(el)
        
        while len(new_population) < args.popsize :

            parents = selectParents(start_population,args.nn,columnNo -1)
            child1, child2 = crossover(parents[0], parents[1],args.nn, columnNo - 1)
            mutate(child1,args.p,args.K)
            mutate(child2,args.p,args.K)
            new_population.append(child1)
            new_population.append(child2)

        start_population = new_population
        elites.clear()

        newEvalResult = evaluatePopulation(start_population, inputXasNParray, inputYasNParray)
        sortedPopulationNew = sorted(start_population, reverse= True)    
        for i in range(args.elitism) :
            elites.append(sortedPopulationNew[i])

    lastEvalResult = evaluatePopulation(start_population, inputXasNParrayTest, inputYasNParrayTest)
    print("[Test error]: {}".format(lastEvalResult))
        