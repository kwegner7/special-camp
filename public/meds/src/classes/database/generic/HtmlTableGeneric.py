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
# HtmlTable.Details
#==============================================================================
class Details(HtmlTable.Base):
    
    def __init__(self, csv_object, csv_sorted, folder_out): 
        HtmlTable.Base.__init__(self, csv_object, csv_sorted, folder_out)
        self.createHtmlTables(csv_object, folder_out)

    def summaryOnly(self):
        return False
            
    def splitSectionsIntoSeparateFiles(self):
        return False
       
    def beginSection(self, writer, first_row):
        self.first_row_of_section = True
        writer.write( self.tableBegin() )
        writer.write( self.tableWidths() )
        self.writeRowsOfColor('white', 2)
        return None
                       
    def endSection(self, writer, last_row):
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

        #self.summaryFollowingDetails(1, row)
        return None
       
        
    def columns(self):
        if not hasattr(self, 'cfg'):
            self.cfg = collections.namedtuple( 'ConfigureColumns',
            'fieldname, heading, width, CellStyle, fontsize' )
        
        nature_of_columns = list()
        for field in self.csv_special_fields.presentTheseFields():
            nature_of_columns.append(self.cfg(field, field,  0, 'nowrapl', '1.0' ))
        
        return nature_of_columns

    def summaryFollowingDetails(self, how_many, bottom_row_prev_section):
        return None
