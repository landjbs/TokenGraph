"""
Implements TokenGraph() object for storing and accesing
relationships between tokens
"""

import pickle
import numpy as np
from tqdm import tqdm
from os import mkdir
from os.path import exists
from operator import itemgetter


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
        self.initialized = False

    def __str__(self):
        return f'<TokenGraph Object: TOKENIZER={self.tokenizer}>'

    # save/load methods
    def save(self, path):
        """ Saves TokenGraph() to folder at path """
        assert isinstance(path, str), ('path expected type str, but found '\
                                        f'type {type(path)}.')
        assert self.initialized, 'TokenGraph must be initialized before saving.'
        assert not exists(path), (f'Folder {path} already exists. Try deleting'\
                                ' it or saving TokenizGraph to different path.')
        mkdir(path)

        def save_attribute(obj, name):
            """ Helper saves attribute to file under path """
            with open(f'{path}/{name}.sav', 'wb+') as attributeFile:
                pickle.dump(obj, attributeFile)
            return True

    # TODO: IMPLEMENT LOAD


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
        for i, text in enumerate(tqdm(iterator(), total=textCount)):
            if i > 1000:
                break
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
        return True

    def search_related_tokens(self, text, n=5):
        """ Finds tokens in text and returns top n related tokens """
        is_positive = lambda score : score > 0
        tokenScores = self.tokenizer.single_mechanically_score_tokens(text)
        idScores = {self.tokenizer.idx[token] : score
                    for token, score in tokenScores.items()}
        for id in idScores:
            relatedTokens = [(relId, score) for relId, score
                            in enumerate(self.corrMatrix[id])
                            if is_positive(score)]
            relatedTokens.sort(reverse=True, key=itemgetter(1))
            topTokens = relatedTokens[:n]
            print(f'{"-"*80}\n{id}')
            for relToken in topTokens:
                print(f'<{relToken[1]}> {self.tokenizer.reverseIdx[relToken[0]]}')
