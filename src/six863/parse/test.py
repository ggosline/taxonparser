from parse.featurechart import load_earley
from parse.treeview import TreeView

def demo():
    cp = load_earley('gazdar6.cfg', trace=1)
    trees = cp.parse('the man that Fido chased returned')
    for tree in trees:
        print(tree)

# run_profile()
if __name__ == '__main__': demo()
