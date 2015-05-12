'''
    Records.Accumulate.Finance
'''

from utils.Container import *
from records.Accumulate.Accumulate import Accumulate
from presentation import SelectOrdering, SelectSections, SelectColumns

#===============================================================================
# Records.Accumulate.Finance
#===============================================================================
class Finance(Accumulate):
    
    #===========================================================================
    # implementations
    #===========================================================================
    def accumulatedFields(self): pass
    def afterSortRestoreAndAccumulate(self): pass
    
    #===========================================================================
    # constructor
    #===========================================================================
    def __init__(self, normalize):
        Accumulate.__init__(self, normalize)
        return None
    
    #===========================================================================
    # Any database
    #===========================================================================
    def accumulatedFields(self): return list([
        'NumberTransactions',
        'RunningTotal',
        'SectionTotal',
        'SectionCredit',
        'SectionDebit',
        'MonthTotal',
        'MonthCredit',
        'MonthDebit',
        'YearTotal',
        'YearCredit',
        'YearDebit',
    ])
    
    # FIX THIS FOR FINANCE
    def afterSortRestoreAndAccumulate(self, field, row):

        if (field == 'NumberTransactions'):
            return self.running_totals.getNumberTransactions()

        elif (field == 'RunningTotal'):
            return self.running_totals.getRunningTotal()

        elif (field == 'SectionTotal'):
            return self.running_totals.getSection()

        elif (field == 'SectionCredit'):
            return self.running_totals.getCredit()

        elif (field == 'SectionDebit'):
            return self.running_totals.getDebit()

        elif (field == 'MonthTotal'):
            return self.month_totals.getSection()

        elif (field == 'MonthCredit'):
            return self.month_totals.getCredit()

        elif (field == 'MonthDebit'):
            return self.month_totals.getDebit()

        elif (field == 'YearTotal'):
            return self.year_totals.getSection()

        elif (field == 'YearCredit'):
            return self.year_totals.getCredit()

        elif (field == 'YearDebit'):
            return self.year_totals.getDebit()

        else:
            return row[field]
                
#===============================================================================
# Records.Accumulate.Finance.BeyondBanking
#===============================================================================
class BeyondBanking(Finance):
        
    #===========================================================================
    # constructor
    #===========================================================================
    def __init__(self, normalize):
        Finance.__init__(self, normalize)
        return None
    
    #===========================================================================
    # implementations
    #===========================================================================
    def isSelectedRow(self, col, records_in):
        return ( True )

    def selectOrdering(self):
        return SelectOrdering.Date()

    def selectSections(self):
        return SelectSections.Year()
    
    def uniqueFields(self):
        return list([])

#===============================================================================
# Records.Accumulate.Finance.PaypalFaraja
#===============================================================================
class PaypalFaraja(Finance):
        
    #===========================================================================
    # constructor
    #===========================================================================
    def __init__(self, normalize):
        Finance.__init__(self, normalize)
        return None
    
    #===========================================================================
    # implementations
    #===========================================================================
    def isSelectedRow(self, col, records_in):
        return ( True )

    def selectOrdering(self):
        return SelectOrdering.Date()

    def selectSections(self):
        return SelectSections.Year()
    
    def uniqueFields(self):
        return list([])
