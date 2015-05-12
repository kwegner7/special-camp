'''
    HtmlTable.SpecialCamp
'''

import sys, os, re, collections
from classes.utils.Container import *
from classes.html import HtmlTable
from classes.html import Html

PLEASE_SPLIT = True
DONT_SPLIT = False

#==============================================================================
# HtmlTable.CategoryDetails
#==============================================================================
class CategoryDetails(HtmlTable.Base):

    def __init__(self, csv_object, sectionChange, subsectionChange, folder_out):
        HtmlTable.Base.__init__(self, csv_object, sectionChange, subsectionChange, folder_out)
        self.createHtmlTables(csv_object, folder_out)

    def insertOneRecord(self, row, bkg_color, font_weight):
        if 'count_campers' not in dir(self):
            self.count_campers = 0
        print row['camper'], self.count_campers
        lines = list()
        line1 = "<td><a href=printform?formtype=INSERT"
        line2 = "&camperid="
        line3 = row['camper-ID'] + ">"+ row['camper']
        line4 = "</a></td>"
        if self.count_campers == 0:
            lines.append('<tr>' + line1 + line2 + line3+ line4)
        elif self.count_campers == 2:
            lines.append('    ' + line1 + line2 + line3+ line4 + '</tr>')
        else:
            lines.append('    ' + line1 + line2 + line3+ line4)
        for line in lines: self.writeln(line)
        self.count_campers = self.count_campers + 1
        if self.count_campers == 3: self.count_campers = 0
        return None
    
    def beginHtml(self, row):
        return None

    def defineStyles(self, row):
        return None

    def beginBody(self, row):
        return None

    def endBodyAndHtml(self):
        return None

    def summaryOnly(self):
        return False
            
    def splitSectionsIntoSeparateFiles(self):
        return False
    
    def beginSection(self, writer, first_row):
        return None
                       
    def endSection(self, writer, last_row):
        return None

    def beginSubsection(self, writer, row, bookmark):
        return None
    
    def endSubsection(self, writer, monitor, is_final_row):
        return None
       
    def summaryFollowingDetails(self, how_many, bottom_row_prev_section):
        return None
    
               
