"""
Implements TokenGraph() object for storing and accesing
relationships between tokens
"""

import numpy as np

class TokenGraph(object):
    """ Stores all methods for building and accessing token relationships """
    # base methods
    def __init__(self, tokenizer):
        assert isinstance(tokenizer, Tokenizer), ('tokenizer expected type ' \
                                                'Tokenizer, but found type ' \
                                                f'{type(tokenizer)}.')
        self.tokenizer = tokenizer
        self.corrMatrix = None

    def __str__(self):
        return f'<TokenGraph Object: TOKENIZER={self.tokenizer}>'

    # save/load methods
    # TODO: IMPLEMENT

    # matrix initialization methods
    def build_corr_matrix_from_iterator(self, iterator):
        """ Builds corr matrix from file iterator """
