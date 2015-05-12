'''
    class HtmlTable
'''

import sys, os, re, collections
from classes.utils.Container import *
from classes.utils import Html

########################################################################
# HtmlTable.Base
########################################################################
class Base():

    def __init__(self, csv_object, sectionChange, subsectionChange, folder_out):
        self.csv_special_fields = csv_object
        self.sectionChange = sectionChange
        self.subsectionChange = subsectionChange
        self.tablename = 'CsvTable'
        self.fieldsDeterminingSection = self.sectionChange
        self.fieldsDeterminingSubsection = self.subsectionChange
        self.colors = Colors()
        self.heading_account = self.headingAccount()
        pass

    def sectionChange(self):
        return self.sectionChange
    
    def subsectionChange(self):
        return self.subsectionChange
    
    def headingAccount(self):
        return 'Account'
    
    def getRowColor(self, row):
        return self.colors.getCyclicColors()

    def bookmark(self, text='RaynaAndLevi'):
        text = '<a name='+text+'></a>\n'    
        return text
    
    def tableHeadings(self):
        text = '<tr>\n'
        
        for next in self.columns():
            invisible = False
            background_white = False
            if next.CellStyle in ['funds']:
                align = 'right; '
            elif next.CellStyle in ['date']:
                align = 'right; '
                background_white = True
                background_white = False
            elif next.CellStyle in ['nowrapr', 'green']:
                align = 'right; '
            elif next.CellStyle in ['nowrapc']:
                align = 'center; '
            elif next.CellStyle in ['hide']:
                align = 'right; '
                invisible = True
            else:
                align = 'left; '

            text += (
                '   <th style="' +
                'font-size:' + next.fontsize+'em; ' +
                'text-align:' + align + 
                'white-space:nowrap;'
                )

            if background_white: text += (
                'background-color:white; ')

            if invisible: text += (
                'background-color:white; ' +
                'visibility:hidden; ')

            text += (
                '">' +
                next.heading +
                '</th>\n')

        text += '</tr>\n'
        return text
            
    def monthlyYearly(self):
        if 'Year' in self.fieldsDeterminingSubsection: return 'Year'
        if 'YearMonth' in self.fieldsDeterminingSubsection: return 'YearMonth'
        return ''
    
    def orderedHtmlColumns(self):
        fieldnames = [ cell.fieldname for cell in self.columns() ]
        return fieldnames
    
    def pleaseSortUnique(self):
        return False

    def hideRunningTotalColumn(self, cell):
        return cell.fieldname == 'RunningTotal' and cell.CellStyle == 'hide' 
    
    def determineBookmark(self, row):
        if len(self.fieldsDeterminingSection) == 0:
            section_name = ''
        else:
            section_name = ''
            first_time = True
            for next in self.fieldsDeterminingSection:
                if first_time:
                    first_time = False
                    section_name = row[next]
                else:
                    section_name = section_name + '-' + row[next]
        return String(section_name).removeBlanksAndSlashes()
            
    def determineFilename(self, html_filename, row):
        if len(self.fieldsDeterminingSection) == 0:
            section_name = ''
        else:
            section_name = ''
            for next in self.fieldsDeterminingSection:
                section_name = section_name + '-' + row[next]
        if self.splitSectionsIntoSeparateFiles():
            return String(
                re.sub('\.html', section_name+'.html', html_filename)).removeBlanks()
        else:
            return String(html_filename).removeBlanks()

    
    def fillTheFields(self, row, bkg_color, font_weight='normal'):
        lines = list()
        color = bkg_color
        lines.append('<tr style=background-color:' + color + '>')
        for cell in self.columns():
            #if not cell.fieldname in row.keys(): return lines
            contents_of_field = row[cell.fieldname]
            #if contents_of_field == 'null': return lines
            if self.hideRunningTotalColumn(cell):
                lines.append('  <td style=background-color:white>&nbsp;</td>')
            elif ( cell.CellStyle in ['green', 'funds'] ):
                amount_no_commas = getFloatNoCommas(contents_of_field)
                if   ( amount_no_commas > 0.0 ):           color = 'green'
                elif ( amount_no_commas < 0.0 ):           color = 'red'
                elif ( cell.fieldname == 'SectionDebit' ): color = 'green'
                else:                                      color = 'red'
                lines.append('  <td class=' + color + '>' + contents_of_field + '</td>')
            else:
                lines.append('  <td class=' + cell.CellStyle + '>' + contents_of_field + '</td>')
        lines.append('</tr>' )
        return lines
    
    
    def fillTheSummaryFields(self, row, bkg_color, font_weight='normal'):
        lines = list()
        color = bkg_color
        lines.append(
            '<tr style="font-weight:' + font_weight +
            ';background-color:' + color + ';">')
        for cell in self.columns():
            contents_of_field = row[cell.fieldname]
            if contents_of_field == 'null': return lines
            if self.hideRunningTotalColumn(cell):
                lines.append('  <td style=background-color:white>&nbsp;</td>')
            elif ( cell.CellStyle in ['green', 'funds'] ):
                amount_no_commas = getFloatNoCommas(contents_of_field)
                if   ( amount_no_commas > 0.0 ):           color = 'green'
                elif ( amount_no_commas < 0.0 ):           color = 'red'
                elif ( cell.fieldname == 'SectionDebit' ): color = 'green'
                else:                                      color = 'red'
                lines.append('  <td class=' + color + '>' + contents_of_field + '</td>')
            else:
                lines.append('  <td class=' + cell.CellStyle + '>' + contents_of_field + '</td>')
        lines.append('</tr>' )
        return lines

    def writeRowsOfTable(self, row, prev_row, html_filename):

        #########################################################
        # Determine if section or subsection has changed
        #########################################################
        self.monitor.slideFieldValues(row)
        self.section_has_changed = bool(
            self.monitor.fieldHasChanged(self.fieldsDeterminingSection))
        self.subsection_has_changed = bool(
            self.monitor.fieldHasChanged(self.fieldsDeterminingSubsection))

        #########################################################
        # if main section has changed
        #   write sub-totals for previous sub-section
        #   if splitting
        #       write html commands to end the table
        #       close file
        #       open new file with name based on main sort field
        #       write top html commands
        #   write headings for new section and new sub-section
        #   change the background color for the next sub-section
        #########################################################
        if self.section_has_changed:
            
            # what to do at the end of a subsection
            self.endSubsection(self.writer, self.monitor, False)
            
            # what to do at the end of a section
            self.endSection(self.writer, prev_row)
            
            if self.splitSectionsIntoSeparateFiles():
                self.endBodyAndHtml()
                self.closeTable()
                
                self.openTable(self.determineFilename(html_filename, row))
                self.beginHtml(row)
                self.defineStyles(row)
                self.beginBody(row)
                
            # what to do at the beginning of a section
            self.beginSection(self.writer, row)

            # what to do at the beginning of a subsection
            bookmark = String(self.determineBookmark(row)).removeBlanksAndSlashes()
            self.beginSubsection(self.writer, row, bookmark)
            
            # advance the color
            #self.background_color = self.getRowColor(row)

        #########################################################
        # Else if sub-section has changed
        #   write sub-totals for previous sub-section
        #   write headings for new sub-section
        #   change the background color for the next sub-section
        #########################################################
        elif self.subsection_has_changed:

            # what to do at the end of a subsection
            self.endSubsection(self.writer, self.monitor, False)

            # what to do at the beginning of the next subsection
            bookmark = String(self.determineBookmark(row)).removeBlanksAndSlashes()
            self.beginSubsection(self.writer, row, bookmark)
 
            # advance the color            
            #self.background_color = self.getRowColor(row)

        #########################################################
        # write the row (this may be under a new section or subsection)
        #########################################################
        self.insertOneRecord(row, self.background_color, 'normal')

        return None

    def createHtmlTables(self, csv_file, folder_out):
        
        # determine the folder and fullpath to the html file
        print "FOLDER_OUT",folder_out
        right0 = os.path.split(folder_out)[0]        # /working/python/db3/out/AccountDate
        right1 = os.path.split(right0)[0]            # /working/python/db3/out
        ordering_section = os.path.split(right1)[1]
        html_folder = right0 + '/' # '/html/'  
        html_fullpath = html_folder+ordering_section+'.html'
        touchFolder(html_folder)

        # loop over the csv file
        csv_file.openRead() 
        first_row = True
        for row in csv_file.reader:
            if first_row:
                first_row = False
                prev_row = row
                
                # initialize color of table cells
                self.background_color = self.getRowColor(row)
                
                # we must detect when section and subsection changes
                self.monitor = MonitorField()

                # top of the html file, begin section, begin subsection                
                self.openTable(self.determineFilename(html_fullpath, row))
                self.beginHtml(row)
                self.defineStyles(row)
                self.beginBody(row)
                
                # what to do when a new section begins
                self.beginSection(self.writer, row)
                
                # what to do when a new subsection begins
                bookmark = String(self.determineBookmark(row)).removeBlanksAndSlashes()
                self.beginSubsection(self.writer, row, bookmark)

            # write rows and sub-totals and begin new sections and subsections                
            self.writeRowsOfTable(row, prev_row, html_fullpath)
            prev_row = row
            pass
        
        # done writing html, end last subsection and last section
        if not first_row:
            
            # what to do at the end of a subsection
            self.endSubsection(self.writer, self.monitor, True)
            
            # what to do at the end of a section
            self.endSection(self.writer, prev_row)
            
            # finish the html file
            self.endBodyAndHtml()
            self.closeTable()
        csv_file.closeRead()
        print "HTML is at", html_fullpath
        print ""
   
             
    ####################################################################
    # helpers
    ####################################################################

    def writeln(self, line):
        self.writer.write( line+'\n' )
        return None
    
    def writeRowsOfColor(self, color, how_many, date_is_white=False):
        if self.summaryOnly(): return None
        for i in range(how_many):
            self.writeln( '<tr>' )
            for next in self.columns():
                if date_is_white and next.fieldname in ['Amount']:
                    self.writeln('  <td style="background-color:' +'white'+ '; border-style:none">&nbsp;</td>')
                else:
                    self.writeln('  <td style="background-color:' +color+ '; border-style:none">&nbsp;</td>')
            self.writeln('</tr>' )
            
    def writeRowsOfSummaryColor(self, color, how_many, date_is_white=False):
        for i in range(how_many):
            self.writeln( '<tr>' )
            for next in self.columns():
                if date_is_white and next.fieldname in ['Amount']:
                    self.writeln('  <td style="background-color:' +'white'+ '; border-style:none">&nbsp;</td>')
                else:
                    self.writeln('  <td style="background-color:' +color+ '; border-style:none">&nbsp;</td>')
            self.writeln('</tr>' )
            
    def insertOneRecord(self, row, bkg_color, font_weight):
        if self.summaryOnly(): return None
        lines = self.fillTheFields(row, bkg_color, font_weight)
        for line in lines: self.writeln(line)
        return None
            
    def insertOneSummaryRecord(self, row, bkg_color, font_weight):
        lines = self.fillTheSummaryFields(row, bkg_color, font_weight)
        for line in lines: self.writeln(line)
        return None
    
    ####################################################################
    # writeStartOfTable
    ####################################################################
    def htmlBegin(self): return (
        '<html>\n'
    )

    def headBegin(self): return (
        '<head>\n'
    )

    def stylesBegin(self): return (
        '<style type="text/css">\n'
    )
    
    def tableStyles(self):
        return(
                      self.tableOneByTwoStyle().applyStyle(          '',     'OneByTwo')
            +                 self.tableStyle().applyStyle(          '', self.tablename)
            +          self.tableHeadingStyle().applyStyle(        'th', self.tablename)
            +              self.tableRowStyle().applyStyle(        'tr', self.tablename)
            +             self.tableCellStyle().applyStyle(        'td', self.tablename)
            +         self.tableCellLeftStyle().applyStyle(   'td.left', self.tablename)
            +        self.tableCellRightStyle().applyStyle(  'td.right', self.tablename)
            +        self.tableCellGreenStyle().applyStyle(  'td.green', self.tablename)
            +        self.tableCellFundsStyle().applyStyle(  'td.funds', self.tablename)
            +   self.tableCellWhiteRightStyle().applyStyle( 'td.whiter', self.tablename)
            +    self.tableCellWhiteLeftStyle().applyStyle( 'td.whitel', self.tablename)
            +          self.tableCellRedStyle().applyStyle(    'td.red', self.tablename)
            +       self.tableCellCenterStyle().applyStyle( 'td.center', self.tablename)
            +   self.tableCellNowrapLeftStyle().applyStyle('td.nowrapl', self.tablename)
            +  self.tableCellNowrapRightStyle().applyStyle('td.nowrapr', self.tablename)
            + self.tableCellNowrapCenterStyle().applyStyle('td.nowrapc', self.tablename)
            + self.tableCellStandardDateStyle().applyStyle(   'td.date', self.tablename)
            +         self.tableCellHideStyle().applyStyle(   'td.hide', self.tablename)
        )
        
    def stylesEnd(self): return (
        '</style>\n'
    )
    
    def headEnd(self): return (
        '</head>\n'
    )
    
    def htmlEnd(self): return (
        '</html>\n'
    )

    def bodyBegin(self): return (
        '<body style="font-size:14px; line-height:14px; margin:10px 1px 30px 100px;">\n'
    )
    
    def tableBegin(self):
        text = '<table id="' +self.tablename+ '">\n'
        return text
    
    def tableEnd(self):
        text = '</table>\n'
        return text
    
    def tableWidths(self):
        text = ''
        for next in self.columns():
            text += '   <col width=' + str(next.width) + '%>\n'
        return text        
    
    def tableWidthsPx(self):
        text = ''
        for next in self.columns():
            text += '   <col width=' + str(next.width) + '>\n'
        return text        

    def openTable(self, html_filename):
        self.writer = open(html_filename, 'wb')
        return None

    def beginHtml(self, first_row):
        self.writer.write( self.htmlBegin() )
        self.writer.write( self.headBegin() )
        
    def defineStyles(self, first_row):
        self.writer.write( self.stylesBegin() )
        self.writer.write( self.tableStyles() )
        self.writer.write( self.stylesEnd() )
        
    def beginBody(self, first_row):
        self.writer.write( self.headEnd() )
        #self.writer.write( self.htmlEnd() )
        self.writer.write( self.bodyBegin() )

    ####################################################################
    # writeEndOfTable
    ####################################################################
    def endBodyAndHtml(self):
        self.writer.write('</body>')
        self.writer.write('</html>')

    def closeTable(self):
        self.writer.close()
    
    ####################################################################
    # These are all of the styles for the table
    ####################################################################
    def tableStyle(self): return Html.Style(Map({

        'font-family'     : 'Verdana, Geneva, sans-serif'       ,
        'border-collapse' : 'collapse'                          ,
        #'width'           : '100%'                              ,
        'width'           : '0%'                                ,
        'table-layout'    : 'auto'                              ,
        'font-size'       : '12px'                              ,
        'line-height'     : '12px'                              }))
        #'font-size'       : '14px'                              ,
        #'line-height'     : '14px'                              }))

    def tableOneByTwoStyle(self): return Html.Style(Map({

        'font-family'     : 'Verdana, Geneva, sans-serif'       ,
        'border-collapse' : 'collapse'                          ,
        'width'           : '100%'                              ,
        'table-layout'    : 'auto'                              ,
        'font-size'       : '14px'                              ,
        'line-height'     : '14px'                              }))

    def tableHeadingStyle(self): return Html.Style(Map({

                'font-size': '1.0em'           ,
               'text-align': 'left'            ,
                   'border': '1px solid black' ,
                   'border': '1px none #DCDCDC'  ,
                  'padding': '3px 10px 3px 10px' ,
         'background-color': '#DCDCDC'           ,
                    'color': 'black'           ,
               'font-style': 'italic'          }))

    def tableRowStyle(self): return Html.Style(Map({

                'font-size': '1.0em'  ,
              'font-weight': 'normal' ,
                    'color': 'black'  ,
         'background-color': 'white'  }))

    def tableCellStyle(self): return Html.Style(Map({

         'text-align': 'center'          ,
             'border': '1px none grey'   ,
            'padding': '3px 10px 3px 10px' }))

    def tableCellLeftStyle(self): return Html.Style(dict({
        'text-align': 'left' }))

    def tableCellRightStyle(self): return Html.Style(dict({
        'text-align': 'right' }))

    def tableCellGreenStyle(self): return Html.Style(dict({
        'background-color': 'white',
        'color': 'green',
        'text-align': 'right' }))

    def tableCellFundsStyle(self): return Html.Style(dict({
        'background-color': 'white',
        'color': 'green',
        'text-align': 'right' }))

    def tableCellWhiteRightStyle(self): return Html.Style(dict({
        'background-color': 'white',
        'color': 'black',
        'white-space': 'nowrap',
        'text-align': 'right' }))

    def tableCellWhiteLeftStyle(self): return Html.Style(dict({
        'background-color': 'white',
        'color': 'black',
        'white-space': 'nowrap',
        'text-align': 'left' }))

    def tableCellRedStyle(self): return Html.Style(dict({
        'background-color': 'white',
        'color': 'red',
        'text-align': 'right' }))

    def tableCellCenterStyle(self): return Html.Style(dict({
        'text-align': 'center' }))

    def tableCellNowrapLeftStyle(self): return Html.Style(dict({
        'text-align': 'left',
        'white-space': 'nowrap' }))

    def tableCellNowrapRightStyle(self): return Html.Style(dict({
        'text-align': 'right',
        'white-space': 'nowrap' }))

    def tableCellNowrapCenterStyle(self): return Html.Style(dict({
        'text-align': 'center',
        'white-space': 'nowrap' }))

    def tableCellStandardDateStyle(self): return Html.Style(dict({
        #'font-family': 'Verdana, Geneva, monospace',
        'font-family': "'Lucida Console', Monaco, monospace",
        'text-align': 'right',
        'white-space': 'nowrap' }))

    def tableCellHideStyle(self): return Html.Style(dict({
        'background-color': 'white',
              'visibility': 'hidden' }))
         
    ####################################################################
    # end styles
    ####################################################################
        
