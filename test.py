# import graphrank

from structs.tokenizer import Tokenizer
from structs.tokengraph import TokenGraph

# tokenizerObj = Tokenizer()
# tokenizerObj.language_from_wiki_file(minFreq=-1000000, maxFreq=1000000,
#                                     tokenNum=5000)
# tokenizerObj.save('data/outData/50000_Tokenizer')
#
# while True:
#     t = input('t: ')
#     if t == 'b':
#         break
#     else:
#         print(tokenizerObj.single_mechanically_score_tokens(t))
# 
# tokenizerObj = Tokenizer()
# tokenizerObj.load('data/outData/50000_Tokenizer')
# print(tokenizerObj)
#
# graphObj = TokenGraph(tokenizerObj)
# graphObj.build_corr_matrix_from_iterator(tokenizerObj.wiki_iterator)
# graphObj.save('data/outData/10000Text_graphObj')
#
# del tokenizerObj

graphObj = TokenGraph()
graphObj.load('data/outData/10000Text_graphObj')

while True:
    t = input('t: ')
    topTokens = (graphObj.graph_rank_text(t))
    for id, score in topTokens:
        word = graphObj.tokenizer.reverseIdx[id]
        print(f'<{score}> {word}')
