'''
    Database.TransformRow.Finance
'''

import re, copy
from classes.utils import Container, CsvObject
from classes.database.Account import Account

from classes.database.Database import Database
from classes.database import Row
from classes.database import TransformRow

super = TransformRow

PLEASE_IMPLEMENT = True

#===============================================================================
# (1) HowToCombineOriginalFiles
#===============================================================================
class HowToCombineOriginalFiles(super.HowToCombineOriginalFiles):
    def __init__(self):
        super.HowToCombineOriginalFiles.__init__(self)

#===============================================================================
# (2) HowToValidateAndNormalizeTheFields
#===============================================================================
class HowToValidateAndNormalizeTheFields(super.HowToValidateAndNormalizeTheFields):
    def __init__(self, csv_in):
        super.HowToValidateAndNormalizeTheFields.__init__(self, csv_in)

#===============================================================================
# (3) HowToDeriveNewFields
#===============================================================================
class HowToDeriveNewFields(super.HowToDeriveNewFields):
    def __init__(self, csv_in):
        super.HowToDeriveNewFields.__init__(self, csv_in)

#===============================================================================
# (4) HowToSortTheRows
#===============================================================================
class HowToSortTheRows(super.HowToSortTheRows):
    def __init__(self, csv_in):
        print "got to Finance"
        super.HowToSortTheRows.__init__(self, csv_in)
                
#===============================================================================
# (5) HowToCollapseOnFields
#===============================================================================
class HowToCollapseOnFields(super.HowToCollapseOnFields):
    def __init__(self, csv_in):
        super.HowToCollapseOnFields.__init__(self, csv_in)
        
#===============================================================================
# (6) HowToSelectTheRows
#===============================================================================
class HowToSelectTheRows(super.HowToSelectTheRows):
    def __init__(self, csv_in):
        super.HowToSelectTheRows.__init__(self, csv_in)
        
#===============================================================================
# (7) HowToAccumulateNewColumns
#===============================================================================
class HowToAccumulateNewColumns(super.HowToAccumulateNewColumns):
    def __init__(self, csv_in):
        super.HowToAccumulateNewColumns.__init__(self, csv_in)
        
#===============================================================================
# (8) HowToFinallyModifyCertainFields
#===============================================================================
class HowToFinallyModifyCertainFields(super.HowToFinallyModifyCertainFields):
    def __init__(self, csv_in):
        super.HowToFinallyModifyCertainFields.__init__(self, csv_in)

#===============================================================================
# Common
#===============================================================================
class Common():  

    def usefulFields(self): return list([
        'Date',
        'Amount',
        'TransferMech1',
        'TransferMech2',
        'AccountAlias'
    ])
     
    def derivedFields(self): return list([
        'Credit',
        'Debit',
        'Year',
        'YearMonth',
        'Mechanism',
        'SimplifiedAlias',
        'Account',
        'Subcategory',
        'Category',
        'CenterAccount',
        'OrbitAccount',
        'FromAccount',
        'ToAccount',
        'Institution',
    ])
    
    def accumulatedFields(self): return list([
        'NumberTransactions',
        'RunningTotal',
        'SectionTotal',
        'SectionCredit',
        'SectionDebit',
        'MonthTotal',
        'MonthCredit',
        'MonthDebit',
        'YearTotal',
        'YearCredit',
        'YearDebit',
    ])
    
common = Common()

#===============================================================================
# (1) HowToCombineOriginalFiles
#===============================================================================
class HowToCombineOriginalFiles(super.HowToCombineOriginalFiles):
    
    def __init__(self):
        super.HowToCombineOriginalFiles.__init__(self)
    
    def usefulFields(self):
        return common.usefulFields()
       
#===============================================================================
# (1) HowToCombineOriginalFiles2
#===============================================================================
class HowToCombineOriginalFiles2(super.HowToCombineOriginalFiles2):
    
    def __init__(self, csv_in):
        super.HowToCombineOriginalFiles2.__init__(self, csv_in)
    
    def usefulFields(self):
        return common.usefulFields()
    
    def transformRow(self, row_in, csv_in, csv_out):
        row_out = self.initializeRowOut(row_in, csv_in, csv_out)
        
        row_out['Date'] = row_in['Trans Date']
        row_out['Amount'] = row_in['Amount']
        row_out['TransferMech1'] = row_in['Type']
        row_out['TransferMech2'] = row_in['Type']
        row_out['AccountAlias'] = row_in['Description']
        
        rows = Container.VectorOfString()    
        rows.append(row_out)   
        return rows
   
