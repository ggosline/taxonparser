# coding=Latin1

import string

from Snobol import *

class txMatcher: 
    
    ucase = string.ascii_uppercase[0:26]
    lcase = string.ascii_lowercase[0:26] + "-àáâãäåçèéêëìíîïñòóôõöøùúûüýÿ"
    ws = ARBNO(" ")

    gPat = (ANY(ucase) + SPAN(lcase) + " ")
    snmPat = SPAN(lcase) + " " | "sp. "

    aunmComp = ANY(ucase) + SPAN(lcase + "-.'") | "van" | "der" | "de"
    aunmPat = (aunmComp + ARBNO(ws + aunmComp) + (LIT(
        "f.") | "fa." | "")) | "DC." | "Figueiredo, Estrella" | "A. DC." | "C. DC." | "al." | "A.DC." | "C.DC."
    authAndPat = (aunmPat + " & " + aunmPat) | (aunmPat + ", " + aunmPat + " & " + aunmPat) | aunmPat
    authExPat = authAndPat + (LIT(" ex ") | " ex. ") + authAndPat | authAndPat
    authCPat = (("(" + authExPat + ") ") . par + authExPat . author + " ") | authExPat . author + " "
    OptAuth = authCPat | LIT("auct. ") . author | ""

    txPat = POS(0) + gPat . genus + snmPat . species + OptAuth + (LIT("subsp. ") . infrarank + snmPat . infraepi + OptAuth | "") + RPOS(0) | \
            POS(0) + gPat.genus + snmPat.species + OptAuth + (
            LIT("subsp. ").infrarank + snmPat.infraepi + OptAuth) + (
            LIT("var. ").infrarank2 + snmPat.infraepi2 + OptAuth | "") + RPOS(0) | \
            POS(0) + gPat . genus + snmPat . species + OptAuth + (LIT("var. ") . infrarank + snmPat . infraepi + OptAuth | "") + RPOS(0) | \
            POS(0) + gPat.genus + snmPat.species + OptAuth + (
            (LIT("f. ") | "fa. ").infrarank + snmPat.infraepi + OptAuth | "") + RPOS(0) | \
            POS(0) + gPat . genus + authCPat + RPOS(0)

    

    def txMatch(txName):
        m = Matcher()
        return m.match(txName + " ", txMatcher.txPat), m.__dict__

if __name__ == "__main__":
    testname = "Salacia dimidia N. Hallé subsp. dimidia var. dimidia"
    print(txMatcher.txMatch(testname))




