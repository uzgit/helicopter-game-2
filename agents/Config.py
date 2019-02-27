
fitness_criterion     = max
fitness_threshold     = 3.9
pop_size              = 150
reset_on_extinction   = False

# node activation options
activation_default      = 'sigmoid'
activation_mutate_rate  = 0.0
activation_options      = 'sigmoid'

# node aggregation options
aggregation_default     = sum
aggregation_mutate_rate = 0.0
aggregation_options     = sum

# node bias options
bias_init_mean          = 0.0
bias_init_stdev         = 1.0
bias_max_value          = 30
bias_min_value          = -30
bias_mutate_power       = 0.5
bias_mutate_rate        = 0.7
bias_replace_rate       = 0.1

# genome compatibility options
compatibility_disjoint_coefficient = 1.0
compatibility_weight_coefficient   = 0.5

# connection add/remove rates
conn_add_prob           = 0.7
conn_delete_prob        = 0.3

# connection enable options
enabled_default         = True
enabled_mutate_rate     = 0.01

feed_forward            = True
initial_connection      = 'full'

# node add/remove rates
node_add_prob           = 0.2
node_delete_prob        = 0.2

# network parameters
num_inputs              = 11
num_outputs             = 2
nodes_per_layer = [9, 6, 3]
num_hidden              = len(nodes_per_layer)

# node response options
response_init_mean      = 1.0
response_init_stdev     = 0.0
response_max_value      = 30
response_min_value      = -30
response_mutate_power   = 0.0
response_mutate_rate    = 0.0
response_replace_rate   = 0.0

# connection weight options
weight_init_mean        = 0.0
weight_init_stdev       = 1.0
weight_max_value        = 3
weight_min_value        = -3
weight_mutate_power     = 0.5
weight_mutate_rate      = 0.8
weight_replace_rate     = 0.1

compatibility_threshold = 3.0

species_fitness_func = max
max_stagnation       = 20
species_elitism      = 2

elitism            = 2
survival_threshold = 0.2

number_of_generations = 500
mutation_probability = 0.01
elitism_portion = 0.3
random_others_portion = 0.2