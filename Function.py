class Function:
    def __init__(self):
        pass

    def backpropagate(self, next_der):
        # backpropagate partial derivative from next layer 
        """
        :type next_der: ndarray of shape num_ex x output_size

        :returns: ndarray of shape num_ex x input_size (input_size = output_size for Activation)
        """
        raise NotImplementedError

    def forward(self, x):
        # Forward propagate through layer
        """
        :type x: ndarray of shape num_ex x input_size

        :returns: ndarray of shape num_ex x output_size (output_size = input_size for Activation)
        """
        raise NotImplementedError

    def apply_function(self):
        """
        TODO: update shapes
        :type z: ndarray of shape num_nodes x num_ex

        :returns: ndarray of shape num_nodes x num_ex
        """
        raise NotImplementedError

    def gradient(self, values):
        """
        TODO: update shapes
        :type z: ndarray of shape num_nodes x num_ex

        :returns: ndarray of shape num_nodes x num_ex
        """
        raise NotImplementedError
