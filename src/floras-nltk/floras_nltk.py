# -*- coding: utf-8 -*-

from pprint import pprint as pp
import re

import nltk
from nltk.data import LazyLoader

#from textblob import TextBlob, Blobber
#from floraparser.bits import find_ranges
#from floraparser.splitter import FlSentenceTokenizer
#from floraparser.pos import FlTagger
from floracorpus.reader import FloraCorpusReader

#nltk.internals.config_java(r"C:\Program Files\Java\jdk1.8.0\bin\java.exe")

testme = """\
Shrub or small tree (1·2)3–5(6) m. high, with rounded crown, without latex;
bark: smooth;
stems: ± flattened with paired raised lines at first, becoming terete and rugulose, densely chocolate-brown- to fawn-pubescent.
Leaves: opposite to subopposite or alternate, petiolate;
lamina: deep dull green above (drying grey-green), markedly paler below, (3·5)5–10·5(13·2) × (1·5)2·1–4·8(6·1) cm., oblong to elliptic or obovate, obtuse to acute or acuminate at the apex, with margin entire or shallowly crenulate-serrulate and slightly reflexed, cuneate to rounded or rarely shallowly cordate at the base, subcoriaceous, with (6)10–12(14) lateral nerves and densely reticulate venation more prominent below than above, sparsely pubescent towards the base below and on both sides of the midrib;
petiole: 2·5–6 mm. long, with entire margins, brownish-pubescent;
stipules: absent.
Flowers: 2–16 in fasciculate axillary subdichasial or monochasial cymes, functionally dioecious, 5–7 mm. in diam., sweetly scented;
buds: c. 2 mm. long, ovoid to subglobose;
inflorescence branches: densely red-brown-tomentose; 
primary peduncle: absent, secondary peduncles fasciculate; 
pedicels: 2–6 mm. long, articulated at the base or in the lower 1/2;
bracts: 0·5 mm. long, triangular, entire, red-brown, sparsely pubescent, persistent.
Sepals: brown, red-brown-tomentose outside, puberulous or glabrous within, c. 1 mm. long, subequal, ovate to oblong, obtuse or subacute, entire, free.
Petals: yellow or greenish-yellow to brownish, 1·5–2 mm. long, ovate to oblong, rounded, entire or with margin ciliolate, sometimes longitudinally ribbed, sparsely pubescent on both surfaces, free. 
Disk: green, thick, convex, 5-angled, sometimes ± fluted, glabrous or puberulous.
Stamens: 3;
in male flowers with filaments slender, equalling the style, and anthers orange, large, fertile, glabrous or ± sparsely pubescent, dehiscing by 2 oblique clefts confluent at the apex;
in female flowers with filaments usually shorter than the anthers and anthers small, sterile, otherwise as in male flowers.
Ovary: conic, glabrous or sparsely pubescent, immersed in the disk, with style narrow, elongated in both forms of flower;
stigma: slightly 3-lobed;
ovules: 2 per loculus.
Fruit: red to red-brown, sometimes glaucous, c. 1·5–2·3 × 1·5–2·7 cm., globose or dorsiventrally somewhat flattened, rugulose, 2–4 seeded.
Seeds: cylindric.
"""

#eflorasDB = r'E:\WTA\FWTA\efloras.accdb'
eflorasDB = r"T:\Cameroon\FWTA\efloras.accdb"

