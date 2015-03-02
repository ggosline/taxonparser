__author__ = 'gg12kg'

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
             "nine|ninths|ninth|tenths|tenth|1/2|1/3|2/3|1/4|1/5".split('|')

ORDNUMBERS = "primary|secondary|tertiary".split('|')

UNITS = "mm.|cm.|dm.|m.|km.".split('|')

DIMENSION = "high|tall|long|wide|diam.|diameter".split('|')

ACCURACY = "c.|about|more_or_less|±|very|a_little|not_much|all|rather|up_to|exactly".split('|')

FREQUENCY = "sometimes|often|usually|rarely|generally|never|always".split('|')

DEGREE = "almost|sparsely|densely|slightly|narrowly|widely|markedly|somewhat|shallowly".split('|')

COMPARISON = "paler|darker|shorter|longer|wider|narrower|bigger|smaller|duller|shinier|higher|shorter".split('|')

TO = ['to']

lexicon = {}


def addlexicon(words: list, POS: str):
    for word in words:
        ws = word.split('_')
        firstword = ws[0]
        if firstword in lexicon:
            lexicon[firstword] += (POS, tuple(ws))
        else:
            lexicon[firstword] = [(POS, tuple(ws))]
    pass


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

pass