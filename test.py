# import graphrank

from structs.tokenizer import Tokenizer
from structs.tokengraph import TokenGraph

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

graphObj = TokenGraph()
graphObj.load('data/outData/10000Text_graphObj')
graphObj.TEMP_corr_matrix_to_dict(n=20)
graphObj.save('data/outData/10000Dict_graphObj')


while True:
    t = input('t: ')
    topTokens = (graphObj.DICT_graph_rank_text(t, 20, 0.00001))
    topList = [(score, id) for id, score in topTokens.items()]
    topList.sort(reverse=True, key=(lambda elt : elt[0]))
    for score, id in topList[:7]:
        word = graphObj.tokenizer.reverseIdx[id]
        print(f'<{score}> {word}')
