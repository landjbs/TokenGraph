from tokenizer import Tokenizer

x = Tokenizer()

x.freq_dict_from_wiki_file()

print(self.freqDict)

x.filter_freq_dict(tokenNum=10)

print(self.freqDict)
