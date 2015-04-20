__author__ = 'Geoge'

import sys

from collections import defaultdict
from floracorpus.reader import AbstractFloraCorpusReader, FloraCorpusReader
import FGParser
from nltk.parse import FeatureEarleyChartParser, FeatureIncrementalBottomUpLeftCornerChartParser, FeatureChartParser

trec = defaultdict(lambda: None)

description = 'lamina dark green, glossy or  rather dull on both surfaces, (3·3)4·4–10·8(15) × (1·2)2·1–4·5 cm., oblong or elliptic-oblong to obovate, acuminate at the apex, obtuse or retuse, with margin shallowly rounded-denticulate, rarely subentire, cuneate to rounded at the base, chartaceous to softly coriaceous, with (6)7–10 lateral nerves, with ± densely reticulate venation varying in prominence'

trec['description'] = description
trdr = [trec]
ttaxa = AbstractFloraCorpusReader(reader=trdr)

ttrace = 4
of = sys.stdout
if __name__ == '__main__':
    if False:
        ttrace = 0
        ttaxa = FloraCorpusReader(db=r'..\resources\efloras.db3',
                                  query="Select * from Taxa where genus = 'Salacia' and species = 'erecta';", )
        of = open('testphrases.txt', 'w', encoding='utf-8')
    parser = FGParser.FGParser(parser=FeatureEarleyChartParser, trace=ttrace)
    for taxon in ttaxa.taxa:
        for sent in taxon.sentences:
            for i, phrase in enumerate(sent.phrases):
                tokens = [tk for tk in phrase.tokens]
                trees = parser.parse(tokens)
                if trees:
                    print('Success: ' + phrase.text, file=of)
                    print('No. of trees: %d' % len(trees), file=of)
                    if ttrace:
                        for treex in trees:
                            treex.draw()
                else:
                    print('Fail:    ' + phrase.text, file=of)
                    trees = parser.partialparses(tokens)
                    print('No. of trees: %d' % len(trees), file=of)
                    if ttrace:
                        for treex in trees:
                            treex.draw()

    of.close()

