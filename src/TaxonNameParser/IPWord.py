from itertools import izip_longest
import pickle
import re
import sys

import Microsoft.Office.Interop.Word as Word
import System
from System.Runtime.InteropServices import Marshal
import clr
import ucsv


clr.AddReference("Microsoft.Office.Interop.Word")

if False:
     word = Word.ApplicationClass
word = Marshal.GetActiveObject("Word.Application")
word.Visible = True

# doc = Word.Document()
doc = word.ActiveDocument

def processKey(keyrange):

    # p = Word.Paragraph()
    kllist = []
    cstack = [0]  # for the very last couplet
    coupletcount = 1
    coupletline = 1
    currcouplet = 1

    for i  in range(2 , keyrange.Paragraphs.Count):

        p = keyrange.Paragraphs(i)
        kl = keyline(p.Range, currcouplet, coupletline)

        if p.Range.Text[-2:-1] == ":" :
            if coupletline == 1: 
                cstack.append (currcouplet)
            coupletline = 1
            coupletcount += 1
            currcouplet = coupletcount
            kl.goto = currcouplet

        elif coupletline == 1 :
            coupletline = 2
        elif coupletline == 2 :
            currcouplet = cstack.pop()
            coupletline = 2

        kllist.append (kl)
    
    for kl in kllist:
        kl.range.InsertBefore(str(kl.coupletno) + "." + str(kl.coupletline) + " | ")
        if kl.goto != 0:
            trng = kl.range
            trng.MoveEnd(Word.WdUnits.wdCharacter, -1)
            trng.InsertAfter("\t" + str(kl.goto))
    pass

def processKeylead(keyrange):
    if False:
        rng = doc.Range(1, 1)
    for i  in range(2 , keyrange.Paragraphs.Count):
        rng = keyrange.Paragraphs(i).Range
        rng.Collapse (Word.WdCollapseDirection.wdCollapseStart)
        rng.MoveEndUntil("\t")
        rng.Collapse(Word.WdCollapseDirection.wdCollapseEnd)
        rng.MoveEnd(Word.WdUnits.wdCharacter, 1)
        rng.Select()
        try:
            word.Selection.ClearCharacterStyle()  # This fails is there is no characterstyle!
        except:
            pass
    pass

def processKeytail(keyrange):

    rng = keyrange.Duplicate 
    
    fnd = rng.Find
    fnd.ClearFormatting
    fnd.Wrap = Word.WdFindWrap.wdFindStop
    fnd.MatchWildcards = True
    # fnd.Text = r"^t[0-9]{1,3}^13"                 # keygoto
    fnd.Text = r"^t[0-9]{1,3}.^s[A-Z]*^13"  # keyends
    while fnd.Execute():  
        rng.MoveStart(Word.WdUnits.wdCharacter, 1)
        rng.MoveEnd(Word.WdUnits.wdCharacter, -1)
        rng.Select()
        rng.Style = "keyends"
        rng.Collapse(Word.WdCollapseDirection.wdCollapseEnd)
        rng.End = keyrange.End
    pass
    
def processKeyText(sectionNo):
    if False:
        p = Word.Paragraph()
    keyrange = doc.Sections(sectionNo).Range
    clist = []
    for i  in range(2 , keyrange.Paragraphs.Count):

        p1 = keyrange.Paragraphs(i)
        p2 = keyrange.Paragraphs(i + 1)
        if p1.Style.NameLocal == "keylead1":
            if p2.Style.NameLocal == "keylead2":
                c1 = p1.Range.Text.split("\t")
                c2 = p2.Range.Text.split("\t")
                print (sectionNo, c1[0])
                try:
                    clist.append((str(sectionNo), c1[0], c1[1], c2[1], c1[2], c2[2]))
                except:
                    pass
    return clist


def processKeys(sectionlist):
    kllist = []
    charlist = []
    if False:
        rng = doc.Range()
    for sectionNo in sectionlist:
        # rng = doc.Sections(sectionNo).Range
        kllist.extend(processKeyText(sectionNo))
    for sectionno, coupletno, tl1, tl2, el1, el2 in kllist:
        chars = izip_longest([t1.strip(" :").lower() for t1 in tl1.split(";")], [t2.strip(" :").lower() for t2 in tl2.split(";")], fillvalue="")
        charlist.extend([(sectionno, coupletno, t1, el1.strip(), t2, el2.strip()) for t1, t2 in chars])

    return charlist

    

def analyzechars(charlist):
    cheads = set()
    for section, coupletno, cp1, el1, cp2, el2 in charlist:
        chead = []
        wl1 = cp1.split()
        wl2 = cp2.split()
        for word1, word2 in zip(wl1, wl2):
            if word1 == word2:
                chead.append(word1)
            else:
                break
        cheads.add(" ".join(chead))
    return cheads

class keyline:
    def __init__(self, rng, coupletno, coupletline):
        self.range = rng
        self.coupletno = coupletno
        self.coupletline = coupletline
        self.goto = 0


if __name__ == "__main__":
    # charlist = []

    if True: 
        charlist = processKeys(range(2, 3))

    # with open(r'T:\Cameroon\FWTA\FWTA-in process\characters.pkl', 'wb') as f:
    #    pickle.dump(charlist,f)

    with open(r'T:\Cameroon\FWTA\FWTA-in process\characters.pkl', 'rb') as f:
        charlist = pickle.load(f)

    cheads = analyzechars (charlist)
    with open(r'T:\Cameroon\FWTA\FWTA-in process\characterkeys.txt', 'wb') as f:
        f.writelines([chead + "\n" for chead in sorted(cheads)])

    # with open(r'T:\Cameroon\FWTA\FWTA-in process\characters.csv', 'wb') as f:
    #    writer = ucsv.UnicodeWriter(f)
    #    writer.writerows(charlist)
    # with open(r'T:\Cameroon\FWTA\FWTA-in process\characters.csv', 'rb') as f:
    #    charlist = ucsv.UnicodeReader(f)
    #    cheads = analyzechars (charlist)
    
    pass
