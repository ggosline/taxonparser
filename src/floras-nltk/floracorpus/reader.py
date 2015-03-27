from itertools import chain
import pickle
from nltk.data import LazyLoader

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters, PunktLanguageVars
# from nltk.util import AbstractLazySequence, LazyMap, LazyConcatenation

from floracorpus.SQLitedb import SQLitedb
from floraparser.fltoken import FlToken, FlTokenizer, FlTaxon, FlPhrase


class AbstractFloraCorpusReader(object):
    def __init__(self, reader=None,
                 sent_tokenizer=LazyLoader(r'..\resources\FloraPunkt.pickle')):
        self._reader = reader  # file reader
        self._word_tokenize = FlTokenizer().span_tokenize
        # punkt_param = PunktParameters()
        # punkt_param.abbrev_types = set(['cm', 'mm', 'km', 'c', 'diam', 'fig'])
        # self._sent_tokenize = PunktSentenceTokenizer(punkt_param).tokenize
        self._sent_tokenize = sent_tokenizer.span_tokenize
        PunktLanguageVars.sent_end_chars = ('.',)  # don't break on question marks !
        self._taxa = [FlTaxon(f, sentence_tokenizer=self._sent_tokenize) for f in self._reader]

    @property
    def taxa(self, taxonids=None):
        """
        :return: the given file(s) as a single string.
        :rtype: str
        """

        return self._taxa

        # def words(self, taxonids=None):
        # """
        # :return: the given taxa as a list of
        # taxonNos + each encoded as a list of sentences, which are
        #         in turn encoded as lists of word strings.
        #     :rtype: list(int, list(list(list(str)))
        #     """
        #     if self._word_tokenize is None:
        #         raise ValueError('No sentence tokenizer for this corpus')
        #     if not self._words:
        #         self._words = [(tid, [self._word_tokenize(sentence) for sentence in sentences]) for tid, sentences in
        #                        self.sents()]
        #         # remove the final full-stop which Punkt leaves with the last word.
        #         for _, sentences in self._words:
        #             for words in sentences:
        #                 if words[-1][0].endswith('.'):
        #                     words[-1] = (words[-1][0][:-1], words[-1][1], words[-1][2]-1)   # trim the full-stop
        #     return self._words
        #
        # def sents(self, taxonids=None):
        #     """
        #     :return: the given file(s) as a list of
        #         sentences or utterances, each encoded as a list of word
        #         strings.
        #     :rtype: list(list(str))
        #     """
        #     if self._sent_tokenize is None:
        #         raise ValueError('No sentence tokenizer for this corpus')
        #     if not self._sents:
        #         self._sents = [(tid, self._sent_tokenize(desc)) for tid, desc in self._taxa if desc]
        #     return self._sents
        #
        # def tokens(self, taxonids=None):
        #     """
        #     :return: the given taxa as a list of
        #         taxonNos + each encoded as a list of sentences, which are
        #         in turn encoded as lists of tokens.
        #     :rtype: list(int, list(list(list(FlToken)))
        #     """
        #     return [(tid, [[FlToken(word, tid) for word in wlist] for wlist in slist]) for tid, slist in self.words()]


class FloraCorpusReader(AbstractFloraCorpusReader):
    def __init__(self, db=r'..\resources\efloras.db3', query='Select * from Taxa;', fieldlst=None, **kwargs):
        # self._seq = list(AccessDBSequence(**kwargs))
        if not fieldlst:
            fieldlst = ['taxonNo', 'flora_name', 'rank', 'family', 'genus', 'species', 'infrarank', 'infraepi',
                        'description', ]
        self.dbr = SQLitedb(db)
        self.rdr = self.dbr.OpenTable(query, fieldlst)
        super().__init__(reader=self.rdr, **kwargs)


if __name__ == "__main__":

    myds = FloraCorpusReader(db=r'..\resources\efloras.db3',
                             query="Select * from Taxa where family = 'Celastraceae';", )
    # myds.OpenTable("SELECT APD.* FROM [APD] WHERE (((APD.[family])='agavaceae'));")
    taxa = myds.taxa
    # for t in taxa:
    # for s in t.sentences:
    # if len(s.phrases) > 1:
    # print(s.phrases)

    pass

    notindict = set()
    for t in taxa:
        for sent in t.sentences:
            for phrase in sent.phrases:
                for token in phrase:
                    if token.POS == 'UNK':
                        print(phrase)
                        notindict.add(token.text)
    with open('notindict.txt', 'w', encoding='utf-8') as nidf:
        for wd in sorted(notindict):
            nidf.write(wd + '\n')

    del myds

