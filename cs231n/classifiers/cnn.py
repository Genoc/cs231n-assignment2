from builtins import object
import numpy as np

from cs231n.layers import *
from cs231n.fast_layers import *
from cs231n.layer_utils import *


class ThreeLayerConvNet(object):
    """
    A three-layer convolutional network with the following architecture:

    conv - relu - 2x2 max pool - affine - relu - affine - softmax

    The network operates on minibatches of data that have shape (N, C, H, W)
    consisting of N images, each with height H and width W and with C input
    channels.
    """

    def __init__(self, input_dim=(3, 32, 32), num_filters=32, filter_size=7,
                 hidden_dim=100, num_classes=10, weight_scale=1e-3, reg=0.0,
                 dtype=np.float32):
        """
        Initialize a new network.

        Inputs:
        - input_dim: Tuple (C, H, W) giving size of input data
        - num_filters: Number of filters to use in the convolutional layer
        - filter_size: Size of filters to use in the convolutional layer
        - hidden_dim: Number of units to use in the fully-connected hidden layer
        - num_classes: Number of scores to produce from the final affine layer.
        - weight_scale: Scalar giving standard deviation for random initialization
          of weights.
        - reg: Scalar giving L2 regularization strength
        - dtype: numpy datatype to use for computation.
        """
        self.params = {}
        self.reg = reg
        self.dtype = dtype

        ############################################################################
        # TODO: Initialize weights and biases for the three-layer convolutional    #
        # network. Weights should be initialized from a Gaussian with standard     #
        # deviation equal to weight_scale; biases should be initialized to zero.   #
        # All weights and biases should be stored in the dictionary self.params.   #
        # Store weights and biases for the convolutional layer using the keys 'W1' #
        # and 'b1'; use keys 'W2' and 'b2' for the weights and biases of the       #
        # hidden affine layer, and keys 'W3' and 'b3' for the weights and biases   #
        # of the output affine layer.                                              #
        ############################################################################
        # conv - relu - pool layer
        self.params['W1'] = np.random.randn(num_filters, input_dim[0], filter_size, filter_size) * weight_scale
        self.params['b1'] = np.zeros((num_filters))
                
        # hidden layer
        self.params['W2'] = np.random.randn(num_filters*input_dim[1]*input_dim[2]/4, hidden_dim) * weight_scale
        self.params['b2'] = np.zeros((hidden_dim))
                
        # affine layer
        self.params['W3'] = np.random.randn(hidden_dim, num_classes) * weight_scale
        self.params['b3'] = np.zeros((num_classes))
        
        
        pass
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)


    def loss(self, X, y=None):
        """
        Evaluate loss and gradient for the three-layer convolutional network.

        Input / output: Same API as TwoLayerNet in fc_net.py.
        """
        W1, b1 = self.params['W1'], self.params['b1']
        W2, b2 = self.params['W2'], self.params['b2']
        W3, b3 = self.params['W3'], self.params['b3']

        # pass conv_param to the forward pass for the convolutional layer
        filter_size = W1.shape[2]
        conv_param = {'stride': 1, 'pad': (filter_size - 1) // 2}

        # pass pool_param to the forward pass for the max-pooling layer
        pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}

        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the three-layer convolutional net,  #
        # computing the class scores for X and storing them in the scores          #
        # variable.                                                                #
        ############################################################################
        # conv - relu - pool layer
        out, conv_cache = conv_relu_pool_forward(X, W1, b1, conv_param, pool_param)
        
        # hidden layer
        out, hidden_cache = affine_relu_forward(out, W2, b2)
        
        # affine layer
        out, affine_cache = affine_forward(out, W3, b3)
        
        scores = out
                
        pass
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        if y is None:
            return scores

        loss, grads = 0, {}
        ############################################################################
        # TODO: Implement the backward pass for the three-layer convolutional net, #
        # storing the loss and gradients in the loss and grads variables. Compute  #
        # data loss using softmax, and make sure that grads[k] holds the gradients #
        # for self.params[k]. Don't forget to add L2 regularization!               #
        ############################################################################
        grads['W1'] = np.zeros_like(W1)
        grads['b1'] = np.zeros_like(b1)
        grads['W2'] = np.zeros_like(W2)
        grads['b2'] = np.zeros_like(b2)
        grads['W3'] = np.zeros_like(W3)
        grads['b3'] = np.zeros_like(b3)
        reg = self.reg
        
        gW1, gW2, gW3 = grads['W1'], grads['W2'], grads['W3']
        gb1, gb2, gb3 = grads['b1'], grads['b2'], grads['b3']
        
        # softmax loss
        loss, dout = softmax_loss(scores, y)
        
        # affine layer 
        dout, dw, db = affine_backward(dout, affine_cache)
        gW3 += dw
        gb3 += db
        
        # hidden layer
        dout, dw, db = affine_relu_backward(dout, hidden_cache)
        gW2 += dw
        gb2 += db
        
        # conv - relu - pool layer
        dout, dw, db = conv_relu_pool_backward(dout, conv_cache)
        gW1 += dw
        gb1 += db
        
        # regularization
        loss += 0.5*reg*(np.sum(gW1*gW1) + np.sum(gW2*gW2) + np.sum(gW3*gW3))
        gW1 += reg*W1
        gW2 += reg*W2
        gW3 += reg*W3
        
        pass
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads
