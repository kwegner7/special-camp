'''
    class HtmlTable
'''

import sys, os, re, collections
from classes.utils.Container import *
from classes.database.finance import HtmlTable
from classes.utils import Html


PLEASE_SPLIT = True
DONT_SPLIT = False
        

#==============================================================================
# HtmlTable.CategoryDetails
#==============================================================================
class CategoryDetails(HtmlTable.Base):

    def __init__(self, csv_object, sectionChange, subsectionChange, folder_out):
        HtmlTable.Base.__init__(self, csv_object, sectionChange, subsectionChange, folder_out)
        self.createHtmlTables(csv_object, folder_out)

    def summaryOnly(self):
        return False
            
    def splitSectionsIntoSeparateFiles(self):
        return False
    
    def columns(self):
        if not hasattr(self, 'cfg'):
            self.cfg = collections.namedtuple( 'ConfigureColumns',
            'fieldname, heading, width, CellStyle, fontsize' )
        nature_of_columns = ([
        self.cfg('Date'          , 'Date'                    ,   0,    'date', '1.0' ),
        #self.cfg('Mechanism'     , 'Method of Transfer'      ,   0, 'nowrapl', '1.0' ),
        self.cfg('Amount'        , 'Amount'                  ,   0,   'funds', '1.0' ),
        self.cfg('Category'      , 'Category'                ,   0, 'nowrapl', '1.0' ),
        self.cfg('Subcategory'   , 'Subcategory'             ,   0, 'nowrapl', '1.0' ),
        self.cfg('Account'       , 'Store'                 ,   0, 'nowrapl', '1.0' ),
        #self.cfg('SimplifiedAlias'   , 'Simplified'             ,   0, 'whitel', '1.0' ),
        #self.cfg('AccountAlias'  , 'Details'                 , 100,  'whitel', '1.0' ),
        #self.cfg('RunningTotal' , 'Running'                 ,   0,   'funds', '1.0' ),
        ])
        return nature_of_columns
       
    def beginSection(self, writer, first_row):
        self.first_row_of_section = True
        writer.write( self.tableBegin() )
        writer.write( self.tableWidths() )
        self.writeRowsOfColor('white', 2)

        if self.summaryOnly():
            # advance the color            
            self.background_color = self.getRowColor(first_row)
            self.writeRowsOfSummaryColor('white', 1)
            self.writeRowsOfSummaryColor(self.background_color, 1, False)
        return None
                       
    def endSection(self, writer, last_row):
        if self.summaryOnly():
            blank_fields = dict()
            for fld in self.orderedHtmlColumns():blank_fields[fld] = '&nbsp;'  
            self.writeRowsOfSummaryColor(self.background_color, 1, False)
            blank_fields['Date']        = last_row['Date'][2:]
            blank_fields['Mechanism']   = '&nbsp;'
            blank_fields['Amount']      = last_row['MonthTotal']
            blank_fields['Account']     = '&nbsp;'
            blank_fields['Category']    = 'Total credit card purchases this month'
            blank_fields['Subcategory'] = '&nbsp;'
            self.insertOneSummaryRecord(blank_fields, self.background_color, 'normal')            
            self.writeRowsOfSummaryColor(self.background_color, 1, False)
        writer.write( self.tableEnd() )
        return None

    def beginSubsection(self, writer, row, bookmark):
        if self.first_row_of_section:       
            writer.write( self.bookmark(bookmark) )
            if not self.summaryOnly():
                writer.write( self.tableHeadings() )
        if not self.summaryOnly():
            # advance the color            
            self.background_color = self.getRowColor(row)
        self.writeRowsOfColor(self.background_color, 1, False)
        self.first_row_of_section = False
        return None
    
    def endSubsection(self, writer, monitor, is_final_row):
        # check if this is last row of the file
        bottom_row_prev_section = monitor.prev_fields
        last_row_of_csv_file = monitor.new_fields

        if is_final_row:
            row = last_row_of_csv_file
        else:
            row = bottom_row_prev_section

        if True:
            self.summaryFollowingDetails(1, row)
        else:
            self.summaryRecordsOnly(self.howManyBlankRows(), row,
                'SectionTotal', 'SectionCredit', 'SectionDebit' )
            if monitor.fieldHasChanged('Year') or is_final_row:
                self.summaryRecordsOnly(1, row,
                    'YearTotal', 'YearCredit', 'YearDebit' )
        return None
       
    def summaryFollowingDetails(self, how_many, bottom_row_prev_section):
        self.writeRowsOfColor(self.background_color, 1, False)
        blank_fields = dict()
        for fld in self.orderedHtmlColumns():blank_fields[fld] = '&nbsp;'  
        blank_fields['Date']        = bottom_row_prev_section['Date'][2:]
        blank_fields['Mechanism']   = '&nbsp;'
        blank_fields['Amount']      = bottom_row_prev_section['SectionTotal']
        blank_fields['Account']     = '&nbsp;'
        blank_fields['Category']    = 'Total'
        blank_fields['Subcategory'] = '&nbsp;'
        self.insertOneSummaryRecord(blank_fields, self.background_color, 'normal')  
        self.writeRowsOfColor(self.background_color, 1, False)
        return None
        
