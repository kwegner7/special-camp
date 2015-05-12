'''
    Database.TransformRow
'''

import re
from classes.utils.ShellCommand import ShellCommand
from classes.utils import Container, CsvObject
from classes.database.Database import Database

PLEASE_CAPITALIZE = True
PLEASE_IMPLEMENT  = True

def MethodNotImplemented():
    raise Exception("Method not implemented")

super = Database

#===============================================================================
# Common
#===============================================================================
class Common():  

    def csvFolder(self):
         return "csv/"
              
common = Common()

#===============================================================================
# (1) HowToCombineOriginalFiles
#===============================================================================
class HowToCombineOriginalFiles(super):

    if PLEASE_IMPLEMENT:
        def folderIn(self):         MethodNotImplemented()
        def originalFields(self):  MethodNotImplemented()
        def dialect(self):          MethodNotImplemented()
        def skipFirstRecord(self): MethodNotImplemented()
        def usefulFields(self):    MethodNotImplemented()

    def __init__(self, single_file=False):
        Container.clearFolder(self.folderOut() + common.csvFolder())
        file_out = self.folderOut() + common.csvFolder() + 'OriginalsCombined0.csv'

        if not single_file:
            csv_folder = CsvObject.CsvFolder( self.folderIn(),
                self.originalFields(), 
                self.dialect(), 
                self.skipFirstRecord() )
            csv_objects = CsvObject.FolderOfCsvObjects(file_out, csv_folder)
            csv_originals = csv_objects.combineIntoOneCsvObject(PLEASE_CAPITALIZE)
            print csv_originals.filename
            print csv_originals.fieldnames
        else:
            csv_originals = CsvObject.CsvObject(
                #"/home/kurt/ubu/finances/Chase/download/2014-04-19.csv",
                "/working/python/finance-old/out/Date/Derived.csv",
                self.originalFields(), 
                self.dialect(), 
                self.skipFirstRecord() )

        fieldnames = self.originalFields()
        filename = common.csvFolder() + 'OriginalsCombined1.csv'
        super.__init__(self, csv_originals, fieldnames, filename)
           
    def transformRow(self, row_in, csv_in, csv_out):
        row_out = self.initializeRowOut(row_in, csv_in, csv_out)
                
        rows = Container.VectorOfString()    
        rows.append(row_out)   
        return rows
        
#===============================================================================
# (1) HowToCombineOriginalFiles2
#===============================================================================
class HowToCombineOriginalFiles2(super):

    def __init__(self, csv_in):
        fieldnames = self.usefulFields()
        filename = common.csvFolder() + 'OriginalsCombined.csv'
        super.__init__(self, csv_in, fieldnames, filename)
    
        
#===============================================================================
# (2) HowToValidateAndNormalizeTheFields
#===============================================================================
class HowToValidateAndNormalizeTheFields(super):

    if PLEASE_IMPLEMENT:
        def usefulFields(self):          MethodNotImplemented()
        def normalizeAmountField(self): MethodNotImplemented()
        def normalizeDateField(self):   MethodNotImplemented()

    def __init__(self, csv_in):
        fieldnames = self.usefulFields()
        filename = common.csvFolder() + 'ValidatedAndNormalized.csv'
        super.__init__(self, csv_in, fieldnames, filename)
    

#===============================================================================
# (3) HowToDeriveNewFields
#===============================================================================
class HowToDeriveNewFields(super):

    if PLEASE_IMPLEMENT:
        def usefulFields(self):        MethodNotImplemented()
        def derivedFields(self):       MethodNotImplemented()

    def __init__(self, csv_in):
        fieldnames = self.usefulFields() + self.derivedFields()
        filename = common.csvFolder() + 'Derived.csv'
        super.__init__(self, csv_in, fieldnames, filename)
    
    
#===============================================================================
# (4) HowToSortTheRows1
#===============================================================================
class HowToSortTheRows1(super):

    def __init__(self, csv_in, sort_order):
        setA = set(csv_in.fieldnames)
        setB = set(sort_order)
        setC = setA - setB
        fieldnames = sort_order + list(setC)
        filename = common.csvFolder() + 'SortOrdered.csv'
        super.__init__(self, csv_in, fieldnames, filename)

    def transformRow(self, row_in, csv_in, csv_out):
        return self.copyMatchingFields(row_in, csv_in, csv_out)              


