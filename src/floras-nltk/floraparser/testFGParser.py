__author__ = 'Geoge'

import sys

from collections import defaultdict
from floracorpus.reader import AbstractFloraCorpusReader, FloraCorpusReader

from nltk.parse import FeatureEarleyChartParser, FeatureIncrementalBottomUpLeftCornerChartParser, FeatureChartParser
from nltk.parse import FeatureBottomUpChartParser, FeatureBottomUpLeftCornerChartParser
from floraparser.FGParser import FGParser, cleanparsetree, FindNode
from floraparser.fltoken import FlToken

trec = defaultdict(lambda: None)

description = 'Leaf-lamina 5–20 × 3·5–19 cm., ovate or narrowly ovate in outline'  # , cordate, ± hairy (especially on the veins), becoming scabrid-punctate, usually deeply palmately 3–5-lobed, with the lobes elliptic, shallowly to usually deeply ± pinnately lobulate, subentire or obscurely sinuate-denticulate, rounded to subacute, apiculate, with the central one  largest.'
fromDB = False
parser = FeatureBottomUpLeftCornerChartParser
parser = FeatureEarleyChartParser
cleantree = True
ttrace = 3

trec['description'] = description
trdr = [trec]
ttaxa = AbstractFloraCorpusReader(reader=trdr)
tfilebase = r'..\..\..\temp\tree'

of = sys.stdout
if __name__ == '__main__':
    if fromDB:
        ttrace = 0
        ttaxa = FloraCorpusReader(db=r'..\resources\efloras.db3',
                                  query="Select * from AllTaxa where flora_name = 'FZ' and rank = 'species' and genus = 'Ficus' and species = 'asperifolia';", )
        of = open('testphrases.txt', 'w', encoding='utf-8')
    parser = FGParser(parser=parser, trace=ttrace)
    for taxon in ttaxa.taxa:
        for sent in taxon.sentences:
            for i, phrase in enumerate(sent.phrases):
                trees = parser.parse(phrase.tokens, cleantree=cleantree, maxtrees=100)
                if trees:
                    print('Success: ' + phrase.text, file=of)
                    print('No. of trees: %d' % len(trees), file=of)
                    if ttrace:
                        for i, treex in enumerate(trees):
                            # cleanparsetree(treex)
                            treex.draw()
                            if True and i <= 20:
                                tfilename = tfilebase + str(i)
                                tfile = open(tfilename, mode='w', encoding='utf-8')
                                print(treex, file=tfile)
                                tfile.close
                    print(FindNode('SUBJECT', trees[0]))
                else:
                    print('Fail:    ' + phrase.text, file=of)
                    trees = parser.partialparses()
                    print('No. of trees: %d' % len(trees), file=of)
                    if ttrace:
                        for treex in trees[0:40]:
                            cleanparsetree(treex)
                            treex.draw()
                    if trees:
                        print(FindNode('SUBJECT', trees[0]))
    of.close()

