# coding=Latin1

import string

from Snobol import *


class txMatcher: 
    
    ucase = string.ascii_uppercase[0:26]
    lcase = string.ascii_lowercase[0:26] + "-àáâãäåçèéêëìíîïñòóôõöøùúûüýÿ"
    ws = ARBNO(" ")

    gPat = (ANY(ucase) + SPAN(lcase) + " ")
    snmPat = SPAN(lcase) + " "

    aunmComp = ANY(ucase) + SPAN(lcase + "-.'") | "van" | "der" | "de"
    aunmPat = (aunmComp + ARBNO(ws + aunmComp) + (LIT(" f.") | "")) | "DC." | "Figueiredo, Estrella" | "A. DC." | "C. DC." | "al." 
    authAndPat = (aunmPat + " & " + aunmPat) | (aunmPat + ", " + aunmPat + " & " + aunmPat) | aunmPat
    authExPat = authAndPat + " ex " + authAndPat | authAndPat
    authCPat = (("(" + authExPat + ") ") . par + authExPat . author + " ") | authExPat . author + " "
    OptAuth = authCPat | LIT("auct. ") . author | ""

    txPat = POS(0) + gPat . genus + snmPat . species + OptAuth + (LIT("subsp. ") . infrarank + snmPat . infraepi + OptAuth | "") + RPOS(0) | \
            POS(0) + gPat . genus + snmPat . species + OptAuth + (LIT("var. ") . infrarank + snmPat . infraepi + OptAuth | "") + RPOS(0) | \
            POS(0) + gPat . genus + snmPat . species + OptAuth + (LIT("f. ") . infrarank + snmPat . infraepi + OptAuth | "") + RPOS(0) | \
            POS(0) + gPat . genus + authCPat + RPOS(0)

    

    def txMatch(txName):
        m = Matcher()
        return m.match(txName + " ", txMatcher.txPat), m.__dict__

if __name__ == "__main__":
    testname = "Salacia dimidia N. Hallé"
    print(txMatcher.txMatch(testname))




