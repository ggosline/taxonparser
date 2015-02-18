# coding=Latin1

import string

from Snobol import *
from recordtype import recordtype


DistRec = recordtype("DistRec", "country, district locref", default=None)
DescRec = recordtype("DescRec", "locations distribution extendeddist habitat altitude notes", default=None)
CountRec = recordtype("CountRec", "country")

class paraDescMatcher: 
    
    '''
       General character patterns 
    '''
    ucase = string.ascii_uppercase
    lcase = string.ascii_lowercase + "-àáâãäåçèéêëìíîïñòóôõöøùúûüýÿ"
    word = SPAN(string.ascii_letters)
    
    ws = SPAN(string.whitespace)

    numidP = SPAN(string.digits) + "."
    alphaidP = ANY(string.ascii_lowercase) + "."
    numrange = SPAN(string.digits + "-, ?") + BREAK(";")

    '''
       Name patterns 
    '''
    countryP = LIT(" <sk>") + (LIT("Uganda") | "Kenya" | "Tanzania" | "Tanganyika" | "Zanzibar") . country + ".</sk>" 
    districtP = (ARB + (LIT(" Districts:") | " District:")) . district + " " + BREAK(";\r") . locref + (LIT("; ") | "\r")

    distP = POS(0) + (countryP) + ws + REM . diststr  

    habitatP = POS(0) + LIT(" <sk>Hab.</sk>") + ws + BREAK(";") . habitat + "; " + ARB . altitude + "\r" 
    usesP = POS(0) + LIT("< sk>Uses.</sk>") + ws + ARB . uses + "\r" 
    notesP = POS(0) + LIT(" <sk>") + (LIT("Notes.") | "Note.") + "</sk>" + ws + ARB . notes + "\r"

    # regionP = "<b>" + (LIT("U") | "K" | "T" | "Z") . cinit  + "</b> " + numrange . nlist + "; "
    regionP = "<b>" + (LIT("U") | "K" | "T" | "Z") + "</b> " + numrange + "; "  
    distrP = POS(0) + LIT(" <sk>Distr.</sk> ") + ALLOF(regionP) . distribution + REM . extendeddist 
    countryP = word . country + (LIT(", ") | "\r") ^ ("['country', country]")
    

    distributionP = habitatP | usesP | notesP | distrP | distP

    def distMatch(disttext):
        cm = Matcher()
        c = cm.match(disttext, paraDescMatcher.distributionP)
        if not c:
            return None

        if hasattr(cm, "country"):  # District lists within countries
            country = cm.country
            dm = Matcher()
            dists = dm.findall(cm.diststr, paraDescMatcher.districtP)
            distlist = []
            for (__, __, d) in dists:
                rp = DistRec(**d)
                rp.country = country
                distlist.append(rp)
            return distlist

        elif hasattr(cm, "distribution"):  # Distr: Flora areas and countries
            # return DescRec(**cm.__dict__) 
            countrym = Matcher()
            if hasattr(cm, "extendeddist"):
                countries = countrym.findall(cm.extendeddist, paraDescMatcher.countryP)
                countrylist = []
                for (__, __, c) in countries:
                    rp = CountRec(**c)
                    # rp.country = country
                    countrylist.append(rp)
                return countrylist

        else:
            return DescRec(**cm.__dict__)

if __name__ == "__main__":
    # testname = ("1. <b>Cryptolepis africana</b> (<i>Bullock</i>) <i>Venter & R.L. Verh.</i> in S. Afr. Journ. Bot. 73: 42 (2007)."
    #            "Type: Kenya, Kwale District: Buda Mafisini Forest, 13 km WSW of Gazi, <i>Drummond & Hemsley</i> 3836 (K!, holo. (2 sheets and spirit collection); EA, iso.)\r")

    # print(paraDescMatcher.paraParse(testname))
    testdist = " <sk>Distr.</sk> <b>U</b> 4; <b>K</b> 1?4, 6; <b>T</b> 4, 5, 7; Rwanda, Burundi, Ethiopia, Zambia, Namibia, South Africa\r"
    # testdist =  "<sk>Kenya.</sk> Northern Frontier/Tana River Districts: Garissa, 26 Dec. 1942, <i>Bally</i> 1995; Machakos District: Kibwezi, 15 Sep. 1961, <i>Polhill & Paulo</i> 463!; Tana River District: Tana River National Primate Reserve, Baomo Lodge road, 3 July 1988, <i>Medley</i> 364!\r" 
    # testdist =  "Northern Frontier/Tana River Districts: Garissa, 26 Dec. 1942, <i>Bally</i> 1995; Machakos District: Kibwezi, 15 Sep. 1961, <i>Polhill & Paulo</i> 463!; Tana River District: Tana River National Primate Reserve, Baomo Lodge road, 3 July 1988, <i>Medley</i> 364!\r"
    print(paraDescMatcher.distMatch(testdist))

