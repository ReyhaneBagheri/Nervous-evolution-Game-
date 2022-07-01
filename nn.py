import numpy as np

def activation(x):
        """
        The activation function of our neural network, e.g., Sigmoid, ReLU.
        :param x: Vector of a layer in our network.
        :return: Vector after applying activation function.
        """
        # TODO (Implement activation function here)sigmoid
        return 1 / (1 + np.exp(-x))


class NeuralNetwork:

    def __init__(self, layer_sizes):
        """
        Neural Network initialization.
        Given layer_sizes as an input, you have to design a Fully Connected Neural Network architecture here.
        :param layer_sizes: A list containing neuron numbers in each layers. For example [3, 10, 2] means that there are
        3 neurons in the input layer, 10 neurons in the hidden layer, and 2 neurons in the output layer.
        """
        # TODO (Implement FCNNs architecture here)
        self.layer1_size=layer_sizes[0]
        self.layer2_size=layer_sizes[1]
        self.layer3_size=layer_sizes[2]
        self.weight1=np.random.normal(size=(self.layer2_size, self.layer1_size))
        self.bayas1=np.zeros((self.layer2_size, 1))
        self.weight2=np.random.normal(size=(self.layer3_size, self.layer2_size))
        self.bayas2=np.zeros((self.layer3_size, 1))
        


    def forward(self, x):
        """
        Receives input vector as a parameter and calculates the output vector based on weights and biases.
        :param x: Input vector which is a numpy array.
        :return: Output vector
        """
        # TODO (Implement forward function here)
        x = x.reshape((self.layer1_size, 1))
        sigmoid1 = activation(self.weight1 @ x + self.bayas1)
        sigmoid2 = activation(self.weight2 @ sigmoid1 + self.bayas2)
        return sigmoid2



