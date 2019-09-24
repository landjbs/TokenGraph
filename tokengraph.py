"""
Implements TokenGraph() object for storing and accesing
relationships between tokens
"""

import numpy as np

class TokenGraph(object):
    """ Stores all methods for building and accessing token relationships """
    def __init__(self):
        self.corrMatrix = None
        self.descriptionMatrix = None
