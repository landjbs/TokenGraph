"""
Implements Tokenizer() class for preprocessing and tokenizing raw-text and
Language() class for storing metrics about the language used.
"""

import re
from unidecode import unidecode
from collections import Counter

class Tokenizer(object):
    """ Stores all methods for working with text """
    def __init__(self, lower=True):
        """ """
        assert isinstance(lower, bool), ('lower expected type bool, but found '
                                        f'type {type(lower)}.')
        self.lower = lower
        # matches non-alphanumeric, space, or sentence-ending punctuation (dash must be at end)
        self.STRIP = re.compile(r'[^0-9a-zA-Z\t\n\s_.?!:;/<>*&^%$#@()"~`+-]')
        # matches any sequence of tabs, newlines, spaces, underscores, and dashes
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


class Language(object):
    """ Defines properties of the Language being delt with """
    def __init__(self, name, tokenizer, vocabFreqs=None):
        assert isinstance(tokenizer, Tokenizer), 'tokenizer expected type Tokenizer()'
        assert isinstance(vocabFreqs, None) or isinstance(vocabFreqs, dict), 'vocabFreqs expected either dict or None'
        self.name = name
        self.tokenizer = tokenizer
        self.vocabFreqs = vocabFreqs
        self.vocabSize = len(vocabSet) if vocabSet else None
        self.idx = None
        self.reverseIdx = None

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
