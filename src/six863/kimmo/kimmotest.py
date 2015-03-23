from .kimmo import *

k = KimmoRuleSet.load('gazdar.kimmo.yaml.yaml')
print(list(k.generate('`slip+ed', TextTrace(3))))
print(list(k.recognize('chased', TextTrace(1))))
