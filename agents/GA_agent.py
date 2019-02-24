from __future__ import print_function
import os
import neat
from .PopulationNew import *
import numpy as np
from .Genome import *
import random




# Initial skeleton for agents
class Agent():
    #nn_architecture = []
    #params_values={}

    def __init__(self, generations=500):

        local_dir = os.path.dirname(__file__)
        config_file = os.path.join(local_dir, 'config-feedforward-with-segments')

        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
        """
        self.nn_architecture = [
            {"input_dim": 11, "output_dim": 50, "activation": "relu"},
            {"input_dim": 50, "output_dim": 70, "activation": "relu"},
            {"input_dim": 70, "output_dim": 100, "activation": "relu"},
            {"input_dim": 100, "output_dim": 30, "activation": "relu"},
            {"input_dim": 30, "output_dim": 1, "activation": "sigmoid"},
        ]

        np.random.seed(99)
        #self.params_values = {}

        for idx, layer in enumerate(self.nn_architecture):
            layer_idx = idx + 1
            layer_input_size = layer["input_dim"]
            layer_output_size = layer["output_dim"]

            self.params_values['W' + str(layer_idx)] = np.random.randn(
                    layer_output_size, layer_input_size) * 0.1
            self.params_values['b' + str(layer_idx)] = np.random.randn(
                    layer_output_size, 1) * 0.1
"""
        self.generations = generations
        self.population_object = Population()
        #self.population_object.add_reporter(neat.StdOutReporter(True))
        self.stats = neat.StatisticsReporter()
        #self.population_object.add_reporter(self.stats)
        #self.population_object.add_reporter(neat.Checkpointer(5))
        #self.config = self.population_object.init_run(n=self.generations)
        self.genome_index = 0
        genome = self.population_object.getPopulation()[self.genome_index]
        self.current_network = genome
        self.DefaultGenome = Genome(11, 1, [50, 70, 100, 30], [-30, 30])


    """
    def sigmoid(self, Z):
        return 1 / (1 + np.exp(-Z))

    def relu(self, Z):
        return np.maximum(0, Z)

    def single_layer_forward_propagation(self, A_prev, W_curr, b_curr, activation="relu"):
        Z_curr = np.matmul(W_curr, A_prev) + b_curr

        if activation is "relu":
            activation_func = self.relu
        elif activation is "sigmoid":
            activation_func = self.sigmoid
        else:
            raise Exception('Non-supported activation function')

        return activation_func(Z_curr), Z_curr

    def full_forward_propagation(self, X):
        # memory = {}
        A_curr = X

        for idx, layer in enumerate(self.nn_architecture):
            layer_idx = idx + 1
            A_prev = A_curr

            activ_function_curr = layer["activation"]
            W_curr = self.params_values["W" + str(layer_idx)]
            b_curr = self.params_values["b" + str(layer_idx)]
            A_curr, Z_curr = self.single_layer_forward_propagation(A_prev, W_curr, b_curr, activ_function_curr)

            # memory["A" + str(idx)] = A_prev
            # memory["Z" + str(layer_idx)] = Z_curr

        return A_curr
"""
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
        Inputs.shape = (1, 11)
        output = self.current_network.full_forward_propagation(Inputs)

        if output[0,0] > output[0,1]:
            action = "up"
       # print(output)

        return action