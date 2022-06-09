import itertools
# pip install platypus
from platypus import Real

import numpy as np
import numba


def squared_exponential_rbf(rbf_input, centers, radii, weights):
    """

    Parameters
    ----------
    rbf_input : numpy array
                1-D, shape is (n_inputs,)
    centers :   numpy array
                2-D, shape is (n_rbfs X n_inputs)
    radii :     2-D, shape is (n_rbfs X n_inputs)
    weights :   2-D, shape is (n_rbfs X n_outputs)

    Returns
    -------
    numpy array


    """

    # sum over inputs 
    a = rbf_input[np.newaxis, :] - centers #(rbf_input[np.newaxis])-centre
    #the np.newaxis function creates a new array, converting the 1D array into 
    #a 2D array, thus making the subtraction possible
    b = a ** 2
    c = radii ** 2
    rbf_scores = np.exp(-(np.sum(b / c, axis=1))) #exp(-b/c)

    # n_rbf x n_output, n_rbf
    weighted_rbfs = weights * rbf_scores[:, np.newaxis]
    output = weighted_rbfs.sum(axis=0)

    return output


def gaussian_rbf(rbf_input, centers, radii, weights):
    """

    Parameters
    ----------
    rbf_input : numpy array
                1-D, shape is (n_inputs,)
    centers :   numpy array
                2-D, shape is (n_rbfs X n_inputs)
    radii :     2-D, shape is (n_rbfs X n_inputs)
    weights :   2-D, shape is (n_rbfs X n_outputs)

    Returns
    -------
    numpy array


    """
    a = rbf_input[np.newaxis, :] - centers
    n = a / radii
    p = n ** 2
    q = np.sum(p, axis=1)
    rbf_scores = np.exp(-1 * q)

    # n_rbf x n_output, n_rbf
    weighted_rbfs = weights * rbf_scores[:, np.newaxis]
    output = weighted_rbfs.sum(axis=0)

    return output


def multiquadric_rbf(rbf_input, centers, radii, weights):
    """

    Parameters
    ----------
    rbf_input : numpy array
                1-D, shape is (n_inputs,)
    centers :   numpy array
                2-D, shape is (n_rbfs X n_inputs)
    radii :     2-D, shape is (n_rbfs X n_inputs)
    weights :   2-D, shape is (n_rbfs X n_outputs)

    Returns
    -------
    numpy array


    """
    a = rbf_input[np.newaxis, :] - centers
    b = a / radii
    c = b ** 2
    d = np.sum(c, axis=1)
    rbf_scores = np.sqrt(1 + d)

    weighted_rbfs = weights * rbf_scores[:, np.newaxis]
    output = weighted_rbfs.sum(axis=0)

    return output


def inverse_quadric_rbf(rbf_input, centers, radii, weights):
    """

    Parameters
    ----------
    rbf_input : numpy array
                1-D, shape is (n_inputs,)
    centers :   numpy array
                2-D, shape is (n_rbfs X n_inputs)
    radii :     2-D, shape is (n_rbfs X n_inputs)
    weights :   2-D, shape is (n_rbfs X n_outputs)

    Returns
    -------
    numpy array


    """
    a = rbf_input[np.newaxis, :] - centers
    b = a / radii
    c = b ** 2
    d = np.sum(c, axis=1)
    rbf_scores = 1 / (1 + d)

    weighted_rbfs = weights * rbf_scores[:, np.newaxis]
    output = weighted_rbfs.sum(axis=0)

    return output


def inverse_multiquadric_rbf(rbf_input, centers, radii, weights):
    """

    Parameters
    ----------
    rbf_input : numpy array
                1-D, shape is (n_inputs,)
    centers :   numpy array
                2-D, shape is (n_rbfs X n_inputs)
    radii :     2-D, shape is (n_rbfs X n_inputs)
    weights :   2-D, shape is (n_rbfs X n_outputs)

    Returns
    -------
    numpy array


    """
    a = rbf_input[np.newaxis, :] - centers
    b = (a / radii) ** 2
    rbf_scores = 1 / np.sqrt(1 + np.sum(b, axis=1))

    weighted_rbfs = weights * rbf_scores[:, np.newaxis]
    output = weighted_rbfs.sum(axis=0)

    return output


