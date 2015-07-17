import EasyExcel
from TaxonNameParser import txMatcher 
from pythonwin import win32ui
from recordtype import recordtype

taxonName = recordtype("taxonName", "genus species author infrarank infraepi par", default="")

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
        elif rec.infrarank == "var. ":
            rank = "variety"
        elif rec.infrarank == "f.":
            rank = "forma"
    return ([taxID, rank] + list(iter(rec)))

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

def ParseActiveRange():

    OutArray = []

    txrows = e.xlApp.Selection

    for row in txrows.Rows:
        # if row(1).Text == "":
        #    break
        txp = txParseName(row.Cells(2).Text)
        if row(4) != "":
            txsym = txParseName(row.Cells(4).Text)
        else:
            txsym = [""]
        OutArray.append(txp + txsym[0:1])
    
    e.setRange(None, txrows.Row, 9, OutArray)
    return len(OutArray)


if __name__ == "__main__":

    o = win32ui.CreateFileDialog(1, ".xls", "APD.xlsm", 0, "Excel Files (*.xls)|*.xlsm;*.xls|All Files (*.*)|*.*||")
    o.SetOFNInitialDir("T:\\Cameroon\\FWTA")
    o.DoModal()

    fp = o.GetPathName()
    fn = o.GetFileName()
    e = EasyExcel.easyExcel(fn, fp)

    # famnames = e.getRange("Families",1,1,300,1)
    # for ind in range(201,202):
    #    rows = ParseFamily(famnames[ind][0])
    #    print (famnames[ind][0], rows)

    ParseActiveRange()