#==============================================================================
# HtmlTable.Chase.CategorySummary
#==============================================================================
class CategorySummary(CategoryDetails):
    
    def __init__(self, csv_object, sectionChange, subsectionChange, folder_out):        
        CategoryDetails.__init__(self, csv_object, sectionChange, subsectionChange, folder_out)

    def summaryOnly(self):
        return True
    
    def summaryFollowingDetails(self, how_many, bottom_row_prev_section):
        self.writeRowsOfColor(self.background_color, 1, False)
        blank_fields = dict()
        for fld in self.orderedHtmlColumns():blank_fields[fld] = '&nbsp;'  
        blank_fields['Date']        = bottom_row_prev_section['Date'][2:]
        blank_fields['Mechanism']   = '&nbsp;'
        blank_fields['Amount']      = bottom_row_prev_section['SectionTotal']
        blank_fields['Account']     = '&nbsp;'
        blank_fields['Category']    = bottom_row_prev_section['Category']
        blank_fields['Subcategory'] = '&nbsp;'
        self.insertOneSummaryRecord(blank_fields, self.background_color, 'normal')  
        self.writeRowsOfColor(self.background_color, 1, False)
        return None

#==============================================================================
# HtmlTable.Chase.Summary
#==============================================================================
class Summary(CategorySummary):
    
    def __init__(self, csv_object, sectionChange, subsectionChange, folder_out):        
        CategorySummary.__init__(self, csv_object, sectionChange, subsectionChange, folder_out)

    def summaryOnly(self):
        return True
    
    def beginSection(self, writer, first_row):
        self.first_row_of_section = True
        writer.write( self.tableBegin() )
        writer.write( self.tableWidths() )
        self.writeRowsOfColor('white', 2)

        if self.summaryOnly():
            # advance the color            
            self.background_color = self.getRowColor(first_row)
            #self.writeRowsOfSummaryColor('white', 1)
            #self.writeRowsOfSummaryColor(self.background_color, 1, False)
        return None
    
    def beginSubsection(self, writer, row, bookmark):
        self.first_row_of_section = False
        return None
                       
    def endSubsection(self, writer, monitor, is_final_row):
        return None

#==============================================================================
# HtmlTable.Chase.Details
#==============================================================================
class Details(CategoryDetails):
    
    def __init__(self, csv_object, sectionChange, subsectionChange, folder_out):        
        CategoryDetails.__init__(self, csv_object, sectionChange, subsectionChange, folder_out)
        
    def columns(self):
        if not hasattr(self, 'cfg'):
            self.cfg = collections.namedtuple( 'ConfigureColumns',
            'fieldname, heading, width, CellStyle, fontsize' )
        
        nature_of_columns = ([
        self.cfg('Date'          , 'Date'                    ,   0,    'date', '1.0' ),
        #self.cfg('Mechanism'     , 'Method of Transfer'      ,   0, 'nowrapl', '1.0' ),
        self.cfg('Amount'        , 'Amount'                  ,   0,   'funds', '1.0' ),
        self.cfg('Account'       , 'Store'                 ,   0, 'nowrapl', '1.0' ),
        #self.cfg('FromAccount'   , 'Funds From'              ,   0, 'nowrapl', '1.0' ),
        #self.cfg('ToAccount'     , 'Have Been Transferred To',   0, 'nowrapl', '1.0' ),
        self.cfg('Category'      , 'Category'                ,   0, 'nowrapl', '1.0' ),
        self.cfg('Subcategory'   , 'Subcategory'             ,   0, 'nowrapl', '1.0' ),
        #self.cfg('SimplifiedAlias'   , 'Simplified'             ,   0, 'whitel', '1.0' ),
        #self.cfg('AccountAlias'  , 'Details'                 , 100,  'whitel', '1.0' ),
        #self.cfg('RunningTotal' , 'Running'                 ,   0,   'funds', '1.0' ),
        ])
        
        return nature_of_columns

    def summaryFollowingDetails(self, how_many, bottom_row_prev_section):

        self.writeRowsOfColor(self.background_color, 1, False)
        blank_fields = dict()
        for fld in self.orderedHtmlColumns():blank_fields[fld] = '&nbsp;'  
        blank_fields['Date']        = bottom_row_prev_section['Date'][2:]
        blank_fields['Mechanism']   = '&nbsp;'
        blank_fields['Amount']      = bottom_row_prev_section['SectionTotal']
        blank_fields['Account']     = 'Total credit card purchases this month'
        blank_fields['Category']    = '&nbsp;'
        blank_fields['Subcategory'] = '&nbsp;'
        if self.summaryOnly():
            self.insertOneSummaryRecord(blank_fields, self.background_color, 'normal')  
        else:          
            self.insertOneSummaryRecord(blank_fields, self.background_color, 'normal')            
        self.writeRowsOfColor(self.background_color, 1, False)
        return None
