'''
    namespace src.finance.SelectColumns
'''

import collections
from utils.Container import *
from utils import Html


#===============================================================================
# TableFinance
#===============================================================================
class TableFinance(Html.Table):
    def __init__(self, table_name):
        Html.Table.__init__(self, table_name)

    #===========================================================================
    # table styles
    #===========================================================================
    def tableStyle(self): return Html.Style(Map({

        'font-family'     : 'Verdana, Geneva, sans-serif'       ,
        'border-collapse' : 'collapse'                          ,
        'width'           : '0%'                                ,
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

    def columns(self):
        
        nature_of_columns = ([
        self.cfg('Date'              , 'Date'              ,   0,    'date', '1.0', 0 ),
        self.cfg('Mechanism'         , 'Method of Transfer',   0, 'nowrapl', '1.0', 0 ),
        self.cfg('Amount'            , 'Amount'            ,   0,   'funds', '1.0', 0 ),
        self.cfg('FromAccount'       , 'Funds From'        ,   0, 'nowrapl', '1.0', 0 ),
        self.cfg('ToAccount'         , 'Have Been Transferred To',   0, 'nowrapl', '1.0', 0 ),
        self.cfg('Category'          , 'Category'          ,   0, 'nowrapl', '1.0', 0 ),
        self.cfg('Subcategory'       , 'Subcategory'       ,   0, 'nowrapl', '1.0', 0 ),
        self.cfg('AccountAlias'      , 'Details'           , 100,  'whitel', '1.0', 0 ),
        #self.cfg('RunningTotal'     , 'Running'           ,   0,   'funds', '1.0', 0 ),
        ])
        
        return nature_of_columns



########################################################################
# SelectColumns.Simple
########################################################################
class Simple():
    def __init__(self, split=True): 
        self.split = split
        pass
    
    def splitSectionsIntoSeparateFiles(self):
        return self.split
    
    def repeatHeadings(self):
        return True
    
    def showMonthlyAverage(self):
        return True
    
    def textOfMechanism(self):
        return "Mechanism Column"
    
    def textOfAccount(self): 
        return "Account Column"
    
    
    def column0s(self, heading_account):
        if not hasattr(self, 'cfg'):
            self.cfg = collections.namedtuple( 'ConfigureColumns',
            'fieldname, heading, width, CellStyle, fontsize' )
        
        nature_of_columns = ([
        self.cfg('Date'         , 'Date'                    ,   0,    'date', '1.0' , 0 ),
        self.cfg('Mechanism'    , 'Method of Transfer'      ,   0, 'nowrapl', '1.0' , 0),
        self.cfg('Amount'       , 'Amount'                  ,   0,   'funds', '1.0' , 0),
        self.cfg('FromAccount'  , 'Funds From'              ,   0, 'nowrapl', '1.0' , 0),
        self.cfg('ToAccount'    , 'Have Been Transferred To',   0, 'nowrapl', '1.0' , 0),
        self.cfg('Category'     , 'Category'                ,   0, 'nowrapl', '1.0' , 0),
        self.cfg('Subcategory'  , 'Subcategory'             ,   0, 'nowrapl', '1.0' , 0),
        self.cfg('AccountAlias' , 'Details'                 , 100,  'whitel', '1.0' , 0),
        ])
        
        return nature_of_columns    
    
    def tableStyle1(self): return Html.Style(Map({
        'border-collapse' : 'collapse'                          ,
        'width'           : '100%'                              ,
        'table-layout'    : 'auto'                              ,
    }))
    
    def rowStyle1(self): return Html.Style(Map({
        'font-family'     : 'Verdana, Geneva, sans-serif'       ,
        'font-size'       : '14px'                              ,
        'line-height'     : '14px'                              ,
        'text-align'      : 'left'                              ,
    }))
 
 
     #h1.hidden {visibility:hidden;}
    #h1.hidden {display:none;}

 
    
    def beginSection(self, writer, first_row, table, count_pages, start_new_section):
        text = VectorOfString()
        text.append( ''                                     )
        text.append( '<table style='                        )
        text.concat(     self.tableStyle1().style()          )
        text.append( '>'                                    )
        text.append( '   <col style=width:80%>'                   )
        text.append( '   <col style=width:20%>'                   )
        text.append( '   <tr style='                        )
        text.concat(        self.rowStyle1().style()         )
        text.append( '   >'                                 )
        text.append( '      <td>'                           )
        text.append( '         THIS IS BEGIN SECTION LEFT'  )
        text.append( '      </td>'                          )
        text.append( '      <td>'                           )
        text.append( '         THIS IS BEGIN SECTION RIGHT' )
        text.append( '      </td>'                          )
        text.append( '   </tr>'                             )
        text.append( '</table>'                             )
        text.append( ''                                     )
        writer.write(text.write())
        return None
                       
    def endSection(self, writer, last_row, htmltable):
        return None

    def beginSubsection(self, writer, row, bookmark, table):
        return None
        writer.write( table.select_columns.table.standardTableBegin() )
        return None
        writer.write( table.select_columns.table.tableBegin() )
        writer.write( table.select_columns.table.tableWidths() )
        writer.write( table.bookmark(bookmark) )
        writer.write( table.tableHeadings() )
        return None
    
    def endSubsection(self, writer, monitor, is_final_row, table):
        # check if this is last row of the file
        bottom_row_prev_section = monitor.prev_fields
        last_row_of_csv_file = monitor.new_fields
        if is_final_row:
            row = last_row_of_csv_file
        else:
            row = bottom_row_prev_section

        if True or self.printDetails():
            table.summaryFollowingDetails(table.howManyBlankRows(), row)
        else:
            table.summaryRecordsOnly(table.howManyBlankRows(), row,
                'SectionTotal', 'SectionCredit', 'SectionDebit' )
            if monitor.fieldHasChanged('Year') or is_final_row:
                table.summaryRecordsOnly(1, row,
                    'YearTotal', 'YearCredit', 'YearDebit' )
        return None

    
########################################################################
# SelectColumns.FinanceDetails
########################################################################
class FinanceDetails(Simple):
    def __init__(self, split=True):
        Simple.__init__(self, split)

    def textOfMechanism(self): return "Income"
    def textOfAccount(self): return "Put Account Here"
    
    ####################################################################
    # the standard columns for a finance report
    ####################################################################
    def columns0(self, heading_account):
        if not hasattr(self, 'cfg'):
            self.cfg = collections.namedtuple( 'ConfigureColumns',
            'fieldname, heading, width, CellStyle, fontsize' )
        
        nature_of_columns = ([
        self.cfg('Date'              , 'Date'              ,   0,    'date', '1.0' ),
        self.cfg('TransferMech1'     , 'Method1'           ,   0,  'whitel', '1.0' ),
        self.cfg('TransferMech2'     , 'Method2'           ,   0,  'whitel', '1.0' ),
        self.cfg('Mechanism'         , 'Method of Transfer',   0, 'nowrapl', '1.0' ),
        self.cfg('Amount'            , 'Amount'            ,   0,   'funds', '1.0' ),
        self.cfg('FromAccount'       , 'Funds From'    ,   0, 'nowrapl', '1.0' ),
        self.cfg('ToAccount'         , 'Have Been Transferred To'      ,   0, 'nowrapl', '1.0' ),
        self.cfg('Category'          , 'Category'          ,   0, 'nowrapl', '1.0' ),
        self.cfg('Subcategory'       , 'Subcategory'       ,   0, 'nowrapl', '1.0' ),
        self.cfg('NumberTransactions', 'Transaction'       ,   0,  'whiter', '1.0' ),
        self.cfg('RunningTotal'      , 'Running'           ,   0,   'funds', '1.0' ),
        self.cfg('Institution'       , 'Database'          ,   0, 'nowrapl', '1.0' ),
        self.cfg('CenterAccount'     , 'Center Account'    ,   0, 'nowrapl', '1.0' ),
        self.cfg('OrbitAccount'      , 'Orbit Account'     ,   0, 'nowrapl', '1.0' ),
        self.cfg('AccountAlias'      , 'Details'           , 100,  'whitel', '1.0' ),
        ])
        
        return nature_of_columns
    
########################################################################
# SelectColumns.FinanceStandard
########################################################################
class FinanceStandard(Simple):
    def __init__(self, split=True):
        Simple.__init__(self, split)
        pass
    
    def textOfMechanism(self):
        return "Mechanism Column"
    
    def textOfAccount(self): 
        return "Account Column"
    

    #===========================================================================
    # example of special begin section
    #===========================================================================
    def tableBeginOneByTwo(self):
        text = '<table id="' +'OneByTwo'+ '">\n'
        return text
    
    def tableWidthsOneByTwo(self):
        text = ''
        for next in [0,0]:
            text += '   <col style=width:' + '0' + '%>\n'
        return text        

    def beginSection(self, writer, first_row, table, count_pages, start_new_section):
        writer.write( self.tableBeginOneByTwo() )
        writer.write( self.tableWidthsOneByTwo() )
        writer.write( '<tr>\n' )
        writer.write( '   <td style="font-size:1.2em; line-height:1.2em; text-align:left; ">' )
        writer.write( '</br>Dear '+first_row['Account']+',</br></br>\n' )
        writer.write( '&nbsp;&nbsp;Thank you for your faithful donations to Faraja Orphans Rescue Ministry.</br>\n' )
        writer.write( '&nbsp;&nbsp;Below you will see your donations sent through Paypal. God bless you.</br>\n' )
        writer.write( '</br>Kurt Wegner</br></br></br>\n' )
        writer.write( '</td>\n' )
        writer.write( '</tr>\n' )
        writer.write( '</table>\n' )

    #===========================================================================
    # section begin and end
    #===========================================================================
    def beginSection(self, writer, first_row, table, count_pages):
        return None
               
    def endSection(self, writer, last_row, htmltable):
        return None

########################################################################
# SelectColumns.FormDonations
########################################################################
class FormDonations(Simple):
    def __init__(self, split=True):
        Simple.__init__(self, split)

    def showMonthlyAverage(self): return False
    def textOfMechanism(self): return "Total Received"
    def textOfAccount(self): return ""
    
    ####################################################################
    # the standard columns for a finance report
    ####################################################################
    def columns0(self, heading_account):
        if not hasattr(self, 'cfg'):
            self.cfg = collections.namedtuple( 'ConfigureColumns',
            'fieldname, heading, width, CellStyle, fontsize' )
        
        nature_of_columns = ([
        self.cfg('Date'              , 'Date'              ,   0,    'date', '1.0' ),
        self.cfg('Mechanism'         , 'Method of Transfer',   0, 'nowrapr', '1.0' ),
        self.cfg('Amount'            , 'Amount'            ,   0,   'funds', '1.0' ),
        self.cfg('FromAccount'       , 'Donor'             ,   0, 'nowrapl', '1.0' ),
        #self.cfg('ToAccount'         , 'Have Been Transferred To'      ,   0, 'nowrapl', '1.0' ),
        #self.cfg('Category'          , 'Category'          ,   0, 'nowrapl', '1.0' ),
        #self.cfg('Subcategory'       , 'Subcategory'       ,   0, 'nowrapl', '1.0' ),
        ])
        
        return nature_of_columns



        
