from parse.featurechart import load_earley
from parse.treeview import TreeView

def demo():
    cp = load_earley('gazdar6.cfg', trace=0)
    cp.batch_test('all-gazdar-sentences.txt')

# run_profile()
if __name__ == '__main__': demo()
