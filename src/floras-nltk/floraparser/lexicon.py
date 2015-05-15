# -*- coding: utf-8 -*-

__author__ = 'gg12kg'

import csv
import pickle
import os

from nltk.grammar import FeatStructNonterminal, TYPE, SLASH

lexicon = {}

multiwords = {}


def pickle_lexicon():
    global lexicon, multiwords
    # class LexEntry():
    # def __init__(self, POS, wordlist, category=None, appliesto=None):
    # self.POS = POS
    # self.wordlist = wordlist
    #         self.category = category
    #         self.appliesto = appliesto
    def addlexicon(words, POS, **morefeatures):
        for word in words:
            addlexentry(word, POS, **morefeatures)

    def addlexentry(word, POS, **morefeatures):
        ws = word.strip('_').split('_')
        if len(ws) > 1:
            firstword = ws[0]
            if firstword in multiwords:
                multiwords[firstword] += [tuple(ws)]
            else:
                multiwords[firstword] = [tuple(ws)]
        # lexicon[tuple(ws)] = LexEntry(POS, tuple(ws), category, appliesto)
        features = {TYPE: POS, 'orth': word}
        for item in morefeatures.items():  # avoid null values
            if item[1]:
                features[item[0]] = item[1]
        lexicon.setdefault(tuple(ws), []).append(FeatStructNonterminal(features=features))

    def readcpglossary(gfile=r'..\resources\glossarycp.csv'):
        with open(gfile) as csvfile:
            mydictreader = csv.DictReader(csvfile)
            for gentry in mydictreader:
                gid, term, category, appliesto = gentry['ID'], gentry['term'], gentry['category'].lower(), gentry[
                    'appliesTo'].lower()
                if category in ('structure', 'feature', 'character',
                                'substance', 'life-form', 'plant', 'taxonomy', 'en', 'process'):
                    POS = 'N'
                elif category != '':
                    POS = 'A'
                else:
                    POS = 'UNK'
                if gid != '#':
                    addlexentry(term, POS, category=category, appliesto=appliesto)

    COORDCONJUNCTION = 'and|or|and/or|neither|nor|otherwise|but|except|except_for|×'.split('|')
    for word in COORDCONJUNCTION:
        addlexentry(word, 'CONJ', conj=word, coord=True)
    SUBCONJUNCTION = 'but|for|yet|so|although|because|since|unless|if'.split('|')
    for word in SUBCONJUNCTION:
        addlexentry(word, 'CONJ', conj=word, coord=False)
    ARTICLE = 'the|a|an'.split('|')
    addlexicon(ARTICLE, 'ART')
    DETERMINER = 'each|every|some|all|other|both|their'.split('|')
    addlexicon(DETERMINER, 'DET')
    PUNCTUATION = ';|(|)'.split('|')
    for char in PUNCTUATION:
        addlexentry(char, 'PUNC', punc=char)
    addlexicon([','], 'COMMA')
    PRONOUN = 'it|one|ones|form|forms|part|parts'.split('|')
    addlexicon(PRONOUN, 'PRO')
    PREPOSITION = 'across|after|along|among|amongst|around|as|at|before|behind|below|beneath|between|beyond|by|' \
                  'during|for|from|in|inside|into|near|off|on|onto|out|outside|over|per|through|throughout|toward|' \
                  'towards|up|upward|with|within|without|when|owing_to|due_to|according_to|on_account_of|' \
                  'tipped_by|to_form'.split('|')
    for word in PREPOSITION:
        addlexentry(word, 'P', prep=word)
    GROUPS = "group|groups|clusters|cluster|arrays|array|series|fascicles|fascicle|" \
             "pairs|pair|row|rows|number|numbers|colonies".split('|')
    addlexicon(GROUPS, 'N', group=True)
    LITNUMBERS = "zero|one|ones|first|two|second|half|three|third|thirds|four|fourth|fourths|quarter|" \
                 "five|fifth|fifths|six|sixth|sixths|seven|seventh|sevenths|eight|eighths|eighth|" \
                 "nine|ninths|ninth|tenths|tenth|1/2|1/3|2/3|1/4|1/5|2/5".split('|')
    addlexicon(LITNUMBERS, 'NUM', literal=True)
    ORDNUMBERS = "principal|primary|secondary|tertiary|1st|2nd|3rd".split('|')
    addlexicon(ORDNUMBERS, 'NUM', ordinal=True)
    UNITS = "mm.|cm.|dm.|m.|km.".split('|')
    addlexicon(UNITS, 'UNIT')
    DIMENSION = "high|tall|long|wide|diam.|diameter|diam|".split('|')
    addlexicon(DIMENSION, 'DIM')
    RANGE = 'up_to|at_least|to'.split('|')
    addlexicon(RANGE, 'ADV')
    POSITIONA = 'below|above|upper|lower|uppermost|lowermost|various|beneath|above_and_beneath|between|' \
                'at_the_base|near_the_base|at_the_apex|outside|inside'.split('|')
    addlexicon(POSITIONA, 'A', position=True, category='position')
    POSITION = 'top|bottom|underside|base|apex|front|back|both_sides|both_surfaces|each_side|section|rest_of'.split('|')
    addlexicon(POSITION, 'N', position=True, category='position')
    ACCURACY = "c.|about|more_or_less|±|exactly".split('|')
    addlexicon(ACCURACY, 'ADV', accuracy=True, timing=False)
    FREQUENCY = "very|a_little|not_much|all|rather|sometimes|often|usually|rarely|generally|never|always|soon|also|even".split(
        '|')
    addlexicon(FREQUENCY, 'ADV', frequency=True, timing=False)
    DEGREE = "almost|sparsely|densely|slightly|narrowly|widely|markedly|somewhat|shallowly|much|dark|light".split('|')
    addlexicon(DEGREE, 'ADV', degree=True, timing=False)
    COMPARISON = "paler|darker|lighter|shorter|longer|wider|narrower|bigger|smaller|duller|shinier|higher|shorter|" \
                 "older|younger|" \
                 "exceeding|equalling|as_long_as|indistinguishable_from".split('|')
    addlexicon(COMPARISON, 'A', compar=True, category='compar')
    COMPADJ = "more|less|most|least".split('|')
    addlexicon(COMPADJ, 'A', makecomp=True)
    TIMING = "at_first|when_young|becoming|remaining|turning|in_age|at_maturity|later|at_length".split('|')
    addlexicon(TIMING, 'ADV', timing=True)
    PRESENCE = "present|absent".split('|')
    addlexicon(PRESENCE, 'A', category='presence')
    GERUND = "covering|closing|enveloping|surrounding|forming|terminating|dehiscing_by|dividing|" \
             "ending|varying_in|arranged_in".split(
        '|')
    addlexicon(GERUND, 'P', verb=True)
    addlexicon(['to'], 'TO')
    addlexicon(['not'], 'NOT')
    addlexicon(['in'], 'IN')
    addlexicon(['than'], 'THAN')
    addlexicon(['for'], 'FOR')
    addlexicon(['that'], 'RCOMP')
    addlexicon(['that'], 'COMP')
    addlexicon(['times'], 'TIMES')
    addlexicon(['NUM'], 'NUM')
    addlexicon(['of'], 'OF')
    readcpglossary()
    # for wlist in multiwords.values():
    # wlist = sorted(wlist, key=len)
    with open('lexicon.pickle', 'wb') as f:
        pickle.dump(lexicon, f)
    with open('multiwords.pickle', 'wb') as f:
        pickle.dump(multiwords, f)


if __name__ == '__main__':
    lexicon = {}
    multiwords = {}
    pickle_lexicon()
else:
    savedir = os.curdir
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    with open('lexicon.pickle', 'rb') as f:
        lexicon = pickle.load(f)
    with open('multiwords.pickle', 'rb') as f:
        multiwords = pickle.load(f)
    os.chdir(savedir)