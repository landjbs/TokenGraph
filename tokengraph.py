"""
Implements TokenGraph() object for storing and accesing
relationships between tokens
"""

import pickle
import numpy as np
from tqdm import tqdm
from operator import itemgetter

import utils as utils
from tokenizer import Tokenizer


class TokenGraph(object):
    """ Stores all methods for building and accessing token relationships """
    # base methods
    def __init__(self, tokenizer=None):
        # FIXME: Tokenizer assertion
        if tokenizer:
            assert tokenizer.initialized, ('tokenizer must be initialized ' \
                                            'before being passed to ' \
                                            'TokenGraph.')
        else:
            assert not isinstance(tokenizer, bool), ('tokenizer must have type'\
                                                    ' Tokenizer or None.')
        self.tokenizer = tokenizer
        self.corrMatrix = None
        self.initialized = False

    def __str__(self):
        return f'<TokenGraph Object: TOKENIZER={self.tokenizer}>'

    # save/load methods
    def save(self, path):
        """ Saves TokenGraph() to folder at path """
        assert isinstance(path, str), ('path expected type str, but found '\
                                        f'type {type(path)}.')
        assert self.tokenizer, ('TokenGraph must have valid tokenizer object '\
                                'prior to saving.')
        assert self.initialized, 'TokenGraph must be initialized before saving.'
        utils.safe_make_folder(path)
        np.save(f'{path}/corrMatrix', self.corrMatrix)
        self.tokenizer.save(f'{path}/tokenizer')
        return True

    def load(self, path):
        """ Loads TokenGraph() from folder at path """
        utils.path_exists(path)
        assert not (self.initialized or self.tokenizer), ('TokenGraph file' \
                                                        "can't be loaded into "\
                                                        'initialized '\
                                                        'TokenGraph.')
        self.corrMatrix = np.load(f'{path}/corrMatrix.npy')
        self.tokenizer = Tokenizer()
        self.tokenizer.load(f'{path}/tokenizer')
        self.initialized = True
        return True

    # matrix initialization methods
    def build_corr_matrix_from_iterator(self, iterator):
        """
        Builds corr matrix from file iterator using mechanical scores from
        tokenizer. Sets initialized to True.
        """
        # cache vars from tokenizer
        vocabSize = self.tokenizer.vocabSize
        idxDict = self.tokenizer.idx
        # initialize matrix to store token-token correlations
        corrMatrix = np.zeros(shape=(vocabSize, vocabSize))
        # get base count of texts in iterator for tqdm
        textCount = len([None for _ in iterator()])
        # iterate over texts returned by iterator
        for i, text in enumerate(tqdm(iterator(), total=textCount)):
            if i > 10:
                break
            # get mechanical scores of tokens in text
            tokenScores = self.tokenizer.single_mechanically_score_tokens(text)
            # iterate over observed tokens, updating correlations
            for id, score in tokenScores.items():
                for relId, relScore in tokenScores.items():
                    corrMatrix[id, relId] += (score * relScore)
        self.corrMatrix = corrMatrix
        self.initialized = True
        return True

    def search_related_tokens(self, text, n=5):
        """ Finds tokens in text and returns top n related tokens """
        is_positive = lambda score : score > 0
        tokenScores = self.tokenizer.single_mechanically_score_tokens(text)
        for id in tokenScores:
            relatedTokens = [(relId, score) for relId, score
                            in enumerate(self.corrMatrix[id])
                            if is_positive(score)]
            relatedTokens.sort(reverse=True, key=itemgetter(1))
            topTokens = relatedTokens[:n]
            print(f'{"-"*80}\n{id}')
            for relToken in topTokens:
                print(f'<{relToken[1]}> {self.tokenizer.reverseIdx[relToken[0]]}')
