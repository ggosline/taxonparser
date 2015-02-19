import win32com
from win32com.client import constants as c   


class easyExcel:
    """A utility to make it easier to get at Excel. Remembering
    to save the data is your problem, as is error handling.
    Operates on one workbook at a time."""

    def __init__(self, filename=None, filepath=None):
        self.xlApp = win32com.client.Dispatch('Excel.Application.12')
        if filename:
            self.filename = filename
            try:
                self.xlBook = self.xlApp.Workbooks(filename)
            except:
                self.xlBook = self.xlApp.Workbooks.Open(filename)
        else:
            self.xlBook = self.xlApp.Workbooks.Add()
            self.filename = ""

        self.sht = self.xlBook.ActiveSheet


    def save(self, newfilename=None):
        if newfilename:
            self.filename = newfilename
            self.xlBook.SaveAs(newfilename)
        else:
            self.xlBook.Save()

    def close(self):
        self.xlBook.Close(SaveChanges=0)
        del self.xlApp

    # Now put in methods to set and get cells. Users can specify a sheet name or index, row, and column:

    def getCell(self, sheet=None, row=1, col=1):
        "Get value of one cell"
        if sheet:  self.sht = self.xlBook.Worksheets(sheet)
        return self.sht.Cells(row, col).Value

    def setCell(self, sheet=None, row=1, col=1, value=None):
        "set value of one cell"
        if sheet: self.sht = self.xlBook.Worksheets(sheet)
        self.sht.Cells(row, col).Value = value

    def getRange(self, sheet=None, row1=1, col1=1, row2=1, col2=1):
        "return a 2d array (i.e. tuple of tuples)"
        if sheet: self.sht = self.xlBook.Worksheets(sheet)
        return self.sht.Range(self.sht.Cells(row1, col1), self.sht.Cells(row2, col2)).Value

    # When you want to insert a block of data, just specify the first cell; there's no need for users to work out the number of rows:

    def setRange(self, sheet=None, topRow=1, leftCol=1, data=None):
        """insert a 2d array starting at given location.
        Works out the size needed for itself"""

        bottomRow = topRow + len(data) - 1
        rightCol = leftCol + len(data[0]) - 1

        if sheet: self.sht = self.xlBook.Worksheets(sheet)
        self.sht.Activate
        rng = self.sht.Range(
            self.sht.Cells(topRow, leftCol),
            self.sht.Cells(bottomRow, rightCol)
            )
        rng.Select
        rng.Value = data

    # Sometimes you need to grab a chunk of data when you don't know how many columns or even rows to expect. The following method scans down and right until it hits a blank: all that is needed is the starting point:

    def getContiguousRange(self, sheet=None, row=1, col=1):
        """Tracks down and across from top left cell until it
        encounters blank cells; returns the non-blank range.
        Looks at first row and column; blanks at bottom or right
        are OK and return None within the array"""

        if sheet: sht = self.xlBook.Worksheets(sheet)

        # find the bottom row
        bottom = row
        while self.sht.Cells(bottom + 1, col).Value not in [None, ""]:
            bottom = bottom + 1

        # right column
        right = col
        while self.sht.Cells(row, right + 1).Value not in [None, ""]:
            right = right + 1

        return self.sht.Range(sht.Cells(row, col), self.sht.Cells(bottom, right)).Value

    # Arrays coming back often contain either Unicode strings or COM dates. You could convert these on a per-column basis as needed (sometimes there's no need to convert them), but here's a utility that returns a new array in which these have been cleaned up:

    def fixStringsAndDates(self, aMatrix):
        # converts all unicode strings and times
        newmatrix = []
        for row in aMatrix:
            newrow = []
            for cell in row:
                if type(cell) is UnicodeType:
                    newrow.append(str(cell))
                elif type(cell) is TimeType:
                    newrow.append(int(cell))
                else:
                    newrow.append(cell)
            newmatrix.append(tuple(newrow))
        return newmatrix
