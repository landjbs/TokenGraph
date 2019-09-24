"""
Implements Tokenizer() class for preprocessing and tokenizing raw-text and
Language() class for storing metrics about the language used.
"""

import re
import pickle
from numpy import log
from tqdm import tqdm
from os import listdir, mkdir
from unidecode import unidecode
from collections import Counter
from flashtext import KeywordProcessor



class Tokenizer(object):
    """ Stores all methods for working with text """
    def __init__(self, lower=True):
        assert isinstance(lower, bool), ('lower expected type bool, but found '
                                        f'type {type(lower)}.')
        self.lower = lower
        # low level attributes to be abstracted
        self.vocabSize  =   0
        self.freqDict   =   None
        self.idx        =   None
        self.reverseIdx =   None
        self.tokenizer  = KeywordProcessor()
        # high level attribute to indicate initialization
        self.initialized = False
        # matches non-alphanumeric, space, or sentence-ending punctuation
        self.STRIP = re.compile(r'[^0-9a-zA-Z\t\n\s_.?!:;/<>*&^%$#@()"~`+-]')
        # matches sequence of tabs, newlines, spaces, underscores, and dashes
        self.SPACE = re.compile(r'[\t\n\s_.?!:;/<>*&^%$#@()"~`+-]+')

    # save/load methods
    def save(self, path):
        """ Saves Tokenizer() to file at path """
        assert self.initialized, 'Tokenizer must be initialized before saving.'
        mkdir(path)

    # misc methods
    def __str__(self):
        return (f'<Tokenizer Object: VOCAB_SIZE={self.vocabSize} | ' \
                f'LOWER={self.lower}>')

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
    def freq_dict_from_wiki_file(self):
        """ Builds freq dict from wiki iterator. Updates vocabSize """
        # initialize counter to map tokens to raw number of occurences
        tokenCounts = Counter()
        # initialize counter to map tokens to number of docs they appear in
        tokenAppearances = Counter()
        # initialize variable to count total number of words used
        totalLength = 0
        # get base count of article num for tqdm
        articleCount = len([None for _ in self.wiki_iterator()])
        # iterate over wiki file
        for i, text in enumerate(tqdm(self.wiki_iterator(), total=articleCount)):
            if i > 1000:
                break
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
        freqDict = {token : (calc_termFreq(rawCount),
                            calc_docFreq(tokenAppearances[token]))
                    for token, rawCount in tokenCounts.items()}
        self.freqDict = freqDict
        self.vocabSize = len(freqDict)
        return True

    def filter_freq_dict(self, minFreq=0, maxFreq=1, tokenNum=50000):
        """
        Filters freq dict to tokenNum tokens between min and maxFreq. Updates
        vocab size in conjunction.
        """
        qualifies = lambda freqTup : (maxFreq > freqTup[0] > minFreq)
        filteredFreqDict = {token : freqTup
                            for i, (token, freqTup)
                            in enumerate(self.freqDict.items())
                            if (qualifies(freqTup) and (i < tokenNum))}
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
        self.freq_dict_from_wiki_file()
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
    def mechanically_rank_tokens(self, text):



class _Tokenizer(object):
    """ Stores all methods for working with text """
    def __init__(self, lower=True):
        assert isinstance(lower, bool), ('lower expected type bool, but found '
                                        f'type {type(lower)}.')
        self.lower = lower
        self.freqDict = None
        self.tokenizer = KeywordProcessor()
        # matches non-alphanumeric, space, or sentence-ending punctuation
        self.STRIP = re.compile(r'[^0-9a-zA-Z\t\n\s_.?!:;/<>*&^%$#@()"~`+-]')
        # matches sequence of tabs, newlines, spaces, underscores, and dashes
        self.SPACE = re.compile(r'[\t\n\s_.?!:;/<>*&^%$#@()"~`+-]+')

    def _to_lower(self, text):
        return text.lower()

    def tokenize(self, text):
        return text.split()

    def _wiki_iterator(name='data/inData/wikiArticles.csv'):
        """ Iterates over wiki csv, yielding raw article text """
        with open(name, 'r') as wikiFile:
            for line in wikiFile:
                commaLoc = line.find(',')
                articleText = line[commaLoc+3:-3]
                yield articleText

    def clean_text(self, rawString):
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

    def clean_and_tokenize(self, rawString, returnCounts=False):
        """ Returns counter of tokens and their freqs in rawString """
        cleanString = self.clean_text(rawString)
        tokenList = self.tokenize(cleanString)
        tokenNum = len(tokenList)
        tokenCounter = Counter({token : (count / tokenNum)
                        for token, count in Counter(tokenList).items()})
        if returnCounts:
            return tokenCounter, tokenNum
        else:
            return tokenCounter

    def build_freq_dict_from_folder(self, folderPath):
        """ """
        # initialize counter to map tokens to raw number of occurences
        tokenCounts = Counter()
        # initialize counter to map tokens to number of docs they appear in
        tokenAppearances = Counter()
        # initialize variable to count total number of words used
        totalLength = 0
        # find and iterate over list of files within folderPath
        for i, file in enumerate(tqdm(listdir(folderPath))):
            with open(f"{folderPath}/{file}") as FileObj:
                # read in the current file
                text = FileObj.read()
                # find tokens in text
                tokensFound, tokenNum = self.clean_and_tokenize(text,
                                                            returnCounts=True)
                # add tokens counts to tokenCounts counter
                tokenCounts.update(tokensFound)
                # add single appearance for each token found
                tokenAppearances.update(set(tokensFound))
                # add number of words in current file to totalLength
                totalLength += tokenNum
        # lambdas for calculating termFreq and docFreq
        calc_termFreq = lambda tokenCount : tokenCount / totalLength
        calc_docFreq = lambda tokenAppearance : log(float(i) / tokenAppearance)
        # use total num to norm tokenCounts and find frequency for each token
        freqDict = {token: (calc_termFreq(tokenCounts[token]),
                            calc_docFreq(tokenAppearances[token]))
                    for token in tokenCounts}
        self.freqDict = freqDict
        return True

    def build_tokenizer(self, minFreq, maxFreq, tokenNum):
        """
        Builds tokenizer from self.freqDict taking tokenNum tokens between
        max and minFreq
        """
        freq_filter = lambda tokenInfo : maxFreq > tokenInfo[1] > minFreq
        validTokens = [token for token, freq in self.freqDict.items()
                        if (minFreq < freq < maxFreq)]
        print(validTokens)
        self.tokenizer.add_keywords_from_list(validTokens)


