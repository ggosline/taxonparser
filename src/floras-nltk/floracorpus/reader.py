from itertools import chain
import pickle
from nltk.data import LazyLoader

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters, PunktWordTokenizer, PunktLanguageVars
# from nltk.util import AbstractLazySequence, LazyMap, LazyConcatenation

from floracorpus.SQLitedb import SQLitedb
from floraparser.fltoken import FlToken, FlTokenizer

# from floracorpus.ADO import ADOdb
#  class AccessDBSequence(AbstractLazySequence):
#
#     def __init__(self, db='test', flora='fz', query="Select * from Taxa;", fieldlst=('taxonNo','family','genus','species','infrarank','infraepi','description')):
#         self.conn = ADOdb(db)
#         self.conn.OpenTable(query, fieldlst)
#
#     def __len__(self):
#         return self.conn.RecordCount()
#
#     def iterate_from(self, start):
#         # f = lambda d: d.get(self.field, '')
#         # return iter(LazyMap(f, self.collection.find(fields=[self.field], skip=start)))
#         self.conn.MoveTo(start)
#         return iter(self.conn.NextRec, None)

class AbstractFloraCorpusReader(object):

    def __init__(self, reader=None,
                 word_tokenizer=PunktWordTokenizer(),
                 sent_tokenizer=LazyLoader(r'..\resources\FloraPunkt.pickle')):

        self._reader = reader   # file reader
        self._word_tokenize = FlTokenizer().word_tokenize
        #punkt_param = PunktParameters()
        # punkt_param.abbrev_types = set(['cm', 'mm', 'km', 'c', 'diam', 'fig'])
        # self._sent_tokenize = PunktSentenceTokenizer(punkt_param).tokenize
        self._sent_tokenize = sent_tokenizer.tokenize
        PunktLanguageVars.sent_end_chars = ('.',)  # don't break on question marks !
        self._taxa = [(f['taxonNo'], f['description']) for f in self._reader]
        self._words = None
        self._sents = None
        self._tokens = None

    def taxa(self, taxonids=None):
        """
        :return: the given file(s) as a single string.
        :rtype: str
        """
        return self._taxa

    def words(self, taxonids=None):
        """
        :return: the given taxa as a list of
            taxonNos + each encoded as a list of sentences, which are
            in turn encoded as lists of word strings.
        :rtype: list(int, list(list(list(str)))
        """
        if self._word_tokenize is None:
            raise ValueError('No sentence tokenizer for this corpus')
        if not self._words:
            self._words = [(tid, [self._word_tokenize(sentence) for sentence in sentences]) for tid, sentences in
                           self.sents()]
            # remove the final full-stop which Punkt leaves with the last word.
            for _, sentences in self._words:
                for words in sentences:
                    if words[-1].endswith('.'):
                        words[-1] = words[-1][:-1]  # trim the full-stop
        return self._words

    def sents(self, taxonids=None):
        """
        :return: the given file(s) as a list of
            sentences or utterances, each encoded as a list of word
            strings.
        :rtype: list(list(str))
        """
        if self._sent_tokenize is None:
            raise ValueError('No sentence tokenizer for this corpus')
        if not self._sents:
            self._sents = [(tid, self._sent_tokenize(desc)) for tid, desc in self._taxa if desc]
        return self._sents

    def tokens(self, taxonids=None):
        """
        :return: the given taxa as a list of
            taxonNos + each encoded as a list of sentences, which are
            in turn encoded as lists of tokens.
        :rtype: list(int, list(list(list(FlToken)))
        """
        return [(tid, [[FlToken(word, tid) for word in wlist] for wlist in slist]) for tid, slist in self.words()]


class FloraCorpusReader(AbstractFloraCorpusReader):

    def __init__(self, db='', query='', fieldlst='', **kwargs):
        # self._seq = list(AccessDBSequence(**kwargs))
        self.dbr = SQLitedb(db)
        self.rdr = self.dbr.OpenTable(query, fieldlst)
        super().__init__(reader=self.rdr, **kwargs)
        # self._sents = list(chain.from_iterable(list(map(self._sent_tokenize, self.text()))))



# class LazyFloraCorpusReader(AbstractFloraCorpusReader):
#
#   def __init__(self, **kwargs):
#     self._seq = AccessDBSequence(**kwargs)
#     super().__init__(self, **kwargs)
#
#   def text(self):
#     return self._seq
#   def words(self):
#     return LazyConcatenation(LazyMap(self._word_tokenize, self.text()))
#   def sents(self):
#     return LazyConcatenation(LazyMap(self._sent_tokenize, self.text()))

if __name__ == "__main__":

    myds = FloraCorpusReader(db=r'..\resources\efloras.db3', query="Select * from Taxa where family = 'Celastraceae';", fieldlst=('taxonNo', 'description', ))
    # myds.OpenTable("SELECT APD.* FROM [APD] WHERE (((APD.[family])='agavaceae'));")
    mytext = myds.taxa()
    mysents = myds.sents()
    mywords = myds.words()
    mytokens = myds.tokens()

    s = mysents[5][1][0]
    w = myds._word_tokenize(s)
    del myds

