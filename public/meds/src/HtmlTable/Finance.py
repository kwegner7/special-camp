'''
    class HtmlTable
'''

import sys, os, re, collections
from utils.Container import *
from Base import HtmlTable
from presentation import SelectOrdering, SelectSections, SelectColumns
    
PLEASE_SPLIT = True
DONT_SPLIT = False

########################################################################
# HtmlTable.Base.Finance
########################################################################
class Finance(HtmlTable):
        
    #===========================================================================
    # __init__
    #===========================================================================
    def __init__(self, accumulate):        
        HtmlTable.__init__(self, accumulate, 'CsvTable', self.headingAccount() )

    def determineSpecialFields(self, row):
        special = dict(row)
        special['Date'] = convertToStandardDate(row['Date'])
        return special

    def tocShow(self):
        return set([''])

    #===========================================================================
    # implementations
    #===========================================================================
    def selectOrdering(self):
        return SelectOrdering.Date()

    def selectSections(self):
        return SelectSections.Year()

    def presentationMainTable(self):
        return SelectColumns.TableFinance('CsvTable')

    def betweenSectionsAndSubsections(self):
        return SelectColumns.FinanceStandard(DONT_SPLIT)

    def headingAccount(self):
        return 'Account'

    def summaryOnly(self):
        return False
    
    def getRowColor(self, row):
        return self.colors.getCyclicColors()       
                
    def monthlyYearly(self):
        if 'Year' in self.fieldsDeterminingSubsection(): return 'Year'
        if 'YearMonth' in self.fieldsDeterminingSubsection(): return 'YearMonth'
        return ''
   
    def summaryFollowingDetails(self, how_many, bottom_row_prev_section):

        # write some blank lines        
        self.writeRowsOfColor('white', 1)
        
        if 'Account' in self.orderedHtmlColumns():
            Account = 'Account'
        elif 'FromAccount' in self.orderedHtmlColumns():
            Account = 'FromAccount'
        else:
            Account = 'Account Not Displayed'
        
        if ( 'SectionTotal'   in bottom_row_prev_section
        and  'SectionCredit'  in bottom_row_prev_section
        and  'SectionDebit'   in bottom_row_prev_section
        and  'Date'           in self.orderedHtmlColumns()
        and  'Mechanism'      in self.orderedHtmlColumns()
        and  Account          in self.orderedHtmlColumns()):

            # format month and year presentation
            month_year = removeDayFromDate(bottom_row_prev_section['Date'])
            if self.monthlyYearly() == 'YearMonth':
                text_month_year = month_year[0] + ' ' + month_year[1]
            elif self.monthlyYearly() == 'Year':
                text_month_year = 'Year ' + month_year[1]
            else:
                text_month_year = ''

            # determine the category and subcategory to print in summary section
            has_category    = ('Category'    in self.orderedHtmlColumns())
            has_subcategory = ('Subcategory' in self.orderedHtmlColumns())
            level1 = level2 = ''
            if 'Category' in self.fieldsDeterminingSubsection():
                level1 = bottom_row_prev_section['Category']
            if 'Subcategory' in self.fieldsDeterminingSubsection():
                level2 = bottom_row_prev_section['Subcategory']

            # maybe this is sectioned by the account name
            account = 'Beyond Banking'
            if Account in self.fieldsDeterminingSubsection():
                account = bottom_row_prev_section[Account]

            # determine how many lines will be printed, depends on credits/debits
            ave_per_month = avePerMonth(bottom_row_prev_section['SectionTotal'])
            no_credits = (bottom_row_prev_section['SectionCredit'] == '0.00')
            no_debits = (bottom_row_prev_section['SectionDebit'] == '0.00')
            
            # Line 1 of sub-totals is income
            blank_fields = dict()
            for fld in self.orderedHtmlColumns():blank_fields[fld] = '&nbsp;'  
            
            blank_fields['Date']         = text_month_year
            blank_fields['RunningTotal'] = bottom_row_prev_section['RunningTotal']
            blank_fields[Account]        = self.betweenSectionsAndSubsections().textOfAccount() # account
            if has_category:    blank_fields['Category']    = level1
            if has_subcategory: blank_fields['Subcategory'] = level2
            
            
                      
            # Line 1 of sub-totals is income
            blank_fields['Mechanism'] = 'Income' # self.betweenSectionsAndSubsections().textOfMechanism() # 
            blank_fields['Amount']    = bottom_row_prev_section['SectionCredit']
            if not no_credits: self.writeLines(self.html_table.insertOneRecord(blank_fields, 'white'))
            
            # Line 2 of sub-totals is expense
            blank_fields['Mechanism']  = 'Expense'
            blank_fields['Amount']     = bottom_row_prev_section['SectionDebit']
            if not no_debits: self.writeLines(self.html_table.insertOneRecord(blank_fields, 'white'))           
            
            # Line 3 of sub-totals is net (only if there are both expenses and income)
            blank_fields['Mechanism'] = 'Net'
            blank_fields['Amount']   = bottom_row_prev_section['SectionTotal']
            if (not no_debits) and (not no_credits): self.writeLines(self.html_table.insertOneRecord(blank_fields, 'white'))           
            
            # Line 2 or 3 of sub-totals is monthly average (only if this is yearly presentation)
            blank_fields['Mechanism']    = 'Ave Per Month'
            blank_fields['Amount']       = ave_per_month
            if ( self.monthlyYearly() == 'Year'
            and  self.betweenSectionsAndSubsections().showMonthlyAverage()):
                self.writeLines(self.html_table.insertOneRecord(blank_fields, 'white'))
            
            # done with sub-totals
            self.writeRowsOfColor('white', 1)
            return None
                                
        else:
            print 'Do not print the summary totals', bottom_row_prev_section
            print 'Do not print the summary totals', self.orderedHtmlColumns
            return None
      
    
    def howManyBlankRows(self):
        return (1)
    
    def orderedHtmlColumns(self):
        fieldnames = [ cell.fieldname for cell in self.html_table.columns() ]
        return fieldnames
    
    def printDetails(self):
        return True


    
