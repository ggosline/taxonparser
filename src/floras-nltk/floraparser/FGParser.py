__author__ = 'gg12kg'
import sys

import nltk
from nltk import grammar, parse
from nltk.grammar import FeatureGrammar, FeatStructNonterminal, FeatStructReader, read_grammar, SLASH, TYPE, Production
from nltk.parse.featurechart import FeatureChart
from floraparser import lexicon


class FGGrammar(FeatureGrammar):
    def __init__(self, start, productions):
        """
        Create a new feature-based grammar, from the given start
        state and set of ``Productions``.

        :param start: The start symbol
        :type start: FeatStructNonterminal
        :param productions: The list of productions that defines the grammar
        :type productions: list(Production)
        """
        FeatureGrammar.__init__(self, start, productions)

    @classmethod
    def fromstring(cls, input, features=None, logic_parser=None, fstruct_reader=None,
                   encoding=None):
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

        # Add the whole lexicon

        for wordtuple, featlist in lexicon.lexicon.items():
            for lexent in featlist:
                lexlhs = lexent
                newprod = Production(lexlhs, (wordtuple,))
                productions.append(newprod)

        return FGGrammar(start, productions)

    def check_coverage(self, tokens):
        '''
        Override the checking of lexical entries since we have already
        :param tokens:
        :return:
        '''
        pass


class FGParser():
    def __init__(self, grammarfile='flg.fcfg', trace=1, parser=parse.FeatureEarleyChartParser):
        with open(grammarfile, 'r', encoding='utf-8') as gf:
            gs = gf.read()
        self._grammar = FGGrammar.fromstring(gs)
        self._parser = parser(self._grammar, trace=trace)
        self._chart = None

    def parse(self, tokens):
        self._chart = self._parser.chart_parse(tokens)
        # charedges = list(chart.select(is_complete=True, lhs='CHAR'))
        # for charedge in charedges:
        # for tree in chart.trees(charedge, complete=True, tree_class=nltk.Tree):
        # trees.append(tree)
        #
        treegen = self._chart.parses(self._grammar.start(), tree_class=nltk.Tree)
        trees = list(treegen)
        return trees

    def partialparses(self):
        trees = []
        charedges = list(self.simple_select(is_complete=True, lhs='CHAR'))
        for charedge in charedges:
            for tree in self._chart.trees(charedge, complete=True, tree_class=nltk.Tree):
                trees.append(tree)
        return trees

    def simple_select(self, **restrictions):
        """
        Returns an iterator over the edges in this chart.
        See ``Chart.select`` for more information about the
        ``restrictions`` on the edges.
        """
        # If there are no restrictions, then return all edges.
        if restrictions == {}: return self._chart.edges()

        # Make sure it's a valid index.
        # for key in restrictions.keys():
        # if not hasattr(EdgeI, key):
        #         raise ValueError('Bad restriction: %s' % key)

        for edge in self._chart.edges():
            matched = True
            for key, val in restrictions.items():
                edval = self._chart._get_type_if_possible(getattr(edge, key)())
                if val != edval:
                    matched = False
                    break
            if matched:
                yield edge
