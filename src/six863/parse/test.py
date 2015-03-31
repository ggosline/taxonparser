from parse.featurechart import load_earley
from parse.treeview import TreeView
import os

def demo():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    cp = load_earley('gazdar6.cfg', trace=1)
    trees = cp.parse('the man chased Fido and the dog')
    for tree in trees:
        print(tree)

# run_profile()
if __name__ == '__main__': demo()
