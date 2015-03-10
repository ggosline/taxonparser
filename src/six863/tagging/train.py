from nltk import tag
from nltk.tag import sequential
from nltk.corpus import brown
import yaml

t0 = tag.DefaultTagger('nn')
t1 = tag.sequential.UnigramTagger(backoff=t0)
t1.train(brown.tagged('f'))    # section a: press-reportage

f = open('demo_tagger.yaml', 'w')
yaml.dump(t1, f)

