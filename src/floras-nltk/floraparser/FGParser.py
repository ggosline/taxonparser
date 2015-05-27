__author__ = 'gg12kg'
import sys

import nltk
from nltk import grammar, parse
from nltk.grammar import FeatureGrammar, FeatStructNonterminal, FeatStructReader, read_grammar, SLASH, TYPE, Production, \
    Nonterminal
from nltk.parse.featurechart import FeatureChart
from nltk.featstruct import FeatStruct, Feature, FeatList
from floraparser import lexicon
from floraparser.fltoken import FlToken
from nltk import Tree, ImmutableTree

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
            fstruct_reader = FeatStructReader(features, FeatStructNonterminal, FeatListNonterminal,
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
                newprod = Production(lexlhs, ['_'.join(wordtuple)])
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

    def parse(self, tokens, cleantree=True, maxtrees=200):
        '''
        :type tokens: builtins.generator
        :return:
        '''
        # check for tokens added by the POS processor -- e.g. ADV
        newprod = False
        for fltoken in tokens:
            if not self._grammar._lexical_index.get(fltoken.lexword):
                newprod = True
                for lexent in fltoken.lexentry:
                    lexrhs = fltoken.lexword
                    newprod = Production(lexent, (lexrhs,))
                    self._grammar._productions.append(newprod)
        if newprod:
            self._grammar.__init__(self._grammar._start, self._grammar._productions)

        tokens = tokens + [FGTerminal('$')]

        self._chart = self._parser.chart_parse([tk for tk in tokens])
        treegen = self._chart.parses(self._grammar.start(), tree_class=nltk.Tree)
        trees = []
        for i, tree in enumerate(treegen):
            if i >= maxtrees:
                break
            if cleantree:
                cleanparsetree(tree)
            if tree not in trees:
                trees.append(tree)
        return trees

    def partialparses(self):
        '''
        In a failed parse check for candidate trees labelled with CHAR
        parse must have been called first! to generate the chart
        '''

        trees = []

        charedges = list(self.simple_select(is_complete=True, lhs='SUBJECT'))
        for charedge in charedges:
            for tree in self._chart.trees(charedge, complete=True, tree_class=nltk.Tree):
                trees.append((tree, charedge.start(), charedge.end()))

        charedges = list(self.simple_select(is_complete=True, lhs='CHR'))

        for charedge in charedges:
            for tree in self._chart.trees(charedge, complete=True, tree_class=nltk.Tree):
                newtree = False
                if not trees:
                    trees.append((tree, charedge.start(), charedge.end()))
                else:
                    for (t, tstart, tend) in trees[:]:
                        if charedge.start() <= tstart and charedge.end() >= tend:  # subsumes
                            trees.remove((t, tstart, tend))
                        elif (charedge.start() >= tstart and charedge.end() < tend) \
                                or (charedge.start() > tstart and charedge.end() <= tend):  # subsumed
                            newtree = False
                            continue
                        newtree = True
                    if newtree:
                        trees.append((tree, charedge.start(), charedge.end()))

        return [t for t, _, _ in trees]

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


class FGTerminal(FlToken):
    def __init__(self, char):
        self.lexword = char

    @property
    def text(self):
        return self.lexword

    def __repr__(self):
        return 'EOPHRASE'


def cleanparsetree(tree):
    purgenodes(tree, ['CTERMINATOR'])
    flattentree(tree, 'CHARLIST')
    collapse_unary(tree)


def collapse_unary(tree, collapsePOS=False, collapseRoot=False, joinChar="+"):
    """
    Collapse subtrees with a single child (ie. unary productions)
    into a new non-terminal (Tree node) joined by 'joinChar'.
    This is useful when working with algorithms that do not allow
    unary productions, and completely removing the unary productions
    would require loss of useful information.  The Tree is modified
    directly (since it is passed by reference) and no value is returned.

    :param tree: The Tree to be collapsed
    :type  tree: Tree
    :param collapsePOS: 'False' (default) will not collapse the parent of leaf nodes (ie.
                        Part-of-Speech tags) since they are always unary productions
    :type  collapsePOS: bool
    :param collapseRoot: 'False' (default) will not modify the root production
                         if it is unary.  For the Penn WSJ treebank corpus, this corresponds
                         to the TOP -> productions.
    :type collapseRoot: bool
    :param joinChar: A string used to connect collapsed node values (default = "+")
    :type  joinChar: str
    """

    if collapseRoot == False and isinstance(tree, Tree) and len(tree) == 1:
        nodeList = [tree[0]]
    else:
        nodeList = [tree]

    # depth-first traversal of tree
    while nodeList != []:
        node = nodeList.pop()
        if isinstance(node, Tree):
            if len(node) == 1 and isinstance(node[0], Tree) and (collapsePOS == True or isinstance(node[0, 0], Tree)):
                node[0:] = [child for child in node[0]]
                # since we assigned the child's children to the current node,
                # evaluate the current node again
                nodeList.append(node)
            else:
                for child in node:
                    nodeList.append(child)


def purgenodes(tree, typelist):
    if isinstance(tree, Tree):
        for i, child in enumerate(tree):
            if isinstance(child, Tree) and isinstance(child.label(), FeatStructNonterminal) and child.label()[
                TYPE] in typelist:
                del tree[i]
            else:
                purgenodes(child, typelist)


def flattentree(tree: Tree, listnodetype):
    # Traverse the tree-depth first keeping a pointer to the parent for modification purposes.
    nodeList = [(tree, [])]
    while nodeList != []:
        node, parent = nodeList.pop()
        if isinstance(node, Tree):
            # if the node contains the 'childChar' character it means that
            # it is an artificial node and can be removed, although we still need
            # to move its children to its parent
            if isinstance(node.label(), FeatStructNonterminal) and node.label()[TYPE] == listnodetype:
                nodeIndex = parent.index(node)
                del parent[nodeIndex]
                # Generated node was on the left if the nodeIndex is 0 which
                # means the grammar was left factored.  We must insert the children
                # at the beginning of the parent's children
                if nodeIndex == 0:
                    parent.insert(0, node[0])
                    if len(node) > 1:
                        parent.insert(1, node[1])
                else:
                    parent.extend(node[:])

                # parent is now the current node so the children of parent will be added to the agenda
                node = parent

            for child in node:
                nodeList.append((child, node))


def FindNode(lab:str, tree:Tree) -> Tree:
    if tree.label()[TYPE] == lab:
        return tree
    for t in tree:
        if isinstance(t, Tree):
            return FindNode(lab, t)


class FeatListNonterminal(FeatList, Nonterminal):
    """A feature structure that's also a nonterminal.  It acts as its
    own symbol, and automatically freezes itself when hashed."""

    def __hash__(self):
        self.freeze()
        return FeatStruct.__hash__(self)

    def symbol(self):
        return self