#==============================================================================
# HtmlTable.SpecialCamp.Details
#==============================================================================
class Details(CategoryDetails):
    
    def __init__(self, csv_file, sectionChange, subsectionChange, folder_out): 
        self.folder_out = folder_out 
        self.index_file = self.folder_out + 'index.html' 
        self.csv_file = csv_file  
        self.createHtmlTables()
        
    def createHtmlTables(self):
        print "FOLDER_OUT",self.folder_out
        clearFolder(self.folder_out)
    
        # loop over the csv file
        self.csv_file.openRead() 
        for row in self.csv_file.reader:
            print row['camper'], row['camper-ID']
        self.csv_file.closeRead()
        
        self.openIndex()
        
        print "HTML is at", self.index_file
        print ""

    def writeLines(self, lines):
        for line in lines:
            self.index.write(line+'\n')
        return None

    def openIndex(self):
        self.index = open(self.index_file, 'wb')
        self.index.write(self.indexA())
        self.writeLines(self.indexA1())
        self.index.write(self.indexA2())
        self.writeLines(self.indexB())
        self.index.write(self.indexC())
        self.writeLines(self.indexD())
        self.index.write(self.indexE())
        self.writeLines(self.indexF())
        self.index.write(self.indexG())
        self.writeLines(self.indexH())
        self.index.write(self.indexI())
        self.writeLines(self.indexJ())
        self.index.write(self.indexK())


    # <td class=week><a href="JavaScript:pop('printform?formtype=hs-master-schedule&day=sun&year=2015');">Sun</a></td>
    # <td class=week><a href="printform?formtype=hs-master-schedule&day=sun&year=2015">Sun</a></td>



    def indexA(self):  return (    
'''
    <base href="http://stark-retreat-1229.herokuapp.com/meds/" target="_blank">
      <title>Special Camp</title>

    <style>

        .main
        {
            font-family:Verdana, Geneva, sans-serif;
            font-size:20px;
            font-weight:bold;
            color:green;
            text-align:left;
            margin-left:150px;
            text-decoration:none;
            line-height:150%
        }

        .heading
        {
             font-family:Verdana, Geneva, sans-serif;
             font-size:18px;
             font-weight:bold;
             color:black;
             text-align:left;
             margin-left:0px;
             text-decoration:none;
             line-height:150%;
        }

        .goto
        {
             font-family:Verdana, Geneva, sans-serif;
             font-size:18px;
             font-weight:bold;
             color:blue;
             text-align:left;
             margin-left:0px;
             text-decoration:underline;
             line-height:150%;
             padding-left:20pt;
        }
        
        .tbl
        {
             font-family:Verdana, Geneva, sans-serif;
             font-size:16px;
             font-weight:bold;
             color:black;
             text-align:left;
             margin-left:20px;
             text-decoration:underline;
             line-height:150%;
             padding-left:20pt;
        }
        
        td
        {
            width:170px;
            white-space:nowrap;
        }
       
        td.week
        {
            width:60px;
            white-space:nowrap;
        }
       
        td.camper
        {
            width:200px;
            white-space:nowrap;
        }
       
        a
        {
            color:black;
        }
        
        a.camper
        {
            color:blue;
        }
        
        .text
        {
             font-family:Verdana, Geneva, sans-serif;
             font-size:12px;
             font-weight:bold;
             black;
             text-align:left;
             margin-left:0px;
             text-decoration:normal;
             line-height:150%;
             padding-left:20pt;
        }

    </style>

</head>

<body>

    <script type="text/javascript">
    function pop(url) {
        popupWindow = window.open(
            url,'popUpWindow','height=300,width=900,left=10,top=10,resizable=yes,scrollbars=no,toolbar=no,menubar=no,location=no,directories=no,status=yes')
    }
    </script>

    <!-- ------------------------------------------------------------------ -->
    <div><hr><span class=main>FORMS FOR HEALTH SUPERVISOR</span><hr><br>
''')
    
    def atag(self, class_is, specs, show, final):
        lines = list()
        lines.append('')
        lines.append( 
            "    <a " + class_is
            + 'target="_blank" href="printform?'
            + specs + '"' ) 
        lines.append( 
            '    >' + show + '</a>' + final) 
        return lines
        
    def indexA1(self):
        lines = self.atag(
            "class=goto ", 
            'formtype=hs-master-schedule&year=2015&usr=special&pwd=camp',
            'Health Supervisor Master Schedule',
            '<br>')
        return lines

    def indexA2(self):  return (    
'''

    <table class=tbl>
      <tr>
        <td class=week><a target="_blank" href="printform?formtype=hs-master-schedule&day=sun&year=2015&usr=special&pwd=camp">Sun</a></td>
        <td class=week><a target="_blank" href="printform?formtype=hs-master-schedule&day=mon&year=2015&usr=special&pwd=camp">Mon</a></td>
        <td class=week><a target="_blank" href="printform?formtype=hs-master-schedule&day=tue&year=2015&usr=special&pwd=camp">Tue</a></td>
        <td class=week><a target="_blank" href="printform?formtype=hs-master-schedule&day=wed&year=2015&usr=special&pwd=camp">Wed</a></td>
        <td class=week><a target="_blank" href="printform?formtype=hs-master-schedule&day=thu&year=2015&usr=special&pwd=camp">Thu</a></td>
        <td class=week><a target="_blank" href="printform?formtype=hs-master-schedule&day=fri&year=2015&usr=special&pwd=camp">Fri</a></td>
        <td class=week><a target="_blank" href="printform?formtype=hs-master-schedule&day=sat&year=2015&usr=special&pwd=camp">Sat</a></td>
        <td class=week><a target="_blank" href="printform?formtype=hs-master-schedule&day=asneeded&year=2015&usr=special&pwd=camp">As&nbsp;Needed</a></td>
      </tr>
    </table><br>

    <a class=goto target="_blank" href="printform?formtype=hs-med-audit-sheets&year=2015&usr=special&pwd=camp"
    >Meds Administered by Health Supervisor</a><br>
        
    <table class=tbl>
''')
    
    def indexB(self):
        day_dict = dict()
        day_dict['sun'] = 'Sun'
        day_dict['mon'] = 'Mon'
        day_dict['tue'] = 'Tue'
        day_dict['wed'] = 'Wed'
        day_dict['thu'] = 'Thu'
        day_dict['fri'] = 'Fri'
        day_dict['sat'] = 'Sat'
        day_dict['asneeded'] = 'As&nbsp;Needed'
        count = 0
        printtr = False
        lines = list()
        lines.append('      <tr>')
        self.csv_file.openRead() 
        for row in self.csv_file.reader:
            if printtr:
                lines.append('      </tr>')
                lines.append('      <tr>')
                printtr = True
            line = ( 
                '        <td class=camper><a class=camper target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid='
                + row['camper-ID'] 
                + "&year=2015&usr=special&pwd=camp"+'">'
                + String(row['camper']).removeBlanks() +'</a></td>' )
            lines.append(line)
            for day in list(['sun','mon','tue','wed','thu','fri','sat','asneeded']):
                line = ( 
                    '        <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid='
                    + row['camper-ID'] 
                    + '&year=2015&usr=special&pwd=camp&day=' + day + '">'
                    + day_dict[day] +'</a></td>' )
                lines.append(line)
                
            count = count+1
            printtr = True
        self.csv_file.closeRead()
        lines.append('      </tr>')
        return lines

    
    def indexC(self):  return (    
'''
    </table><br>

    </div>
    <!---------------------------------------------------------------------->
    <div><hr><span class=main>FORMS FOR CABIN CARE GROUP</span><hr><br>
    
    <a class=goto target="_blank" href="printform?formtype=caregroup-med-audit-sheets&year=2015&usr=special&pwd=camp"
    >Meds Administered by Camper Care Group</a><br>
    <table class=tbl>
    
''')
    
    def forEachCamper(self, formtype):
        count = 0
        printtr = False
        lines = list()
        lines.append('      <tr>')
        self.csv_file.openRead() 
        for row in self.csv_file.reader:
            if printtr:
                lines.append('      </tr><tr>')
                printtr = False
            line = ( 
                '        <td><a target="_blank" href="printform?formtype=' + formtype + "&camperid="
                + row['camper-ID'] 
                + "&year=2015&usr=special&pwd=camp" + '">'
                + String(row['camper']).removeBlanks() +'</a></td>' )
            lines.append(line)
            count = count+1
            if count > 2:
                count = 0
                printtr = True
        self.csv_file.closeRead()
        lines.append('      </tr>')
        return lines

    def indexD(self):
        return self.forEachCamper("caregroup-med-audit-sheets")
    
    def indexE(self):  return (    
'''
    </table><br>

    <a class=goto target="_blank" href="printform?formtype=caregroup-hs-med-schedule&year=2015&usr=special&pwd=camp"
    >Care Group Med Schedule for Health Supervisor Administered Meds</a><br>
    <table class=tbl>
''')
        
    def indexF(self):
        return self.forEachCamper("caregroup-hs-med-schedule")
    
    def indexG(self):  return (    
'''
    </table><br>
    
    </div
    <!---------------------------------------------------------------------->
    <div><hr><span class=main>FORMS FOR GUARDIAN</span><hr><br>

    <a class=goto target="_blank" href="printform?formtype=guardian-signature-sheet&year=2015&usr=special&pwd=camp"
    >Guardian Signature</a><br>
    <table class=tbl>
''')
    
    def indexH(self):
        return self.forEachCamper("guardian-signature-sheet")
    
    def indexI(self):  return (    
'''
    </table><br>
    
    <a class=goto target="_blank" href="printform?formtype=leftover-meds-receipt&year=2015&usr=special&pwd=camp"
    >Leftover Meds Receipt Acknowledgment</a><br>
    <table class=tbl>
''')
    
    def indexJ(self):
        return self.forEachCamper("leftover-meds-receipt")
    
    def indexK(self):  return (    
'''
    </table><br>
    
    </div>
    <!---------------------------------------------------------------------->
    <div><hr><span class=main>FORMS FOR LA BUS CAPTAIN</span><hr><br>
    
    <a class=goto target="_blank" href="printform?formtype=bus-med-audit-sheet&year=2015&usr=special&pwd=camp"
    >Meds Administered During LA Bus Trip</a><br>
    <table class=tbl>
      <tr>
        <td class=week><a target="_blank" href="printform?formtype=bus-med-audit-sheet&day=sun&year=2015&usr=special&pwd=camp">Sun</a></td>
        <td class=week><a target="_blank" href="printform?formtype=bus-med-audit-sheet&day=sat&year=2015&usr=special&pwd=camp">Sat</a></td>
        <td class=week><a target="_blank" href="printform?formtype=bus-med-audit-sheet&day=asneeded&year=2015&usr=special&pwd=camp">As&nbsp;Needed</a></td>
      </tr>
    </table><br>  
    
    </div>
    <!---------------------------------------------------------------------->
    <hr>
    
</body>
</html>
''')

























      
        
       
#==============================================================================
# HtmlTable.SpecialCamp.Details
#==============================================================================
class Details0(CategoryDetails):
    
    def __init__(self, csv_object, sectionChange, subsectionChange, folder_out):        
        CategoryDetails.__init__(self, csv_object, sectionChange, subsectionChange, folder_out)
        
    def columns(self):
        if not hasattr(self, 'cfg'):
            self.cfg = collections.namedtuple( 'ConfigureColumns',
            'fieldname, heading, width, CellStyle, fontsize' )
        
        nature_of_columns = ([
        self.cfg('camper'       , 'Camper Name'                 ,   0, 'nowrapl', '1.0' ),
        self.cfg('camper-ID'       , 'Camper ID'                 ,   0, 'nowrapl', '1.0' ),
        ])
        
        return nature_of_columns

    def summaryFollowingDetails(self, how_many, bottom_row_prev_section):
        return None

