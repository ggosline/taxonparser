
import string

from Snobol import *
from recordtype import recordtype


taxonRec = recordtype("taxonRec", "txid status rank genus species infrarank infraepi author par litref type", default="")

class paraDescMatcher: 
    
    ucase = string.ascii_uppercase
    lcase = string.ascii_lowercase + "-אבגדהוחטיךכלםמןסעףפץצרשתûü‎ÿ"
    
    ws = SPAN(string.whitespace)

    numidP = SPAN(string.digits) + "."
    alphaidP = ANY(string.ascii_lowercase) + "."

    genameP = (ANY(ucase) + (SPAN(lcase) | ".")) 
    snameP = SPAN(lcase)

    spnameP = "<b>" + genameP . genus + ws + snameP . species + "</b>" 
    txauthP = ARBNO("(<i>" + ARB . par + "</i>)" + ws) + "<i>" + ARB . author + "</i>"

    litrefP = (("in " + ARB).litref + ("Type: " + REM).type) | ("in " + REM).litref | ", " + (ARB . litref) + ("Type: " + REM).type | ", " + REM . litref

    speciesP = POS(0) + ARBNO(numidP) . txid + ws + spnameP + ws + txauthP + ws + litrefP 

    genusP = POS(0) + ARBNO(numidP).txid + ws + "<b>" + genameP . genus + "</b>" + ws + txauthP + ws + litrefP

    infrataxonnameP = POS(0) + ARBNO(alphaidP).txid + ws + (LIT("subsp.") | LIT("var.")) . infrarank + ws + "<b>" + snameP . infraepi + "</b>" 

    infrataxonP = infrataxonnameP + ws + txauthP + ws + litrefP | \
                    infrataxonnameP

    alltaxaP = speciesP | genusP | infrataxonP

    synspnameP = "<i>" + genameP . genus + ws + snameP . species + "</i>"
    syninfrataxonnameP = "<i>" + genameP . genus + ws + snameP . species + "</i>" + (LIT("subsp.") | LIT("var.")) . infrarank + ws + "<i>" + snameP . infraepi + "</i>"

    syntaxonnameP = syninfrataxonnameP | synspnameP  
    syntxauthP = ARBNO("(" + ARB . par + ")" + ws) + ARB . author

    synP = ARBNO("<sk>SYN.</sk>") + "\t" + syntaxonnameP + ws + syntxauthP . author + litrefP
    
    def paraParse(nm, status):
        if status == "A":
            tp = paraDescMatcher.paraMatch(nm)
        elif status == "S":
            tp = paraDescMatcher.synMatch(nm)

        if tp[0] == None:
            return None
        else:
            rec = taxonRec(**tp[1])
            # taxID = ("_").join([rec.genus, rec.species, rec.infrarank, rec.infraepi]).replace(" ","").replace(".","").rstrip("_")
    
            rec.rank = "species"
            if (rec.genus != "" and rec.species == ""):            
                rec.rank = "genus"
            if rec.infrarank == "subsp.":
                rec.rank = "subspecies"
            elif rec.infrarank == "var.":
                rec.rank = "variety"
            elif rec.infrarank == "f.":
                rec.rank = "forma"
        return rec
    
    def paraMatch(txName):
        m = Matcher()
        m.status = "A"
        return m.match(txName, paraDescMatcher.alltaxaP), m.__dict__

    def synMatch(txName):
        m = Matcher()
        m.status = "S"
        return m.match(txName, paraDescMatcher.synP), m.__dict__

if __name__ == "__main__":
    # testname = ("1. <b>Cryptolepis africana</b> (<i>Bullock</i>) <i>Venter & R.L. Verh.</i> in S. Afr. Journ. Bot. 73: 42 (2007)."
    #            "Type: Kenya, Kwale District: Buda Mafisini Forest, 13 km WSW of Gazi, <i>Drummond & Hemsley</i> 3836 (K!, holo. (2 sheets and spirit collection); EA, iso.)\r")

    # print(paraDescMatcher.paraParse(testname))

    testsyn = "\t<i>C. buxifolia</i> Chiov., Racc. Bot. Miss. Consol. Kenya: 80 (1935). Type: Kenya, Mt Kenya NE, Meru, <i>Balbo</i> 16 (FT!, lecto., designated here; FT!, iso.)\r"
    print(paraDescMatcher.paraParse(testsyn, "S"))

