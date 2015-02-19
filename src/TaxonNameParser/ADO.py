import win32com.client
win32com.client.gencache.is_readonly = False

from win32com.client import Dispatch, constants

class ADOdb(object):

    # provider = "Provider=Microsoft.Jet.OLEDB.4.0;"
    # dsource  = "Data Source=MDB; User ID=Admin; Password=;"
    provider = "Provider=Microsoft.Ace.OLEDB.12.0;"
    dsource = dsource = "Provider=Microsoft.Ace.OLEDB.12.0; Data Source=%s; User ID=Admin; Password=;"
    

    def __init__(self, databasename):
        global connection, command
        connection = Dispatch("ADODB.Connection")
        command = Dispatch("ADODB.Command")
        
        connection.Open(ADOdb.dsource % databasename)
        command.ActiveConnection = connection
                

    def __del__(self):
        connection.Close

    def printerrs(self):
        for err in connection.Errors:
            print (err.Number, err.Description, err.Source)
        
    def OpenTable(self, selectstmt, fldlist):
        
        self.rs = Dispatch("ADODB.Recordset")
        self.rs.CursorLocation = constants.adUseClient
        self.rs.Open(selectstmt, connection, constants.adOpenStatic, constants.adLockOptimistic)
        self.fldlist = fldlist
        self.reccount = self.rs.RecordCount
        self.rs.AbsolutePosition = 1

    def NextRec(self):
        if not self.rs.EOF:
            # flds = {fld : self.rs.Fields(fld).Value if self.rs.Fields(fld).Value is not None else '' for fld  in self.fldlist}
            flds = ' '.join([self.rs.Fields(fld).Value if self.rs.Fields(fld).Value is not None else '' for fld in self.fldlist])
            self.rs.MoveNext()
            return flds
        else:
            return(None)

    def MoveTo(self, absoluterec):
        self.rs.AbsolutePosition = absoluterec + 1 

    def RecordCount(self):
        return self.reccount

parserflds = ['taxonkey', 'rank', 'genus', 'species', 'author', 'infrarank', 'infraepi', 'par']
  
if __name__ == "__main__":

    myds = ADOdb(r'"T:\Cameroon\FWTA\APD.accdb"')
    myds.OpenTable("SELECT APD.* FROM [APD] WHERE (((APD.[family])='agavaceae'));", parserflds)
    print (myds.RecordCount())
    print (myds.NextRec())

    del myds
