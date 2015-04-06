# coding: utf-8
__author__ = 'gg12kg'
from collections import defaultdict
import sys
from parse.featurechart import FeatureEarleyChartParse
from parse.category import GrammarFile

# from floracorpus.reader import FloraCorpusReader
from floraparser import lexicon
from floraparser.fltoken import FlSentence
from floracorpus.reader import AbstractFloraCorpusReader, FloraCorpusReader
# myds = FloraCorpusReader(db=r'..\resources\efloras.db3',
# query="Select * from Taxa where family = 'Celastraceae';", )


def lexicon(node):
    return node.lexentry


def load_earley(filename, trace=1):
    """
    Load a grammar from a file, and build an Earley feature parser based on
    that grammar.

    You can optionally specify a tracing level, for how much output you
    want to see:

    0: No output.
    1: Show edges from scanner and completer rules (not predictor).
    2 (default): Show all edges as they are added to the chart.
    3: Show all edges, plus the results of successful unifications.
    4: Show all edges, plus the results of all attempted unifications.
    5: Show all edges, plus the results of all attempted unifications,
       including those with cached results.
    """

    grammar = GrammarFile.read_file(filename)
    return FeatureEarleyChartParse(grammar.earley_grammar(),
        lexicon=lexicon, trace=trace)


trec = defaultdict(lambda: None)

description1 = 'Shrublets, shrubs or small trees ' \
               '(0·3)1–8 m. high' \
               ', with spines up to 8 cm. long' \
               ', axillary or terminating short axillary branches' \
               ', sometimes sarmentose' \
               ', without latex ' \
               '; branches 4-lined, reddish-purple to reddish-brown, with numerous pale somewhat prominent lenticels, sometimes puberulous when young' \
               ', becoming eventually terete, pale grey or cream, glabrous, slender.'

description2 = 'A glabrous spiny scrambling shrub 5 m. high; ' \
               'branches alternate, terete, more or less flexuous' \
               ', shining, green; spines straight, very acute, c. 2·5 cm. long, subinterpetiolar' \
               ', in age apparently at the forks of the older branches. ' \
               'Leaf-lamina 4–6 × 2–2·5 cm., shining above, narrowly ovate, subacuminate and acute at the apex, margin spinulose-serrulate or subentire' \
               ', broadly cuneate at the base' \
               ', smaller on the flowering branches; ' \
               'petiole 0·5–0·8 cm. long. ' \
               'Flowers white, in subinterpetiolar dichotomous cymes. ' \
               'Petals 3 times as long as the pubescent calyx-lobes. ' \
               'Fruit yellow-orange, c. 1 cm. long, slightly compressed, tipped by the persistent style.'

description3 = 'lamina dull on both surfaces'  # , (3·3)4·4–10·8(15) × (1·2)2·1–4·5 cm., oblong or elliptic-oblong, acuminate, obtuse or retuse, with margin shallowly rounded-denticulate, rarely subentire, cuneate to rounded, chartaceous to softly coriaceous, with (6)7–10 lateral nerves and ± densely reticulate venation varying in prominence'

trec['description'] = description3
trdr = [trec]
ttaxa = AbstractFloraCorpusReader(reader=trdr)
ttrace = 1
ofile = sys.stdout
if __name__ == '__main__':
    if False:
        ttrace = 0
        ttaxa = FloraCorpusReader(db=r'..\resources\efloras.db3',
                                  query="Select * from Taxa where genus = 'Salacia' and species = 'erecta';", )
        ofile = open('testphrases.txt', 'w', encoding='utf-8')
    grammar = load_earley('flg.fcfg', trace=ttrace)
    with ofile as of:
        for taxon in ttaxa.taxa:
            for sent in taxon.sentences:
                for i, phrase in enumerate(sent.phrases):
                    trees = grammar.get_parse_list(phrase.tokens)
                    if trees:
                        print('Success: ' + phrase.text, file=of)
                        print('No. of trees: %d' % len(trees), file=of)
                        if ttrace:
                            for treex in trees:
                                treex.draw()
                    else:
                        print('Fail:    ' + phrase.text, file=of)