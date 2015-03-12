from nltk import parse, grammar

grammar1 = grammar.FeatureGrammar.fromstring(
    open(r'C:\GitHub\taxonparser\src\six863\semantics\gazdar4.fcfg').readlines())

pass