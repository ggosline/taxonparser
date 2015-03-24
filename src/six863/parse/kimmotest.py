from kimmo.kimmo import KimmoRuleSet, TextTrace

k = KimmoRuleSet.load('../parse/gazdar.kimmo.yaml')
print(list(k.generate('`slip+ed', TextTrace(3))))
print(list(k.recognize('chased', TextTrace(1))))