if __name__ == "__main__":

    #myds = FloraCorpusReader(db=eflorasDB, query='Taxa', fieldlst=['description', ])
    #testtext = ('\n').join(myds.text())
    testtext = testme

    if (False):
        myglossary = botglossary()
        fnagl = myglossary.glossary()

        btagger = nltk.pos_tag
        notinlist = []
        mysents = myds.sents()
        initialwords = [s.split(' ')[0] for s in mysents]
        wrds = nltk.Text(myds.words)
        btagger = nltk.pos_tag
        tagger = nltk.UnigramTagger(model=myglossary.glossary())
        poss = btagger(mysents[1][0])
        myparser = StanfordParser(path_to_jar=r'C:\stanford-parser\stanford-parser.jar',
                                  path_to_models_jar=r'C:\stanford-parser\stanford-parser-3.4.1-models.jar')
        myparser.tagged_parse(poss)
        print([i + "\n" for i in initials])

    if (False):
        from collections import Counter

        tb = TextBlob(testtext)
        wordlist = Counter((word, posfromglossary(word)) for word in tb.words if posfromglossary(word)[0] == 'UNK')
        with  open(r'notingloss.txt', 'w', encoding='utf-8') as f:
            for w in wordlist.most_common(1000):
                print(w, file=f)

    if (False):
        stokenizer = FlSentenceTokenizer()
        tagger = FlTagger()
        bber = Blobber(sent_tokenizer=stokenizer, pos_tagger=tagger)
        tb = bber(testtext)
        # wordlist = [(word, posfromglossary(word))for word in tb.words]
        sents = tb.sentences
        sp = [sent.pos_tags for sent in sents]

        grammar = r"""
  PP: {<PP><ART>?<JJ>*<NN.?><JJ>*}  # prepositional phrase
  NP: {<ART>?<JJ>*<NN.?><JJ>*}   # chunk determiner/possessive, adjectives and noun
"""
        cp = nltk.RegexpParser(grammar)
        parses = cp.parse_sents(sp)
        for p in parses:
            print(p)

    if (False):
        from floraparser.bits import find_ranges

        find_ranges(testtext)

    if (False):
        tbwc = tb.word_counts
        srtd = sorted(tbwc, key=tbwc.get, reverse=True)
        for w in srtd:
            if not w in fnagl:
                notinlist.append(w)
        with  open(r'notingloss.txt', 'w', encoding='utf-8') as f:
            for w in notinlist:
                print(w, file=f)

    if (False):
        from nltk import grammar, parse

        sent = ' to 1·5–2·3 cm. tall'
        tokens = ['to', '15', '-', '23', 'cm', '.', 'in', 'diam.']
        # tokens = ['to','23','m','tall']
        cp = parse.load_parser('../resources/simplerange.fcfg', trace=2)
        trees = cp.parse(tokens)
        for tree in trees:
            print(tree)

    if (False):
        import linkgrammar as lg

        sents = re.split(r'(?<=\.)\s+(?=[A-Z])|;\s+', testtext)

        p = lg.Parser(lang="en", verbosity=1, max_null_count=10)
        for sent in sents:
            print(sent)
            linkages = p.parse_sent(sent)
            for linkage in linkages[0:1]:
                print(linkage.num_of_links, linkage.constituent_phrases_nested)
                pass
        pass

    if False:
        from floraparser.fltoken import FlTokenizer
        from nltk.stem import WordNetLemmatizer
        from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters, PunktLanguageVars

        fltk = FlTokenizer()
        wnl = WordNetLemmatizer()
        NUMBERS = re.compile(r'^[0-9–—.·()-]+$')
        sent_tokenizer = LazyLoader(r'..\resources\FloraPunkt.pickle')
        PunktLanguageVars.sent_end_chars = ('.',)
        wordset = set()
        with open('../resources/AllTaxa.txt') as at:
            for desc in at:
                sents = sent_tokenizer.tokenize(desc)
                for sent in sents:
                    tl = fltk.tokenize(sent)
                    if tl[-1].endswith('.'):
                        tl[-1] = tl[-1][:-1]

                    wl = [wnl.lemmatize(word.lower()) for word in tl if (not NUMBERS.match(word) and not '.' in word)]
                    wordset.update(wl)
        with open('../resources/AllTaxa.words', 'w', encoding='utf-8') as wf:
            for w in sorted(wordset):
                print(w, file=wf)

    if True:
        with open('../resources/specificnames.txt', 'r', encoding='utf-8') as namesf:
            namesset = {word.rstrip() for word in namesf}
        with open('../resources/KewGlossary.txt', 'r') as kf:
            kewset = {word.rstrip() for word in kf}
        with open('../resources/AllTaxa.words', 'r', encoding='utf-8') as wf:
            wordset = {word.rstrip() for word in wf}

        wordset -= namesset
        hyphwords = {word for word in wordset if '-' in word}
        hyphparts = {word for hyph in hyphwords for word in hyph.split('-')}
        plainwords = wordset - hyphwords
        notkwords = plainwords - kewset
        pass

