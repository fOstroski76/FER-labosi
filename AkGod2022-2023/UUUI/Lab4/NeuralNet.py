import numpy as np

class NeuralNetwork() :

    def __init__(self, configuration, input_dim):
        
        self.layers = []
        self.layers.append(input_dim)  # to add input dimension to all layers list
        for el in configuration.strip().split("s")[:-1] :
            self.layers.append(int(el))

        self.layers.append(1) # to add the output dimension
        
        self.configuration = configuration
        self.input_dim = input_dim
        self.biasesMatrix = []
        self.weightsMatrix = []
        self.fitnessScore = 0

        #print("New NN: conf:{}, inputDim:{}".format(configuration,input_dim))

        #print(self.layers)

    def __lt__(self, other) :

        return self.fitnessScore < other.fitnessScore

    def generateRandomNNValues(self) :

        for i in range(1, len(self.layers)) :

            self.biasesMatrix.append(np.random.normal(loc=0, scale=0.01, size=(self.layers[i],1)))
            self.weightsMatrix.append(np.random.normal(loc=0,scale=0.01,size=(self.layers[i-1], self.layers[i])))

        #self.printInitialValues()


    def addNNCalculatedValues(self, inputBiasMatrix, inputWeightMattrix) :

        self.biasesMatrix.append(inputBiasMatrix)
        self.weightsMatrix.append(inputWeightMattrix)
        
    
    def activation_func(self,x) :
        
        #print("X:",x)
        result = 1 / (1 + np.exp(-x))

        #print("result:",result)
        return result


    def forward_advance(self, input_Xs) :
        
        result = 0
        tempResult = input_Xs
        

        for currWeight, currBias in zip(self.weightsMatrix[:-1], self.biasesMatrix[:-1]) :
            
            tempResult = np.dot(currWeight.T, tempResult) + currBias

            tempResult = self.activation_func(tempResult)


        #print("WM:",self.weightsMatrix,"BM:", self.biasesMatrix)
        result = np.dot(self.weightsMatrix[-1].T, tempResult) + self.biasesMatrix[-1]

        return result
    

    def calculateFitness(self, computed_MSE) :

        result = float(0)

        result = np.abs(1 / (computed_MSE))

        self.fitnessScore = result
    
        return result
    

    def printInitialValues(self) :

        print("Biases:")
        for el in self.biasesMatrix :
            print(el)
            print(" ")
        print("Shape of biases:",self.biasesMatrix.shape)
        print("Weights:") 
        for el in self.weightsMatrix :
            print(el)
            print(" ")


    
def calculateError(computed_Ys, expected_Ys) :

    result = float(0)

    #print(computed_Ys, expected_Ys)
    for eY, cY in zip(computed_Ys.T, expected_Ys) :
        
        #print("ey:",eY)
        #print("cy:",cY)
        #print("ey-cy sqr:",np.square((cY - eY)))
        result += np.square((cY - eY))

    #print("Prije cutta:",result)
    result = result / (len(computed_Ys.T)) #* 10)

    result = float(result)
    #print(result)
    
    return result

    
def createNewPopulation(population_size,configuration, input_size) :

    newPop = list()
    for i in range(population_size) :

        entity = NeuralNetwork(configuration,input_size)
        entity.generateRandomNNValues()

        newPop.append(entity)
    
    return newPop