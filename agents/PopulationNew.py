"""
    This class implements the core evolution algorithm:
        1. Evaluate fitness of all genomes.
        2. Generate the next generation from the current population.
        3. Go to 1.
    """
from __future__ import print_function

from .Config import *
from .Genome import *
import time
import copy


class Population(object):

    def __init__(self):

        self.generationNumber=0
        self.population = []
        self.populationSize = pop_size
        self.averageFitness = 0
        self.bestFitness = 0
        self.elapsedTime = 0
        self.generationsToRun = 0
        self.startTime = 0
        self.bestFitnessEver = 0

        for i in range(self.populationSize):
            self.population.append(Genome(num_inputs, num_outputs, nodes_per_layer, [weight_min_value, weight_max_value]))

        self.startTime = time.time()

    def crossover(self, genome1, genome2):

            alpha = 0.6
            # alpha=np.random.randint(0, 1)
            #        genome1_array = []
            #        genome2_array = []
            #        for k in range (len(genome1.weights)):
            #            genome1_array.append(np.squeeze(np.asarray(genome1.weights[k])))
            #            genome2_array.append(np.squeeze(np.asarray(genome2.weights[k])))
            A = copy.deepcopy(genome1.weights)
            B = copy.deepcopy(genome1.weights)
            I = copy.deepcopy(genome1.weights)
            for i in range(len(genome1.weights)):
                (rows, columns) = genome1.weights[i].shape
                for j in range(rows):
                    for k in range(columns):
                        B[i][j, k] = max(genome1.weights[i][j, k], genome2.weights[i][j, k])
                        A[i][j, k] = min(genome1.weights[i][j, k], genome2.weights[i][j, k])
                        I[i][j, k] = abs(genome1.weights[i][j, k] - genome2.weights[i][j, k])

            C1 = copy.deepcopy(genome1)
            C2 = copy.deepcopy(genome1)
            for i in range(len(A)):
                (rows, columns) = A[i].shape
                for j in range(rows):
                    for k in range(columns):
                        C1.weights[i][j, k] = np.random.uniform(A[i][j, k] - alpha * I[i][j, k],
                                                                B[i][j, k] + alpha * I[i][j, k])
                        C2.weights[i][j, k] = np.random.uniform(A[i][j, k] - alpha * I[i][j, k],
                                                                B[i][j, k] + alpha * I[i][j, k])
            # counter = 0

            return [C1, C2]


    def mutation(self, genome):

        for i in genome.weights:
            b = np.random.uniform(0, 1, i.shape) #mutation chance
            c = np.random.uniform(-1, 1, i.shape) #new values
            mask1 = (b<mutation_probability)*1 #b values on proper positions
            mask2 = (b>=mutation_probability)*1 #reversed mask2
            temp = np.multiply(mask2, i)
            i = temp + np.multiply(c, mask1)


        return genome

    def createNewGeneration(self): #creates 1 generation

        newPopulation = sorted(self.population, key=lambda x: -x.getFitness())
        self.bestFitness = newPopulation[0].getFitness()

        if self.bestFitness > self.bestFitnessEver:
            self.bestFitnessEver = self.bestFitness
            with open('data.txt', 'a') as output:
                output.write(str(newPopulation[0].weights)+"\n")
                output.write(str(self.bestFitness)+"\n")
                output.close()


        fitnessList = []
        for i in newPopulation:
            fitnessList.append(i.getFitness())

        self.averageFitness = np.mean(fitnessList)

        self.population = []

        #30% of best genomes
        for i in range(int(elitism_portion*pop_size)):
            self.population.append(newPopulation[i])

        #20% of random other genomes
        randomGenomes = np.random.randint(int(elitism_portion*pop_size), pop_size, int(random_others_portion*pop_size))
        #what if a same genome is selected multiple times
        for i in randomGenomes:
            self.population.append(newPopulation[i])

        #50% new children
        listOfParents = []

        iter = len(newPopulation)-1
        while(len(listOfParents) < int(0.5*pop_size)):
            if np.random.random() < (newPopulation[iter].getFitness())/self.bestFitness:
                listOfParents.append(newPopulation[iter])
            if iter <= 0:
                iter = len(newPopulation)-1
            else:
                iter -= 1

        for i in range(int(0.5*pop_size)-1):

            [a, b] = self.crossover(listOfParents[i], listOfParents[i+1])
            self.population.append(self.mutation(a))
            self.population.append(self.mutation(b))

        return self.population

    def getPopulation(self):
        return self.population

    def initRun(self, n):
        self.generationsToRun = n
        self.generationNumber += 1
        #self.startTime = time.time()

    def finishRun(self):

        #print([genome.Fitness for genome in self.population])


       # Create the next generation from the current generation.
        self.population = self.createNewGeneration()
        self.elapsedTime = time.time() - self.startTime
        print("Best Distance of generation: ", self.bestFitness)
        print("Average distance of generation", self.generationNumber+1, "is:", self.averageFitness)
        print("Elapsed time:", self.elapsedTime, "seconds")
        print("Best Distance reached is: ", self.bestFitnessEver)

        if self.generationNumber < self.generationsToRun:
            # return list(iteritems(self.population)), self.config
            self.startTime = time.time()
            return True
        else:
            # return None, self.config
            self.startTime = time.time()
            return False