#===============================================================================
# (2) HowToValidateAndNormalizeTheFields
#===============================================================================        
class HowToValidateAndNormalizeTheFields(super.HowToValidateAndNormalizeTheFields):
    
    if PLEASE_IMPLEMENT:
        def normalizeAmountField(self): MethodNotImplemented()
        def normalizeDateField(self):   MethodNotImplemented()
    
    def __init__(self, csv_in):
        self.processRow = Row.HowToValidateAndNormalizeTheFields()
        super.HowToValidateAndNormalizeTheFields.__init__(self, csv_in)
        
    def usefulFields(self):
        return common.usefulFields()

    def normalizeAmountField(self, amount_text, row):
        as_float = Container.getFloat(amount_text)
        return  Container.formatDollars(as_float)

    def determineAmount(self, field, row, out):
        if ((field == 'Amount')
        or  (field == 'AmountPositive')
        or  (field == 'Adjusted')):
            amount = self.normalizeAmountField(row['Amount'], row)
            #amount = getAsPositive(row['Amount'])
            return True, amount      
        return False, '0.0'

    def normalizeDateField(self, date_text):
        return Container.convertDateWithSlashes(date_text)
 
    def transformRow(self, row_in, csv_in, csv_out):
        
        #return self.processRow.transform(row_in)

        row_out = self.initializeRowOut(row_in, csv_in, csv_out)              

        row_out['Amount'] = \
            self.normalizeAmountField(row_in['Amount'], row_in)
       
        row_out['Date'] = \
            self.normalizeDateField(row_in['Date'])
            
        row_out['TransferMech1'] = \
            row_in['TransferMech1']
            
        row_out['TransferMech2'] = \
            row_in['TransferMech2']

        row_out['AccountAlias'] = \
            row_in['AccountAlias']

        return Container.VectorOfString(row_out);
   
