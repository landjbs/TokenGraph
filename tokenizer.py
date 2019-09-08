"""
Implements Tokenizer() class for preprocessing and tokenizing raw-text and
Language() class for storing metrics about the language used.
"""

import re
from unidecode import unidecode
from collections import Counter
from flashtext import KeywordProcessor

class Tokenizer(object):
    """ Stores all methods for working with text """
    def __init__(self, lower=True, freqDict=None, tokenizer=None):
        """ """
        assert isinstance(lower, bool), ('lower expected type bool, but found '
                                        f'type {type(lower)}.')
        self.lower = lower
        self.freqDict = freqDict
        self.tokenizer = tokenizer
        # matches non-alphanumeric, space, or sentence-ending punctuation
        self.STRIP = re.compile(r'[^0-9a-zA-Z\t\n\s_.?!:;/<>*&^%$#@()"~`+-]')
        # matches sequence of tabs, newlines, spaces, underscores, and dashes
        self.SPACE = re.compile(r'[\t\n\s_.?!:;/<>*&^%$#@()"~`+-]+')

    def _to_lower(self, text):
        return text.lower()

    def tokenize(self, text):
        return text.split()

    def clean_text(self, rawString):
        """
        Cleans rawString by replacing spaceMatcher and tagMatcher with a single
        space, removing non-alpha chars, and lowercasing alpha chars
        """
        unicodedString = unidecode(rawString)
        # replace stripMatcher with ""
        cleanedString = re.sub(self.STRIP, "", rawString)
        # replace spaceMatcher with " " and strip surround whitespace
        spacedString = re.sub(self.SPACE, " ", cleanedString)
        # lowercase the alpha chars that remain
        if self.lower:
            return self._to_lower(spacedString)
        else:
            return spacedString

    def clean_and_tokenize(self, rawString):
        """ Returns counter of tokens and their freqs in rawString """
        cleanString = self.clean_text(rawString)
        tokenList = self.tokenize(cleanString)
        tokenNum = len(tokenList)
        tokenCounter = Counter({token : (count / tokenNum)
                        for token, count in Counter(tokenList).items()})
        return tokenCounter

    def build_freq_dict_from_folder(self, folderPath, tokenNum=50000):
        """ """
        # initialize counter to map tokens to raw number of occurences
        tokenCounts = Counter()
        # initialize counter to map tokens to number of docs they appear in
        tokenAppearances = Counter()
        # initialize variable to count total number of words used
        totalLength = 0
        




class Language(object):
    """ Defines properties of the Language being delt with """
    def __init__(self, name, tokenizer, vocabFreqs=None):
        assert isinstance(tokenizer, Tokenizer), ('tokenizer expected type'
                                                'Tokenizer() but found type'
                                                f'{type(tokenizer)}')
        assert (isinstance(vocabFreqs, None)
                or isinstance(vocabFreqs, dict)), ('vocabFreqs expected either'
                                                    'dict or None, but found'
                                                    f'type {type(vocabFreqs)}.')
        self.name = name
        self.tokenizer = tokenizer
        self.vocabFreqs = vocabFreqs
        self.vocabSize = len(vocabSet) if vocabSet else None
        self.idx = None
        self.reverseIdx = None


    def fredDict_from_folderPath(folderPath, knowledgeProcessor, outPath=None):
        """
        Args: folderPath to folder containing files from which to read,
        knowledgeProcessor for token extraction.
        Returns: dict mapping knowledge tokens to tuple of (termFreq, docFreq)
        observed in documents.
            termFreq = (number of times a token is used) / (number of words used)
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
