"""
The SearchTable is a wide-column store in which tokens keys hash to numpy
arrays of page token vectors
"""

class SearchTable(object):
    def __init__(self, tokenGraph):
        self.tokenGraph = tokenGraph
        # build dict mappping each element of vocabulary to None
        idxDict = {token : None for token in tokenGraph.corrDict.keys()}

    def save(self, path):
        """ Saves search table to path """
        
