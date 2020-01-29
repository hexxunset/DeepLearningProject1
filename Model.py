from Function import *
import numpy as np


class Model:
    def __init__(self, learning_rate, loss_type):
        self.layers = []
        self.learning_rate = learning_rate
        self.loss_type = loss_type

    def add_layer(self, no_nodes, activation, input_dim):
        weights = self.get_weights(no_nodes, input_dim)
        self.layers.append({'weights_transposed': weights,
                            'nodes': np.zeros((no_nodes, 1)),
                            'activation': activation,
                            'input_dim': input_dim})

    def get_weights(self, no_nodes, input_dim):
        """
        Initializes transposed weight matrix on shape input dim, no_nodes with the Xavier initialization
        """
        np.random.seed(42)
        return np.random.normal(0, 1/(np.sqrt(input_dim)), (input_dim, no_nodes)).transpose()

    def train(self, inputs, targets, epochs):
        # Add layer for inputs-nodes
        self.layers.insert(0, {'weights_transposed': None,
                            'nodes': inputs,
                            'activation': None,
                            'input_dim': None})
        # Run FP, BP for each epoch
        for e in range(epochs):
            self.forward_propagation()
            print(self.layers)
            print(inputs.shape)
            print('... backpropagation')
            estimated_values = self.layers[-1]['nodes']
            assert estimated_values.shape == targets.shape
            output_errors = estimated_values - targets
            if np.abs(np.sum(output_errors)) < 0.0000002:
                print('stop training on round',e,'loss is', np.sum(output_errors))
                return
            print('loss:', np.sum(output_errors))
            error_change = inputs*output_errors
            print(error_change)
            self.layers[1]['weights_transposed'] -= self.learning_rate * \
                np.transpose(error_change)
            print('new weights:', self.layers[0]['weights_transposed'])

    def jacobian_iteration(self):
        # Size of output layer, check 0 or 1 index
        # output_size = self.layers[-1]['weights'].shape[0]
        estimated_values = self.layers[-1]['nodes']

        J_output_layer_by_sum = self.layers[-1]['activation'].derivative(estimated_values)
        # R = np.multiply(np.identity(output_size), J_output_layer_by_sum)

        # NOT JUST FOR FIRST WEIGHTS; BUT ITERATIVE
        # TODO: Rename 'weights' to 'weights_transposed'
        # Change in loss by change of output values (L by Z)
        J_loss_by_output = self.loss_type.derivative(estimated_values)
        # Change in a layer's nodes by the earlier layer's nodes (Z by Y)
        J_layer_by_earlier_layer = J_output_layer_by_sum @ self.layers[-1]['weights_transposed']
        # Values of previours layer (Y)
        earlier_layer = self.layers[-2]['nodes']
        J_layer_by_incoming_weights_simplified = np.outer(earlier_layer, J_output_layer_by_sum)
        print('Shape of J_Z_by_W_simplified should be len(y) times len(z):', J_layer_by_incoming_weights_simplified.shape)
        # Initialize before iteration
        J_loss_by_layer = J_loss_by_output
        # TODO: Add stuff for softmax
        # j_s_z is softmax jacobian(z)
        for i, layer in enumerate(reversed(self.layers)):
            # Calculate values for updating weights
            J_loss_by_input_weights = J_loss_by_layer * J_layer_by_incoming_weights_simplified
            # TODO: Update for earlier layer
            J_layer_by_incoming_weights_simplified = 3
            # Calculate values for further iterations
            J_loss_by_layer = J_loss_by_layer @ J_layer_by_earlier_layer
            input_sum_to_layer = layer['weights'] @ self.layers[len(self.layers) - 1 - i]['nodes']
            J_layer_by_sum = layer['activation'].derivative(input_sum_to_layer)
            J_layer_by_earlier_layer = J_layer_by_sum @ layer['weights_transposed']
            # Check shape
            # Break before input, maybe not needed? No, but add layer for input-values

        # Diagonal matrix with output derivatives (slide 48, lecture 2)
        # TODO: Update W with new weights

    def forward_propagation(self):
        print('... forward propagation')
        for i, layer in enumerate(self.layers[:-1]):
            z = np.matmul(self.layers[i+1]['weights_transposed'], layer['nodes'])
            self.layers[i+1]['nodes'] = self.layers[i+1]['activation'].apply_function(z)
            

