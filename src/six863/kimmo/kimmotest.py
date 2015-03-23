from six863.kimmo.kimmo import *

k = KimmoRuleSet.load('../parse/gazdar.kimmo.yaml')
print(list(k.generate('`slip+ed', TextTrace(3))))
print(list(k.recognize('chased', TextTrace(1))))
