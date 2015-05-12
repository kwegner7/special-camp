'''
    Report.Chase
'''

from classes.report.Report import Report 
from classes.html import HtmlFinance
from classes.database import Db
from classes.database.config import Finance
  
#===============================================================================
# TotalsEachMonth
#===============================================================================
class TotalsEachMonth(Report):

    def __init__(self):
        Report.__init__(self)

    def whichConfigClass(self):
        return Finance.config
    
    def htmlFolder(self):
        return 'TotalsEachMonth/'
    
    def whichCsvModule(self):
        return Db
    
    def whichHtmlModule(self):
        return HtmlFinance.Summary
  
#===============================================================================
# TotalsEachMonthEachCategory
#===============================================================================
class TotalsEachMonthEachCategory(Report):

    def __init__(self):
        Report.__init__(self)

    def whichConfigClass(self):
        return Finance.config
    
    def htmlFolder(self):
        return 'TotalsEachMonthEachCategory/'
    
    def whichCsvModule(self):
        return Db
    
    def whichHtmlModule(self):
        return HtmlFinance.CategorySummary
       
#===============================================================================
# DetailsEachMonthEachCategory
#===============================================================================
class DetailsEachMonthEachCategory(Report):
   
    def __init__(self):
        Report.__init__(self)
   
    def whichConfigClass(self):
        return Finance.config
    
    def htmlFolder(self):
        return 'DetailsEachMonthEachCategory/'

    def whichCsvModule(self):
        return Db
    
    def whichHtmlModule(self):
        return HtmlFinance.CategoryDetails
  
#===============================================================================
# DetailsEachMonth
#===============================================================================
class DetailsEachMonth(Report):
    
    def __init__(self):
        Report.__init__(self)

    def whichConfigClass(self):
        return Finance.config
    
    def htmlFolder(self):
        return 'DetailsEachMonth/'
    
    def whichCsvModule(self):
        return Db
    
    def whichHtmlModule(self):
        return HtmlFinance.Details

 
