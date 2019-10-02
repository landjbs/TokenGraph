# import graphrank

# from structs.tokenizer import Tokenizer
# from structs.tokengraph import TokenGraph

# tokenizerObj = Tokenizer()
# tokenizerObj.language_from_wiki_file(minFreq=-1000000, maxFreq=1000000,
#                                     tokenNum=50000)
# tokenizerObj.save('data/outData/50000_Tokenizer')

# tokenizerObj = Tokenizer()
# tokenizerObj.load('data/outData/50000_Tokenizer')
# print(tokenizerObj)
#
# graphObj = TokenGraph(tokenizerObj)
# graphObj.build_corr_matrix_from_iterator(tokenizerObj.wiki_iterator)
# graphObj.save('data/outData/10000Text_graphObj')
#
# del tokenizerObj

# graphObj = TokenGraph()
# graphObj.load('data/outData/10000Text_graphObj')
#
# while True:
#     t = input('t: ')
#     topTokens = (graphObj.graph_rank_text(t))
#     for id, score in topTokens:
#         word = graphObj.tokenizer.reverseIdx[id]
#         print(f'<{score}> {word}')


import numpy as np
from time import time

def make_big():
    return np.random.randint(0, 10000, size=100000)

def sort_1(l, n):
    newList = []
    for i in range(n):
        minLoc = l.index(min(l))
        newAdd = l.pop(minLoc)
        newList += newAdd
    return newList

def sort_2(l, n):
    newList = l[:n]
    maxElt = max(newList)
    maxLoc = newList.index(maxElt)
    for elt in l:
        if elt < maxElt:
            _ = newList.pop(maxLoc)
            newList.append(elt)
            maxElt = max(newList)
            maxLoc = newList.index(maxElt)
    newList.sort()
    return newList


t_1 = 0
t_2 = 0
iter = 100
n = 50

from tqdm import tqdm

for i in tqdm(range(iter)):
    x = make_big()
    # 1
    s_1 = time()
    l_1 = sort_1(x, n)
    t_1 += time() - s_1
    # 2
    s_2 = time()
    l_2 = sort_2(x, n)
    t_2 += time() - s_2
    if not l_1 == l_2:
        print('No')

print(f'Results:\n\tMethod 1: {t_1 / iter}\n\tMethod 2: {t_2 / iter}')
