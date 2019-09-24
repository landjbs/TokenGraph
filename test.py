from tokenizer import Tokenizer
from tokengraph import TokenGraph

x = Tokenizer()

x.load('data/outData/10000_token_test')

z = TokenGraph(x)

z.build_corr_matrix_from_iterator(x.wiki_iterator)