def exponential_rbf(rbf_input, centers, radii, weights):
    """

    Parameters
    ----------
    rbf_input : numpy array
                1-D, shape is (n_inputs,)
    centers :   numpy array
                2-D, shape is (n_rbfs X n_inputs)
    radii :     2-D, shape is (n_rbfs X n_inputs)
    weights :   2-D, shape is (n_rbfs X n_outputs)

    Returns
    -------
    numpy array


    """
    a = rbf_input[np.newaxis, :] - centers
    b = (a / radii) ** 2
    rbf_scores = np.exp(-1 * np.sum(b, axis=1))

    weighted_rbfs = weights * rbf_scores[:, np.newaxis]
    output = weighted_rbfs.sum(axis=0)
    return output


def multi_quadric2_rbf(rbf_input, centers, radii, weights):
    """

    Parameters
    ----------
    rbf_input : numpy array
                1-D, shape is (n_inputs,)
    centers :   numpy array
                2-D, shape is (n_rbfs X n_inputs)
    radii :     2-D, shape is (n_rbfs X n_inputs)
    weights :   2-D, shape is (n_rbfs X n_outputs)

    Returns
    -------
    numpy array

    """

    rbf_scores = np.sqrt(np.sum((radii ** 2) + ((rbf_input - centers) ** 2),
                                axis=1))
    weighted_rbfs = weights * rbf_scores[:, np.newaxis]
    output = weighted_rbfs.sum(axis=0)
    return output


def matern32_rbf(rbf_input, centers, radii, weights):
    """

    Parameters
    ----------
    rbf_input : numpy array
                1-D, shape is (n_inputs,)
    centers :   numpy array
                2-D, shape is (n_rbfs X n_inputs)
    radii :     2-D, shape is (n_rbfs X n_inputs)
    weights :   2-D, shape is (n_rbfs X n_outputs)

    Returns
    -------
    numpy array


    """
    diff = rbf_input - centers
    squared = (diff / radii) ** 2
    sqrt = np.sqrt(3 * np.sum(squared, axis=1))
    rbf_scores = (1 + sqrt) * (np.exp(-sqrt))

    weighted_rbfs = weights * rbf_scores[:, np.newaxis]
    output = weighted_rbfs.sum(axis=0)
    return output


rbfs = [squared_exponential_rbf,
        gaussian_rbf,
        multiquadric_rbf,
        inverse_multiquadric_rbf,
        inverse_quadric_rbf,
        exponential_rbf,
        multi_quadric2_rbf,
        matern32_rbf]


class RBF:

    def __init__(self, n_rbfs, n_inputs, n_outputs,
                 rbf_function=squared_exponential_rbf):
        self.n_rbfs = n_rbfs
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.rbf = rbf_function

        types = []
        c_i = []
        r_i = []
        w_i = []
        count = itertools.count()
        for i in range(self.n_rbfs):
            for j in range(self.n_inputs):
                types.append(Real(-1, 1))  # center
                c_i.append(next(count))
                types.append(Real(0, 1))  # radius
                r_i.append(next(count))

        for _ in range(self.n_rbfs):
            for _ in range(self.n_outputs):
                types.append(Real(0, 1))  # weight
                w_i.append(next(count))  # weight

        self.platypus_types = types
        self.c_i = np.asarray(c_i, dtype=np.int)
        self.r_i = np.asarray(r_i, dtype=np.int)
        self.w_i = np.asarray(w_i, dtype=np.int)

        self.centers = None
        self.radii = None
        self.weights = None

    def set_decision_vars(self, decision_vars):
        decision_vars = decision_vars.copy()

        self.centers = decision_vars[self.c_i].reshape((self.n_rbfs,
                                                        self.n_inputs))
        self.radii = decision_vars[self.r_i].reshape((self.n_rbfs,
                                                      self.n_inputs))
        self.weights = decision_vars[self.w_i].reshape((self.n_rbfs,
                                                        self.n_outputs))

        # sum of weights per input is 1
        self.weights /= self.weights.sum(axis=0)[np.newaxis, :]

    def apply_rbfs(self, inputs):
        outputs = self.rbf(inputs, self.centers, self.radii, self.weights)

        return outputs

# # @numba.jit
# def format_output(output, weights):
#     a = weights * output[:, np.newaxis]  # n_rbf x n_output, n_rbf
#     b = a.sum(axis=1)
#
#     return b
