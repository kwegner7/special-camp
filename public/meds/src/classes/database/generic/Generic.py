'''
    Database.TransformRow.Finance
'''

import re, copy, glob
from classes.utils import Container, CsvObject
from classes.database.Account import Account

from classes.database.Database import Database
from classes.database import TransformRow

super = TransformRow

#===============================================================================
# Common
#===============================================================================
class Common(): 

    def __init__(self):
        csv_files = glob.glob(self.folderIn() + '*.csv')
        print "number fields is", CsvObject.numberOfFields(csv_files[0])
    
    def folderIn(self):
        return "/home/kurt/ubu/finances/MerrilLynch/download/"
        return "/home/kurt/ubu/finances/Chase/download/" 

    def dialect(self):
        return CsvObject.CsvStandardDialect()

    def skipFirstRecord(self):
        return True
        
    def originalFields(self): return list([
        "Trade Date",
        "Settlement Date",
        "Pending/Settled",
        "Account Nickname",
        "Account Registration",
        "Account #",
        "Type",
        "Description 1",
        "Description 2",
        "Symbol/CUSIP #",
        "Quantity",
        "Price ($)",
        "Amount ($)"
    ])
    
    def usefulFields(self):
        return self.originalFields()
        titles = list([ str(x) for x in range(0,13) ])
        return titles
           
    def derivedFields(self): return list([
    ])

    def accumulatedFields(self): return list([
    ])

    def presentTheseFields(self): return list([
        "Settlement Date",
        "Type",
        "Description 1",
        "Description 2",
        "Amount ($)"
    ])

    def isSelectedRow(self, row, csv_out):
        return True
    
    
    def collapseOnFields(self): return list([
    ])

    def sectionChange(self): return list([
    ])
               
    def subsectionChange(self): return list([
    ])

    
    def sortOrder(self): return list([
    ])
    
common = Common()


#===============================================================================
# (1) HowToCombineOriginalFiles
#===============================================================================
class HowToCombineOriginalFiles(super.HowToCombineOriginalFiles):
    def __init__(self):
        super.HowToCombineOriginalFiles.__init__(self)

#===============================================================================
# (2) HowToValidateAndNormalizeTheFields
#===============================================================================
class HowToValidateAndNormalizeTheFields(super.HowToValidateAndNormalizeTheFields):
    def __init__(self, csv_in):
        super.HowToValidateAndNormalizeTheFields.__init__(self, csv_in)

#===============================================================================
# (3) HowToDeriveNewFields
#===============================================================================
class HowToDeriveNewFields(super.HowToDeriveNewFields):
    def __init__(self, csv_in):
        super.HowToDeriveNewFields.__init__(self, csv_in)

#===============================================================================
# (4) HowToSortTheRows
#===============================================================================
class HowToSortTheRows(super.HowToSortTheRows):
    def __init__(self, csv_in):
        super.HowToSortTheRows.__init__(self, csv_in)
        
#===============================================================================
# (5) HowToCollapseOnFields
#===============================================================================
class HowToCollapseOnFields(super.HowToCollapseOnFields):
    def __init__(self, csv_in):
        super.HowToCollapseOnFields.__init__(self, csv_in)
        
#===============================================================================
# (6) HowToSelectTheRows
#===============================================================================
class HowToSelectTheRows(super.HowToSelectTheRows):
    def __init__(self, csv_in):
        super.HowToSelectTheRows.__init__(self, csv_in)
        
#===============================================================================
# (7) HowToAccumulateNewColumns
#===============================================================================
class HowToAccumulateNewColumns(super.HowToAccumulateNewColumns):
    def __init__(self, csv_in):
        super.HowToAccumulateNewColumns.__init__(self, csv_in)
        
#===============================================================================
# (8) HowToFinallyModifyCertainFields
#===============================================================================
class HowToFinallyModifyCertainFields(super.HowToFinallyModifyCertainFields):
    def __init__(self, csv_in):
        super.HowToFinallyModifyCertainFields.__init__(self, csv_in)

