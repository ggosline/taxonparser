__author__ = 'gg12kg'

import re
from floraparser import glossaryreader, pos


class FlTokenizer():
    '''
    Taken from Punkttokenizer
    '''

    _re_number_range = r'''(?:\(\d+(?:[.·]\d+)\))?
                            \d+(?:[.·]\d)?
                            (?:[--–]\d+(?:[.·]\d+)?)?
                            (?:\(\d+(?:[.·]\d+)?\))?
                        '''

    _re_word_start = r"[^\(\"\`{\[:;&\#\*@\)}\]\-,]"
    """Excludes some characters from starting word tokens"""

    _re_non_word_chars = r"(?:[?!)\";}\]\*:@\'\({\[])"
    """Characters that cannot appear within words"""

    _re_multi_char_punct = r"(?:\-{2,}|\.{2,}|(?:\.\s){2,}\.)"
    """Hyphen and ellipsis are multi-character punctuation"""

    _word_tokenize_fmt = r'''(
        %(MultiChar)s
        |
        %(NumberRange)s
        |
        (?=%(WordStart)s)\S+?  # Accept word characters until end is found
        (?= # Sequences marking a word's end
            \s|                                 # White-space
            $|                                  # End-of-string
            %(NonWord)s|%(MultiChar)s|          # Punctuation
            ,(?=$|\s|%(NonWord)s|%(MultiChar)s) # Comma if at end of word
        )
        |
        \S
    )'''
    """Format of a regular expression to split punctuation from words,
    excluding period."""

    def _word_tokenizer_re(self):
        """Compiles and returns a regular expression for word tokenization"""
        try:
            return self._re_word_tokenizer
        except AttributeError:
            self._re_word_tokenizer = re.compile(
                self._word_tokenize_fmt %
                {
                    'NonWord': self._re_non_word_chars,
                    'MultiChar': self._re_multi_char_punct,
                    'WordStart': self._re_word_start,
                    'NumberRange': self._re_number_range,
                },
                re.UNICODE | re.VERBOSE
            )
            return self._re_word_tokenizer

    def word_tokenize(self, s):
        """Tokenize a string to split off punctuation other than periods"""
        return self._word_tokenizer_re().findall(s)

class FlToken():

    mybotg = glossaryreader.botglossary()
    fltagger = pos.FlTagger()

    def __init__(self, text : str, taxonno : int , fromc : int = 0, toc : int = 0):
        self._text = text
        self.floraDb = None
        self.taxonNo = taxonno
        self.flDictEntry = None
        self.flPOS = None
        self.fromc = fromc
        self.toc = toc
        self.flRoot, self.flPOS, self.flDictEntry = FlToken.fltagger.tag_word(text)

    def __str__(self):
        return self._text + '<' + self.flPOS + '>'

if __name__ == '__main__':
    tryme = FlTokenizer().word_tokenize('c. (0.5)1·5-2·3(4) × 1·5-2·7 cm.')

    # tryme = FlToken('glabrous',1,4)
    pass

