'''
    Database.TransformRow.Finance.ChaseCreditCard.Date
'''

from classes.database.finance.chase import ChaseCreditCard

#===============================================================================
# Database.TransformRow.Finance.ChaseCreditCard.Date
#===============================================================================
class HowToCombineOriginalFiles(ChaseCreditCard.HowToCombineOriginalFiles):
    def __init__(self):
        ChaseCreditCard.HowToCombineOriginalFiles.__init__(self)
        
class HowToValidateAndNormalizeTheFields(ChaseCreditCard.HowToValidateAndNormalizeTheFields):
    def __init__(self, csv_in):
        ChaseCreditCard.HowToValidateAndNormalizeTheFields.__init__(self, csv_in)
        
class HowToDeriveNewFields(ChaseCreditCard.HowToDeriveNewFields):
    def __init__(self, csv_in):
        ChaseCreditCard.HowToDeriveNewFields.__init__(self, csv_in)
        
class HowToSortTheRows(ChaseCreditCard.HowToSortTheRows):
    def __init__(self, csv_in):
        ChaseCreditCard.HowToSortTheRows.__init__(self, csv_in)
        
class HowToCollapseOnFields(ChaseCreditCard.HowToCollapseOnFields):
    def __init__(self, csv_in):
        ChaseCreditCard.HowToCollapseOnFields.__init__(self, csv_in)
        
class HowToSelectTheRows(ChaseCreditCard.HowToSelectTheRows):
    def __init__(self, csv_in):
        ChaseCreditCard.HowToSelectTheRows.__init__(self, csv_in)
        
class HowToAccumulateNewColumns(ChaseCreditCard.HowToAccumulateNewColumns):
    def __init__(self, csv_in):
        ChaseCreditCard.HowToAccumulateNewColumns.__init__(self, csv_in)
        from classes.database.finance import Configuration  

class HowToFinallyModifyCertainFields(ChaseCreditCard.HowToFinallyModifyCertainFields):
    def __init__(self, csv_in):
        ChaseCreditCard.HowToFinallyModifyCertainFields.__init__(self, csv_in)
#===============================================================================
# end
#===============================================================================


#===============================================================================
# (1) HowToCombineOriginalFiles2
#===============================================================================
class HowToCombineOriginalFiles2(ChaseCreditCard.HowToCombineOriginalFiles2):
    def __init__(self, csv_in):
        ChaseCreditCard.HowToCombineOriginalFiles2.__init__(self, csv_in)

#===============================================================================
# HowToSortTheRows
#===============================================================================
class HowToSortTheRows(ChaseCreditCard.HowToSortTheRows):

    def __init__(self, csv_in):
        ChaseCreditCard.HowToSortTheRows.__init__(self, csv_in)
                
    def sortOrder(self): return list([
        'Date',
        'Account',
        'Category',
        'Subcategory',
        'AccountAlias',
    ]) 
               
#===============================================================================
# HowToCollapseOnFields
#===============================================================================
class HowToCollapseOnFields(ChaseCreditCard.HowToCollapseOnFields):
    
    def __init__(self, csv_in):
        ChaseCreditCard.HowToCollapseOnFields.__init__(self, csv_in)
        
    def collapseOnFields(self): return list([
    ])


#===============================================================================
# HowToAccumulateNewColumns
#===============================================================================
class HowToAccumulateNewColumns(ChaseCreditCard.HowToAccumulateNewColumns):

    def __init__(self, csv_in):
        ChaseCreditCard.HowToAccumulateNewColumns.__init__(self, csv_in)
        
    def sectionChange(self): return list([
        'YearMonth'
    ])
               
    def subsectionChange(self): return list(['YearMonth'])
    
#===============================================================================
# HowToSelectTheRows
#===============================================================================
class HowToSelectTheRows(ChaseCreditCard.HowToSelectTheRows):
    
    def __init__(self, csv_in): 
        ChaseCreditCard.HowToSelectTheRows.__init__(self, csv_in)
    
    def isSelectedRow(self, row, csv_out):
        return (
            row['Mechanism'] == 'Credit Card Purchase' or
            row['Mechanism'] == 'Credit Card Refund' )