#===============================================================================
# (4) HowToSortTheRows2 - THIS IS SAME FOR BEYOND BANKING
#===============================================================================
class HowToSortTheRows2(super):

    def __init__(self, csv_in):
        fieldnames = csv_in.fieldnames
        filename = common.csvFolder() + 'Sorted0.csv'
        super.__init__(self, csv_in, fieldnames, filename)

        print "TransformRow.py",csv_in.filename,self.filename
        ShellCommand( 'sort  ' + csv_in.filename 
           ).redirect(self.filename)
        return None
    
    def transformRow(self, row_in, csv_in, csv_out):
        return self.returnNoRowsAtAll(row_in, csv_in, csv_out) 

#===============================================================================
# (4) HowToSortTheRows
#===============================================================================
class HowToSortTheRows(super):

    if PLEASE_IMPLEMENT:
        def sortOrder(self): MethodNotImplemented()

    def __init__(self, csv_in):
        csv_sorted_order = HowToSortTheRows1(csv_in, self.sortOrder())        
        csv_sorted       = HowToSortTheRows2(csv_sorted_order)  
        
        fieldnames = csv_sorted.fieldnames
        filename = common.csvFolder() + 'Sorted.csv'
        super.__init__(self, csv_sorted, fieldnames, filename)

    def transformRow(self, row_in, csv_in, csv_out):
        return self.copyMatchingFields(row_in, csv_in, csv_out) 
            
#===============================================================================
# (5) HowToCollapseOnFields
#===============================================================================
class HowToCollapseOnFields(super):

    if PLEASE_IMPLEMENT:
        def collapseOnFields(self): MethodNotImplemented()
    
    def __init__(self, csv_in):
        fieldnames = csv_in.fieldnames
        filename = common.csvFolder() + 'Collapsed.csv'
        super.__init__(self, csv_in, fieldnames, filename)

    def transformRow(self, row_in, csv_in, csv_out):
        row_out = self.initializeRowOut(row_in, csv_in, csv_out)
        rows = Container.VectorOfString()
        matches = True
        
        if 'prev_collapse_row' not in dir(self):
            self.prev_collapse_row = row_in
            matches = False
        elif len(self.collapseOnFields()) == 0:
            matches = False
        else:
            for field in self.collapseOnFields():
                if self.prev_collapse_row[field] != row_in[field]:
                    matches = False
        if not matches:
            rows.append(row_out)
        self.prev_collapse_row = row_in
        return rows

#===============================================================================
# (6) HowToSelectTheRows
#===============================================================================
class HowToSelectTheRows(super):

    if PLEASE_IMPLEMENT:
        def usefulFields(self):                    MethodNotImplemented()
        def derivedFields(self):                   MethodNotImplemented()
        def isSelectedRow(self, row_out, csv_out): MethodNotImplemented()

    def __init__(self, csv_in):
        fieldnames = self.usefulFields() + self.derivedFields()
        filename = common.csvFolder() + 'Selected.csv'
        super.__init__(self, csv_in, fieldnames, filename)
    
    def transformRow(self, row_in, csv_in, csv_out):
        row_out = self.initializeRowOut(row_in, csv_in, csv_out)
        rows = Container.VectorOfString() 
        if self.isSelectedRow(row_out, self):
            rows.append(row_out)
        return rows
        
#===============================================================================
# (7) HowToAccumulateNewColumns
#===============================================================================
class HowToAccumulateNewColumns(super):
    
    if PLEASE_IMPLEMENT:
        def accumulatedFields(self):               MethodNotImplemented()
        def sectionChange(self):                   MethodNotImplemented()
        def subsectionChange(self):                MethodNotImplemented()
        def afterSortRestoreAndAccumulate(self): MethodNotImplemented()

    def __init__(self, csv_in):
        fieldnames = csv_in.fieldnames + self.accumulatedFields()
        filename = common.csvFolder() + 'Accumulated.csv'
        
        self.monitor_unique = Container.MonitorField()
        self.monitor = Container.MonitorField()
        self.running_totals = Container.RunningTotals() # RunningTotals(14119.05)
        self.month_totals = Container.RunningTotals()
        self.year_totals = Container.RunningTotals()

        super.__init__(self, csv_in, fieldnames, filename)
        return None
  

#===============================================================================
# (8) HowToFinallyModifyCertainFields
#===============================================================================
class HowToFinallyModifyCertainFields(super):

    def __init__(self, csv_in):
        fieldnames = self.presentTheseFields()
        filename = common.csvFolder() + 'SpecialFields.csv'
        super.__init__(self, csv_in, fieldnames, filename)
        if True: print " CSV is at", self.filename
        return None
    
    def transformRow(self, row_in, csv_in, csv_out):
        row_out = self.initializeRowOut(row_in, csv_in, csv_out)

        rows = Container.VectorOfString()    
        rows.append(row_out)   
        return rows
    

