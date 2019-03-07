from __future__ import print_function
from .PopulationNew import *
from .Genome import *
import time



# Initial skeleton for agents
class Agent():

    def __init__(self, generations=500):

        self.generations = generations
        self.population_object = Population()
        self.genome_index = 0
        self.current_network = self.population_object.getPopulation()[self.genome_index]


    # This is the name of the constructor used by the game.
    # Be sure to call the actual constructor here.
    def Agent(self):
        self.__init__()

    def reset(self, game_state):

        genome = self.population_object.getPopulation()[self.genome_index]
        genome.Fitness = game_state["distance_traveled"]

        self.genome_index += 1
        if self.genome_index == len(self.population_object.getPopulation()):
            self.population_object.finishRun()
            self.population_object.initRun(n=self.generations)
            self.genome_index = 0
            self.startTime = time.time()
        else:
            genome = self.population_object.getPopulation()[self.genome_index]
            self.current_network = genome

    def get_action(self, game_state):
        """
        Gets a non-visual state representation of the game.

        Returns
        -------

        dict
            * player distance traveled
            * player y position.
            * player velocity.
            * player distance to floor.
            * player distance to ceiling.
            * next block x distance to player.
            * next blocks top y location,
            * next blocks bottom y location.

            See code for structure.

        """
        inputs = list(game_state.values())[1:8]
        inputs[0] /= 500
        inputs[1] /= 50
        inputs[2] /= 500
        inputs[3] /= 500
        inputs[4] /= 500
        inputs[5] /= 500
        inputs[6] /= 500
        for i in game_state["segments"]:
            inputs.append(i)

        action = None
        Inputs=np.array(inputs)
        Inputs.shape = (1, 12)
        output = self.current_network.full_forward_propagation(Inputs)

        if output[0, 0] > output[0, 1]:
            action = "up"

        return action