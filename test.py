from structs.tokenizer import Tokenizer
from structs.tokengraph import TokenGraph

tokenizerObj = Tokenizer()
tokenizerObj.language_from_wiki_file(minFreq=0.0000001, maxFreq=0.0007,
                                    tokenNum=50000)
tokenizerObj.save('data/outData/50000_Tokenizer')


graphObj = TokenGraph(tokenizerObj)
graphObj.build_corr_matrix_from_iterator(x.wiki_iterator)
graphObj.save('data/outData/10000Text_graphObj')

del tokenizerObj

while True:
    t = input('t: ')
    z.search_related_tokens(t)
