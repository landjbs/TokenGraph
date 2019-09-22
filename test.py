from tokenizer import Tokenizer

x = Tokenizer()

x.freqDict = {'the':(1)}

x.build_tokenizer(10,-1, 1)

print(x.tokenizer)
