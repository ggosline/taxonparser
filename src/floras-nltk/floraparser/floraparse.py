
__author__ = 'gg12kg'
from collections import defaultdict
from parse.featurechart import FeatureEarleyChartParse
from parse.category import GrammarFile

# from floracorpus.reader import FloraCorpusReader
from floraparser import lexicon
from floraparser.fltoken import FlSentence
from floracorpus.reader import AbstractFloraCorpusReader
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

description1 = 'Shrublets or shrubs or small trees ' \
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
               ', broadly cuneate at the base, smaller on the flowering branches; ' \
               'petiole 0·5–0·8 cm. long. ' \
               'Flowers white, in subinterpetiolar dichotomous cymes. ' \
               'Petals 3 times as long as the pubescent calyx-lobes. ' \
               'Fruit yellow-orange, c. 1 cm. long, slightly compressed, tipped by the persistent style.'

trec['description'] = description2
trdr = [trec]
ttaxa = AbstractFloraCorpusReader(reader=trdr)

if __name__ == '__main__':
    # myds = FloraCorpusReader(db=r'..\resources\efloras.db3',
    # query="Select * from Taxa where family = 'Celastraceae';", )

    grammar = load_earley('flg.cfg')
    trees = grammar.get_parse(ttaxa.taxa[0].sentences[3].phrases[0])
    for tree in trees:
        tree.draw()