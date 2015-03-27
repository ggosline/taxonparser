# -*- coding: utf-8 -*-

__author__ = 'gg12kg'

import csv
from six863.parse.category import GrammarCategory

lexicon = {}

multiwords = {}


class LexEntry():
    def __init__(self, POS, wordlist, category=None, appliesto=None):
        self.POS = POS
        self.wordlist = wordlist
        self.category = category
        self.appliesto = appliesto


def addlexicon(words, POS):
    for word in words:
        addlexentry(word, POS, None, None)


def addlexentry(word, POS, category, appliesto):
    ws = word.strip('_').split('_')
    if len(ws) > 1:
        firstword = ws[0]
        if firstword in multiwords:
            multiwords[firstword] += [tuple(ws)]
        else:
            multiwords[firstword] = [tuple(ws)]
    # lexicon[tuple(ws)] = LexEntry(POS, tuple(ws), category, appliesto)
    features = {'pos': POS, 'category': category, 'appliesto': appliesto}
    lexicon.setdefault(tuple(ws), []).append(GrammarCategory(features=features))


def readcpglossary(gfile=r'..\resources\glossarycp.csv'):
    with open(gfile) as csvfile:
        mydictreader = csv.DictReader(csvfile)
        for gentry in mydictreader:
            term, category, appliesto = gentry['term'], gentry['category'], gentry['appliesTo']
            if category in ('structure', 'FEATURE', 'substance', 'life_style', 'PLANT', 'taxonomy', 'EN'):
                POS = 'NN'
            elif category != '':
                POS = 'JJ'
            else:
                POS = 'UNK'
            addlexentry(term, POS, category, appliesto)


COORDCONJUNCTION = 'and|or|and/or|neither|nor|otherwise|except|except_for|×'.split('|')
addlexicon(COORDCONJUNCTION, 'CC')

SUBCONJUNCTION = 'but|for|yet|so|although|because|since|unless'.split('|')
addlexicon(SUBCONJUNCTION, 'CJ')

ARTICLE = 'the|a|an'.split('|')
addlexicon(ARTICLE, 'ART')

DETERMINER = 'each|every|some|all|other|both|their'.split('|')
addlexicon(DETERMINER, 'DET')

PUNCTUATION = ';|(|)'.split('|')
addlexicon(PUNCTUATION, 'PUNC')

addlexicon([','], 'COMMA')

PRONOUN = 'it|one|ones|form|forms|parts'.split('|')
addlexicon(PRONOUN, 'PRO')

PREPOSITION = 'above|across|after|along|among|amongst|around|as|at|before|behind|below|beneath|between|beyond|by|' \
              'during|for|from|in|inside|into|near|of|off|on|onto|out|outside|over|per|than|through|throughout|toward|' \
              'towards|up|upward|with|within|without|when|owing_to|due_to|according_to|on_account_of|if'.split('|')
addlexicon(PREPOSITION, 'PP')

GROUPS = "group|groups|clusters|cluster|arrays|array|series|fascicles|fascicle|" \
         "pairs|pair|row|rows|number|numbers|colonies".split('|')
addlexicon(GROUPS, 'NG')

LITNUMBERS = "zero|one|ones|first|two|second|half|three|third|thirds|four|fourth|fourths|quarter|" \
             "five|fifth|fifths|six|sixth|sixths|seven|seventh|sevenths|eight|eighths|eighth|" \
             "nine|ninths|ninth|tenths|tenth|1/2|1/3|2/3|1/4|1/5|2/5".split('|')
addlexicon(LITNUMBERS, 'NUML')

ORDNUMBERS = "principal|primary|secondary|tertiary|1st|2nd|3rd".split('|')
addlexicon(ORDNUMBERS, 'NUMO')

UNITS = "mm.|cm.|dm.|m.|km.".split('|')
addlexicon(UNITS, 'UNIT')

DIMENSION = "high|tall|long|wide|diam.|diameter|diam".split('|')
addlexicon(DIMENSION, 'DIM')

RANGE = 'up_to|at_least'.split('|')
addlexicon(RANGE, 'PR')

POSITIONA = 'upper|lower|uppermost|lowermost|various'.split('|')
addlexicon(POSITIONA, 'AJP')

POSITION = 'top|on_bottom|base|at apex|front|back|both_sides|each_side|section|rest_of'.split('|')
addlexicon(POSITION, 'NP')

ACCURACY = "c.|about|more_or_less|±|very|a_little|not_much|all|rather|exactly".split('|')
addlexicon(ACCURACY, 'AVA')

FREQUENCY = "sometimes|often|usually|rarely|generally|never|always|soon|also|even".split('|')
addlexicon(FREQUENCY, 'AVF')

DEGREE = "almost|sparsely|densely|slightly|narrowly|widely|markedly|somewhat|shallowly|much".split('|')
addlexicon(DEGREE, 'AVD')

COMPARISON = "paler|darker|shorter|longer|wider|narrower|bigger|smaller|duller|shinier|higher|shorter|" \
             "older|younger|" \
             "exceeding|equalling|as_long_as|indistinguishable_from".split('|')
addlexicon(COMPARISON, 'AJC')

COMPADJ = "more|less|most|least".split('|')
addlexicon(COMPADJ, 'AJCA')

TIMING = "at_first|when young|becoming|remaining|turning".split('|')
addlexicon(TIMING, 'AJT')

VERB = 'to_form|forming'.split('|')
addlexicon(VERB, 'PV')

addlexicon(['to'], 'TO')
addlexicon(['not'], 'NOT')

readcpglossary()

for wlist in multiwords.values():
    wlist = sorted(wlist, key=len)

pass