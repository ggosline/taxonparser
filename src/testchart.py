from nltk.app.chartparser_app import CFG, ChartParserApp


def test():
    grammar = CFG.fromstring("""
    # Grammatical productions.
        S -> NP VP
        VP -> VP PP | V NP | V
        NN -> Det Adjcl N | Det N
        NP -> NN | NP PP
        NP ->
        PP -> P NP
        Adjs -> Adj | Adj Adjs
        NNL -> NN CC NN
        Adjl -> Adjs CC Adjs | Adjs comma CC Adjs | Adjs
        Adjcl -> Adj comma Adjl | Adj comma Adjcl | Adjl

    # Lexical productions.
        NP -> 'John' | 'I'
        Det -> 'the' | 'my' | 'a'
        N -> 'dog' | 'cookie' | 'table' | 'cake' | 'fork'
        V -> 'ate' | 'saw'
        P -> 'on' | 'under' | 'with'
        Adj -> 'large' | 'brown' | 'bad'
        CC -> 'or' | 'and'
        comma -> ','
    """)

    sent = 'John ate the cake on the table with a fork'
    sent = 'John ate the cake on the table'
    sent = 'the large brown dog ate the cake'
    tokens = list(sent.split())

    print('grammar= (')
    for rule in grammar.productions():
        print(('    ', repr(rule) + ','))
    print(')')
    print(('tokens = %r' % tokens))
    print('Calling "ChartParserApp(grammar, tokens)"...')
    ChartParserApp(grammar, tokens).mainloop()


if __name__ == '__main__':
    test()