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

x = {'a' : [np.random.randint(0,10) for _ in range(np.random.randint(0, 100))]
    for _ in range(100)}

z = set()

for t in x.keys():
    z.add(t)

for l in x.values():
    for e in l:
        z.add(e)

print(z)
