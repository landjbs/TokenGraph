"""
Implements graph ranking using TokenGraph() across a set of text to generate
features of pre-ranked word vectors and targets of convergence ranked word
vectors.
"""

import numpy as np

corrMatrix = np.array([[1, 0.9, 0.1], [0.2, 1, 0.1], [0.0001, 0.0001, 1]])
textVec = np.array([0.2, 0.2, 0.6])

for num, col in enumerate(corrMatrix.T):
    colSum = np.sum(col)
    print(colSum)
    corrMatrix[:, num] = np.divide(col, colSum)

def graph_rank_test(corrMatrix, textVec, iter=400):
    iterMatrix = np.linalg.matrix_power(corrMatrix, iter)
    scoreVec = np.dot(iterMatrix, textVec)
    return scoreVec


print(graph_rank_test(corrMatrix, textVec))


def graph_rank_weight_vector(text, maxIter, minDelta):
    """
    Rescores mechanical token weight vector using TokenGraph by running shadow
    token voting and graph ranking to convergence (as determined by first of
    maxIter or minDelta). Returns rescored vector as list of tuples in form
    (token id, token rank).
    """
    pass
