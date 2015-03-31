__author__ = 'gg12kg'

from parse.featurechart import FeatureEarleyChartParse
from parse.category import GrammarFile

# from floracorpus.reader import FloraCorpusReader
from floraparser import lexicon
from floraparser.fltoken import FlSentence

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

class TaxonTest():
    description = 'Shrublets or shrubs or small trees ' \
                  '(0·3)1–8 m. high' \
                  ', sometimes sarmentose' \
                  ', without latex '
    # '; branches 4-lined, reddish-purple to reddish-brown with numerous pale somewhat prominent lenticels and sometimes puberulous when young' \
    # ', becoming eventually terete, pale grey or cream, glabrous, slender.'
    # ', with spines up to 8 cm. long, axillary or terminating short axillary branches' \


tsent = FlSentence(TaxonTest, 0, len(TaxonTest.description))

if __name__ == '__main__':
    # myds = FloraCorpusReader(db=r'..\resources\efloras.db3',
    # query="Select * from Taxa where family = 'Celastraceae';", )

    grammar = load_earley('flg.cfg')
    trees = grammar.get_parse(tsent.phrases[0])
    for tree in trees:
        print(tree)