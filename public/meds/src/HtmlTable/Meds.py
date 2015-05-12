'''
    class HtmlTable
'''

import sys, os, re, collections, textwrap
from utils.CsvObject import *
from utils.Container import *
from utils.ShellCommand import *
from utils import Html
from Base import HtmlTable
from presentation import SelectOrdering, SelectSections, SelectColumns
    
PLEASE_SPLIT = True
DONT_SPLIT = False

#===============================================================================
# MainTable
#===============================================================================
class MainTable:
    
    #===========================================================================
    # MainTable.SpecialCamp
    #===========================================================================
    class SpecialCamp(Html.Table):
      
        def __init__(self, table_name):
            Html.Table.__init__(self, table_name)
    
        def tableStyle(self): return Html.Style(Map({
    
            'font-family'     : 'Verdana, Geneva, sans-serif' ,
            'border-collapse' : 'collapse'                    ,
            'width'           : '1238'                         ,
            'table-layout'    : 'fixed'                       ,
            'margin-left'     : '12px'                        ,
        }))
    
        def tableHeadingStyle(self): return Html.Style(Map({
    
                    'font-size': '16px'            ,
                  'line-height': '16px'            ,
                  'font-weight': 'bold'            ,
                   'text-align': 'left'            ,
                       'border': '1px solid black' ,
                  'padding-top': '5px' ,
                'padding-right': '0px' ,
               'padding-bottom': '5px' ,
                 'padding-left': '5px' ,
             'background-color': 'white'       ,
                        'color': 'blue'           ,
                   'font-style': 'italic'          }))
        
        def tableRowStyle(self): return Html.Style(Map({
    
                    'font-size': '10px'            ,
                  'line-height': '12px'            ,
                  'font-weight': 'bold'            ,
                        'color': 'black'           ,
             'background-color': 'white'           ,
        }))
        
        def tableCellStyle(self): return Html.Style(Map({
    
                   'text-align': 'center'          ,
                       'border': '1px solid black' ,
                  'padding-top': '5px' ,
                'padding-right': '0px' ,
               'padding-bottom': '5px' ,
                 'padding-left': '5px' ,
        }))
    
    #=============================================================================
    # 1) MainTable.CabinDaysTogether
    #=============================================================================
    class CabinDaysTogether(SpecialCamp):
      
        def __init__(self, table_name):
            MainTable.SpecialCamp.__init__(self, table_name)
    
        def columns(self):
            nature_of_columns = ([
            
            self.cfg('day'                 , 'Day'                 ,  '75', 'nowrapc', '12px', 0 ),
            self.cfg('time'                , 'Time'                ,  '68', 'nowrapc', '12px', 0 ),
            self.cfg('medication'          , 'Medication'          , '203', 'nowrapl', '12px', 30 ),
            self.cfg('dosage'              , 'Dosage'              , '203', 'nowrapl', '12px', 30 ),
            self.cfg('frequency'           , 'Frequency'           , '203', 'nowrapl', '12px', 30 ),
            self.cfg('special-instructions', 'Special Instructions', '203', 'nowrapl', '12px', 30 ),
            self.cfg('purpose'             , 'Purpose'             , '203', 'nowrapl', '12px', 30 ),
            self.cfg('BLANK'               , 'Admin'               ,  '40', 'nowrapc', '8px', 0 ),
            self.cfg('BLANK'               , 'Witness'             ,  '40', 'nowrapc', '7px', 0 ),
                                                                     # 985 --> 1238
            
            ])
            return nature_of_columns
        
    #=============================================================================
    # 2) MainTable.HsDaysSeparated
    #=============================================================================
    class HsDaysSeparated(SpecialCamp):
      
        def __init__(self, table_name):
            MainTable.SpecialCamp.__init__(self, table_name)
    
        def columns(self):
            nature_of_columns = ([
            
            self.cfg('time'                , 'Time'                ,  '76', 'nowrapl', '12px', 0 ),
            self.cfg('medication'          , 'Medication'          , '216', 'nowrapl', '12px', 32 ),
            self.cfg('dosage'              , 'Dosage'              , '216', 'nowrapl', '12px', 32 ),
            self.cfg('frequency'           , 'Frequency'           , '216', 'nowrapl', '12px', 32 ),
            self.cfg('special-instructions', 'Special Instructions', '216', 'nowrapl', '12px', 32 ),
            self.cfg('purpose'             , 'Purpose'             , '216', 'nowrapl', '12px', 32 ),
            self.cfg('BLANK'               , 'HS'                  ,  '41', 'nowrapc', '12px', 0 ),
            self.cfg('BLANK'               , 'Aide'                ,  '41', 'nowrapc', '10px', 0 ),
                                                                     # 985
            ])
            
            return nature_of_columns

    #===========================================================================
    # 3) MainTable.HsDaysCollapsed
    #===========================================================================
    class HsDaysCollapsed(SpecialCamp):
      
        def __init__(self, table_name):
            MainTable.SpecialCamp.__init__(self, table_name)
    
        def columns(self):
            nature_of_columns = ([
                                            
            self.cfg('time'                , 'Time'                ,  '75', 'nowrapl', '12px', 0 ),
            self.cfg('medication'          , 'Medication'          , '233', 'nowrapl', '12px', 34 ),
            self.cfg('dosage'              , 'Dosage'              , '232', 'nowrapl', '12px', 34 ),
            self.cfg('frequency'           , 'Frequency'           , '233', 'nowrapl', '12px', 34 ),
            self.cfg('special-instructions', 'Special Instructions', '232', 'nowrapl', '12px', 34 ),
            self.cfg('purpose'             , 'Purpose'             , '233', 'nowrapl', '12px', 34 ),
            ])
            return nature_of_columns

    #=============================================================================
    # 4) MainTable.MasterSchedule
    #=============================================================================
    class MasterSchedule(SpecialCamp):
      
        def __init__(self, table_name):
            MainTable.SpecialCamp.__init__(self, table_name)
    
        def columns(self):
            nature_of_columns = ([
                                  
            self.cfg('time'         , 'Time'      ,  '70', 'nowrapl', '12px', 0 ),
            self.cfg('camper'       , 'Camper'    , '110', 'nowrapl', '12px', 0 ),
            self.cfg('medication'   , 'Medication', '160', 'nowrapl', '12px', 33 ),
            self.cfg('dosage'       , 'Dosage'    , '220', 'nowrapl', '12px', 34 ),
            self.cfg('frequency'    , 'Frequency' , '215', 'nowrapl', '12px', 36 ),
            self.cfg('purpose'      , 'Purpose'   , '180', 'nowrapl', '12px', 33 ),
            self.cfg('HS-dispenses' , 'HS'        ,  '30', 'nowrapl', '12px', 0 ),
                                                    # 985
            ])
            return nature_of_columns
        
        def columns(self):
            nature_of_columns = ([
                                  
            self.cfg('time'         , 'Time'      ,  '70', 'nowrapl', '12px', 0 ),
            self.cfg('camper'       , 'Camper'    , '130', 'nowrapl', '12px', 0 ),
            self.cfg('medication'   , 'Medication', '252', 'nowrapl', '12px', 33 ),
            self.cfg('dosage'       , 'Dosage'    , '252', 'nowrapl', '12px', 34 ),
            self.cfg('frequency'    , 'Frequency' , '252', 'nowrapl', '12px', 36 ),
            self.cfg('purpose'      , 'Purpose'   , '252', 'nowrapl', '12px', 33 ),
            self.cfg('HS-dispenses' , 'HS'        ,  '30', 'nowrapl', '12px', 0 ),
                                                    # 1238
            ])
            return nature_of_columns

    #===========================================================================
    # 5) MainTable.CabinAndHsCollapsed
    #===========================================================================
    class CabinAndHsCollapsed(SpecialCamp):
      
        def __init__(self, table_name):
            MainTable.SpecialCamp.__init__(self, table_name)
    
        def columns(self):
            nature_of_columns = ([
                                              
            self.cfg('time'                , 'Time'                ,  '76', 'nowrapl', '12px', 0 ),
            self.cfg('all_days'            , 'Days'                , '131', 'nowrapl', '12px', 0 ),
            self.cfg('medication'          , 'Medication'          , '198', 'nowrapl', '12px', 32 ),
            self.cfg('dosage'              , 'Dosage'              , '198', 'nowrapl', '12px', 32 ),
            self.cfg('frequency'           , 'Frequency'           , '198', 'nowrapl', '12px', 32 ),
            self.cfg('special-instructions', 'Special Instructions', '198', 'nowrapl', '12px', 32 ),
            self.cfg('purpose'             , 'Purpose'             , '198', 'nowrapl', '12px', 32 ),
            self.cfg('BLANK'               , 'Initial'             ,  '41', 'nowrapc', '8px', 0 ),
            
            ])
            return nature_of_columns

    #=============================================================================
    # 6) MainTable.LaBusDaysSeparated
    #=============================================================================
    class LaBusDaysSeparated(SpecialCamp):
      
        def __init__(self, table_name):
            MainTable.SpecialCamp.__init__(self, table_name)
    
        def columns(self):
            nature_of_columns = ([
                                  
            self.cfg('time'                , 'Time'                ,  '75', 'nowrapl', '12px', 0 ),
            self.cfg('camper'              , 'Camper'              , '130', 'nowrapl', '12px', 0 ),
            self.cfg('medication'          , 'Medication'          , '196', 'nowrapl', '12px', 30 ),
            self.cfg('dosage'              , 'Dosage'              , '196', 'nowrapl', '12px', 30 ),
            self.cfg('frequency'           , 'Frequency'           , '196', 'nowrapl', '12px', 30 ),
            self.cfg('special-instructions', 'Special Instructions', '196', 'nowrapl', '12px', 30 ),
            self.cfg('purpose'             , 'Purpose'             , '196', 'nowrapl', '12px', 30 ),
            self.cfg('BLANK'               , 'Admin'               ,  '41', 'nowrapc', '8px', 0 ),
            self.cfg('BLANK'               , 'Witness'             ,  '41', 'nowrapc', '7px', 0 ),
            
            ])
            return nature_of_columns

    #=============================================================================
    # 7) MainTable.LeftoverMeds
    #=============================================================================
    class LeftoverMeds(SpecialCamp):
      
        def __init__(self, table_name):
            MainTable.SpecialCamp.__init__(self, table_name)
    
        def columns(self):
            nature_of_columns = ([
                                  
            self.cfg('medication' , 'MED NAME'          , '350', 'left', '14px', 0 ),
            self.cfg('BLANK'      , 'QUANTITY RECEIVED' , '350', 'left', '14px', 0 ),
            
            ])
            return nature_of_columns
        
        def tableStyle(self): return Html.Style(Map({
    
            'font-family'     : 'Verdana, Geneva, sans-serif'       ,
            'border-collapse' : 'collapse'                          ,
            #'width'           : '0%'                                ,
            'width'           : '700'                                ,
            'table-layout'    : 'auto'                              ,
            #'font-size'       : '12px'                              ,
            #'line-height'     : '12px'                              ,
            'margin-left'      : '100px'
            }))
        
        def tableHeadingStyle(self): return Html.Style(Map({
    
                    'font-size': '16px'            ,
                  'line-height': '16px'            ,
                  'font-weight': 'bold'            ,
                   'text-align': 'center'          ,
                       'border': '1px solid black' ,
                      'padding': '4px 5px 4px 5px' ,
             'background-color': 'lightgrey'       ,
                        'color': 'black'           ,
                      'padding': '10px 10px 10px 10px' ,
                   'font-style': 'italic'          }))

        def tableRowStyle(self): return Html.Style(Map({
    
                    'font-size': '14px'            ,
                  'line-height': '16px'            ,
                  'font-weight': 'bold'            ,
                        'color': 'black'           ,
             'background-color': 'white'           ,
             'white-space'     : 'nowrap'          ,

        }))
        
        def tableCellStyle(self): return Html.Style(Map({
    
                   'text-align': 'center'          ,
                       'border': '1px solid black' ,
                      'padding': '10px 10px 10px 10px' ,
             'background-color': 'white'           ,
        }))
       
