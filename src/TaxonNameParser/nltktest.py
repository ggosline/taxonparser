import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import WhitespaceTokenizer


corpus_root = 'E:\\WTA\\FWTA\\'

wordlists = PlaintextCorpusReader(corpus_root, '.*\.txt', encoding='latin1')

print(wordlists.fileids())

s = wordlists.raw()
spans = list(WhitespaceTokenizer().span_tokenize(s))

pass