#===============================================================================
# (1) HowToCombineOriginalFiles
#===============================================================================
class HowToCombineOriginalFiles(super.HowToCombineOriginalFiles):
    
    def __init__(self):
        super.HowToCombineOriginalFiles.__init__(self, False)
    
    def usefulFields(self):
        return common.usefulFields()
    
    def folderIn(self):
        return common.folderIn()
        
    def originalFields(self):
        return common.usefulFields()

    def dialect(self):
        return common.dialect()

    def skipFirstRecord(self):
        return common.skipFirstRecord()
    
#===============================================================================
# (1) HowToCombineOriginalFiles2
#===============================================================================
class HowToCombineOriginalFiles2(super.HowToCombineOriginalFiles2):
    
    def __init__(self, csv_in):
        super.HowToCombineOriginalFiles2.__init__(self, csv_in)
    
    def usefulFields(self):
        return common.usefulFields()
    
    def folderIn(self):
        return common.folderIn()
        
    def originalFields(self):
        return common.usefulFields()

    def dialect(self):
        return common.dialect()

    def skipFirstRecord(self):
        return common.skipFirstRecord()
    
#===============================================================================
# (2) HowToValidateAndNormalizeTheFields
#===============================================================================        
class HowToValidateAndNormalizeTheFields(super.HowToValidateAndNormalizeTheFields):
    
    def __init__(self, csv_in):
        super.HowToValidateAndNormalizeTheFields.__init__(self, csv_in)
        
    def usefulFields(self):
        return common.usefulFields()
    
    def transformRow(self, row_in, csv_in, csv_out):
        row_out = self.initializeRowOut(row_in, csv_in, csv_out)              
        return Container.VectorOfString(row_out);fieldnames
    
#===============================================================================
# (3) HowToDeriveNewFields
#===============================================================================        
class HowToDeriveNewFields(super.HowToDeriveNewFields):
    
    def __init__(self, csv_in):            
        super.HowToDeriveNewFields.__init__(self, csv_in)
    
    def usefulFields(self):
        return common.usefulFields()

    def derivedFields(self):
        return common.derivedFields()   

#===============================================================================
# (4) HowToSortTheRows
#===============================================================================
class HowToSortTheRows(super.HowToSortTheRows):
    def __init__(self, csv_in):
        super.HowToSortTheRows.__init__(self, csv_in)
                        
    def sortOrder(self): return list([
    ])

#===============================================================================
# (5) HowToCollapseOnFields
#===============================================================================
class HowToCollapseOnFields(super.HowToCollapseOnFields):
    
    def __init__(self, csv_in):
        super.HowToCollapseOnFields.__init__(self, csv_in)
            
    def collapseOnFields(self):
        return common.collapseOnFields()   

#===============================================================================
# (6) HowToSelectTheRows
#===============================================================================
class HowToSelectTheRows(super.HowToSelectTheRows):
    def __init__(self, csv_in):
        super.HowToSelectTheRows.__init__(self, csv_in)
 
    def usefulFields(self):
        return common.usefulFields()
 
    def derivedFields(self):
        return common.derivedFields()
       
    def isSelectedRow(self, row, csv_out):
        return common.isSelectedRow(row, csv_out)   
    
#===============================================================================
# (7) HowToAccumulateNewColumns
#===============================================================================
class HowToAccumulateNewColumns(super.HowToAccumulateNewColumns):
    
    def __init__(self, csv_in):
        super.HowToAccumulateNewColumns.__init__(self, csv_in)

    def collapseOnFields(self): return list([
    ])

    def sectionChange(self): return list([
    ])
               
    def subsectionChange(self): return list([
    ])

    def accumulatedFields(self): return list([
    ])
            
    def afterSortRestoreAndAccumulate(self, field, row):
        return row[field]
        
#===============================================================================
# (8) HowToFinallyModifyCertainFields
#===============================================================================
class HowToFinallyModifyCertainFields(super.HowToFinallyModifyCertainFields):
    
    def __init__(self, csv_in):
        super.HowToFinallyModifyCertainFields.__init__(self, csv_in)
        
    def presentTheseFields(self):
        return common.presentTheseFields()


