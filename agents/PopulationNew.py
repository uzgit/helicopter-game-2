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
        child1 = genome1
        child2 = genome2
        separator = np.random.randint(1, len(genome1.weights))
        # Child 1 is going to inherit weights/bias of parent 1 before separator and weights/bias of parent 2 after separator
        for i in range(separator, len(genome1.weights)):
            child1.weights[i] = genome2.weights[i]
            child2.weights[i] = genome1.weights[i]
            child1.bias[i] = genome2.bias[i]
            child2.bias[i] = genome1.bias[i]

        return [child1, child2]


    def mutation(self, genome):
        separator = np.random.randint(1, len(genome.weights))
        if np.random.random() < mutation_probability:
            [a, b] = genome.weights[separator].shape
            genome.weights[separator] = np.random.rand(a, b)-0.5

        return genome

    def createNewGeneration(self): #creates 1 generation

        newPopulation = sorted(self.population, key=lambda x: -x.getFitness())
        self.bestFitness = newPopulation[0].getFitness()

        #if self.bestFitness > self.bestFitnessEver:
        #    self.bestFitnessEver = self.bestFitness
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
                iter = len(newPopulation)
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
        print("Average distance of generation", self.generationNumber+1, "is:", self.averageFitness)
        print("Elapsed time:", self.elapsedTime, "seconds")

        if self.generationNumber < self.generationsToRun:
            # return list(iteritems(self.population)), self.config
            self.startTime = time.time()
            return True
        else:
            # return None, self.config
            self.startTime = time.time()
            return False