class Language(object):
    """ Defines properties of the Language being delt with """
    def __init__(self, name, tokenizer, vocabSet=None):
        assert isinstance(tokenizer, Tokenizer), ('tokenizer expected type'
                                                'Tokenizer() but found type'
                                                f'{type(tokenizer)}')
        assert (isinstance(vocabFreqs, None)
                or isinstance(vocabFreqs, dict)), ('vocabFreqs expected either'
                                                    'dict or None, but found'
                                                    f'type {type(vocabFreqs)}.')
        self.name = name
        self.tokenizer = tokenizer
        self.vocabSet = vocabSet
        self.vocabSize = len(vocabSet) if vocabSet else None
        self.idx = None
        self.reverseIdx = None


    def fredDict_from_folderPath(folderPath, knowledgeProcessor, outPath=None):
        """
        Args: folderPath to folder containing files from which to read,
        knowledgeProcessor for token extraction.
        Returns: dict mapping knowledge tokens to tuple of (termFreq, docFreq)
        observed in documents.
            termFreq = (number of times token is used) / (number of words used)
            docFreq = log ((num of documents) / (num of documents with token))
        """
        # initialize counter to map knowledge tokens to raw number of occurences
        tokenCounts = Counter()
        # initialize counter to map knowledge tokens to number of docs they appear in
        tokenAppearances = Counter()
        # initialize variable to count total number of words used
        totalLength = 0
        # find and iterate over list of files within folderPath
        for i, file in enumerate(os.listdir(folderPath)):
            print(f"\tBuilding freqDict: {i}", end='\r')
            with open(f"{folderPath}/{file}") as FileObj:
                # read in the current file
                text = FileObj.read()
                # find both greedy and subtokens in text
                tokensFound = list(knowledgeFinder.find_rawTokens(text,
                                                            knowledgeProcessor))
                # add tokens counts to tokenCounts counter
                tokenCounts.update(tokensFound)
                # add single appearance for each token found
                tokenAppearances.update(set(tokensFound))
                # find number of words in the current file
                textLen = len(text.split())
                # add number of words in current file to totalLength
                totalLength += textLen

        # lambdas for calculating termFreq and docFreq
        calc_termFreq = lambda tokenCount : tokenCount / totalLength
        calc_docFreq = lambda tokenAppearance : log(float(i) / tokenAppearance)

        # use total num to normalize tokenCounts and find frequency for each token
        freqDict = {token: (calc_termFreq(tokenCounts[token]),
                            calc_docFreq(tokenAppearances[token]))
                    for token in tokenCounts}
        if outPath:
            save(freqDict, outPath)
        return freqDict

    def freqDict_from_wikiCsv(self):
        """ Builds freq dict  """

    def vocab_freqs_from_string(self, textString):
        self.vocabFreqs = tokenizer.clean_and_tokenize(textString)

    def build_idx(self):
        if self.vocabFreqs:
            self.idx = {word : i for i, word in enumerate(vocabFreqs)}
        else:
            raise ValueError('Vocab Set has not yet been initialized.')

    def build_reverse_idx(self):
        if self.idx:
            self.reverseIdx = {i : word for word, i in self.idx.items()}
        else:
            raise ValueError('Idx has not yet been initialized.')
