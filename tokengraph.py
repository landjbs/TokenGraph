"""
Implements TokenGraph() object for storing and accesing
relationships between tokens
"""

import numpy as np
from tqdm import tqdm


class TokenGraph(object):
    """ Stores all methods for building and accessing token relationships """
    # base methods
    def __init__(self, tokenizer):
        # FIXME: Tokenizer assertion
        # assert isinstance(tokenizer, tokenizer), ('tokenizer ' \
        #                         ' expected type Tokenizer, but found type ' \
        #                         f'{type(tokenizer)}.')
        assert tokenizer.initialized, ('tokenizer must be initialized before ' \
                                        'being passed to TokenGraph.')
        self.tokenizer = tokenizer
        self.corrMatrix = None

    def __str__(self):
        return f'<TokenGraph Object: TOKENIZER={self.tokenizer}>'

    # save/load methods
    # TODO: IMPLEMENT

    # matrix initialization methods
    def build_corr_matrix_from_iterator(self, iterator):
        """
        Builds corr matrix from file iterator using mechanical scores from
        tokenizer
        """
        # cache vars from tokenizer
        vocabSize = self.tokenizer.vocabSize
        idxDict = self.tokenizer.idx
        # initialize matrix to store token-token correlations
        corrMatrix = np.zeros(shape=(vocabSize, vocabSize))
        # get base count of texts in iterator for tqdm
        textCount = len([None for _ in iterator()])
        # iterate over texts returned by iterator
        for text in tqdm(iterator(), total=textCount):
            # get mechanical scores of tokens in text
            tokenScores = self.tokenizer.single_mechanically_score_tokens(text)
            # cast token names to token idx nums
            idScores = {idxDict[token] : score
                        for token, score in tokenScores.items()}
            # iterate over observed tokens, updating correlations
            for id, score in idScores.items():
                for relId, relScore in idScores.items():
                    corrMatrix[id, relId] += (score * relScore)
        self.corrMatrix = corrMatrix
        print(sum(sum(corrMatrix)))
        return True
