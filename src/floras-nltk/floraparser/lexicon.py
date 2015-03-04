__author__ = 'gg12kg'

import csv

COORDCONJUNCTION = 'and|or|nor|×'.split('|')
SUBCONJUNCTION = 'but|for|yet|so|although|because|since|unless'.split('|')

ARTICLE = 'the|a|an'.split('|')

PUNCTUATION = ',|;|(|)'.split('|')

NOT = 'not'

PREPOSITION = 'above|across|after|along|among|amongst|around|as|at|before|behind|below|beneath|between|beyond|by|' \
              'during|for|from|in|into|near|of|off|on|onto|out|outside|over|per|than|through|throughout|toward|' \
              'towards|up|upward|with|without|when'.split('|')

CLUSTERSTRINGS = "group|groups|clusters|cluster|arrays|array|series|fascicles|fascicle|" \
                 "pairs|pair|rows|number|numbers".split('|')

LITNUMBERS = "zero|one|ones|first|two|second|half|three|third|thirds|four|fourth|fourths|quarter|" \
             "five|fifth|fifths|six|sixth|sixths|seven|seventh|sevenths|eight|eighths|eighth|" \
             "nine|ninths|ninth|tenths|tenth|1/2|1/3|2/3|1/4|1/5|2/5".split('|')

ORDNUMBERS = "primary|secondary|tertiary".split('|')

UNITS = "mm.|cm.|dm.|m.|km.".split('|')

DIMENSION = "high|tall|long|wide|diam.|diameter".split('|')

ACCURACY = "c.|about|more_or_less|±|very|a_little|not_much|all|rather|up_to|exactly".split('|')

FREQUENCY = "sometimes|often|usually|rarely|generally|never|always".split('|')

DEGREE = "almost|sparsely|densely|slightly|narrowly|widely|markedly|somewhat|shallowly".split('|')

COMPARISON = "paler|darker|shorter|longer|wider|narrower|bigger|smaller|duller|shinier|higher|shorter".split('|')

TO = ['to']

lexicon = {}

multiwords = {}


class LexEntry():
    def __init__(self, POS:str, wordlist:tuple, category=None, appliesto=None):
        self.POS = POS
        self.wordlist = wordlist
        self.category = category
        self.appliesto = appliesto

def addlexicon(words: list, POS: str):
    for word in words:
        addlexentry(word, POS, None, None)


def addlexentry(word: str, POS: str, category, appliesto):
    ws = word.strip('_').split('_')
    if len(ws) > 1:
        firstword = ws[0]
        if firstword in multiwords:
            multiwords[firstword] += [tuple(ws)]
        else:
            multiwords[firstword] = [tuple(ws)]
    lexicon[tuple(ws)] = LexEntry(POS, tuple(ws), category, appliesto)


def readcpglossary(gfile=r'..\resources\glossarycp.csv'):
    with open(gfile) as csvfile:
        mydictreader = csv.DictReader(csvfile)
        for gentry in mydictreader:
            term, category, appliesto = gentry['term'], gentry['category'], gentry['appliesto']
            if category in ('structure', 'FEATURE', 'substance''life_style', 'PLANT'):
                POS = 'NN'
            else:
                POS = 'JJ'
            addlexentry(term, POS, category, appliesto)


addlexicon(PUNCTUATION, 'PUNC')

addlexicon(PREPOSITION, 'PP')

addlexicon(COORDCONJUNCTION, 'CC')

addlexicon(TO, 'TO')

addlexicon(ARTICLE, 'ART')

addlexicon(ACCURACY, 'RBA')

addlexicon(FREQUENCY, 'RBF')

addlexicon(DEGREE, 'RBD')

addlexicon(['not'], 'NOT')

addlexicon(ORDNUMBERS, 'NUMO')

addlexicon(LITNUMBERS, 'NUML')

addlexicon(UNITS, 'UNIT')

addlexicon(DIMENSION, 'DIM')

addlexicon(COMPARISON, 'JJC')

readcpglossary()

for wlist in multiwords.values():
    wlist = sorted(wlist, key=len)

pass