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

    def recombination(self, target, mutant):
        cross_points = np.random.rand(len(target.weights)) < crossp
        trial = copy.deepcopy(mutant)
        for i in range(len(cross_points)):
            if cross_points[i] == False:
                trial.weights[i] = target.weights[i]
        return trial


    def mutation(self, target, a, b, c):

        mutant = copy.deepcopy(target)
        for i in range(len(target.weights)):
            mutant.weights[i] = a.weights[i] + mutation_rate * (b.weights[i] - c.weights[i])
        return mutant


    def createNewGeneration(self): #creates 1 generation

        for i in range(self.populationSize):

            target = self.population[i]
            indexes = [idx for idx in range(self.populationSize) if idx != i]
            selected = np.random.choice(indexes, 3, replace=False)
            a = self.population[selected[0]]
            b = self.population[selected[1]]
            c = self.population[selected[2]]

            mutant = self.mutation(target, a, b, c)
            trial = self.recombination(target, mutant)
            self.population[i] = trial
        return self.population

    def getPopulation(self):
        return self.population

    def initRun(self, n):
        self.generationsToRun = n
        self.generationNumber += 1

    def finishRun(self):


       # Create the next generation from the current generation.
        pop = self.population
        self.population = self.createNewGeneration()
        for i in range(self.populationSize):
            if self.population[i].getFitness() < pop[i].getFitness():
                self.population[i] = pop[i]

        newPopulation = sorted(self.population, key=lambda x: -x.getFitness())
        self.bestFitness = newPopulation[0].getFitness()

        fitnessList = []
        for i in newPopulation:
            fitnessList.append(i.getFitness())

        self.averageFitness = np.mean(fitnessList)

        if self.bestFitness > self.bestFitnessEver:
            self.bestFitnessEver = self.bestFitness
            with open('data.txt', 'a') as output:
                output.write(str(newPopulation[0].weights) + "\n")
                output.write(str(self.bestFitness) + "\n")
                output.close()
            self.elapsedTime = time.time() - self.startTime
           

        print("Best Distance of generation: ", self.bestFitness)
        print("Average distance of generation", self.generationNumber+1, "is:", self.averageFitness)
        print("Elapsed time:", self.elapsedTime, "seconds")
        print("Best Distance reached is: ", self.bestFitnessEver)
        print("_________________________________________________________")

        if self.generationNumber < self.generationsToRun:
            self.startTime = time.time()
            return True
        else:
            self.startTime = time.time()
            return False



