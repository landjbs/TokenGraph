"""
Implements Tokenizer() class for preprocessing and tokenizing raw-text and
Language() class for storing metrics about the language used.
"""

import re
import pickle
from tqdm import tqdm
from numpy import log, mean
from unidecode import unidecode
from collections import Counter
from flashtext import KeywordProcessor

import utils as utils


class Tokenizer(object):
    """ Stores all methods for working with text """
    # base methods
    def __init__(self, lower=True):
        assert isinstance(lower, bool), ('lower expected type bool, but found '
                                        f'type {type(lower)}.')
        self.lower = lower
        # low level attributes to be abstracted
        self.vocabSize  =   0
        self.freqDict   =   None
        self.idx        =   None
        self.reverseIdx =   None
        self.tokenizer  =   KeywordProcessor()
        # high level attribute to indicate initialization
        self.initialized = False
        # matches non-alphanumeric, space, or sentence-ending punctuation
        self.STRIP = re.compile(r'[^0-9a-zA-Z\t\n\s_.?!:;/<>*&^%$#@()"~`+-]')
        # matches sequence of tabs, newlines, spaces, underscores, and dashes
        self.SPACE = re.compile(r'[\t\n\s_.?!:;/<>*&^%$#@()"~`+-]+')

    def __str__(self):
        return (f'<Tokenizer Object: VOCAB_SIZE={self.vocabSize} | ' \
                f'LOWER={self.lower}>')

    # save/load methods
    def save(self, path):
        """ Saves Tokenizer() to folder at path """
        assert isinstance(path, str), ('path expected type str, but found '\
                                        f'type {type(path)}.')
        assert self.initialized, 'Tokenizer must be initialized before saving.'
        utils.safe_make_folder(path)
        # save neccessary attributes for lossless reconstruction
        utils.save_obj(self.freqDict, f'{path}/freqDict')
        utils.save_obj(self.idx, f'{path}/idx')
        utils.save_obj(self.tokenizer, f'{path}/tokenizer')
        with open(f'{path}/lower.sav', 'w+') as lowerFile:
            lowerStr = 't' if self.lower else 'f'
            lowerFile.write(lowerStr)
        return True

    def load(self, path):
        """ Loads Tokenizer() from folder at path """
        utils.path_exists(path)
        assert not self.initialized, ("Tokenizer file can't be loaded into an "\
                                        "initialized Tokenizer.")

        # load pickled objects
        self.freqDict = utils.load_obj(f'{path}/freqDict')
        self.idx = utils.load_obj(f'{path}/idx')
        self.tokenizer = utils.load_obj(f'{path}/tokenizer')
        # load lower bool
        with open(f'{path}/lower.sav', 'r') as lowerFile:
            lowerStr = lowerFile.read()
        self.lower = True if (lowerStr=='t') else False
        # extrapolate from loaded objects
        self.build_reverse_idx()
        self.vocabSize = len(self.freqDict)
        self.initialized = True
        return True

    # common file iterators
    def wiki_iterator(self, path='data/inData/wikiArticles.csv'):
        """ Iterates over wiki csv, yielding raw article text """
        with open(path, 'r') as wikiFile:
            for line in wikiFile:
                commaLoc = line.find(',')
                articleText = line[commaLoc+3:-3]
                yield articleText

    # methods for preprocessing text
    def to_lower(self, rawString):
        """ Lowercases string """
        return rawString.lower()

    def clean(self, rawString):
        """
        Cleans rawString by replacing spaceMatcher and tagMatcher with a single
        space, removing non-alpha chars, and lowercasing alpha chars
        """
        unicodedString = unidecode(rawString)
        # replace STRIP Matcher with ""
        cleanedString = re.sub(self.STRIP, "", rawString)
        # replace SPACE Matcher with " " and strip surround whitespace
        spacedString = re.sub(self.SPACE, " ", cleanedString)
        # lowercase the alpha chars that remain
        if self.lower:
            return self.to_lower(spacedString)
        else:
            return spacedString

    # methods for gathering language data
    def calc_tf_idf(self, termFreq, docFreq):
        """ Calcs scalar token freq score from tf and idf """
        # DEBUG: TF IDF SEEMS OFF
        return 1 + log(termFreq * docFreq)

    def freq_dict_from_file_iterator(self, iterator):
        """ Builds freq dict from file iterator. Updates vocabSize """
        # initialize counter to map tokens to raw number of occurences
        tokenCounts = Counter()
        # initialize counter to map tokens to number of docs they appear in
        tokenAppearances = Counter()
        # initialize variable to count total number of words used
        totalLength = 0
        # get base count of article num for tqdm
        articleCount = len([None for _ in iterator()])
        # iterate over wiki file
        for i, text in enumerate(tqdm(iterator(), total=articleCount)):
            # find tokens in text
            cleanText = self.clean(text)
            tokenList = cleanText.split()
            # count number of times each token appears
            currentCounts = Counter(tokenList)
            # get total length of text
            wordCount = len(tokenList)
            # add tokens counts to tokenCounts counter
            tokenCounts.update(currentCounts)
            # add single appearance for each token found
            tokenAppearances.update(set(currentCounts))
            # add number of words in current file to totalLength
            totalLength += wordCount
        # lambdas for calculating termFreq and docFreq
        calc_termFreq = lambda tokenCount : tokenCount / totalLength
        calc_docFreq = lambda tokenAppearance : log(float(i) / tokenAppearance)
        # use total num to norm tokenCounts and find frequency for each token
        freqDict = {token : self.calc_tf_idf(calc_termFreq(rawCount),
                            calc_docFreq(tokenAppearances[token]))
                    for token, rawCount in tokenCounts.items()}
        meanScore = mean([elt for elt in freqDict.values()])
        self.freqDict = freqDict
        self.vocabSize = len(freqDict)
        return True

    def filter_freq_dict(self, minFreq=0, maxFreq=1, tokenNum=50000):
        """
        Filters freq dict to tokenNum tokens between min and maxFreq. Updates
        vocab size in conjunction.
        """
        assert (tokenNum > 0), f'Filtering to tokenNum={tokenNum} would result'\
                                'in empty freqDict.'
        qualifies = lambda freq : (maxFreq > freq > minFreq)
        filteredFreqDict = {token : freq
                            for i, (token, freq)
                            in enumerate(self.freqDict.items())
                            if (qualifies(freq) and (i < tokenNum))}
        assert (filteredFreqDict != dict()), ('Filtering removed all elements '\
                                            'from freqDict. Try chaning min '\
                                            'or max frequency parameters.')
        self.freqDict = filteredFreqDict
        self.vocabSize = len(filteredFreqDict)
        return True

    # methods for tokenizer modification
    def build_tokenizer(self):
        """ Builds flashtext tokenizer from freq dict """
        assert (self.freqDict), f'freqDict must be built before tokenizer.'
        self.tokenizer.add_keywords_from_list(list(self.freqDict.keys()))
        return True

    # methods for idx modification
    def build_idx(self):
        assert (self.freqDict), f'freqDict must be built before idx.'
        self.idx = {word : i for i, word in enumerate(self.freqDict)}

    def build_reverse_idx(self):
        assert (self.idx), f'idx must be built before reverse idx.'
        self.reverseIdx = {i : word for word, i in self.idx.items()}

    # higher level initialization methods
    def language_from_wiki_file(self, minFreq, maxFreq, tokenNum):
        """
        Builds freqDict, vocabSize, tokenizer, idx, and reverse idx from wiki
        file. Takes tokenNum tokens between minFreq and maxFreq.
        """
        self.freq_dict_from_file_iterator(iterator=self.wiki_iterator)
        self.filter_freq_dict(minFreq, maxFreq, tokenNum)
        self.build_tokenizer()
        self.build_idx()
        self.build_reverse_idx()
        self.initialized = True
        return True

    # tokenization methods
    def clean_and_tokenize(self, text):
        """ Returns Counter() of recognized tokens in raw text """
        return Counter(self.tokenizer.extract_keywords(self.clean(text)))

    # mechanical token ranking in text
    def score_single_token(self, token, observedFreq):
        """ Scores a single token in text according to observed tf """
        freqDiff = self.calc_tf_idf(observedFreq, 1) - self.freqDict[token]
        if freqDiff <= 0:
            return None
        return round(freqDiff, 4)

    def single_mechanically_score_tokens(self, text):
        """
        Ranks token scores in text using freqDict and assuming no subtokens
        and converts token names to idx number
        """
        tokenCounts = self.clean_and_tokenize(text)
        wordNum = len(text.split())
        tokenScores =  {token : self.score_single_token(token,
                                                        (count/wordNum))
                        for token, count in tokenCounts.items()}
        return {self.idx[token] : score for token, score in tokenScores.items()
                if ((score != None) and (token in self.idx))}

    # def KNOWLEDGE_mechanically_score_tokens(self, text, maxChunkSize=5):
    #     """ Ranks tokenes according to freqDict and observed freq in text """
    #     # find counter of greedy tokens in text
    #     greedyTokens = self.clean_and_tokenize(test)
    #     subTokens = Counter()
    #     # iterate over greedy counter
    #     for greedyToken, greedyCount in greedyTokens.items():
    #         greedyWords = greedyToken.split()
    #         wordNum = len(greedyWords)
    #         # if multiple words in cur topToken, recursively look for sub tokens
    #         if wordNum > 1:
    #             # init chunk is 1 smaller than wordNum but capped at maxChunkSize
    #             chunkSize = min(maxChunkSize, (wordNum - 1))
    #             # iterate over greedy tokens, analyzing smaller chunks at a time
    #             while chunkSize > 0:
    #                 for i in range(wordNum):
    #                     chunkWords = greedyWords[i : i+chunkSize]
    #                     textChunk = ' '.join(chunkWords)
    #                     # if the chunk is a token in the tokenizer,
    #                     # add its count tokenCounts after norming by fraction
    #                     # of larger token and multiplying by larger token's count
    #                     # (becuase you're iterating over a set)
    #                     if textChunk in knowledgeProcessor:
    #                         subTokens.update({textChunk :
    #                                             (greedyCount * (len(chunkWords)
    #                                                             / wordNum))})
    #                 chunkSize -= 1
    #     greedyTokens.update(subTokens)
    #     return greedyTokens
