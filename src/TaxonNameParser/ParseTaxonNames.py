from ADO import  ADOdb
from TaxonNameParser import txMatcher
import win32ui
from recordtype import recordtype

taxonName = recordtype("taxonName", "genus species author infrarank infraepi infrarank2 infraepi2 par", default="")

def txParseName(nm):
    tp = txMatcher.txMatch(nm)
    if tp[0] == None:
        taxID = nm
        rank = "NP"
        rec = taxonName()
        print (taxID)
    else:
        rec = taxonName(**tp[1])
        taxID = ("_").join([rec.genus, rec.species, rec.infrarank, rec.infraepi]).replace(" ", "").replace(".", "").rstrip("_")
    
        rank = "species"
        if (rec.species == ""):            
            rank = "genus"
        if rec.infrarank == "subsp. ":
            rank = "subspecies"
        elif rec.infrarank == "var. " or rec.infrarank2 == "var. ":
            rank = "variety"
        elif rec.infrarank2 == "f.":
            rank = "forma"
    return ([taxID, rank, rec])

def ParseFamily(famname):

    OutArray = []
    txnames = e.getRange(famname, 1, 2, 10000, 5)
    for row in txnames:
        if row[0] == None:
            break
        txp = txParseName(row[0])
        if row[2] != None:
            txsym = txParseName(row[2])
        else:
            txsym = [""]
        OutArray.append(txp + txsym[0:1])
    
    e.setRange(famname, 1, 9, OutArray)
    return len(OutArray)


if __name__ == "__main__":

    db = ADOdb(r"T:\Drylands Africa\ReddataWorkbench\Reddata release.accdb")
    rs = db.OpenTable("Select * from [Species]",[])
    print(db.RecordCount())
    #for i in range(0,100):
    while not rs.EOF:
        print(rs.Fields('Taxon').Value)
        tx = txParseName(rs.Fields('Taxon').Value)[2]
        rs.Fields('GENUS').Value = tx.genus
        rs.Fields('SP1').Value = tx.species
        rs.Fields('RANK1').Value = tx.infrarank
        rs.Fields('RANK2').Value = tx.infrarank2
        rs.Fields('SP2').Value = tx.infraepi
        rs.Fields('SP3').Value = tx.infraepi2
        rs.Update()
        rs.MoveNext()
    rs.Close()
    db.Close()
