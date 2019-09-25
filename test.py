from tokenizer import Tokenizer
from tokengraph import TokenGraph

x = Tokenizer()

x.load('data/outData/10000_token_test')

z = TokenGraph(x)

z.build_corr_matrix_from_iterator(x.wiki_iterator)

print(z)

z.save('test')

del x
del z

z = TokenGraph()

z.load('test')

print(z)

while True:
    t = input('t: ')
    z.search_related_tokens(t)