#===============================================================================
# (3) HowToDeriveNewFields
#===============================================================================        
class HowToDeriveNewFields(super.HowToDeriveNewFields):
    
    if PLEASE_IMPLEMENT:
        def usefulFields(self):        MethodNotImplemented()
        def derivedFields(self):       MethodNotImplemented()
        def getMethodOfPayment(self): MethodNotImplemented()
        def getAccountTitle(self):     MethodNotImplemented()
        def getSubcategory(self):      MethodNotImplemented()
        def getCategory(self):         MethodNotImplemented()
    
    def __init__(self, csv_in):
        super.HowToDeriveNewFields.__init__(self, csv_in)
    
    def usefulFields(self):
        return common.usefulFields()

    def derivedFields(self):
        return common.derivedFields()
    
    def getCategory(self, account_title):
        if account_title in self.map_title_to_account.keys():
            return self.map_title_to_account[account_title].category
        else:
            return "CATEGORY NOT FOUND"
   
    def getSubcategory(self, account_title):
        if account_title in self.map_title_to_account.keys():
            return self.map_title_to_account[account_title].subcategory
        else:
            return "SUB-CATEGORY NOT FOUND"
    
    def getMethodOfPayment(self, mechanism1, mechanism2):
        if not ("map_mechanisms" in dir(self)):
            self.map_mechanisms = dict()
            self.map_mechanisms['SALE'] = 'Credit Card Purchase'
            self.map_mechanisms['RETURN'] = 'Credit Card Refund'
            self.map_mechanisms['PAYMENT'] = 'Beyond Banking Transfer'
            self.map_mechanisms['ADJUSTMENT'] = 'Chase Rewards'
        if mechanism1 in self.map_mechanisms.keys():
            return self.map_mechanisms[mechanism1]
        else:
            return 'UNKNOWN MECHANISM'
            
    def getAccountTitle(self, alias, mechanism1, mechanism2):
        simplified = Container.String(alias).removeBlanksAndNumbers()
        if simplified in self.map_alias_to_title.keys():
            return self.map_alias_to_title[simplified]
        else:
            return alias

    def createAccount(self, title_in, alias_in, category_in, subcategory_in):
        title = Container.String(title_in).whiteSpaceToBlank()
        alias = Container.String(alias_in).removeBlanksAndNumbers().upper()
        category = Container.String(category_in).whiteSpaceToBlank()
        subcategory = Container.String(subcategory_in).whiteSpaceToBlank()
        if not title in self.map_title_to_account.keys():
            account = Account(title, category, subcategory)
            account.addAlias(alias)
            self.map_alias_to_title[alias] = title
            self.map_title_to_account[title] = account
        else:
            account = self.map_title_to_account[title]           
            account.addAlias(alias)  
            self.map_alias_to_title[alias] = title
        return None
    
    def transformRow(self, row_in, csv_in, csv_out):
        row_out = self.initializeRowOut(row_in, csv_in, csv_out)              
        
        row_out['AmountPositive'] = row_in['Amount']
        row_out['Adjusted'] = row_in['Amount']
       
        amount = row_in['Amount']
        no_commas = re.sub(',','', amount)
        if float(no_commas) >= 0.0:
            row_out['Credit'] = amount
        else:
            row_out['Credit'] = ''


        if float(no_commas) < 0.0:
            row_out['Debit'] = amount
        else:
            row_out['Debit'] = ''

        row_out['Year'] = \
            Container.convertStandardDateToYear(row_in['Date'])

        row_out['YearMonth'] = \
            Container.convertStandardDateToYearMonth(row_in['Date'])

        row_out['Mechanism'] = \
        mech = self.getMethodOfPayment(
            row_in['TransferMech1'], row_in['TransferMech2'] )
        if row_in['TransferMech1'] == "Checking":
            show_check_number = re.sub(
                'Check','Paper Check ',row_in['TransferMech2'])
            row_out['Mechanism'] = show_check_number
        elif row_in['TransferMech2'] == "Bill Payment":
            show_check_number = re.sub(
                'THE LION OF JUDA00','ML BillPay Check ',row_in['AccountAlias'])
            row_out['Mechanism'] = show_check_number
        else:
            row_out['Mechanism'] = mech

        self.simplified_alias = re.sub('[0123456789]+', '', row_in['AccountAlias'])
        self.simplified_alias = Container.String(self.simplified_alias).removeBlanks()
        row_out['SimplifiedAlias'] = self.simplified_alias
        row_out['SimplifiedAlias'] = Container.String(row_in['AccountAlias']).removeBlanksAndNumbers()


        self.account_name = self.getAccountTitle(
            row_in['AccountAlias'],
            row_in['TransferMech1'],
            row_in['TransferMech2'],
        )
        
        row_out['Account'] = \
            self.account_name

        row_out['Institution'] = \
            'self.institutionName()'

        row_out['CenterAccount'] = \
            'self.centerAccount()'

        row_out['OrbitAccount'] = \
            self.account_name

        if Container.getFloatNoCommas(row_in['Amount']) < 0.0:
            row_out['FromAccount'] = 'self.centerAccount()'
        else:
            row_out['FromAccount'] = self.account_name

        if Container.getFloatNoCommas(row_in['Amount']) < 0.0:
            row_out['ToAccount'] = self.account_name
        else:
            row_out['ToAccount'] = 'self.centerAccount()'
        
        row_out['Subcategory'] = \
            self.getSubcategory(self.account_name)

        row_out['Category'] = \
            self.getCategory(self.account_name)
            
        rows = Container.VectorOfString()    
        rows.append(row_out)   
        if row_out['Account'] == "Borrow from Other ML":
            additional = copy.deepcopy(row_out)
            additional['Amount'] = "-" + row_out['Amount']                        
            rows.append(additional) 

        return rows

#===============================================================================
# (5) HowToCollapseOnFields
#===============================================================================
class HowToCollapseOnFields(super.HowToCollapseOnFields):
    
    def __init__(self, csv_in):
        super.HowToCollapseOnFields.__init__(self, csv_in)
    
    def usefulFields(self):
        return common.usefulFields()

