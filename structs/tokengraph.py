"""
Implements TokenGraph() object for storing and accesing
relationships between tokens
"""

import pickle
import numpy as np
from tqdm import tqdm
from operator import itemgetter

import utils as utils
from structs.tokenizer import Tokenizer

# tiny booster to prevent zero values in division
ZERO_BOOSTER = 0.0000000001

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
        # FIXME: IMP CORR DICT
        self.corrDict = None
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
                                                        'an initialized '\
                                                        'TokenGraph.')
        self.corrMatrix = np.load(f'{path}/corrMatrix.npy')
        self.tokenizer = Tokenizer()
        self.tokenizer.load(f'{path}/tokenizer')
        self.initialized = True
        return True

    # matrix initialization methods
    # TODO: Corr matrix --> corr dict
    def build_corr_matrix_from_iterator(self, iterator, n):
        """
        Builds corr matrix from file iterator using mechanical scores from
        tokenizer and uses corr matrix to build dict of top related tokens for
        each token. Sets initialized to True.
        Args:
            iterator:       File iterator that returns generator of text strings
            n:              Number of tokens to include in each token's ranked
                            related token list
        """
        # cache vars from tokenizer
        vocabSize = self.tokenizer.vocabSize
        # initialize matrix to store token-token correlations
        corrMatrix = np.zeros(shape=(vocabSize, vocabSize), dtype=np.float32())
        # get base count of texts in iterator for tqdm
        textCount = len([None for _ in iterator()])
        # iterate over texts returned by iterator
        for i, text in enumerate(tqdm(iterator(), total=textCount)):
            if i > 1:
                break
            # get mechanical scores of tokens in text
            tokenScores = self.tokenizer.single_mechanically_score_tokens(text)
            # iterate over observed tokens, updating correlations
            for id, score in tokenScores.items():
                for relId, relScore in tokenScores.items():
                    corrMatrix[id, relId] += (score * relScore)

        def norm_sort_and_filter_row(rowVals):
            """
            Helper takes a single row from corr matrix and returns top n tokens
            from row after norming.
            """
            # norm row to unit sum
            rowSum = np.sum(rowVals)
            if (rowSum == 0):
                return []
            normedVals = np.divide(rowVals, rowSum)
            ## tag and grab top n tokens from normedVals as tuple (score, id) ##
            topVals = [(val, id) for id, val in enumerate(normedVals[:n])]
            minElt = min(topVals, key=itemgetter(1))
            minVal, minLoc = minElt[0], minElt[1]
            for id, val in enumerate(normedVals[n:]):
                if val > minVal:
                    _ = topVals.pop(minLoc)
                    topVals.append((val, id + n))
                    minElt = min(topVals, key=itemgetter(1))
                    minVal, minLoc = minElt[0], minElt[1]
            topVals.sort(reverse=True, key=itemgetter(1))
            return topVals

        # build corr dict from corr matrix
        corrDict = {topId : norm_sort_and_filter_row(corrRow)
                    for topId, corrRow in tqdm(enumerate(corrMatrix))}

        del corrMatrix

        # update object
        self.corrDict = corrDict
        self.initialized = True
        return True

    # TODO: Deprecate searching
    def search_related_tokens(self, text, n=5):
        """ Finds tokens in text and returns top n related tokens """
        # TODO: REIMP OR REMOVE
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

    def graph_rank_text(self, text, iter=2, delta=0.001, n=5):
        # find token counts in text
        tokenFreqs = self.tokenizer.single_mechanically_score_tokens(text)
        # init numpy vector of tiny delta weights
        rawWeights = np.tile([delta], reps=self.tokenizer.vocabSize)
        # replace delta with observed freq in observed token idx of weight vec
        for tokenId, tokenFreq in tokenFreqs.items():
            rawWeights[tokenId] = tokenFreq
        # norm weight vector to unit sum
        weightSum = np.sum(rawWeights)
        normedWeights = np.divide(rawWeights, weightSum)
        # run graph ranking over normed weights for iter
        iterMatrix = np.linalg.matrix_power(self.corrMatrix, n=iter)
        scoreVec = np.dot(iterMatrix, normedWeights)
        ## find location and score of top n tokens ##
        # BUG: sorting method not completely effective
        # initialize top token list with first n tokens of scoreVec
        topTokens = list(zip((i for i in range(n)), scoreVec[:n]))
        minTup = min(topTokens, key=itemgetter(1))
        minLoc, minScore = minTup[0], minTup[1]
        # search score vec for tokens with higher ranking than min top token
        for id, score in tqdm(enumerate(scoreVec)):
            if score > minScore:
                topTokens.pop(minLoc)
                topTokens.append((id, score))
                minTup = min(topTokens, key=itemgetter(1))
                minLoc, minScore = minTup[0], minTup[1]
        topTokens.sort(key=itemgetter(1), reverse=True)
        return topTokens

    def DICT_graph_rank_text(self, text, iter, delta):
        """
        Ranks text using corr dict of top related tokens for each token found
        Args:
            text:       String of raw text to tag
            iter:       Number of iterations over which to approximate ranking
            delta:      Initial score to assign shadow token candidates
        """
        # find token counts in text
        tokenFreqs = self.tokenizer.single_mechanically_score_tokens(text)
        # find all related tokens of those found
        relatedTokens = {token : self.corrDict[token]
                            for token in tokenFreqs.keys()}
        # build a dict of candidates for scoring and new id in miniCorr
        candidateTokens = dict()
        newId = 0
        for token in relatedTokens.keys():
            candidateTokens.update({token : newId})
            newId += 1
        for tokenList in relatedTokens.values():
            for token in tokenList:
                candidateTokens.update({token : newId})
                newId += 1
        # miniCorr matrix has dimensions equal to cardinality of candidate dict
        candidateNum = len(candidateTokens)
        miniCorr = np.zeros(shape=(candidateNum, candidateNum))
        # update correlation pointers in minCorr matrix
        for baseToken, curRelated in relatedTokens.items():
            # find new id of baseToken
            baseId = candidateTokens[baseToken]
            # add all pointer from baseId
            for relatedScore, relatedToken in curRelated:
                relatedId = candidateTokens[relatedToken]
                miniCorr[baseId, relatedId] += relatedScore
        print(miniCorr)
        # approximate graph ranking over miniCorr for iter iterations
        iterCorr = np.linalg.matrix_power(miniCorr, n=iter)
        # build initial weight vector of all candidate tokens
        rawWeights = np.tile([delta], reps=candidateNum)
        # update weights of those tokens actually present
        for token, freq in tokenFreqs.items():
            rawWeights[candidateTokens[token]] += 1
        # norm weight vector to unit
        normedWeights = np.divide(rawWeights, (sum(rawWeights) + ZERO_BOOSTER))
        # pass normed weight vector through ranked matrix
        convergedWeights = np.dot(iterCorr, normedWeights)
        # build reverse index to access original token id from mini id
        reverseCandidateIdx = {newId : oldId for newId, oldId
                                in candidateTokens.items()}
        # return dict mapping tokens to their ranked weights
        return {reverseCandidateIdx[newId] : weight
                for newId, weight in enumerate(convergedWeights)}
