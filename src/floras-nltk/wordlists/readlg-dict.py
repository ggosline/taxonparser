import os
import re
import pickle

from floracorpus.reader import FloraCorpusReader
#eflorasDB = r'E:\WTA\FWTA\efloras.accdb'
eflorasDB = r"T:\Cameroon\FWTA\efloras.accdb"


lgwordset = set()
florawordset = set()
missingwords = set()

def lgvocab():
    #
    # read the lg dictionary files and pull the words
    #

    dictdir = '.\\resources\\lg-floras\\en\\words\\'

    files = os.listdir(dictdir)
    wf = [dictdir + file for file in files if file.startswith('word')]

    mylines = []
    word = ''

    for file in wf:
        with open(file) as f:
            mylines = mylines + f.readlines()
            word = ''
            mywords = [word.rsplit('.', 1)[0] for word in mylines if mylines[0:1] not in ['\n', '%']]
            lgwordset.update(mywords)
            f.close

    with open(".\\resources\\lg-floras\\en\\4.0.dict",'r',encoding='utf-8') as dictfile:
        dictwords = set()
        dictlines = [line.strip() for line in dictfile.readlines() if len(line.strip()) > 0 and line.strip()[0] != '%']
        dicttext = ' '.join(dictlines)
        dictentries = dicttext.split(';')
        for e in dictentries:
            wlist = e.rsplit(':',1)[0]
            words = wlist.split()
            dwords = [word.rsplit('.', 1)[0] for word in words if word[0] != '<']
            dictwords.update(dwords)
        lgwordset.update(dictwords)

    pickle.dump(lgwordset, open('lgwordset.pickle', 'wb'))

#lgvocab()


#lgwordset = pickle.load(open('lgwordset.pickle','rb'))

famlist = open('FZfamlist.txt','r').read().splitlines()

numpat = '[-–0-9·.]+'
dashpat = '[-–]'

# florawordset = pickle.load(open('florawordset.pickle','rb'))

florawordset = set()
taxawords = []
hyphenated_words = set()
# wscopy = florawordset.copy()

for fname in famlist:

    print(faname)
    myds = FloraCorpusReader(db=eflorasDB, query="Select description from Taxa where family = '{}';".format(fname),
                        fieldlst=['description', ])
    taxawords = myds.words()

    for word in taxawords:
        if '.' in word:      # run on sentence
            hyparts = word.split('.')
            florawordset.update([word.lower() for word in hyparts if not re.match(numpat,word)])
        else:
            florawordset.update(word)
            # florawordset.remove(word)
        # if re.search(dashpat,word):     # hyphenated
        #     hyparts = re.split(dashpat,word)
        #     taxawords = [w + '-' for w in hyparts[:-1]] + [('-' + hyparts[-1])]
        #     florawordset.update([word.lower() for word in taxawords if not re.match(numpat,word)])
        #     florawordset.discard(word)
        #     hyphenated_words.add(word)
        #     pass

pickle.dump(florawordset, open('florawordset.pickle', 'wb'))
# pickle.dump(hyphenated_words, open('hyphenated_words.pickle', 'wb'))

f=open('florawordset.txt','wt',encoding='utf-8')

mw = list(florawordset)
mw.sort()
for w in mw:
    print(w,file=f)

f.close

# f=open('hyphenated_words.txt','wt',encoding='utf-8')
#
# mw = list(hyphenated_words)
# mw.sort()
# for w in mw:
#     print(w,file=f)
#
# f.close


# missingwords = florawordset - lgwordset
#
# f=open('missingvocab.txt','wt',encoding='utf-8')
#
# mw = list(missingwords)
# mw.sort()
# for w in mw:
#     print(w,file=f)
#
# f.close

pass