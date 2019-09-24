from tokenizer import Tokenizer

x = Tokenizer()

# x.language_from_wiki_file(minFreq=0, maxFreq=1, tokenNum=10000)

x.load('data/outData/10000_token_test')

print(x)

while True:
    t = input('t: ')
    print(x.single_mechanically_score_tokens(t))
