#! /usr/bin/env python
# -*- coding: utf8 -*-
#
# Link Grammar example usage 
#
# May need to set the PYTHONPATH to get this to work:
# PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/dist-packages/link_grammar
# or something similar ...
#
from linkgrammar import Parser, Linkage, ParseOptions, Link


# English is the default language
p = Parser(lang='en', islands_ok=True)
linkages = p.parse_sent("This is a test.")
print ("English: found ", len(linkages), "linkages")
for linkage in linkages :
    print (linkage.diagram)
    print (linkage.constituent_phrases_nested)

# Russian
try:
    p = Parser(lang = 'ru')
    linkages = p.parse_sent("это большой тест.")
    print ("Russian: found ", len(linkages), "linkages")
    for linkage in linkages :
        print (linkage.diagram)
except:
    pass 
# Turkish
try:
    p = Parser(lang = 'tr')
    linkages = p.parse_sent("çok şişman adam geldi")
    print ("Turkish: found ", len(linkages), "linkages")
    for linkage in linkages :
        print (linkage.diagram)
except:
    pass

