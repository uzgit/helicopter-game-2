pop_size              = 150 #has to be >=10

# network parameters
num_inputs              = 12
num_outputs             = 2
nodes_per_layer = [8, 4]
num_hidden              = len(nodes_per_layer)


# connection weight options
weight_init_mean        = 0.0
weight_init_stdev       = 1.0
weight_max_value        = 100
weight_min_value        = -100
weight_mutate_power     = 0.5
weight_mutate_rate      = 0.8
weight_replace_rate     = 0.1

number_of_generations = 150
mutation_probability = 0.01
mutation_rate = 0.8
crossp = 0.5
elitism_portion = 0.3
random_others_portion = 0.2
currentToPBest = 0.1