#===============================================================================
# Used for special tables
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
        'width'           : '1238'                              ,
        'table-layout'    : 'fixed'                              ,
        'margin-left'     : '12px'       ,
    }))
    
    def rowCommonStyle(self): return Html.Style(Map({
        'font-family'     : 'Verdana, Geneva, sans-serif'       ,
        'font-size'       : '14px'                              ,
        'line-height'     : '14px'                              ,
        'margin-left'     : '20px'       ,
        'margin-right'    : '20px'       ,
        'white-space'     : 'nowrap'     ,
    }))
    
    def cellBlackLeft(self): return Html.Style(Map({
        'background-color': 'white' ,
        'color'           : 'black' ,
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
    
#===============================================================================
# BetweenSectionsAndSubsections.SpecialCamp
#===============================================================================
class BetweenSectionsAndSubsections:
    
    #===========================================================================
    # BetweenSectionsAndSubsections.SpecialCamp
    #===========================================================================
    class SpecialCamp():
                
        def repeatHeadings(self):
            return False
    
        def splitSectionsIntoSeparateFiles(self):
            return True
        
        def beginSection(self, writer, first_row, htmltable, count_pages, camper_has_changed):
            writer.write('</br>')
            table = Html.Table('LeftRight')
            item = Item()
            table_html = table.twoCells(
                item.tableCommonStyle().style(),
                item.rowCommonStyle().style(),
                item.cellBlackLeft().style(),
                item.cellBlackRight().style(),
                htmltable.title(),
                ( 'Camper: ' + first_row['camper'] + 
                  '&nbsp;&nbsp;&nbsp;' + first_row['day'] +
                  '&nbsp;&nbsp;&nbsp;' + first_row['date'] ),
                )
            writer.write(table_html)
            writer.write('</br>\n')
            return None
    
        def endSection(self, writer, last_row, htmltable):
            writer.write('</br>')
            table = Html.Table('LeftRight')
            item = Item()
            table_html = table.twoCells(
                item.tableCommonStyle().style(),
                item.rowCommonStyle().style(),
                item.cellBlackLeft().style(),
                item.cellBlackRight().style(),
                htmltable.title(),
                ( 'Camper: ' + last_row['camper'] + 
                  '&nbsp;&nbsp;&nbsp;' + last_row['day'] +
                  '&nbsp;&nbsp;&nbsp;' + last_row['date'] ),
                )
            writer.write(table_html)
            #writer.write('</br>\n')
            return None
        
    #===========================================================================
    # 1) BetweenSectionsAndSubsections.CabinDaysTogether
    #===========================================================================
    class CabinDaysTogether(SpecialCamp):   
             
        def beginSection(self, writer, first_row, table, count_pages, camper_has_changed):
            table_html = Html.Table().twoCells(
                item.tableCommonStyle().style(),
                item.rowCommonStyle().style(),
                item.cellBlackLeft().style(),
                item.cellBlackRight().style(),
                self.contentsCellA(first_row, count_pages),
                self.contentsCellB(),
                '619', '619') #1238
            writer.write(table_html)
            
            writer.write('<hr style="margin-left:12px; width:1238;">')
            writer.write('</br>')
            
            table_html = Html.Table().oneCell(
                item.tableCommonStyle().style(),
                item.rowCommonStyle().style(),
                item.cellRedLeft().style(),
                self.contentsBelowLine(),
                '1238')
            writer.write(table_html)
            writer.write('</br>')
            return None

        def endSection(self, writer, last_row, htmltable):
            writer.write('</br>')
            table_html = Html.Table().oneCell(
                item.tableCommonStyle().style(),
                item.rowCommonStyle().style(),
                item.cellRedBold().style(),
                item.endText(),
                '1238')
            writer.write(table_html)
            #writer.write('</br>')
            return None
    
        def beginSubsection(self, writer, row, bookmark, table):        
            return None
    
        def endSubsection(self, writer, monitor, is_final_row, table):
            table.writeRowsOfColor('white', 2)
            return None
    
        def contentsCellA(self, row, count_pages): 
            contents = 'Camper Med Schedule For:&nbsp;&nbsp;<font style=color:red>' + row['camper'] +'</font>'
            if not count_pages == 1: return contents
            else: return (
                Html.tagSurround('h1',
                    'style="' 
                    + item.rowCommonStyle().style().write() 
                    + item.cellBlackLeft().style().write(),
                    contents
                )
            )
        
        def contentsCellB(self): 
            return 'JEMS Special Camp ' + YEAR_OF_CAMP
        
        def contentsBelowLine(self): 
            return (
                "The following are to be administered " 
                + "<font style=font-weight:bold;text-decoration:underline>"
                + "by camper's Camper Care Group</font>&nbsp;&nbsp;in his/her dorm:"
            )
                           
    #===========================================================================
    # 2) BetweenSectionsAndSubsections.HsDaysSeparated
    #===========================================================================
    class HsDaysSeparated(SpecialCamp):
        
        def __init__(self):
            self.check_camper = ''
                  
        def beginSection(self, writer, first_row, table, count_pages, camper_has_changed):
            
            table_html = Html.Table().threeCells(
                item.tableCommonStyle().style(),
                item.rowCommonStyle().style(),
                item.cellBlackLeft().style(),
                item.cellBlackCenter().style(),
                item.cellBlackRight().style(),
                self.contentsCellA(first_row, count_pages, camper_has_changed),
                self.contentsCellB(first_row),
                self.contentsCellC(first_row),
                '350', '250', '638') #1238

            writer.write(table_html)            
            
            #writer.write('<hr style="margin-left:12px; width:1238;">')
            writer.write('<br />')
            return None
        
        def endSection(self, writer, last_row, htmltable):
            return None

        def beginSubsection(self, writer, row, bookmark, table):        
            return None
    
        def endSubsection(self, writer, monitor, is_final_row, table):
            table.writeRowsOfColor('white', 2)
            return None

        def contentsCellA(self, row, count_pages, camper_has_changed):             
            
            contents = 'Camper Name:&nbsp;&nbsp;<font style=color:red>' + row['camper'] +'</font>'
            if not camper_has_changed:
                 #print "NO HTAG", row['day'], row['camper']
                 return contents
            else:
                #print "YES HTAG", row['day'], row['camper']
                return (
                Html.tagSurround('h1',
                    'style="' 
                    + item.rowCommonStyle().style().write() 
                    + item.cellBlackLeft().style().write(),
                    contents
                )
            )
            self.check_camper = row['camper']
        
        def contentsCellB(self, row): 
            if row['day'] == 'as needed':
                return (
                    '<div style="font-size:18px;font-weight:bold;text-align:center;line-height:20px;">'
                    + 'As Needed' + '<br />'
                    + '<font style=font-size:12px;>' + '&nbsp;' + '</font></div>'
                )
            return (
                '<div style="font-size:18px;font-weight:bold;text-align:center;line-height:20px;">'
                + row['day'] + '<br />'
                + '<font style=font-size:12px;>' + row['date'] + '</font></div>'
            )

        def contentsCellC(self, row): 
            return (
                '''
                <div style="font-size:12px;font-weight:bold;text-align:right;line-height:25px;">
                Camper Care Group: _________________________________________<br />
                Camper Care Lead: _________________________________________</div>
                ''')

    #===========================================================================
    # 3) BetweenSectionsAndSubsections.HsDaysCollapsed
    #===========================================================================
    class HsDaysCollapsed(SpecialCamp):
                  
        def beginSection(self, writer, first_row, table, count_pages, camper_has_changed):
            
            table_html = Html.Table().twoCells(
                item.tableCommonStyle().style(),
                item.rowCommonStyle().style(),
                item.cellBlackLeft().style(),
                item.cellBlackRight().style(),
                self.contentsCellA(first_row, count_pages),
                self.contentsCellB(),
                '619', '619') #1238
            writer.write(table_html)
            
            writer.write('<hr style="margin-left:12px; width:1238;">')
            writer.write('</br>')
            
            table_html = Html.Table().oneCell(
                item.tableCommonStyle().style(),
                item.rowCommonStyle().style(),
                item.cellRedLeft().style(),
                self.contentsBelowLine(),
                '1238')
            writer.write(table_html)

            writer.write('</br>')
            return None

        def endSection(self, writer, last_row, htmltable):
            writer.write('</br>')
           
            table_html = Html.Table().oneCell(
                item.tableCommonStyle().style(),
                item.rowCommonStyle().style(),
                item.cellRedBold().style(),
                item.endText(),
                '1238')
            writer.write(table_html)
            
            #writer.write('</br>')
            return None
    
        def beginSubsection(self, writer, row, bookmark, table):        
            return None
    
        def endSubsection(self, writer, monitor, is_final_row, table):
            return None
    
        def contentsCellA(self, row, count_pages): 
            contents = 'Camper Med Schedule For:&nbsp;&nbsp;<font style=color:red>' + row['camper'] +'</font>'
            if not count_pages == 1: return contents
            else: return (
                Html.tagSurround('h1',
                    'style="' 
                    + item.rowCommonStyle().style().write() 
                    + item.cellBlackLeft().style().write(),
                    contents
                )
            )
        
        def contentsCellB(self): 
            return 'JEMS Special Camp ' + YEAR_OF_CAMP
        
        def contentsBelowLine(self): 
            return (
                "Camper is to be " 
                + "<font style=font-weight:bold;text-decoration:underline>"
                + "taken to the Health Supervisor every day</font>&nbsp;at the following times for medication administration:")

    #===========================================================================
    # 4) BetweenSectionsAndSubsections.MasterSchedule
    #===========================================================================
    class MasterSchedule(SpecialCamp):
                  
        def beginSection(self, writer, first_row, table, count_pages, camper_has_changed):
            table_html = Html.Table().threeCells(
                item.tableCommonStyle().style(),
                item.rowCommonStyle().style(),
                item.cellBlackLeft().style(),
                item.cellBlackCenter().style(),
                item.cellBlackRight().style(),
                self.contentsCellA(first_row),
                self.contentsCellB(first_row, count_pages),
                self.contentsCellC(first_row, count_pages),
                '300', '638', '300') #985 --> 1238
            writer.write(table_html)            
            writer.write('</br>')
            return None
    
        def endSection(self, writer, last_row, htmltable):
            #writer.write('</br>')
            return None

        def beginSubsection(self, writer, row, bookmark, table):        
            return None
    
        def endSubsection(self, writer, monitor, is_final_row, table):
            table.writeRowsOfColor('white', 2)
            return None

        def contentsCellA(self, row): 
            return (
                'Special Camp ' + YEAR_OF_CAMP
            )
        
        def contentsCellB(self, row, count_pages):
            if row['day'] == 'as needed': 
                contents = 'Medications Admin Schedule -- As Needed'
            else:
                contents = 'Medications Admin Schedule -- ' + row['day'] + ', ' + row['date']
            if not count_pages == 1: return contents
            else: return (
                Html.tagSurround('h1',
                    'style="' 
                    + item.rowCommonStyle().style().write() 
                    + item.cellBlackCenter().style().write(),
                    contents
                )
            )
                    
        def contentsCellC(self, row, count_pages): 
            return (
                'Page ' + str(count_pages)
            )

    #===========================================================================
    # 5) BetweenSectionsAndSubsections.CabinAndHsCollapsed
    #===========================================================================
    class CabinAndHsCollapsed(SpecialCamp):
                  
        def beginSection(self, writer, first_row, table, count_pages, camper_has_changed):
            
            table_html = Html.Table().twoCells(
                item.tableCommonStyle().style(),
                item.rowCommonStyle().style(),
                item.cellBlackLeft().style(),
                item.cellBlackRight().style(),
                self.contentsCellA(first_row, count_pages),
                self.contentsCellB(),
                '619', '619') #1238
            writer.write(table_html)
            
            writer.write('<hr style="margin-left:12px; width:1238;">')
            writer.write('</br>')
            
            table_html = Html.Table().oneCell(
                item.tableCommonStyle().style(),
                item.rowCommonStyle().style(),
                item.cellRedLeft().style(),
                self.contentsBelowLine(),
                '1238')
            writer.write(table_html)

            writer.write('</br>')
            return None

        def endSection(self, writer, last_row, htmltable):
            writer.write('</br>')
           
            table_html = Html.Table().oneCell(
                item.tableCommonStyle().style(),
                item.rowCommonStyle().style(),
                item.cellRedBold().style(),
                item.endText2(),
                '1238')
            writer.write(table_html)
            
            #writer.write('</br>')
            return None
    
        def beginSubsection(self, writer, row, bookmark, table):        
            return None
    
        def endSubsection(self, writer, monitor, is_final_row, table):
            table.writeRowsOfColor('white', 2)
            return None
    
        def contentsCellA(self, row, count_pages): 
            contents = 'Camper Med Schedule For:&nbsp;&nbsp;<font style=color:red>' + row['camper'] +'</font>'
            if not count_pages == 1: return contents
            else: return (
                Html.tagSurround('h1',
                    'style="' 
                    + item.rowCommonStyle().style().write() 
                    + item.cellBlackLeft().style().write(),
                    contents
                )
            )
        
        def contentsCellB(self): 
            return 'JEMS Special Camp ' + YEAR_OF_CAMP
        
        def contentsBelowLine(self): 
            return (
                "Camper will receive the following medications/supplements at the indicated times:" )
                
    #===========================================================================
    # 6) BetweenSectionsAndSubsections.LaBusDaysSeparated
    #===========================================================================
    class LaBusDaysSeparated(SpecialCamp):
          
        def beginSection(self, writer, first_row, table, count_pages, camper_has_changed):

            table_html = Html.Table().threeCells(
                item.tableCommonStyle().style(),
                item.rowCommonStyle().style(),
                item.cellBlackLeft().style(),
                item.cellBlackCenter().style(),
                item.cellBlackRight().style(),
                self.contentsCellA(first_row),
                self.contentsCellB(first_row, count_pages),
                self.contentsCellC(first_row, count_pages),
                '250', '738', '250') #1238

                
            writer.write(table_html)            
            
            writer.write('</br>')
            return None
    
        def endSection(self, writer, last_row, htmltable):
            #writer.write('</br>')
            return None

        def beginSubsection(self, writer, row, bookmark, table):        
            return None
    
        def endSubsection(self, writer, monitor, is_final_row, table):
            table.writeRowsOfColor('white', 2)
            return None

        def contentsCellA(self, row): 
            return 'Special Camp ' + YEAR_OF_CAMP
        
        def contentsCellB(self, row): 
            show = 'Los Angeles Bus -- ' + row['day'] + ', ' + row['date']
            if row['day'] == 'as needed':
                show = 'Los Angeles Bus -- ' + 'As Needed'
            return show
        
        def contentsCellB(self, row, count_pages):
            if row['day'] == 'as needed': 
                contents = 'Los Angeles Bus -- As Needed'
            else:
                contents = 'Los Angeles Bus -- ' + row['day'] + ', ' + row['date']
            if not count_pages == 1: return contents
            else: return (
                Html.tagSurround('h1',
                    'style="' 
                    + item.rowCommonStyle().style().write() 
                    + item.cellBlackCenter().style().write(),
                    contents
                )
            )
        


        def contentsCellC(self, row, count_pages): 
            return (
                'Page ' + str(count_pages)
            )

    #===========================================================================
    # 7) BetweenSectionsAndSubsections.LeftoverMeds
    #===========================================================================
    class LeftoverMeds(SpecialCamp):
          
        def beginSection(self, writer, first_row, table, count_pages, camper_has_changed):
            writer.write('</br>')
            table_html = Html.Table().oneCell(
                item.tableCommonStyle().style(),
                item.rowCommonStyle().style(),
                self.beginTextStyle().style(),
                self.beginText(first_row),
                '600')
            writer.write(table_html)
            writer.write('</br>')
            return None
    
        def endSection(self, writer, last_row, htmltable):
            writer.write('</br>')
            table_html = Html.Table().oneCell(
                item.tableCommonStyle().style(),
                item.rowCommonStyle().style(),
                item.cellBlackLeft().style(),
                self.endText(last_row),
                '600')
            writer.write(table_html)
            #writer.write('</br>')
            return None

        def beginSubsection(self, writer, row, bookmark, table):        
            return None
    
        def endSubsection(self, writer, monitor, is_final_row, table):
            return None

        def beginTextStyle(self): return Html.Style(Map({
            'background-color': 'white' ,
            'line-height'     : '21px'  ,
            'font-size'       : '19px'  ,
            'white-space'     : 'normal',
        }))
        
        def beginText(self, row): 
            return (
                '<div style="font-size:19px; font-weight:bold; color:blue; text-align:center; text-decoration:underline">' +
                    '<h1 style="font-size:19px;">Leftover Meds Receipt Acknowledgment - ' + row['camper'] + '</h1>'
                '</div><br />' +
                '<div style="font-size:16px; font-weight:normal; color:green; text-align:left; margin-left:40px">' +
                    'This is to acknowledge that I received the following leftover meds for Special Camper&nbsp;' +
                        '<font style="color:red">' +
                            row['camper'] +
                        '</font>' + 
                    '&nbsp;from the Special Camp Health Supervisor at the end of camp:' +
                '</div>'
            )
            
        def endText(self, row): 
            return (
        '''    
        <div style="font-size:16px;font-weight:normal;color:black;text-align:left;margin-left:40px;line-height:80%">
        <br />
        _________________________________________________________________<br /><br />
        Print Name
        <br />
        <br />
        <br />
        _________________________________________________________________<br /><br />
        Signature
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        Date
        <br />
        <br />
        <br />
        <br />
        <br />
        Notes for LA Bus Campers:        
        <br />
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        Notes/Comments
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;
        Initial
        <br />
        <br />
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        __________________________________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__________<br /><br /><br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        __________________________________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__________<br /><br /><br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        __________________________________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__________<br /><br /><br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        __________________________________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__________<br /><br /><br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        __________________________________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__________<br /><br /><br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        __________________________________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__________<br /><br /><br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        __________________________________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__________<br /><br /><br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        __________________________________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__________<br /><br /><br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        __________________________________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__________<br /><br /><br />
        </div>
        ''')
            
#===============================================================================
# HtmlTable.Meds
#===============================================================================
class Meds(HtmlTable):

    def __init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh): 
        HtmlTable.__init__(self, accumulate, 'CsvTable', 'THIS IS MEDS', is_last_table, website, camperid, day, dest, page, year, refresh)
        
#===============================================================================
# HtmlTable.Meds.SpecialCamp
#===============================================================================
class SpecialCamp:
    
    #===========================================================================
    # HtmlTable.Meds.SpecialCamp.Common
    #===========================================================================
    class Common(Meds):
            
        def __init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh): 
            Meds.__init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh)
            
        def noBlankRows(self):
            return False

        def orientationLandscape(self):
            return True

        def tocHeading(self):
            return 'Medications Admin Schedule'
        
        def tocShow(self):
            return set(['show_pages'])
    
        def getRowColor(self, row):
            return self.colors.getBasedUponTime(row)

        def textWrap(self):
            return Html.TextWrap(
                      width_pixels = 190,
                         font_size = 10,
                       line_height = 12,
                       font_weight = 'bold',
                horizontal_padding = 5,      
                  vertical_padding = 5,
                  chars_to_wrap = 31)
                 
        def determineSpecialFields(self, row):
            scaling = 5.7 + 0.6
            special = dict(row)
            cell = self.textWrap()
            row_height = 0
            for cols in self.html_table.columns():
                if cols.chars_to_wrap != 0:
                    chars_to_wrap = int(round(float(cols.width) / scaling))
                    special[cols.fieldname] = cell.lineWrapped(row[cols.fieldname], chars_to_wrap)
                    row_height = max(row_height, cell.cellHeight())
            special['row_height'] = str(row_height)
            return special
                
                
            special['medication'] = cell.lineWrapped(row['medication'])
            row_height = max(0, cell.cellHeight())
            special['dosage']     = cell.lineWrapped(row['dosage'])
            row_height = max(row_height, cell.cellHeight())
            special['frequency']  = cell.lineWrapped(row['frequency'])
            row_height = max(row_height, cell.cellHeight())
            special['purpose']    = cell.lineWrapped(row['purpose'])
            row_height = max(row_height, cell.cellHeight())
            special['row_height'] = str(row_height)
            return special

        def determineReversedFields(self, row, reset_totals):
            special = dict(row)
            if reset_totals:
                self.running_height = 0
                #self.all_days = ''
                #special['all_days'] = ''
            self.running_height += int(row['row_height'])
            special['running_height'] = str( self.running_height )
            
            #day = str(row['day'])[0:2]
            #special['all_days'] = "Nary"
            #print "new subsection", reset_totals, row['camper'], row['day'], row['medication'], self.all_days
            if False:
                day = str(row['day'])[0:2]
                if day == 'as': self.all_days += "as needed" + " "
                else: self.all_days += day + " "
                print "reversing", row['camper'], row['day'], row['medication'], self.all_days
                special['all_days'] = self.all_days
            
            return special

        def recordsSpecialFields(self, rows_accumulated):
            
            # normal order of rows
            rows_in = rows_accumulated
            rows_out = CsvObject(
                self.folder_out+'SpecialFields1.csv',
                rows_in.fieldnames + ['row_height'])
            
            rows_in.openRead(); rows_out.openWrite()
            for row in rows_in.reader:
                special = self.determineSpecialFields(row)
                rows_out.writer.writerow([special[x] for x in rows_out.fieldnames])
            rows_in.closeRead(); rows_out.closeWrite()            
            
            # reverse the rows
            rows_reversed = self.accumulate.pleaseSort(
                rows_out, self.accumulate.sortOrder(),
                self.folder_out+'Reversed.csv', True)
            
            # accumulate in reverse order of rows
            rows_in = rows_reversed
            rows_out = CsvObject(
                self.folder_out+'SpecialFields2.csv',
                rows_in.fieldnames + ['running_height'])
            
            first_time = True; monitor = MonitorField()
            rows_in.openRead(); rows_out.openWrite();
            for row in rows_in.reader:
                monitor.slideFieldValues(row)
                subsection_has_changed = ( first_time or 
                    monitor.fieldHasChanged(self.fieldsDeterminingSubsection()))
                special = self.determineReversedFields(row, subsection_has_changed)
                rows_out.writer.writerow([special[x] for x in rows_out.fieldnames])
                first_time = False
            rows_in.closeRead(); rows_out.closeWrite()            

            # revert to normal order
            rows_normal = self.accumulate.pleaseSort(
                rows_out, self.accumulate.sortOrder(),
                self.folder_out+'SpecialFields.csv', False)

            return rows_normal

    #===========================================================================
    # 1) HtmlTable.Meds.SpecialCamp.CabinDaysTogether
    #===========================================================================
    class CabinDaysTogether(Common):
            
        def __init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh): 
            SpecialCamp.Common.__init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh)
            
        def getRowColor(self, row):
            return self.colors.getBasedUponDay(row)

        def presentationMainTable(self):
            return MainTable.CabinDaysTogether('CsvTable')

        def betweenSectionsAndSubsections(self):
            if False: print self.title()
            return BetweenSectionsAndSubsections.CabinDaysTogether()
        
        def tocHeading(self):
            return 'Medications Administered in Camper Care Group'
        
        def tocShow(self):
            return set(['camper_pages'])
    
    #===========================================================================
    # 2) HtmlTable.Meds.SpecialCamp.HsDaysSeparated
    #===========================================================================
    class HsDaysSeparated(Common):
    
        def __init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh): 
            SpecialCamp.Common.__init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh)
    
        def presentationMainTable(self):
            return MainTable.HsDaysSeparated('CsvTable')

        def betweenSectionsAndSubsections(self):
            return BetweenSectionsAndSubsections.HsDaysSeparated()

        def tocHeading(self):
            return 'Medications Administered By Health Supervisor (For Health Supervisor)'

        def tocShow(self):
            return set(['camper_day_pages'])
            return set(['camper_pages'])
            return set(['camper_days'])

    #===========================================================================
    # 3) HtmlTable.Meds.SpecialCamp.HsDaysCollapsed
    #===========================================================================
    class HsDaysCollapsed(Common):
    
        def __init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh): 
            SpecialCamp.Common.__init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh)

        def presentationMainTable(self):
            return MainTable.HsDaysCollapsed('CsvTable')

        def betweenSectionsAndSubsections(self):
            return BetweenSectionsAndSubsections.HsDaysCollapsed()
        
        def tocHeading(self):
            return 'Medications Administered By Health Supervisor (For Cabin Lead)'

        def noBlankRows(self):
            return True
        
        def tocShow(self):
            return set(['camper_pages'])

    #===========================================================================
    # 4) HtmlTable.Meds.SpecialCamp.MasterSchedule
    #===========================================================================
    class MasterSchedule(Common):
    
        def __init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh): 
            SpecialCamp.Common.__init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh)

        def presentationMainTable(self):
            return MainTable.MasterSchedule('CsvTable')

        def betweenSectionsAndSubsections(self):
            return BetweenSectionsAndSubsections.MasterSchedule()
        
        def tocHeading(self):
            return 'Master Schedule'

        def tocShow(self):
            return set(['day_pages'])

    #===========================================================================
    # 5) HtmlTable.Meds.SpecialCamp.CabinAndHsCollapsed
    #===========================================================================
    class CabinAndHsCollapsed(Common):
    
        def __init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh): 
            SpecialCamp.Common.__init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh)

        def presentationMainTable(self):
            return MainTable.CabinAndHsCollapsed('CsvTable')

        def betweenSectionsAndSubsections(self):
            return BetweenSectionsAndSubsections.CabinAndHsCollapsed()
        
        def tocHeading(self):
            return 'Guardian Signature Sheet'

        def tocShow(self):
            return set(['camper_pages'])

    #===========================================================================
    # 6) HtmlTable.Meds.SpecialCamp.LaBusDaysSeparated
    #===========================================================================
    class LaBusDaysSeparated(Common):
    
        def __init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh): 
            SpecialCamp.Common.__init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh)
    
        def presentationMainTable(self):
            return MainTable.LaBusDaysSeparated('CsvTable')

        def betweenSectionsAndSubsections(self):
            return BetweenSectionsAndSubsections.LaBusDaysSeparated()
        
        def tocHeading(self):
            return 'Medications Administered During LA Bus Trip'

        def tocShow(self):
            return set(['day_pages'])
        
    #===========================================================================
    # 7) HtmlTable.Meds.SpecialCamp.LeftoverMeds
    #===========================================================================
    class LeftoverMeds(Common):
    
        def __init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh): 
            SpecialCamp.Common.__init__(self, accumulate, is_last_table, website, camperid, day, dest, page, year, refresh)
    
        def presentationMainTable(self):
            return MainTable.LeftoverMeds('CsvTable')

        def betweenSectionsAndSubsections(self):
            return BetweenSectionsAndSubsections.LeftoverMeds()

        def tocHeading(self):
            return 'Leftover Medications'
        
        def tocShow(self):
            return set(['camper_pages'])
            return set(['camper_only'])
        
        def orientationLandscape(self):
            return False

