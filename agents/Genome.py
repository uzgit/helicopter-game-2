import numpy as np

class Genome(object):
    def __init__(self, inputs, outputs, layers, rangeOfWeights):
        self.NumberOfInputs = inputs
        self.NumberOfOutputs = outputs
        self.NumberOfLayers = len(layers)
        self.Fitness = 0
        self.weights = []
        self.bias = []
        self.activation = []

        for i in range(self.NumberOfLayers):
            if i == 0:
                weight_matrix = np.asmatrix(np.random.rand(self.NumberOfInputs, layers[i]))
                weight_matrix = np.dot(rangeOfWeights[0] + (rangeOfWeights[1] - rangeOfWeights[0]), weight_matrix)
                self.weights.append(weight_matrix)
                #print(self.NumberOfInputs, layers[i])
                bias_matrix = np.asmatrix(np.random.rand(1, layers[i]))
                bias_matrix = np.dot(rangeOfWeights[0] + (rangeOfWeights[1] - rangeOfWeights[0]), bias_matrix)
                self.bias.append(bias_matrix)
                self.activation.append("relu")
                #self.activation.append("sigmoid")
            else:
                weight_matrix = np.asmatrix(np.random.rand(layers[i - 1], layers[i]))
                weight_matrix = np.dot(rangeOfWeights[0] + (rangeOfWeights[1] - rangeOfWeights[0]), weight_matrix)
                #print(layers[i - 1], layers[i])
                self.weights.append(weight_matrix)
                bias_matrix = np.asmatrix(np.random.rand(1, layers[i]))
                bias_matrix = np.dot(rangeOfWeights[0] + (rangeOfWeights[1] - rangeOfWeights[0]), bias_matrix)
                self.bias.append(bias_matrix)
                self.activation.append("relu")
                #self.activation.append("sigmoid")

        weight_matrix = np.asmatrix(np.random.rand(layers[i], self.NumberOfOutputs))
        weight_matrix = np.dot(rangeOfWeights[0] + (rangeOfWeights[1] - rangeOfWeights[0]), weight_matrix)
        self.weights.append(weight_matrix)
        self.bias.append(0)
        self.activation.append("sigmoid")
        #print(layers[i], self.NumberOfOutputs)
        # print(self.bias)
        #print(self.activation)

    def sigmoid(self, Z):
        return 1 / (1 + np.exp(-Z))

    def relu(self, Z):
        return np.maximum(0, Z)

    def single_layer_forward_propagation(self, A_prev, W_curr, b_curr, activation="relu"):
        Z_curr = np.matmul(A_prev, W_curr) + b_curr

        if activation is "relu":
            activation_func = self.relu
        elif activation is "sigmoid":
            activation_func = self.sigmoid
        else:
            raise Exception('Non-supported activation function')

        return activation_func(Z_curr), Z_curr

    def full_forward_propagation(self, X):
        A_curr = X

        for idx in range(self.NumberOfLayers + 1):
            A_prev = A_curr
            activ_function_curr = self.activation[idx]
            W_curr = self.weights[idx]
            b_curr = self.bias[idx]
            A_curr, Z_curr = self.single_layer_forward_propagation(A_prev, W_curr, b_curr, activ_function_curr)

        return A_curr

    def getFitness(self):
        return self.Fitness
