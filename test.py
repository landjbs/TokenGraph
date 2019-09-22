from tokenizer import Tokenizer

x = Tokenizer()

x.language_from_wiki_file(minFreq=0, maxFreq=1, tokenNum=100)

print(x.idx)

while True:
    t = input('t: ')
    print(x.clean_and_tokenize(t))