#===============================================================================
# (6) HowToSelectTheRows
#===============================================================================
class HowToSelectTheRows(super.HowToSelectTheRows):

    def __init__(self, csv_in):
        super.HowToSelectTheRows.__init__(self, csv_in)
        return None
    
    def usefulFields(self):
        return common.usefulFields()
    
    def derivedFields(self):
        return common.derivedFields()
    
#===============================================================================
# (7) HowToAccumulateNewColumns
#===============================================================================
class HowToAccumulateNewColumns(super.HowToAccumulateNewColumns):
    
    def __init__(self, csv_in):
        print "Selected", csv_in.fieldnames 
        super.HowToAccumulateNewColumns.__init__(self, csv_in)


    def accumulatedFields(self):
        return common.accumulatedFields()
    
    def collapseOnFields(self): return list([
    ])
            
    def afterSortRestoreAndAccumulate(self, field, row):

        if (field == 'NumberTransactions'):
            return self.running_totals.getNumberTransactions()

        elif (field == 'RunningTotal'):
            return self.running_totals.getRunningTotal()

        elif (field == 'SectionTotal'):
            return self.running_totals.getSection()

        elif (field == 'SectionCredit'):
            return self.running_totals.getCredit()

        elif (field == 'SectionDebit'):
            return self.running_totals.getDebit()

        elif (field == 'MonthTotal'):
            return self.month_totals.getSection()

        elif (field == 'MonthCredit'):
            return self.month_totals.getCredit()

        elif (field == 'MonthDebit'):
            return self.month_totals.getDebit()

        elif (field == 'YearTotal'):
            return self.year_totals.getSection()

        elif (field == 'YearCredit'):
            return self.year_totals.getCredit()

        elif (field == 'YearDebit'):
            return self.year_totals.getDebit()

        else:
            return row[field]
        
    def forEachRow(self, csv_in):
        
        def checkForChanges(row):
            self.monitor_unique.slideFieldValues(row)
            self.monitor.slideFieldValues(row)
            unique_has_changed = self.monitor_unique.fieldHasChanged(self.collapseOnFields())
            field_list = self.sectionChange() + self.subsectionChange()
            field_has_changed  = self.monitor.fieldHasChanged(field_list)
            month_has_changed  = self.monitor.fieldHasChanged(['YearMonth'])
            year_has_changed   = self.monitor.fieldHasChanged(['Year'])
            # FIX THIS
            if 'Amount' in row.keys():
                self.running_totals.accumulate(row['Amount'], field_has_changed)
                self.month_totals.accumulate(row['Amount'], month_has_changed)
                self.year_totals.accumulate(row['Amount'], year_has_changed)
            return unique_has_changed

        rows_selected = csv_in
        fieldnames = rows_selected.fieldnames + self.accumulatedFields()
        rows_accumulated = self
        
        rows_selected.openRead(); rows_accumulated.openWrite()
        for row in rows_selected.reader:
            unique_has_changed = checkForChanges(row)
            out = dict()
            for x in rows_accumulated.fieldnames:
                out[x] = self.afterSortRestoreAndAccumulate(x, row)
                out[x] = Container.String(out[x]).whiteSpaceToBlank()
            if len(self.collapseOnFields()) == 0 or unique_has_changed:
                fields_out = [out[x] for x in rows_accumulated.fieldnames]
                rows_accumulated.writer.writerow(fields_out)            
        rows_selected.closeRead(); rows_accumulated.closeWrite()
        
        if False: print "The new accumulated .csv file is", rows_accumulated.filename
        return rows_accumulated
      

#===============================================================================
# (8) HowToFinallyModifyCertainFields
#===============================================================================
class HowToFinallyModifyCertainFields(super.HowToFinallyModifyCertainFields):
    
    def __init__(self, csv_in):
        super.HowToFinallyModifyCertainFields.__init__(self, csv_in)
    
    def presentTheseFields(self):
        return common.usefulFields() + common.derivedFields() + common.accumulatedFields()
