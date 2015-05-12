'''
    class HtmlTable
'''

import sys, os, re, collections, exceptions
from utils.CsvObject import *
from utils.Container import *
from utils import Html
import time
from datetime import datetime, tzinfo
from Database import Database
from classes.pdf.Pdf import Pdf


########################################################################
# HtmlTable
########################################################################
class HtmlTable(Database):

    def __init__(self, accumulate, tablename, heading_account, is_last_table, website, camperid, day, dest, page, year, refresh):
        Database.__init__(self, website, camperid, day, dest, page, year, refresh)
        self.rows_only = False
        self.accumulate = accumulate
        csv_object_in = self.accumulate.csv_object        
        self.folder_out = csv_object_in.foldername
        self.toc_folder = os.path.dirname(os.path.dirname(self.folder_out)) + '/'

        self.tablename = tablename
        self.colors = Colors()
        self.html_table = self.presentationMainTable()
        self.heading_account = heading_account
        self.is_last_table = is_last_table

        csv_object_special = self.recordsSpecialFields(csv_object_in)
        self.createHtmlTables(csv_object_special, csv_object_special.foldername)
        if self.is_last_table:
            self.closeMainTableOfContents()
                        
        # now create the PDF
        if False:
            # folder_2014   is "/meds/out/2014"
            # report_type   is "Master-Schedule"

            folder_2014 = os.path.dirname(os.path.dirname(csv_object_special.foldername))
            report_type = os.path.basename(os.path.dirname(csv_object_special.foldername))

            pdf = Pdf()
            pdf.createPdfFile(
                folder_2014,
                report_type,
                self.orientationLandscape(),
                self.tocHeading(),
                self.isHeroku(),
                camperid, day, page
            )

        return None
        
        # now create the PDF
        path_to_input_csv = (
            csv_object_special.foldername + '../../../in/Med_Schedule_Items.csv')
        epochtime = os.path.getmtime(path_to_input_csv)
        struct_time = time.localtime(epochtime)
        
        datetime_of_database = datetime.fromtimestamp(epochtime)
        warning = (
            '"The instructions on this page are based upon the medication database dated ' +
            datetime_of_database.strftime("%A %B %d, %Y")+
            #str(struct_time.tm_mon) + '/' + str(struct_time.tm_mday) + '/' + str(struct_time.tm_year) + 
            '"'
        )

        printall_file = csv_object_special.foldername + 'PRINTALL.pdf'
        html_folder = csv_object_special.foldername + 'html'
        if self.orientationLandscape(): orientation = " --orientation Landscape "
        else:                           orientation = " --orientation Portrait "
        
        options = (
            orientation +
            '--page-size Letter --margin-bottom 0mm --quiet'+' '+
            ''
        )
        
        footer = (
            ' '+    
            '--footer-font-name Arial'  +' '+
            '--footer-font-size 10'     +' '+
            '--footer-center ' + warning  +' '+
            '--footer-line'             +' '+
            '--footer-spacing 0'        +' '+
            ''
        )
        
        toc = (
            ' toc --enable-toc-back-links --toc-level-indentation 1em ' +
            '--toc-header-text "' + self.tocHeading() + '" ' + 
            ''
        )
   
        toc1 = (
            ' --toc  --toc-l1-indentation 1 '
            '--toc-header-text "' + self.tocHeading() + '" ' + 
            ''
        )
        
        if self.isHeroku():
            wkhtmltopdf = "/app/vendor/bundle/ruby/1.9.1/gems/wkhtmltopdf-heroku-1.0.0/bin/wkhtmltopdf-linux-amd64"
            command = wkhtmltopdf + options + toc + html_folder + "/*.html " + printall_file 
        else:
            wkhtmltopdf = "/usr/bin/wkhtmltopdf11.prev"
            command = wkhtmltopdf + options + toc + html_folder + "/*.html " + printall_file
        if self.isLocal():
            retvalue = os.system(command)
            print "Return status from wkhtmltopdf is:", retvalue
        
        return None
    
    #wkhtmltopdf --enable-toc-back-links --footer-center [page] toc --xsl-style-sheet toc.xsl book.html book.pdf    
    #      + ' --disable-toc-back-links '
    #h1.hidden {visibility:hidden;}
    #h1.hidden {display:none;}
    
    def recordsSpecialFields(self, rows_accumulated):
        rows_in = rows_accumulated
        rows_out = CsvObject(self.folder_out+'SpecialFields.csv', rows_accumulated.fieldnames)
        
        rows_in.openRead(); rows_out.openWrite()
        for row in rows_in.reader:
            special = self.determineSpecialFields(row)
            rows_out.writer.writerow([special[x] for x in rows_out.fieldnames])
        rows_in.closeRead(); rows_out.closeWrite()
        return rows_out

    def title(self):
        return self.accumulate.title()

    def fieldsDeterminingSection(self):
        return self.accumulate.fieldsDeterminingSection()
    
    def fieldsDeterminingSubsection(self):
        return self.accumulate.fieldsDeterminingSubsection()

    def writeLine(self, line):
        self.writer.write( line+'\n' )
        return None
   
    def writeLines(self, lines):
        for line in lines: self.writeLine( line )
        
    def topOfFileAndCommonStyles(self, row):
        self.openTable(self.determineFilename(self.html_fullpath, row))
        self.beginHtml(row)
        self.writeLine( self.stylesBegin() )
        self.writeLine( self.html_table.tableStyles() )
        self.writeLine( self.stylesEnd() )
        self.beginBody(row)
        self.openTableOfContents()
        self.tableOfContents(row, self.count_pages)

    def itemsPrecedingSection(self, row, count_pages, camper_has_changed):
        self.betweenSectionsAndSubsections().beginSection(self.writer, row, self, count_pages, camper_has_changed)

    def itemsPrecedingSubsection(self, row):
        bookmark = String(self.determineBookmark(row)).removeBlanksAndSlashes()
        if not self.rows_only:
            self.betweenSectionsAndSubsections().beginSubsection(self.writer, row, bookmark, self)
        self.writeLine( self.html_table.standardTableBegin(bookmark) )
        
    def itemsFollowingSection(self, row):
        self.writeLine(self.html_table.tableEnd())
        self.betweenSectionsAndSubsections().endSection(self.writer, row, self)
        if False: self.writeLine(
        '<a style="margin-left:10px;font-size:14;" HREF="/top/remotePrint">Print this page at the remote Special Camp printer</a>'
        )
        
    def itemsFollowingSubsection(self, row):
        if self.rows_only: return None
        self.betweenSectionsAndSubsections().endSubsection(self.writer, self.monitor, False, self)
        
    def endingFile(self, row):
        self.endBodyAndHtml()
        self.closeTable()

    def tocHeading(self):
        return 'HEADING'
    
    def beginTOC(self):  return ((     
'''
<html>
<body>
<hr>
<p style="
    font-family:Verdana, Geneva, sans-serif;
    text-align:left;
    color:green;
    font-weight:bold;
    font-size:16px;
    margin-left:20px;
    line-height:20px;
    text-decoration:underline;
">
''')
    + self.tocHeading() + (
'''
<br/>
</p>
'''))
    
    '''    
    <p style="
        font-family:Verdana, Geneva, sans-serif;
        text-align:left;
        color:green;
        font-weight:bold;
        font-size:14px;
        margin-left:60px;
        line-height:20px;
    ">
    '''
    
    def beginTOP1(self):
        #relative_html = os.path.dirname(os.path.dirname(re.sub(self.toc_folder,'',self.writer.name)))
        #reference = (
        #    '<a HREF="' + relative_html + "/TOC.html"
        #    '">' + self.tocHeading() + '</a>\n')

        return ((     
'''
<html>
<head>
<style type="text/css">
p.heading
{
    font-family:Verdana, Geneva, sans-serif;
    text-align:left;
    color:green;
    font-weight:bold;
    font-size:16px;
    margin-left:30px;
    line-height:20px; 
    text-decoration:underline;  
}
</style>
</head>
<body>
<br>
<p class=heading>SPECIAL CAMP
''')
+ YEAR_OF_CAMP + '</p>\n')
    
    def beginTOP2(self):
        relative_html = os.path.dirname(os.path.dirname(re.sub(self.toc_folder,'',self.writer.name)))
        remove_dashes = re.sub('-','', relative_html)
                
        #argument_which = '/top/getcsv'+remove_dashes+'?which='
        argument_which = '/top/createHtmlPages?which='
        if self.isLocal():
            filename_html = relative_html + '/TOC.html'
        elif self.isHeroku() or self.isRails():
            filename_html = argument_which + relative_html

        reference_html = (
            '<a style="margin-left:10px;font-size:14;font-weight:normal;font-style:italic;" HREF="' 
            + filename_html + '">' + 'SELECT' + '</a>\n' )
        
        argument_which = '/top/print'+remove_dashes+'?which='
        if self.isLocal():
            filename_pdf = relative_html + '/PRINTALL.pdf'
        elif self.isHeroku() or self.isRails():
            filename_pdf = argument_which + relative_html
        reference_pdf = (
            '<a style="margin-left:10px;font-size:14;font-weight:normal;font-style:italic;" HREF="' 
            + filename_pdf + '">' + 'PRINT' + '</a>\n' )
        
        blanks = '&nbsp;&nbsp;'
        
        return (
            '<p class=heading style="margin-left:30px;color:black;text-decoration:none;">' 
            #+ reference_html + reference_pdf + blanks + self.tocHeading() + '</p>\n\n'
            + reference_html + blanks + self.tocHeading() + '</p>\n\n'
        )
    

    def endTOC(self):  return ( 
'''    
<hr>
</body>
</html>
''')
    
    def endTOP(self):  return ( 
'''    
</body>
</html>
''')


    def endTOP1(self):  return ( 
'''
''')

    def ref(self, fullpath, text): return (
        '&nbsp;&nbsp;&nbsp;&nbsp;' 
        + Html.tagHref(fullpath, text))
        
    def refBreak(self, fullpath, text1, text2):
        return (        
            '<br>'+text1+
            '&nbsp;&nbsp;&nbsp;&nbsp;'
            + Html.tagHref(fullpath, text2))


    def shiftDay(self):
        if self.day_of_week == "Sun": self.day_of_week = "Mon"
        elif self.day_of_week == "Mon": self.day_of_week = "Tue"
        elif self.day_of_week == "Tue": self.day_of_week = "Wed"
        elif self.day_of_week == "Wed": self.day_of_week = "Thu"
        elif self.day_of_week == "Thu": self.day_of_week = "Fri"
        elif self.day_of_week == "Fri": self.day_of_week = "Sat"
        elif self.day_of_week == "Sat": self.day_of_week = "As Needed"
        elif self.day_of_week == "As Needed": self.day_of_week = "Sun"
    
    
    def tableOfContents(self, row, count_pages):

        self.relative_html = 'html/'+os.path.basename(self.writer.name)
        
        if True:
            report_name = os.path.basename(os.path.dirname(os.path.dirname(self.writer.name)))
            html_filename = os.path.basename(self.writer.name)   
            self.relative_html1 = '/top/printLocalOnePage?report_name='+report_name+';html_filename='+html_filename
            self.relative_html2 = '/top/printRemoteOnePage?report_name='+report_name+';html_filename='+html_filename
            self.view_tag = '<!--VIEW-->'
            self.local_tag = '<!--LOCAL-->'
            self.remote_tag = '<!--REMOTE-->'
        
        show = os.path.basename(self.writer.name)
        show = re.sub('-1-','-',show)
        show = re.sub('-2-','-',show)
        show = re.sub('-3-','-',show)
        show = re.sub('-4-','-',show)
        show = re.sub('-5-','-',show)
        show = re.sub('-6-','-',show)
        show = re.sub('-7-','-',show)
        show = re.sub('-8-','-',show)
        show = re.sub('.html','-',show)
        show = re.sub('-',' ',show)
        page = 'Page '+str(count_pages)
        
            
        if (set(['day_pages']) == self.tocShow()
        or  set(['camper_pages']) == self.tocShow()):
            if set(['day_pages']) == self.tocShow():
                field = row['day']
                first_width = 120
                if field == 'as needed': field = 'As Needed'
            if set(['camper_pages']) == self.tocShow():
                field = row['camper']
                first_width = 200
            if count_pages <= 1:
                if not self.first_time:
                    table_html = Html.Table().manyCellsEnd()
                    self.TOC.write(table_html)                
                table_html = Html.Table().manyCellsBegin(
                    item.tableCommonStyle1(50).style(),
                    item.rowCommonStyle1().style(),
                    80, first_width, 80, 6)
                self.TOC.write(table_html)
                table_html = Html.Table().manyCellsNext(
                    item.cellBlackLeft().style(),
                    field)
                self.TOC.write(table_html)
            table_html = Html.Table().manyCellsNext(
                item.cellBlackLeft().style(),
                Html.tagHref(self.relative_html,  page) + self.view_tag + '\n' +
                Html.tagHref(self.relative_html1, page) + self.local_tag+ '\n' +
                Html.tagHref(self.relative_html2, page) + self.remote_tag)
                 
            self.TOC.write(table_html)
            
        # each row is camper day page1 page2 ...
        elif ( set(['camper_day_pages']) == self.tocShow() ):
            if not hasattr(self, 'prev_camper'): self.prev_camper = ''
            camper = row['camper']
            if self.prev_camper != camper:
                self.camper_has_changed = True
            else:
                self.camper_has_changed = False                 
            self.prev_camper = camper

            if set(['camper_day_pages']) == self.tocShow():
                field = row['camper'] + " " + row['day']
                first_width = 180
                second_width = 120

            if count_pages <= 1:
                
                # write the end of the table of single row
                if not self.first_time:
                    table_html = Html.Table().manyCellsEnd()
                    self.TOC.write(table_html)  
                    if self.camper_has_changed:                 
                        self.TOC.write('<br />')  
                    
                # begin a new table of single row              
                table_html = Html.Table().manyCellsBegin(
                    item.tableCommonStyle1(50).style(), # table style
                    item.rowCommonStyle1().style(),     # row style
                    80,                                 # width of subsequent
                    first_width,                        # width of 1st column
                    second_width,                       # width of 2nd column
                    7)                                  # max number of columns after first
                self.TOC.write(table_html)
                
                if not self.camper_has_changed:
                    
                    # write the first column of table
                    table_html = Html.Table().manyCellsNext(
                        item.cellBlackLeft().style(),       # style of 1st cell
                        '&nbsp;')                           # contents of 1st cell
                    self.TOC.write(table_html)
                    
                else:
                    
                    # write the first column of table
                    table_html = Html.Table().manyCellsNext(
                        item.cellBlackLeft().style(),       # style of 1st cell
                        camper)                             # contents of 1st cell
                    self.TOC.write(table_html)
                
                # write the second column of table
                table_html = Html.Table().manyCellsNext(
                    item.cellGrayLeft().style(),            # style of 2nd cell
                    row['day'])                             # contents of 2nd cell
                self.TOC.write(table_html)
                
            # write one column subsequent to the first                
            table_html = Html.Table().manyCellsNext(
                item.cellBlackLeft().style(),
                Html.tagHref(self.relative_html,  page) + self.view_tag + '\n' +
                Html.tagHref(self.relative_html1, page) + self.local_tag+ '\n' +
                Html.tagHref(self.relative_html2, page) + self.remote_tag)
            self.TOC.write(table_html)
            
        elif (set(['camper_only']) == self.tocShow()):
            #print self.writer.name
            field = row['camper']
            first_width = 170
            if count_pages <= 1:
                if not self.first_time:
                    table_html = Html.Table().manyCellsEnd()
                    self.TOC.write(table_html)                
                table_html = Html.Table().manyCellsBegin(
                    item.tableCommonStyle1(50).style(),
                    item.rowCommonStyle1().style(),
                    100, first_width, 100, 6)
                self.TOC.write(table_html)
                #table_html = Html.Table().manyCellsNext(
                #    item.cellBlackLeft().style(),
                #    field)
                #self.TOC.write(table_html)
            table_html = Html.Table().manyCellsNext(
                item.cellBlackLeft().style(),
                Html.tagHref(self.relative_html,  page) + self.view_tag + '\n' +
                Html.tagHref(self.relative_html1, page) + self.local_tag+ '\n' +
                Html.tagHref(self.relative_html2, page) + self.remote_tag)
            self.TOC.write(table_html)
        
        elif (set(['camper_days']) == self.tocShow()):
            if not hasattr(self, 'prev_camper'): self.prev_camper = ''
            camper = row['camper']
            first_width = 170
            day = row['day'][0:3]
            if day == 'as ':
                day = 'As Needed'
            
            if self.prev_camper != camper: 
                self.day_of_week = "Sun"      
                if not self.first_time:
                    table_html = Html.Table().manyCellsEnd() # end the table tr table
                    self.TOC.write(table_html)                
                table_html = Html.Table().manyCellsBegin(
                    item.tableCommonStyle1(50).style(),
                    item.rowCommonStyle1().style(),
                    60, first_width, 60, 8)
                self.TOC.write(table_html)
                table_html = Html.Table().manyCellsNext(
                    item.cellBlackLeft().style(),
                    camper)
                self.TOC.write(table_html)
            while False and self.day_of_week != day:
                table_html = Html.Table().manyCellsNext(
                    item.cellBlackLeft().style(),
                    '&nbsp;')
                self.TOC.write(table_html)
                self.shiftDay()
            table_html = Html.Table().manyCellsNext(
                item.cellBlackLeft().style(),
                Html.tagHref(self.relative_html,  page) + self.view_tag + '\n' +
                Html.tagHref(self.relative_html1, page) + self.local_tag+ '\n' +
                Html.tagHref(self.relative_html2, page) + self.remote_tag)
            self.TOC.write(table_html)
            self.shiftDay()
            self.prev_camper = camper
        

        '''        
        elif (set(['day']) == self.tocShow()
        or set(['camper']) == self.tocShow()):
            for next in self.tocShow(): show = row[next]
            if count_pages > 1:
                show = page
            reference = self.ref(self.writer.name, show)
            reference_break = self.refBreak(self.writer.name, show, page)
            if count_pages == 1:       
                self.TOC.write(reference_break)
            else:
                self.TOC.write(reference)
            return None
            
        elif ( set(['camper']) == self.tocShow() ):
            show = row['camper']
            if count_pages > 1:
                show = show
            reference = self.ref(self.writer.name, show)
            reference_break = self.refBreak(self.writer.name, '', show)
            if count_pages == 1:       
                self.TOC.write(reference_break)
            else:
                self.TOC.write(reference)
            return None
            
        elif set(['camper', 'day']) == self.tocShow():
            if not hasattr(self, 'prev_camper'): self.prev_camper = ''

            camper = row['camper']
            day = row['day']
            reference = self.ref(self.writer.name, day)
            reference_break = self.refBreak(self.writer.name, camper, day)
            if self.prev_camper != camper:       
                self.TOC.write(reference_break)
            else:
                self.TOC.write(reference)
                
            self.prev_camper = camper
            return None  
        ''' 
        
        self.first_time = False
        return None      

    def openTableOfContents(self):
        each_report = self.folder_out + 'TOC.html'
        self.main_toc_filename = self.toc_folder + '/TOC.html'

        if not os.access(each_report, os.F_OK):
            self.TOC = open(each_report, 'wb')
            self.first_time = True
            self.TOC.write(self.beginTOC())
            if not os.access(self.main_toc_filename, os.F_OK):
                self.TOP = open(self.main_toc_filename, 'wb')
                self.TOP.write(self.beginTOP1())
                self.TOP.write(self.beginTOP2())
            else:
                self.TOP = open(self.main_toc_filename, 'ab')
                self.TOP.write(self.beginTOP2())

    def practiceManyCells(self):
        
        table_html = Html.Table().threeCells(
            item.tableCommonStyle().style(),
            item.rowCommonStyle().style(),
            item.cellBlackLeft().style(),
            item.cellBlackLeft().style(),
            item.cellBlackLeft().style(),
            'Nary',
            'Rayna',
            'Levi',
            '400', '300', '538') #985 --> 1238
        self.TOC.write(table_html)

        table_html = Html.Table().manyCellsBegin(
            item.tableCommonStyle1(200).style(),
            item.rowCommonStyle().style(),
            50)
        self.TOC.write(table_html)
   
        table_html = Html.Table().manyCellsNext(
            item.cellBlackLeft().style(),
            'Nary')
        self.TOC.write(table_html)
   
        table_html = Html.Table().manyCellsNext(
            item.cellBlackLeft().style(),
            'Rayna')
        self.TOC.write(table_html)        
      
        table_html = Html.Table().manyCellsEnd()
        self.TOC.write(table_html)                
        
        self.TOC.write('</body></html>')
        
    def closeTableOfContents(self):
        table_html = Html.Table().manyCellsEnd()
        self.TOC.write(table_html)                
        self.TOC.write(self.endTOC())
        self.TOC.close()
        self.TOP.close()
        #print self.TOC.name
        toc_local_fullpath = String(self.TOC.name).sub('TOC.html', 'TOC1.html')
        toc_remote_fullpath = String(self.TOC.name).sub('TOC.html', 'TOC2.html')
        toc_tmp_fullpath = String(self.TOC.name).sub('TOC.html', 'TOCtmp.html')
        #print toc_local_fullpath
        #print toc_remote_fullpath
        
        os.system('grep -v ' + "'" + self.view_tag   + "' " + self.TOC.name    + ' > ' + toc_tmp_fullpath)
        os.system('grep -v ' + "'" + self.remote_tag + "' " + toc_tmp_fullpath + ' > ' + toc_local_fullpath)
        os.system('grep -v ' + "'" + self.local_tag  + "' " + toc_tmp_fullpath + ' > ' + toc_remote_fullpath)
        
        os.system('grep -v ' + "'" + self.remote_tag + "' " + self.TOC.name    + ' > ' + toc_tmp_fullpath)
        os.system('grep -v ' + "'" + self.local_tag  + "' " + toc_tmp_fullpath + ' > ' + self.TOC.name)
        
        os.system('rm ' + toc_tmp_fullpath)
        #os.system('ls -l ' + os.path.dirname(self.TOC.name) + '/*.html')
        return None

    def closeMainTableOfContents(self):
        self.TOP = open(self.main_toc_filename, 'ab')
        self.TOP.write(self.endTOP())
        self.TOP.close()

    def writeOneRowOfMainTable(self, row):
        self.count_main_writes += 1
        self.writeLines(self.html_table.insertOneRecord(row, self.background_color))
      
    def processRow(self, row, row_new,
        this_is_first_row_of_csv_file, # True
        this_is_last_row_of_csv_file,
        this_is_last_row_of_section, # True
        this_is_last_row_of_subsection,
        this_is_last_row_of_page,
        camper_has_changed):
        
        # FIX THIS            
        if this_is_first_row_of_csv_file and this_is_last_row_of_section:
            self.background_color = self.getRowColor(row)
            self.topOfFileAndCommonStyles(row)
            self.itemsPrecedingSection(row, self.count_pages, camper_has_changed)
            self.itemsPrecedingSubsection(row)
            self.writeOneRowOfMainTable(row)

            if self.betweenSectionsAndSubsections().splitSectionsIntoSeparateFiles():
                #self.writeOneRowOfMainTable(row)
                self.itemsFollowingSubsection(row)
                self.itemsFollowingSection(row)
                self.endingFile(row)
                
                self.topOfFileAndCommonStyles(row_new)
                self.itemsPrecedingSection(row_new, self.count_pages, camper_has_changed)
                self.itemsPrecedingSubsection(row_new)
            else:
                self.writeOneRowOfMainTable(row)
                self.itemsFollowingSubsection(row)
                self.itemsFollowingSection(row)
                
                self.itemsPrecedingSection(row_new, self.count_pages, camper_has_changed)
                self.itemsPrecedingSubsection(row_new)
            self.background_color = self.getRowColor(row_new)
            

        # FIX THIS            
        elif this_is_first_row_of_csv_file and this_is_last_row_of_subsection:
            self.background_color = self.getRowColor(row)
            self.topOfFileAndCommonStyles(row)
            self.itemsPrecedingSection(row, self.count_pages, camper_has_changed)
            self.itemsPrecedingSubsection(row)
            self.writeOneRowOfMainTable(row)
            
            #self.writeOneRowOfMainTable(row)
            self.itemsFollowingSubsection(row)
            if this_is_last_row_of_page:
                if self.betweenSectionsAndSubsections().splitSectionsIntoSeparateFiles():
                    self.writeLine(self.html_table.tableEnd())
                    #self.writeOneRowOfMainTable(row)
                    #self.itemsFollowingSubsection(row)
                    #self.itemsFollowingSection(row)
                    self.endingFile(row)
                    self.topOfFileAndCommonStyles(row_new)
                    self.itemsPrecedingSection(row_new, self.count_pages, camper_has_changed)
                    self.itemsPrecedingSubsection(row_new)
            
            if self.betweenSectionsAndSubsections().repeatHeadings():
                self.writeLine( self.html_table.tableHeadings() )
            self.background_color = self.getRowColor(row_new)
            
            
        elif this_is_first_row_of_csv_file:
            if False: print "First Row"
            self.background_color = self.getRowColor(row)
            self.topOfFileAndCommonStyles(row)
            self.itemsPrecedingSection(row, self.count_pages, camper_has_changed)
            self.itemsPrecedingSubsection(row)
            self.writeOneRowOfMainTable(row)
            pass
            
        elif this_is_last_row_of_csv_file:
            if False: print "Last Row"
            self.writeOneRowOfMainTable(row)
            self.itemsFollowingSubsection(row)
            self.itemsFollowingSection(row)
            self.endingFile(row)
            pass
                        
        elif this_is_last_row_of_section:
            if False: print "Section has changed"
            if self.betweenSectionsAndSubsections().splitSectionsIntoSeparateFiles():
                self.writeOneRowOfMainTable(row)
                self.itemsFollowingSubsection(row)
                self.itemsFollowingSection(row)
                self.endingFile(row)
                
                self.topOfFileAndCommonStyles(row_new)
                self.itemsPrecedingSection(row_new, self.count_pages, camper_has_changed)
                self.itemsPrecedingSubsection(row_new)
            else:
                self.writeOneRowOfMainTable(row)
                self.itemsFollowingSubsection(row)
                self.itemsFollowingSection(row)
                
                self.itemsPrecedingSection(row_new, self.count_pages, camper_has_changed)
                self.itemsPrecedingSubsection(row_new)
            self.background_color = self.getRowColor(row_new)
            pass

        elif this_is_last_row_of_subsection:
            if False: print "Subsection has changed"
            self.writeOneRowOfMainTable(row)
            self.itemsFollowingSubsection(row)
            if this_is_last_row_of_page:
                if self.betweenSectionsAndSubsections().splitSectionsIntoSeparateFiles():
                    self.writeLine(self.html_table.tableEnd())
                    #self.writeOneRowOfMainTable(row)
                    #self.itemsFollowingSubsection(row)
                    #self.itemsFollowingSection(row)
                    self.endingFile(row)
                    self.topOfFileAndCommonStyles(row_new)
                    self.itemsPrecedingSection(row_new, self.count_pages, False)
                    self.itemsPrecedingSubsection(row_new)
            
            if self.betweenSectionsAndSubsections().repeatHeadings():
                self.writeLine( self.html_table.tableHeadings() )
            self.background_color = self.getRowColor(row_new)

        elif this_is_last_row_of_page:
            if self.betweenSectionsAndSubsections().splitSectionsIntoSeparateFiles():
                self.writeOneRowOfMainTable(row)
                self.writeLine(self.html_table.tableEnd())
                #self.itemsFollowingSubsection(row)
                #self.itemsFollowingSection(row)
                self.endingFile(row)
                self.topOfFileAndCommonStyles(row_new)
                self.itemsPrecedingSection(row_new, self.count_pages, False)
                self.itemsPrecedingSubsection(row_new)
        else:
            self.writeOneRowOfMainTable(row)
        return None

    def pleasePageEject(self,
        prev_is_first_row_of_csv_file, #True
        row_prev,
        row_new,
        prev_is_last_row_of_section,  #True
        prev_is_last_row_of_subsection): #True

        DEBUG = False
        
        font_size = 10
        vertical_padding = 5
        fudge = 0
        if self.noBlankRows():
            size_blank_row = 0
        else:
            size_blank_row = (
                vertical_padding + font_size + vertical_padding + fudge)
        max_height = 700-60+40

        # this is the beginning of the first page        
        if prev_is_first_row_of_csv_file:
            please_page_eject = False
            self.height_of_table = 0
            if 'running_height' in row_new.keys():
                self.height_of_table = int(row_prev['row_height'])
            self.count_pages = 1
        
        # this is the beginning of a new section (camper) thus page reset to 1
        elif prev_is_last_row_of_section:
            please_page_eject = False
            self.height_of_table = 0
            self.count_pages = self.last_page = 1

        #  this is the beginning of a subsection (hour) so check for eject           
        elif prev_is_last_row_of_subsection:
            please_page_eject = False
            if 'running_height' in row_new.keys():

                # size of the rows of the next section plus blank lines                
                size_of_next = int(row_new['running_height'])
                size_of_next += size_blank_row
                size_of_next += size_blank_row
                
                # add size of the last row of this subsection plus blank lines
                self.height_of_table += int(row_prev['row_height'])
                self.height_of_table += size_blank_row
                self.height_of_table += size_blank_row
 
                # height if add the next subsection               
                total = (self.height_of_table + size_of_next)
                
                # if adding next subsection exceeds max, then page eject
                if DEBUG:
                    print row_prev['day'], row_prev['time'], "end of section height", self.height_of_table, "plus next subsection",
                    print size_of_next, "is", total, "check", max_height
                if total > max_height:
                    if DEBUG:
                        print "PAGE EJECT END OF SUBSECTION, new page is", self.count_pages+1
                    please_page_eject = True
                    self.count_pages += 1
                    self.height_of_table = 0
        else:
            # in the middle of a subsection
            please_page_eject = False
            if 'running_height' in row_new.keys():
                self.height_of_table += int(row_prev['row_height'])
                if DEBUG:
                    print row_prev['day'], row_prev['time'], "middle of section height", self.height_of_table, "check", max_height
                if self.height_of_table > max_height:
                    if DEBUG:
                        print "PAGE EJECT IN MIDDLE, new page is", self.count_pages+1
                    please_page_eject = True
                    self.count_pages += 1
                    self.height_of_table = 0
        #print "PRINTING PAGE NUMBER", self.count_pages     
        return please_page_eject 
        return prev_is_last_row_of_subsection and not prev_is_last_row_of_section 


    def createHtmlTables(self, csv_file, folder_out):
        html_folder = folder_out + 'html/'
        #print "       HTML files:", html_folder
        self.html_fullpath = html_folder+self.title()+'.html'
        self.html_fullpath = html_folder+'.html'
        touchFolder(html_folder)
        
        self.monitor = MonitorField()
                
        csv_file.openRead() 
        count_rows = 0
        this_is_first_row_of_csv_file = True
        prev_is_first_row_of_csv_file = False
        self.count_main_writes = 0
        for row_new in csv_file.reader:
            
            # is this row last in section or last of subsection?
            self.monitor.slideFieldValues(row_new)
            prev_is_last_row_of_section = bool(
                self.monitor.fieldHasChanged(self.fieldsDeterminingSection()))
            prev_is_last_row_of_subsection = bool(
                self.monitor.fieldHasChanged(self.fieldsDeterminingSubsection()))
            
            # slide the rows and process previous row                    
            if this_is_first_row_of_csv_file:
                row_prev = row_new
                this_is_first_row_of_csv_file = False
                prev_is_first_row_of_csv_file = True        
            else:
                
                # determine if time to change the page
                please_page_eject = self.pleasePageEject(
                    prev_is_first_row_of_csv_file,
                    row_prev,
                    row_new,
                    prev_is_last_row_of_section, 
                    prev_is_last_row_of_subsection)
                
                # process the previous row
                self.processRow(row_prev, row_new, prev_is_first_row_of_csv_file, False, 
                    prev_is_last_row_of_section, 
                    prev_is_last_row_of_subsection, 
                    please_page_eject,
                    not row_prev['camper'] == row_new['camper'] or prev_is_first_row_of_csv_file)

                row_prev = row_new
                count_rows += 1
                prev_is_first_row_of_csv_file = False        
            pass

        try:
            self.processRow(row_prev, row_prev, count_rows == 0, True, False, False, False, False)
        except UnboundLocalError:
            print "EXCEPTION EMPTY FILE:",csv_file.filename
            
        count_rows += 1
        csv_file.closeRead()
        if False: print "CSV files at", os.path.dirname(csv_file.filename)
        #print "Number Rows Written:", self.count_main_writes

        try:        
            self.closeTableOfContents()
        except AttributeError:
            print"EXCEPTION EMPTY FILE:",csv_file.filename

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
    
        
    def stylesEnd(self): return (
        '</style>\n'
    )
    
    def headEnd(self): return (
        '</head>\n'
    )
    
    def htmlEnd(self): return (
        '</html>\n'
    )

    def bodyBegin(self):
        return (
            '<body>' 
            #'<h1>Nary Rayna Levi</h1>\n'
            #'<h1 style="visibility:hidden;display:none;">Nary Rayna Levi</h1>\n'
        )
        return '<body style="font-size:14px; line-height:14px;">\n'
    
    def openTable(self, html_filename):
        self.writer = open(html_filename, 'wb')
        return None

    def beginHtml(self, first_row):
        self.writeLine( self.htmlBegin() )
        self.writeLine( self.headBegin() )
        
    def defineStyles(self, first_row):
        self.writeLine( self.stylesBegin() )
        self.writeLine( self.html_table.tableStyles() )
        self.writeLine( self.stylesEnd() )
        
    def beginBody(self, first_row):
        self.writeLine( self.headEnd() )
        #self.writeLine( self.htmlEnd() )
        self.writeLine( self.bodyBegin() )
        
               

    ####################################################################
    # writeEndOfTable
    ####################################################################
    def endBodyAndHtml(self):
        if True: self.writeLine(
            '<div style="width:1200px;text-align:right;font-size:8;color:black;">'
            + self.refresh + '</div>')
        self.writeLine('</body>')
        self.writeLine('</html>')

    def closeTable(self):
        self.writer.close()
    
    def determineBookmark(self, row):
        if self.fieldsDeterminingSection()[0] == '':
            section_name = ''
        else:
            section_name = ''
            first_time = True
            for next in self.fieldsDeterminingSection():
                if first_time:
                    first_time = False
                    section_name = row[next]
                else:
                    section_name = section_name + '-' + row[next]
        return String(section_name).removeBlanksAndSlashes()

            
    def determineFilename(self, html_filename, row):
        if self.fieldsDeterminingSection()[0] == '':
            section_name = ''
        else:
            section_name = ''
            for next in self.fieldsDeterminingSection():
                if section_name == '':
                    if next == 'camper':
                        section_name = row[next]+"-"+row['camper-ID']
                    else:
                        section_name = row[next]
                else:
                    section_name = section_name + '-' + row[next]
        if self.betweenSectionsAndSubsections().splitSectionsIntoSeparateFiles():
            #return String(section_name+'-Page-'+str(self.count_pages)+'.html').removeBlanks()
            return String(
                re.sub('\.html', section_name+'-pg-'+str(self.count_pages)+'.html', html_filename)).removeBlanks()
        else:
            return String(html_filename).removeBlanks()

    def writeRowsOfColor(self, color, how_many):
        for i in range(how_many):
            self.writeLine( '<tr style="background-color:' +color+ '; border-style:none">' )
            for i in range(len(self.html_table.columns())): self.writeLine('  <td>&nbsp;</td>')
            self.writeLine('</tr>' )

