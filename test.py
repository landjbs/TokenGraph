import graphrank

# from structs.tokenizer import Tokenizer
# from structs.tokengraph import TokenGraph
#
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
#
# graphObj = TokenGraph(tokenizerObj)
# graphObj.build_corr_matrix_from_iterator(x.wiki_iterator)
# graphObj.save('data/outData/10000Text_graphObj')
#
# del tokenizerObj
#
# while True:
#     t = input('t: ')
#     z.search_related_tokens(t)
