# -*- coding: utf-8 -*-

__author__ = 'gg12kg'

import csv
import pickle
import os
from nltk.featstruct import Feature, FeatStruct, FeatStructReader

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
    featurereader = FeatStructReader(fdict_class=FeatStructNonterminal)

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
        if 'category' not in morefeatures:
            category = ""
        else:
            category = morefeatures['category']
        # lexicon[tuple(ws)] = LexEntry(POS, tuple(ws), category, appliesto)
        featstring = POS + "[ category= '" + category + "', orth='" + word + "'] "
        newfeature = featurereader.fromstring(featstring)
        newfeature.update(morefeatures)

        # head = FeatStructNonterminal({'orth': word})
        # if 'category' in morefeatures:
        #     head['category'] = morefeatures['category']
        # features = {TYPE: POS, 'H': head}
        # for item in morefeatures.items():  # avoid null values
        #     # if item[1]:
        #     features[item[0]] = item[1]
        lexicon.setdefault(tuple(ws), []).append(newfeature)

    def readcpglossary(gfile=r'..\resources\glossarycp.csv'):
        with open(gfile) as csvfile:
            mydictreader = csv.DictReader(csvfile)
            for gentry in mydictreader:
                morefeatures = {}
                gid, term, category, appliesto = gentry['ID'], gentry['term'], gentry['category'].lower(), gentry[
                    'appliesTo'].lower()
                if category in ('structure', 'feature', 'character',
                                'substance', 'life-form', 'plant', 'taxonomy', 'en', 'process'):
                    POS = 'N'
                elif category != '':
                    POS = 'A'
                    morefeatures = {'position': False, 'timing': False}
                else:
                    POS = 'UNK'
                if gid != '#':
                    # addlexentry(term, POS, category=category, appliesto=appliesto, **morefeatures)
                    addlexentry(term, POS, category=category, **morefeatures)

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
    PREPOSITION = 'among|amongst|around|as|below|beneath|between|beyond|by|' \
                  'during|for|from|in|inside|into|near|off|on|onto|out|outside|over|per|through|throughout|toward|' \
                  'towards|up|upward|when|owing_to|due_to|according_to|on_account_of|' \
                  'tipped_by|to_form'.split('|')
    for word in PREPOSITION:
        addlexentry(word, 'P', prep=word, position=False)

    WITH = 'with|without'.split('|')
    for word in WITH:
        addlexentry(word, 'WITH', position=False, presence=True)
    POSITIONP = 'on|at|near|outside|inside|above|below|beneath|outside|inside|between|' \
                'before|after|behind|across|along|around|from|within|without|' \
                'attached_to'.split('|')
    for word in POSITIONP:
        addlexentry(word, 'P', prep=word, position=True)
    GROUPS = "group|groups|clusters|cluster|arrays|array|series|fascicles|fascicle|" \
             "pairs|pair|row|rows|number|numbers|colonies".split('|')
    addlexicon(GROUPS, 'N', group=True, category='grouping')
    LITNUMBERS = "zero|one|ones|first|two|second|half|three|third|thirds|four|fourth|fourths|quarter|" \
                 "five|fifth|fifths|six|sixth|sixths|seven|seventh|sevenths|eight|eighths|eighth|" \
                 "nine|ninths|ninth|tenths|tenth|1/2|1/3|2/3|1/4|1/5|2/5".split('|')
    addlexicon(LITNUMBERS, 'NUM', literal=True)
    ORDNUMBERS = "principal|primary|secondary|tertiary|1st|2nd|3rd".split('|')
    addlexicon(ORDNUMBERS, 'NUM', ordinal=True)
    UNITS = "mm.|cm.|dm.|m.|km.".split('|')
    addlexicon(UNITS, 'UNIT')
    DIMENSION = "high|tall|long|wide|diam.|diameter|diam|in_height|in_width|in_diameter".split('|')
    addlexicon(DIMENSION, 'DIM')
    RANGE = 'up_to|at_least|to'.split('|')
    addlexicon(RANGE, 'RANGE')
    POSITIONA = 'upper|lower|uppermost|lowermost|outer|inner|outermost|innermost|various|above_and_beneath'.split('|')
    addlexicon(POSITIONA, 'A', position=True, timing=False, category='position')

    POSITION = 'top|bottom|underside|base|apex|front|back|both_sides|both_surfaces|each_side|section|rest_of'.split('|')
    addlexicon(POSITION, 'N', position=True, category='position')
    ACCURACY = "c.|about|more_or_less|±|exactly|almost".split('|')
    addlexicon(ACCURACY, 'DEG', accuracy=True, timing=False)
    FREQUENCY = "very|a_little|not_much|all|sometimes|often|usually|rarely|generally|never|always|" \
                "soon|also|even|especially|?".split('|')
    addlexicon(FREQUENCY, 'DEG', frequency=True, timing=False)
    DEGREE = "sparsely|densely|slightly|narrowly|widely|markedly|somewhat|rather|shallowly|much|dark|light".split('|')
    addlexicon(DEGREE, 'ADV', timing=False)
    COMPARISON = "paler|darker|lighter|shorter|longer|wider|narrower|bigger|smaller|duller|shinier|higher|" \
                 "older|younger|" \
                 "exceeding|equalling|as_long_as|indistinguishable_from".split('|')
    addlexicon(COMPARISON, 'A', compar=True, category='compar')
    COMPADJ = "more|less|most|least".split('|')
    addlexicon(COMPADJ, 'A', makecomp=True)
    TIMING = "at_first|when_young|becoming|remaining|turning|in_age|at_maturity|later|at_length|eventually".split('|')
    addlexicon(TIMING, 'A', timing=True, position=False)
    PRESENCE = "present|absent".split('|')
    addlexicon(PRESENCE, 'A', category='presence')
    ISA = "is|consisting_of".split('|')
    addlexicon(ISA, 'IS', category='ISA')
    GERUND = "covering|closing|enveloping|surrounding|forming|terminating|dehiscing_by|dividing|" \
             "ending|varying_in|arranged_in".split('|')
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