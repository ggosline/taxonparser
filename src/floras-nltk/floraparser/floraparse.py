__author__ = 'gg12kg'

from parse.featurechart import FeatureEarleyChartParse
from parse.category import GrammarFile

from floracorpus.reader import FloraCorpusReader
from floraparser import lexicon

myds = FloraCorpusReader(db=r'..\resources\efloras.db3',
                         query="Select * from Taxa where family = 'Celastraceae';", )


def lexicon(node):
    return node.lexicon


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


if __name__ == '__main__':
    # myds = FloraCorpusReader(db=r'..\resources\efloras.db3',
    # query="Select * from Taxa where family = 'Celastraceae';", )

    grammar = load_earley('../../six863/semantics/lab3-slash.cfg')
    print(grammar)