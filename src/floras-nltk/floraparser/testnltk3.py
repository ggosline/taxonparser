__author__ = 'Geoge'

import sys

import nltk
from nltk import grammar, parse
from nltk.grammar import FeatureGrammar, FeatStructNonterminal, FeatStructReader, read_grammar, SLASH, TYPE, Production

from collections import defaultdict
from floraparser import lexicon
from floraparser.fltoken import FlSentence, FlToken
from floracorpus.reader import AbstractFloraCorpusReader, FloraCorpusReader


class FGFlora(FeatureGrammar):
    @classmethod
    def fromstring(cls, input, features=None, logic_parser=None, fstruct_reader=None,
                   encoding=None, fltokens:[FlToken]=None):
        """
        Return a feature structure based ``FeatureGrammar``.

        :param input: a grammar, either in the form of a string or else
        as a list of strings.
        :param features: a tuple of features (default: SLASH, TYPE)
        :param logic_parser: a parser for lambda-expressions,
        by default, ``LogicParser()``
        :param fstruct_reader: a feature structure parser
        (only if features and logic_parser is None)
        """
        if features is None:
            features = (TYPE, SLASH)

        if fstruct_reader is None:
            fstruct_reader = FeatStructReader(features, FeatStructNonterminal,
                                              logic_parser=logic_parser)
        elif logic_parser is not None:
            raise Exception('\'logic_parser\' and \'fstruct_reader\' must '
                            'not both be set')

        start, productions = read_grammar(input, fstruct_reader.read_partial,
                                          encoding=encoding)
        if fltokens:
            for fltoken in fltokens:
                for lexent in fltoken.lexentry:
                    lexlhs = FeatStructNonterminal(**lexent._features)
                    lexlhs[TYPE] = lexent['pos']
                    newprod = Production(lexlhs, (fltoken,))
                    productions.append(newprod)
        return FeatureGrammar(start, productions)


trec = defaultdict(lambda: None)

description = 'lamina dull on both sides, (3·3)4·4–10·8(15) × (1·2)2·1–4·5 cm., reddish, oblong to elliptic-oblong,  acuminate, obtuse or retuse, with margin shallowly rounded-denticulate or rarely subentire, cuneate to rounded, chartaceous to softly coriaceous, with (6)7–10 lateral nerves'  # and ± densely reticulate venation varying in prominence'

trec['description'] = description
trdr = [trec]
ttaxa = AbstractFloraCorpusReader(reader=trdr)

with open('flg.fcfg', 'r', encoding='utf-8') as gf:
    gs = gf.read()

ttrace = 4
of = sys.stdout
if __name__ == '__main__':
    if False:
        ttrace = 0
        ttaxa = FloraCorpusReader(db=r'..\resources\efloras.db3',
                                  query="Select * from Taxa where genus = 'Salacia' and species = 'erecta';", )
        of = open('testphrases.txt', 'w', encoding='utf-8')
    alltokens = [tk for taxon in ttaxa.taxa for sent in taxon.sentences for tk in sent.tokens]
    pr = FGFlora.fromstring(gs, fltokens=alltokens)
    parser = parse.FeatureEarleyChartParser(pr, trace=ttrace)
    for taxon in ttaxa.taxa:
        for sent in taxon.sentences:
            for i, phrase in enumerate(sent.phrases):
                trees = list(parser.parse(phrase.tokens))
                if trees:
                    print('Success: ' + phrase.text, file=of)
                    print('No. of trees: %d' % len(trees), file=of)
                    if ttrace:
                        for treex in trees:
                            treex.draw()
                else:
                    print('Fail:    ' + phrase.text, file=of)
    of.close()

