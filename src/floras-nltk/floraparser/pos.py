# -*- coding: utf-8 -*-
__author__ = 'George'

import re
from textblob import Word, TextBlob
from textblob.base import BaseTagger
from floraparser.botglossary import botglossary
from nltk.tag.api import TaggerI

fnaglossary = botglossary().glossary

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

# PREFIX = re.compile(r'\b(?P<prefix>ab|ad|bi|deca|de|dis|di|dodeca|endo|end|e|hemi|hetero|hexa|homo|infra|inter|ir|'
# r'macro|mega|meso|micro|'
#                     r'mid|mono|multi|ob|octo|over|penta|poly|postero|post|ptero|pseudo|quadri|quinque|semi|sub|sur|syn|'
#                     r'tetra|tri|uni|un|xero)(?P<root>.*)\b')
PREFIX = re.compile(r'\b(?P<prefix>ab|ad|bi|deca|dis|dodeca|hemi|hetero|hexa|homo|infra|inter|'
                    r'macro|mega|meso|micro|'
                    r'mid|mono|multi|ob|octo|over|penta|poly|postero|post|ptero|pseudo|quadri|quinque|semi|sub|sur|syn|'
                    r'tetra|tri|uni|xero)(?P<root>.+)\b')

# SUFFIX = re.compile(r"\b(?P<root>\w*)(?P<suffix>er|est|fid|form|ish|less|like|ly|merous|most|shaped)\b")
SUFFIX = re.compile(r"\b(?P<root>\w+)(?P<suffix>form|ish|merous|most|shaped)\b")

PLENDINGS = re.compile(r"(?:[^aeiou]ies|i|ia|(x|ch|sh)es|ves|ices|ae|s)$")

LITNUMBERS = "zero|one|ones|first|two|second|half|three|third|thirds|four|fourth|fourths|quarter|" \
             "five|fifth|fifths|six|sixth|sixths|seven|seventh|sevenths|eight|eighths|eighth|" \
             "nine|ninths|ninth|tenths|tenth|1/2|1/3|2/3|1/4|1/5".split('|')

ORDNUMBERS = "primary|secondary|tertiary".split('|')

NUMBERS = re.compile(r'^[0-9–—.·()]+$')

UNITS = "mm.|cm.|dm.|m.|km.".split('|')

DIMENSION = "high|tall|long|wide|diam.|diameter".split('|')

ACCURACY = "c.|about|more_or_less|±|very|a_little|not_much|all|rather|up_to|exactly".split('|')

FREQUENCY = "sometimes|often|usually|rarely|generally|never|always".split('|')

DEGREE = "almost|sparsely|densely|slightly|narrowly|widely|markedly|somewhat|shallowly".split('|')

COMPARISON = "paler|darker|shorter|longer|wider|narrower|bigger|smaller|duller|shinier|higher|shorter".split('|')

TO = ['to']


class FlTagger():
    def rootword(self, word):
        # hyphenated word
        if '-' in word:
            wrds = word.split('-')
            if NUMBERS.match(wrds[0]):
                rootw = '_' + wrds[1]
                return rootw, [wrds[1]]
            return wrds[-1], wrds[0:-1]

        # prefix or suffix
        m = PREFIX.match(word)
        if m:
            return m.group('root'), m.group('prefix')

        ms = SUFFIX.match(word)
        if ms:
            return ms.group('root'), ms.group('suffix')

    def singularize(self, word):  # Using textblob Word here
        """
        :param word: textblob.Word
        """
        if PLENDINGS.search(word):
            return word.singularize()


    def tag_word(self, tbword):
        """
        :param word: textblob.Word
        """
        word = Word(tbword.lower())
        if word in PUNCTUATION:
            return word, 'PUNC', None
        if word in PREPOSITION:
            return word, 'PP', None
        if word in COORDCONJUNCTION:
            return word, 'CC', None
        if word in TO:
            return 'to', 'TO', None
        if word in ARTICLE:
            return word, 'ART', None
        if NUMBERS.match(word):
            return word, 'NUM', None
        if word in ACCURACY:
            return word, 'RBA', None
        if word in FREQUENCY:
            return word, 'RBF', None
        if word in DEGREE:
            return word, 'RBD', None
        if word in NOT:
            return word, 'NOT', None
        if word in ORDNUMBERS:
            return word, 'NUMO', None
        if word in LITNUMBERS:
            return word, 'NUML', None
        if word in UNITS:
            return word, 'UNIT', None
        if word in DIMENSION:
            return word, 'DIM', None
        if word in COMPARISON:
            return word, 'JJC', None

        if word in fnaglossary:
            if fnaglossary[word].category in ('structure','FEATURE','substance''life-style','PLANT'):
                return word, 'NN', fnaglossary[word]
            else:
                # print(word, fnaglossary[word].category)
                return word, 'JJ', fnaglossary[word]

        ws = FlTagger.singularize(self, word)
        if ws in fnaglossary:
            if fnaglossary[ws].category in ('structure','FEATURE','substance''life-style','PLANT'):
                return ws, 'NNS', fnaglossary[ws]
        else:
            root = self.rootword(word)
            if root:
                if root[0] in fnaglossary:
                    return root, 'JJ', fnaglossary[root[0]]
                if '_' + root[0] in fnaglossary:
                    return root, 'JJ', fnaglossary['_' + root[0]]

        if word.endswith('ly'):
            return word, 'RB', None

        # Didn't find in fnaglossary; try WordNet
        # synsets = word.synsets
        # for sy in synsets:
        # pass

        return word, 'UNK', None

    # def tag(self, blob):
        # return [self.tag_word(word) for word in blob.words]


if __name__ == "__main__":
    tagger = FlTagger()
    testword = "3-locular"
    print(tagger.tag_word(testword))
    # print(posfromglossary(word))