#===============================================================================
# helper functions
#===============================================================================
def TopOfHsMeds(camper_name, day, date):
    print "DAY", day
    showday = str(day)
    if day == 'as needed': showday = 'As Needed'
    if False: print day, showday
    
    return (
    '''
    <table>
    <col style=width:33%>
    <col style=width:24%>
    <col style=width:33%>
    <tr style="background-color:white;">
    <td style="border-style:hidden;color:black;font-size:0.9em;
        font-weight:bold;text-align:left;margin-left:20px;line-height:150%;">
    Camper&nbsp;Name:&nbsp;&nbsp;<font color="red">
    '''
    + camper_name +
    '''
    </font></td>
    <td style="border-style:hidden;color:black;font-size:1.1em;
        font-weight:bold;text-align:center;margin-left:0px;line-height:20px;">
    '''
    + showday +
    '''
    <font style=font-size:0.6em; line-height:20px;><br />
    '''
    + date +
    '''
    </font></td>
    <td style="border-style:hidden;color:black;font-size:1.0em;
        font-size:0.8em;font-weight:bold;text-align:right;
        margin-left:0px;line-height:25px;">
    Camper&nbsp;Care&nbsp;Group:&nbsp;_______________________________<br />
    Camper&nbsp;Care&nbsp;Lead:&nbsp;_______________________________</td>
    </tr>
    </table>
    ''')
