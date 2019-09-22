
def wiki_iterator():
    with open('data/inData/wikiArticles.csv', 'r') as wikiFile:
        for line in wikiFile:
            commaLoc = line.find(',')
            articleText = line[commaLoc+3:-3]
            yield articleText
