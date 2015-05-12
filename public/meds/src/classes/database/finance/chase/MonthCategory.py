'''
    Database.TransformRow.Finance.ChaseCreditCard.MonthCategory
'''

from classes.database.finance.chase import ChaseCreditCard

super = ChaseCreditCard

#===============================================================================
# (1) HowToCombineOriginalFiles
#===============================================================================
class HowToCombineOriginalFiles(super.HowToCombineOriginalFiles):
    def __init__(self):
        super.HowToCombineOriginalFiles.__init__(self)

#===============================================================================
# (1) HowToCombineOriginalFiles2
#===============================================================================
class HowToCombineOriginalFiles2(super.HowToCombineOriginalFiles2):
    def __init__(self, csv_in):
        super.HowToCombineOriginalFiles2.__init__(self, csv_in)

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
        print "got to MonthCategory"
        super.HowToSortTheRows.__init__(self, csv_in)
                
    def sortOrder(self): return list([
        'YearMonth',
        'Category',
        'Date',
        'Subcategory',
        'Account',
        'SimplifiedAlias',
    ])

#===============================================================================
# (5) HowToCollapseOnFields
#===============================================================================
class HowToCollapseOnFields(super.HowToCollapseOnFields):
    def __init__(self, csv_in):
        super.HowToCollapseOnFields.__init__(self, csv_in)
        
    def collapseOnFields(self): return list([
    ])

#===============================================================================
# (6) HowToSelectTheRows
#===============================================================================
class HowToSelectTheRows(super.HowToSelectTheRows):
    def __init__(self, csv_in):
        super.HowToSelectTheRows.__init__(self, csv_in)

    def isSelectedRow(self, row, csv_out):
        return (
            row['Mechanism'] == 'Credit Card Purchase' or
            row['Mechanism'] == 'Credit Card Refund' )
        
#===============================================================================
# (7) HowToAccumulateNewColumns
#===============================================================================
class HowToAccumulateNewColumns(super.HowToAccumulateNewColumns):
    def __init__(self, csv_in):
        super.HowToAccumulateNewColumns.__init__(self, csv_in)
        
    def sectionChange(self): return list([
        'YearMonth'
    ])
               
    def subsectionChange(self): return list([
        'Category'
    ])

#===============================================================================
# (8) HowToFinallyModifyCertainFields
#===============================================================================
class HowToFinallyModifyCertainFields(super.HowToFinallyModifyCertainFields):
    def __init__(self, csv_in):
        super.HowToFinallyModifyCertainFields.__init__(self, csv_in)
       