#===============================================================================
# Item
#===============================================================================
class Item():
    
    def tableCommonStyle(self): return Html.Style(Map({
        'border-collapse' : 'collapse'                          ,
        'border-style'    : 'hidden'                            ,
        'width'           : '100%'                              ,
        'table-layout'    : 'auto'                              ,
    }))
    
    def tableCommonStyle(self): return Html.Style(Map({
        'border-collapse' : 'collapse'                          ,
        'border-style'    : 'hidden'                            ,
        'width'           : '1238',   #'985'
        'table-layout'    : 'fixed'                              ,
        'margin-left'     : '12px'       ,
    }))
    
    def tableCommonStyle1(self, margin): return Html.Style(Map({
        'border-collapse' : 'collapse'                          ,
        'border-style'    : 'hidden'                            ,
        'width'           : '0'                              ,
        'table-layout'    : 'fixed'                              ,
        'margin-left'     : str(margin) + 'px'       ,
    }))
    
    def rowCommonStyle(self): return Html.Style(Map({
        'font-family'     : 'Verdana, Geneva, sans-serif'       ,
        'font-size'       : '14px'                              ,
        'line-height'     : '14px'                              ,
        'margin-left'     : '20px'       ,
        'margin-right'    : '20px'       ,
        'white-space'     : 'nowrap'     ,
    }))
    
    def rowCommonStyle1(self): return Html.Style(Map({
        'font-family'     : 'Verdana, Geneva, sans-serif'       ,
        'font-size'       : '14px'                              ,
        'line-height'     : '20px'                              ,
        #'margin-left'     : '20px'       ,
        #'margin-right'    : '20px'       ,
        'white-space'     : 'nowrap'     ,
    }))
    
    def cellBlackLeft(self): return Html.Style(Map({
        'background-color': 'white' ,
        'color'           : 'black' ,
        'text-align'      : 'left'  ,
        'font-weight'     : 'bold'  ,
    }))
    
    def cellGrayLeft(self): return Html.Style(Map({
        'background-color': 'white' ,
        'color'           : 'DimGray' ,
        'text-align'      : 'left'  ,
        'font-weight'     : 'bold'  ,
    }))
    

    def cellBlackCenter(self): return Html.Style(Map({
        'background-color': 'white' ,
        'color'           : 'black' ,
        'text-align'      : 'center' ,
        'font-weight'     : 'bold'  ,
    }))
    
    def cellBlackRight(self): return Html.Style(Map({
        'background-color': 'white' ,
        'color'           : 'black' ,
        'text-align'      : 'right' ,
        'font-weight'     : 'bold'  ,
    }))
    
    def cellRedBold(self): return Html.Style(Map({
        'background-color': 'white' ,
        'color'           : 'red'   ,
        'text-align'      : 'left'  ,
        'font-weight'     : 'bold',
        'line-height'     : '8px'                              ,
        'font-size'       : '12px'                              ,
    }))

    def cellRedLeft(self): return Html.Style(Map({
        'background-color': 'white' ,
        'color'           : 'red'   ,
        'text-align'      : 'left'  ,
        'font-weight'     : 'normal',
    }))

    def cellRedRight(self): return Html.Style(Map({
        'background-color': 'white' ,
        'color'           : 'red'   ,
        'text-align'      : 'right' ,
        'font-weight'     : 'normal',
    }))
    
    def contentsBlank(self): 
        return ''

    def endText0(self): return (
    '''
        <p style="font-family:Verdana, Geneva, sans-serif;color:black;font-size:1.4em;text-align:left;margin-left:20px;line-height:150%;
        color:red;font-size:0.8em;text-align:left;margin-left:10px;line-height:70%;line-height:70%;font-weight:bold;">IMPORTANT:
        
        <ul style="font-family:Verdana, Geneva, sans-serif;color:black;font-size:1.4em;text-align:left;margin-left:20px;line-height:150%;
        color:red;font-size:0.8em;text-align:left;margin-left:10px;line-height:70%;font-weight:normal;font-size:0.9em;margin-left:0px;line-height:100%;"><li>For any camper care health issue requiring immediate attention, contact Lisa Hirano
        by cell phone at&nbsp;(408)&nbsp;981-7282.</li>
        <li>Return this form to Health Supervisor Eiko Kanzaki at the end of camp.
        </li></ul></p>
    ''' )
    
    def endText(self): return (
    '''
        &nbsp;&nbsp;IMPORTANT:
        <ul style=font-weight:normal;margin-left:0px;line-height:135%;font-size:14px;">
        <li>For any camper care health issue requiring immediate attention, contact Lisa Hirano
        by cell phone at&nbsp;(408)&nbsp;981-7282.</li>
        <li>Return this form to Health Supervisor Eiko Kanzaki at the end of camp.
        </li></ul>
    ''' )
    
    
    
    def endText2(self): return (
    '''
        <div style=font-size:13px;>
        I acknowledge that the above medications listed are complete and accurate for the above camper.
        <br /><br /><br />
        signed: ______________________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;relationship to camper: ____________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;date: __________
        </div>
    ''')

item = Item()

