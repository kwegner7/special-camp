'''
    namespace src.finance.SelectOrdering
'''
    
########################################################################
# SelectOrdering.Date
########################################################################
class Date():
    
    def title(self): return 'Date'
                
    def sortOrder(self): return list([
        'Date',
        'Category',
        'Subcategory',
        'Account',
        'AccountAlias',
    ])

    def sectionChange(self):
        return list([ '' ])

########################################################################
# SelectOrdering.CategoryDate
########################################################################
class CategoryDate():

    def title(self): return 'Category'
              
    def sortOrder(self): return list([
        'Category',
        'Date',
        'Subcategory',
        'Account',
        'AccountAlias',
    ])

    def sectionChange(self): return list([
        'Category'
    ])
    
########################################################################
# SelectOrdering.CategorySubcategoryDate
########################################################################
class CategorySubcategoryDate():

    def title(self): return 'Subcategory'
                
    def sortOrder(self): return list([
        'Category',
        'Subcategory',
        'Date',
        'Account',
        'AccountAlias',
    ])

    def sectionChange(self): return list([
        'Category', 'Subcategory'
    ])
    
########################################################################
# SelectOrdering.AccountDate
########################################################################
class AccountDate():

    def title(self): return 'Account'
                
    def sortOrder(self): return list([
        'Account',
        'Date',
        'AccountAlias',
    ])

    def sectionChange(self): return list([
        'Account',
    ])
    
#===============================================================================
# Special Camp
#===============================================================================
class ByCamper():

    def title(self): return 'SectionCamper'
                
    def sortOrder(self):
        return ['camper', 'ordered_day', 'ordered_time', 'medication']

    def sectionChange(self): return list([
        'camper',
    ])
    
class EachDaySeparate():

    def title(self): return 'SectionEachDaySeparate'
                
    def sortOrder(self):
        return ['camper', 'ordered_day', 'ordered_time', 'medication']

    def sectionChange(self):
        return list([ 'camper', 'day' ])
    
class DaysCombined():

    def title(self): return 'SectionDaysCombined'
                
    def sortOrder(self):
        return ['camper', 'ordered_time', 'medication']

    def sectionChange(self):
        return list([ 'camper' ])
    
class TimeMed():

    def title(self): return 'SectionTimeMed'
                
    def sortOrder(self):
        return [ 'ordered_time', 'medication', 'camper', 'ordered_day']

    def sectionChange(self): return list([
        'camper'
    ])
