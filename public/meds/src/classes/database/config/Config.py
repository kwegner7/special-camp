'''
    Config
'''

from classes.utils.CsvObject import CsvObject, CsvFolder, CsvStandardDialect, FolderOfCsvObjects
from classes.utils import Container
from classes.database.Account import Account

PLEASE_CAPITALIZE = True

#===============================================================================
# helpers
#===============================================================================
class Helpers():  

    def HowToCombineFromFolder(self):
        Container.clearFolder(self.folderOut() + self.csvFolder())
        file_out = self.folderOut() + self.csvFolder() + 'OriginalsCombined0.csv'
    
        csv_folder = CsvFolder( self.folderIn(),
            self.originalFields(), 
            self.dialect(), 
            self.skipFirstRecord() )
        csv_objects = FolderOfCsvObjects(file_out, csv_folder)
        csv_originals = csv_objects.combineIntoOneCsvObject(not PLEASE_CAPITALIZE)
        return csv_originals

    def HowToCollapseOnFields(self, row_in):          
        row_out = dict(row_in)
        matches = True
        if 'prev_collapse_row' not in dir(self):
            self.prev_collapse_row = row_in
            matches = False
        elif len(self.collapseOnFields()) == 0:
            matches = False
        else:
            for field in self.collapseOnFields():
                if self.prev_collapse_row[field] != row_in[field]:
                    matches = False
        if not matches:
            please_write_row = True
        else:
            please_write_row = False
        self.prev_collapse_row = row_in
        return please_write_row, row_out
    
    def HowToSelectTheRows(self, row_in):          
        row_out = dict(row_in)
        if self.isSelectedRow(row_in):
            please_write_row = True
        else:
            please_write_row = False
        return please_write_row, row_out
    
    def HowToAccumulateNewColumns(self, csv_in, csv_out): 
        
        def forEachRow(csv_in, csv_out):
            
            def checkForChanges(row):
                monitor_unique.slideFieldValues(row)
                monitor.slideFieldValues(row)
                unique_has_changed = monitor_unique.fieldHasChanged(collapseOnFields)
                field_list = self.sectionChange() + self.subsectionChange()
                field_has_changed  = monitor.fieldHasChanged(field_list)
                month_has_changed  = monitor.fieldHasChanged(['YearMonth'])
                year_has_changed   = monitor.fieldHasChanged(['Year'])
                # FIX THIS
                if 'Amount' in row.keys():
                    self.running_totals.accumulate(row['Amount'], field_has_changed)
                    self.month_totals.accumulate(row['Amount'], month_has_changed)
                    self.year_totals.accumulate(row['Amount'], year_has_changed)
                return unique_has_changed
    
            rows_selected = csv_in
            fieldnames = rows_selected.fieldnames + self.accumulatedFields()
            rows_accumulated = csv_out
            
            rows_selected.openRead(); rows_accumulated.openWrite()
            for row in rows_selected.reader:
                unique_has_changed = checkForChanges(row)
                out = dict()
                for x in rows_accumulated.fieldnames:
                    out[x] = self.afterSortRestoreAndAccumulate(x, row)
                    out[x] = Container.String(out[x]).whiteSpaceToBlank()
                if len(collapseOnFields) == 0 or unique_has_changed:
                    fields_out = [out[x] for x in rows_accumulated.fieldnames]
                    rows_accumulated.writer.writerow(fields_out)            
            rows_selected.closeRead(); rows_accumulated.closeWrite()
            return rows_accumulated
        
        collapseOnFields = list([])   
        monitor_unique = Container.MonitorField()
        monitor = Container.MonitorField()
        self.running_totals = Container.RunningTotals() # RunningTotals(14119.05)
        self.month_totals = Container.RunningTotals()
        self.year_totals = Container.RunningTotals()
        forEachRow(csv_in, csv_out)
        return csv_out

    def normalizeAmountField(self, amount_text, row):
        as_float = Container.getFloat(amount_text)
        return  Container.formatDollars(as_float)
    
    def normalizeDateField(self, date_text):
        return Container.convertDateWithSlashes(date_text)
    
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

#===============================================================================
# common to all databases
#===============================================================================
class ConfigDatabase(Helpers):  

    def folderOut(self):
        return Container.TheBaseFolder.location + "/out/"
    
    def csvFolder(self):
         return "csv/"

    def sortedFilename(self):
        return self.folderOut() + "csv/Sorted.csv"
    
    def accumulatedFilename(self):
        return self.folderOut() + "csv/Accumulated.csv"
'''    
#===============================================================================
# common to a category of database
#===============================================================================
class ConfigDatabaseCatagory(ConfigDatabase):  

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

    #===========================================================================
    # HowToValidateAndNormalizeTheFields
    #===========================================================================
    def HowToValidateAndNormalizeTheFields(self, row_in):
        
        row_out = dict(row_in)
        
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
            
        return True, row_out

    #===========================================================================
    # HowToDeriveNewFields
    #===========================================================================
    def HowToDeriveNewFields(self, row_in):
        
        if 'map_title_to_account' not in dir(self):
            self.initializeAccounts()
        
        row_out = dict(row_in)

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
            
        return True, row_out
    
#===============================================================================
# configure a particular institution within the category
#===============================================================================
class ConfigInstitution(ConfigDatabaseCatagory):  

    def folderIn(self):
        return "/home/kurt/ubu/finances/Chase/download/" 

    def originalFields(self): return list([
        "Type",
        "Trans Date",
        "Post Date",
        "Description",
        "Amount",
    ])

    def dialect(self):
        return CsvStandardDialect()

    def skipFirstRecord(self):
        return True

    #===========================================================================
    # HowToCombineOriginalFiles
    #===========================================================================
    def HowToCombineOriginalFiles(self, row_in):
        row_out = dict()
        row_out['Date'] = row_in['Trans Date']
        row_out['Amount'] = row_in['Amount']
        row_out['TransferMech1'] = row_in['Type']
        row_out['TransferMech2'] = row_in['Type']
        row_out['AccountAlias'] = row_in['Description']
        
        return True, row_out
    
#===============================================================================
# specific to report types
#===============================================================================
class ConfigReportType(ConfigInstitution):  

    def sortOrder(self): return list([
        'YearMonth',
        'Category',
        'Date',
        'Subcategory',
        'Account',
        'SimplifiedAlias',
    ])
    
    def sectionChange(self): return list([
        'YearMonth'
    ])
               
    def subsectionChange(self): return list([
        'Category'
    ])

    def collapseOnFields(self): return list([
    ])

    def isSelectedRow(self, row):
        return (
            row['Mechanism'] == 'Credit Card Purchase' or
            row['Mechanism'] == 'Credit Card Refund' )
       
    def HowToFinallyModifyCertainFields(self, row_in):          
        row_out = dict(row_in)
        return True, row_out
    
    #===========================================================================
    # initialize account titles, aliases, categories, subcategories
    #===========================================================================
    def initializeAccounts(self): 

        self.map_title_to_account = dict()
        self.map_alias_to_title = dict()

        self.createAccount("ADVANCE AUTO PARTS","ADVANCE AUTO PARTS #8830","Car","Auto Parts")
        self.createAccount("AGODA TRAVEL WEBSITE","AGODA.COM","Travel","Hotel")
        self.createAccount("AGODA TRAVEL WEBSITE","AGODA.COM","Travel","Hotel")        
        self.createAccount("ALBERTO'S RESTAURANT - HYANNIS", "ALBERTO'S RISTORANTE","Food","Eating Out")
        self.createAccount("ALBERTSONS GROCERY STORE","ALBERTSONS #0967","Food","Grocery Store")
        self.createAccount("ALBERTSONS GROCERY STORE","ALBERTSONS #0967","Food","Grocery Store")
        self.createAccount("AMAZON ONLINE SHOPPING","AMAZON MKTPLACE PMTS","Clothing","Cloud Store")
        self.createAccount("AMTRAK TRAIN","AMTRAK      0209646558533","Travel","Train/Bus/Taxi")
        self.createAccount("FEDEX","ANDERSEN PACK N SHIP","Mail","Fedex")
        self.createAccount("APPLEBEES","APPLEBEES GARD48248272","Food","Eating Out")
        self.createAccount("ASIAN PACIFIC MARKET","ASIAN PACIFIC MARK","Food","Grocery Store")
        self.createAccount("ASIAN PACIFIC MARKET","ASIAN PACIFIC MARK","Food","Grocery Store")
        self.createAccount("ASIAN PACIFIC MARKET","ASIAN PACIFIC MARK","Food","Grocery Store")
        self.createAccount("ASIAN PACIFIC MARKET","ASIAN PACIFIC MARK","Food","Grocery Store")
        self.createAccount("BEYOND BANKING TRANSFER","AUTOMATIC PAYMENT - THANK","Credit Card","Pay Credit Card")
        self.createAccount("BEYOND BANKING TRANSFER","AUTOMATIC PAYMENT - THANK","Credit Card","Pay Credit Card")
        self.createAccount("BEYOND BANKING TRANSFER","AUTOMATIC PAYMENT - THANK","Credit Card","Pay Credit Card")
        self.createAccount("BARNES & NOBLE","BARNES & NOBLE #2092","Gifts","Book Store")
        self.createAccount("BASKIN ROBBINS ICE CREAM","BASKIN #360035     Q35","Food","Eating Out")
        self.createAccount("BASS SHOE OUTLET","BASS SHOE OUTLET 361","Clothing","Shoe Store")
        self.createAccount("BED BATH & BEYOND","BED BATH & BEYOND #338","Household","Department Store")
        self.createAccount("BEST BUY","BEST BUY      00017822","Electronics","Computer Store")
        self.createAccount("BEST BUY","BEST BUY MHT  00005686","Electronics","Computer Store")
        self.createAccount("BEST BUY","BEST BUY MHT  00005686","Electronics","Computer Store")
        self.createAccount("BLUEMOUNTAIN GREETING CARDS","BLUEMOUNTAIN*0101-0131","Gifts","Cloud Greeting Card")
        self.createAccount("BLUEMOUNTAIN GREETING CARDS","BLUEMOUNTAIN*0131-0302","Gifts","Cloud Greeting Card")
        self.createAccount("BLUEMOUNTAIN GREETING CARDS","BLUEMOUNTAIN*0302-0401","Gifts","Cloud Greeting Card")
        self.createAccount("BLUEMOUNTAIN GREETING CARDS","BLUEMOUNTAIN*0401-0501","Gifts","Cloud Greeting Card")
        self.createAccount("BRUEGGER'S BAGLES","BRUEGGER'S BAGLES","Food","Eating Out")
        self.createAccount("BURGER KING","BURGER KING #17712","Food","Eating Out")
        self.createAccount("BURGER KING","BURGER KING #5778","Food","Eating Out")
        self.createAccount("CALPHALON KITCHEN OUTLET","CALPHALON KITCHEN OUTL","Household","Kitchen Store")
        self.createAccount("CANOPY AIRPORT PARKING","CANOPY AIRPORT PARKING","Travel","Parking")
        self.createAccount("CANOPY AIRPORT PARKING","CANOPY AIRPORT PARKING","Travel","Parking")
        self.createAccount("CAPE COD POTATO CHIPS","CAPE COD POTATO CHIPS","Food","Eating Out")
        self.createAccount("CAPE TIRE SERVICE INC","CAPE TIRE SERVICE INC","Car","Auto Parts")
        self.createAccount("CHEVRON GAS STATION","CHEVRON 00075703","Car","Gas Station")
        self.createAccount("CHEVRON GAS STATION","CHEVRON 00090172","Car","Gas Station")
        self.createAccount("CHEVRON GAS STATION","CHEVRON 00090172","Car","Gas Station")
        self.createAccount("CHEVRON GAS STATION","CHEVRON 00096368","Car","Gas Station")
        self.createAccount("CHICO HATS","CHICO HATS","Clothing","Cloud Hat Store")
        self.createAccount("CHINA TOWN RESTAURANT","CHINA TOWN","Food","Eating Out")
        self.createAccount("DISNEYLAND CHURRO STAND","CHURRO - TOMORROWLA","Food","Eating Out")
        self.createAccount("CITY OF SANTA MONICA PARKING","CITY OF SM PARKING","Car","Parking")
        self.createAccount("CITY MARKET","CITY-MARKET #0431","Food","Grocery Store")
        self.createAccount("CITY MARKET","CITY-MARKET #0431","Food","Grocery Store")
        self.createAccount("COCO'S RESTAURANT","COCO'S - 503","Food","Eating Out")
        self.createAccount("CHINA BUFFET SF VALLEY","CP CHINA BUFFET","Food","Eating Out")
        self.createAccount("CA SCIENCE MUSEUM STORE","CSCF EXPLORASTORE","Entertainment","Museum")
        self.createAccount("CVS PHARMACY","CVS PHARMACY #0050 Q03","Household","Drug Store")
        self.createAccount("DARRELLS AUTOMOTIVE","DARRELLS AUTOMOTIVE","Car","Auto Repair")
        self.createAccount("DAYS INN CLEVELAND","DAYS INN CLEVELAND AIRPO","Travel","Hotel")
        self.createAccount("DELL SALES & SERVICE","DELL SALES & SERVICE","Electronics","Cloud Computer")
        self.createAccount("DENNY'S","DENNY'S #8097","Food","Eating Out")
        self.createAccount("DISNEYLAND GIFT STORE","DISNEY SHOWCASE - D","Gifts","Gift Shop")
        self.createAccount("DISNEYLAND TICKETS","DISNEYLAND TICKETS","Entertainment","Amusement Park")
        self.createAccount("DUNKIN DONUTS","DUNKIN DONUTS MAIN MT270","Food","Eating Out")
        self.createAccount("E-470 EXPRESS TOLLS","E 470 EXPRESS TOLLS","Car","Toll Road")
        self.createAccount("EINSTEIN BAGELS","EINSTEIN BAGELS","Food","Eating Out")
        self.createAccount("EINSTEIN BAGELS","EINSTEIN BROS BAGELS1599","Food","Eating Out")
        self.createAccount("PHARMACY IN SO CALIF","ESI PHARM COLUMBUS","Household","Drug Store")
        self.createAccount("FEDEX","FEDEXOFFICE   00004762","Mail","Fedex")
        self.createAccount("FOX RENT A CAR","FOX RENT A CAR LAX","Travel","Rental Car")
        self.createAccount("FOX RENT A CAR","FOX RENT A CAR LAX","Travel","Rental Car")
        self.createAccount("FOX RENT A CAR","FOX RENT A CAR LAX","Travel","Rental Car")
        self.createAccount("FRONTIER AIRLINES","FRONTIER AI 4222178188503","Travel","Airplane")
        self.createAccount("FRONTIER AIRLINES","FRONTIER AI 4222178188504","Travel","Airplane")
        self.createAccount("FRYS GAS STATION","FRYS #7104","Car","Gas Station")
        self.createAccount("FURHATWORLD.COM","FURHATWORLD.COM","Clothing","Cloud Hat Store")
        self.createAccount("Foxworth-Galbraith Lumber","FXWTH GALB LMBR CO 90","Household","Hardware Store")
        self.createAccount("GALLERIA MARKET SO CALIF","GALLERIA MARKET","Food","Grocery Store")
        self.createAccount("GIANT GROCERY STORE","GIANT 6037","Food","Grocery Store")
        self.createAccount("GOLD HILL JAVA","GOLD HILL JAVA","Food","Eating Out")
        self.createAccount("GOLD HILL JAVA","GOLD HILL JAVA","Food","Eating Out")
        self.createAccount("GOLDEN FOUNTAIN RESTAURANT","GOLDEN FOUNTAIN RESTAURAN","Food","Eating Out")
        self.createAccount("GRAND CANYON TICKET","GRAND CYN NP-SOUTH ES","Entertainment","Site Seeing")
        self.createAccount("GREYHOUND BUS","GREYHOUND KIOSK 0550","Travel","Train/Bus/Taxi")
        self.createAccount("GRAND CANYON STORE","GRNDCYNASSN-YAVAPAI","Gifts","Gift Shop")
        self.createAccount("HANNOUSH JEWELERS CAPE COD MALL","HANNOUSH JEWELERS #260","Clothing","Jewelry Store")
        self.createAccount("HARRY & DAVID OUTLET STORE","HARRY & DAVID #529","Clothing","Fur/Leather")
        self.createAccount("HOPI HOUSE GIFT SHOP","HOPI HOUSE GIFT SHOP","Gifts","Gift ShoFinance.Financep")
        self.createAccount("HOUDINI'S MAGIC SHOP DISNEYLAND","HOUDINI'S MAGIC SHO","Gifts","Magic Shop")
        self.createAccount("HUNTINGTON GARDENS","HUNTINGTON ADMISSIONS 2","Entertainment","Park/Gardens")
        self.createAccount("HUNTINGTON BOOKSTORE","HUNTINGTON BOOKSTORE","Gifts","Gift Shop")
        self.createAccount("HUNTINGTON BOOKSTORE","HUNTINGTON BOOKSTORE","Gifts","Gift Shop")
        self.createAccount("TURBOTAX","INTUIT *TURBOTAX","Government","Taxes")
        self.createAccount("ITOPIT YOGURT","ITOPIT","Food","Eating Out")
        self.createAccount("ITOPIT YOGURT","ITOPIT","Food","Eating Out")
        self.createAccount("ITOPIT YOGURT","ITOPIT","Food","Eating Out")
        self.createAccount("JAPANESE FUSION RESTAURANT","JAPANESE FUSION","Food","Eating Out")
        self.createAccount("JAPANESE FUSION RESTAURANT","JAPANESE FUSION","Food","Eating Out")
        self.createAccount("JOLLY HOLIDAY BAKERY DISNEYLAND","JOLLY HOLIDAY BAKER","Food","Eating Out")
        self.createAccount("KITCHEN COLLECTION OUTLET STORE","KITCHEN COLLECTION #82","Household","Kitchen Store")
        self.createAccount("KMART","KMART 3040","Household","Department Store")
        self.createAccount("KMART","KMART 3040","Household","Department Store")
        self.createAccount("KNOTT'S BERRY FARM","KNOTT'S BERRY FARM","Food","Eating Out")
        self.createAccount("KNOTT'S BERRY FARM","KNOTT'S BERRY FARM","Food","Eating Out")
        self.createAccount("KNOTT'S BERRY FARM","KNOTT'S BERRY FARM","Food","Eating Out")
        self.createAccount("LOAF N JUG GAS STATION","LOAF N JUG #0099   Q81","Car","Gas Station")
        self.createAccount("LOVE SUSHI RESTAURANT","LOVE SUSHI","Food","Eating Out")
        self.createAccount("LOWES HARDWARE STORE","LOWES #01099*","Household","Hardware Store")
        self.createAccount("LOWES HARDWARE STORE","LOWES #02578*","Household","Hardware Store")
        self.createAccount("LOWES HARDWARE STORE","LOWES #02578*","Household","Hardware Store")
        self.createAccount("MACY'S DEPT STORE","MACY'S EAST #523","Clothing","Department Store")
        self.createAccount("MARSHALLS DEPT STORE","MARSHALLS #0004","Clothing","Department Store")
        self.createAccount("MAYFLOWER CHINESE RESTAURANT","MAYFLOWER CHINESE REST","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S F10576","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S F10576","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S F1212","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S F1212","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S F13573","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S F32477","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S F32477","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S F6231","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S M2368 OF CA","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S M2368 OF CA","Food","Eating Out")
        self.createAccount("MONARCH MOUNTAIN SKI","MONARCH MOUNTAIN RENTAL","Entertainment","Skiing")
        self.createAccount("MONARCH MOUNTAIN SKI","MONARCH ON MOUNTAIN TICKE","Entertainment","Skiing")
        self.createAccount("MORRISON MOTOR WORKS HYANNIS","MORRISON MOTOR WORKS","Car","Auto Repair")
        self.createAccount("MOUNTAIN HARDWEAR SKI","MOUNTAIN HARDWEAR 418","Entertainment","Skiing")
        self.createAccount("NAVAJO HOPI INDIAN ART","NAVAJO HOPI INDIAN ART","Gifts","Gift Shop")
        self.createAccount("NETFLIX.COM","NETFLIX.COM","Entertainment","Streaming")
        self.createAccount("NETFLIX.COM","NETFLIX.COM","Entertainment","Streaming")
        self.createAccount("NETFLIX.COM","NETFLIX.COM","Entertainment","Streaming")
        self.createAccount("NETFLIX.COM","NETFLIX.COM","Entertainment","Streaming")
        self.createAccount("NOMORERACK ONLINE STORE","NOMORERACK 18005389798","Clothing","Cloud Clothing Store")
        self.createAccount("NOMORERACK ONLINE STORE","NOMORERACK 18005389798","Clothing","Cloud Clothing Store")
        self.createAccount("NOMORERACK ONLINE STORE","NOMORERACK 18005389798","Clothing","Cloud Clothing Store")
        self.createAccount("NORDSTROM RACK DEPT STORE","NORDSTROM-RACK #0347","Clothing","Department Store")
        self.createAccount("OFFICE MAX","OFFICE MAX","Electronics","Computer Store")
        self.createAccount("OLD NAVY STORE","OLD NAVY STORE 6706","Clothing","Clothing Store")
        self.createAccount("OTG MANAGEMENT TAXI","OTG MANAGEMENT BOS, LLC","Travel","Train/Bus/Taxi")
        self.createAccount("PANDA EXPRESS","PANDA EXPRESS #1141","Food","Eating Out")
        self.createAccount("PANDA EXPRESS","PANDA EXPRESS #1491","Food","Eating Out")
        self.createAccount("PANDA EXPRESS","PANDA EXPRESS 700","Food","Eating Out")
        self.createAccount("PANDA EXPRESS","PANDA EXPRESS 700","Food","Eating Out")
        self.createAccount("PANDA EXPRESS","PANDA EXPRESS 700","Food","Eating Out")
        self.createAccount("PANDA EXPRESS","PANDA EXPRESS 700","Food","Eating Out")
        self.createAccount("PATRIOT HEALTH INSTITUTE","PATRIOTHEALTHINSTITUTE","Medical/Dental","Cloud Pharmacy")
        self.createAccount("PEARL RESTAURANT","PEARL RESTAURANT","Food","Eating Out")
        self.createAccount("PRICELINE HOTELS","PLN*PRICELINE HOTELS","Travel","Hotel")
        self.createAccount("PRICELINE HOTELS","PLN*PRICELINE HOTELS","Travel","Hotel")
        self.createAccount("PRICELINE HOTELS","PLN*PRICELINE.COM HTL","Travel","Hotel")
        self.createAccount("PRICELINE HOTELS","PLN*PRICELINE.COM HTL","Travel","Hotel")
        self.createAccount("PRICELINE HOTELS","PLN*PRICELINE.COM HTL","Travel","Hotel")
        self.createAccount("PLYMOUTH AND BROCKTON BUS","PLYMOUTH AND BROCK","Travel","Train/Bus/Taxi")
        self.createAccount("DISNEYLAND?","PP*0934CODE","Entertainment","Amusement Park")
        self.createAccount("Pikes Peak Regional Hospital","PPRH MEDICAL CARE","Medical/Dental","Medical Office")
        self.createAccount("Parking Meter","PUBLIC WORKS-PRKG METR","Car","Parking")
        self.createAccount("Rock and Roll Museum Cleveland","R AND R HOF BOX OFFICE","Entertainment","Site Seeing")
        self.createAccount("RALPHS GROCERY STORE","RALPHS #0060","Food","GrocFinanceery Store")
        self.createAccount("RALPHS GROCERY STORE","RALPHS #0235","Food","Grocery Store")
        self.createAccount("RALPHS GROCERY STORE","RALPHS #0712","Food","Grocery Store")
        self.createAccount("RALPHS GROCERY STORE","RALPHS #0717","Food","Grocery Store")
        self.createAccount("RALPHS GROCERY STORE","RALPHS #0717","Food","Grocery Store")
        self.createAccount("RALPHS GROCERY STORE","RALPHS #0717","Food","Grocery Store")
        self.createAccount("RALPHS GROCERY STORE","RALPHS #0717","Food","Grocery Store")
        self.createAccount("RALPHS GROCERY STORE","RALPHS #0717","Food","Grocery Store")
        self.createAccount("RALPHS GAS STATION","RALPHS FUEL #1717","Car","Gas Station")
        self.createAccount("RAPID LUBE OF WOODLAND PARK","RAPID LUBE OF WOOD","Car","Auto Repair")
        self.createAccount("Chase Credit Card","REDEMPTION CREDIT","Credit Card","Reward Money Back")
        self.createAccount("Rendezvous Cafe Hyannis","Rendezvous Cafe & Creperi","Food","Eating Out")
        self.createAccount("RHAPSODY","RI *RHAPSODY","Entertainment","Streaming")
        self.createAccount("RHAPSODY","RI *RHAPSODY","Entertainment","Streaming")
        self.createAccount("RHAPSODY","RI *RHAPSODY","Entertainment","Streaming")
        self.createAccount("RHAPSODY","RI *RHAPSODY","Entertainment","Streaming")
        self.createAccount("RITE AID STORE","RITE AID STORE #10189","Household","Drug Store")
        self.createAccount("RITE AID STORE","RITE AID STORE #10190","Household","Drug Store")
        self.createAccount("RITE AID STORE","RITE AID STORE #10190","Household","Drug Store")
        self.createAccount("RITE AID STORE","RITE AID STORE 5661","Household","Drug Store")
        self.createAccount("RITE AID STORE","RITE AID STORE 5661","Household","Drug Store")
        self.createAccount("S & Z PETROLEUM INC GAS STATION","S & Z PETROLEUM INC","Car","Gas Station")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE10046134","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE10046134","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE10046134","Food","Grocery Store")
        self.createAccount("SARKU JAPAN RESTAURANT SANTA MONICA","SARKU JAPAN 263","Food","Eating Out")
        self.createAccount("SARKU JAPAN RESTAURANT SANTA MONICA","SARKU JAPAN 263","Food","Eating Out")
        self.createAccount("SHANGHAI CHINESE REST","SHANGHAI CHINESE REST","Food","Eating Out")
        self.createAccount("SHELL OIL GAS STATION","SHELL OIL 57442462909","Car","Gas Station")
        self.createAccount("SHELL OIL GAS STATION","SHELL OIL 57442462909","Car","Gas Station")
        self.createAccount("SHELL OIL GAS STATION","SHELL OIL 57442718805","Car","Gas Station")
        self.createAccount("SHELL OIL GAS STATION","SHELL OIL 57443811500","Car","Gas Station")
        self.createAccount("SHELL OIL GAS STATION","SHELL OIL 57443812102","Car","Gas Station")
        self.createAccount("SHELL OIL GAS STATION","SHELL OIL 57444230007","Car","Gas Station")
        self.createAccount("SHELL OIL GAS STATION","SHELL OIL 57445118805","Car","Gas Station")
        self.createAccount("SHELL OIL GAS STATION","SHELL OIL 57445118805","Car","Gas Station")
        self.createAccount("SMARTE CARTE LOCKER SKI","SMARTE CARTE","Entertainment","Skiing")
        self.createAccount("SMILE WORKS DENTAL CS","SMILE WORKS DENTAL","Medical/Dental","Dental Office")
        self.createAccount("SOHO ARTS COMPANY HYANNIS","SOHO ARTS COMPANY","Gifts","Gift Shop")
        self.createAccount("GRAND CANYON STORE","SOUTH RIM GENERAL STOR","Gifts","Gift Shop")
        self.createAccount("SPEEDWAY GAS & OIL CAPE COD","SPEEDWAY GAS & OIL","Car","Gas Station")
        self.createAccount("SPIRIT AIRLINES","SPIRIT AIRL 4870097262339","Travel","Airplane")
        self.createAccount("SPIRIT AIRLINES","SPIRIT AIRL 4870097551484","Travel","Airplane")
        self.createAccount("STAPLES STATIONARY STORE","STAPLES       00101543","Household","Stationary Store")
        self.createAccount("STAPLES STATIONARY STORE","STAPLES       00113480","Household","Stationary Store")
        self.createAccount("STAPLES STATIONARY STORE","STAPLES       00113480","Household","Stationary Store")
        self.createAccount("STAR MARKET CAPE COD","STAR MARKET #7595","Food","Grocery Store")
        self.createAccount("STAR MARKET CAPE COD","STAR MARKET #7595","Food","Grocery Store")
        self.createAccount("STAR MARKET CAPE COD","STAR MARKET #7595","Food","Grocery Store")
        self.createAccount("SUBWAY SANDWICHES","SUBWAY        00478453","Food","Eating Out")
        self.createAccount("SUNBIRD RESTAURANT COLORADO SPRINGS","SUNBIRD","Food","Eating Out")
        self.createAccount("SIRIUS XM","SXM*SIRIUSXM.COM/ACCT","Entertainment","Streaming")
        self.createAccount("SIRIUS XM","SXM*SIRIUSXM.COM/ACCT","Entertainment","Streaming")
        self.createAccount("THAI MINI CAFE","THAI MINI CAFE","Food","Eating Out")
        self.createAccount("THE CAFE","THE CAFE","Food","Eating Out")
        self.createAccount("THE HOME DEPOT HARDWARE STORE","THE HOME DEPOT 2612","Household","Hardware Store")
        self.createAccount("THE HOT CHOCOLATE SPARROW","THE HOT CHOCOLATE SPAR","Food","Eating Out")
        self.createAccount("THE LEGO STORE","THE LEGO STORE","Gifts","Toy Store")
        self.createAccount("THELADDERS.COM","THELADDERS.COM","Job","Cloud Job Search")
        self.createAccount("DISNEYLAND TIKI JUICE BAR","TIKI JUICE BAR - DL","Food","Eating Out")
        self.createAccount("TJMAXX DEPT STORE","TJMAXX #0241","Clothing","Clothing Store")
        self.createAccount("TJMAXX DEPT STORE","TJMAXX #0241","Clothing","Clothing Store")
        self.createAccount("TJMAXX DEPT STORE","TJMAXX #0241","Clothing","Clothing Store")
        self.createAccount("TJMAXX DEPT STORE","TJMAXX #0241","Clothing","Clothing Store")
        self.createAccount("TOBY KEITH'S RESTAURANT LA","TOBY KEITH'S I LOVE TH","Food","Eating Out")
        self.createAccount("DISNEYLAND PARKING","TOLLS WEST - PARKIN","Entertainment","Amusement Park")
        self.createAccount("DISNEYLAND RESTAURANT","TOMORROWLAND TERRAC","Food","Eating Out")
        self.createAccount("DISNEYLAND TOONTOWN RESTAURANT","TOONTOWN - DL","Food","Eating Out")
        self.createAccount("DISNEYLAND TOONTOWN RESTAURANT","TOONTOWN - DL","Food","Eating Out")
        self.createAccount("TRADER JOE'S GROCERY STORE","TRADER JOE'S #217  QPS","Food","Grocery Store")
        self.createAccount("TRADER JOE'S GROCERY STORE","TRADER JOE'S #217  QPS","Food","Grocery Store")
        self.createAccount("TRADER JOE'S GROCERY STORE","TRADER JOE'S #514  QPS","Food","Grocery Store")
        self.createAccount("TRADER JOE'S GROCERY STORE","TRADER JOE'S #514  QPS","Food","Grocery Store")
        self.createAccount("TRADER JOE'S GROCERY STORE","TRADER JOE'S #514  QPS","Food","Grocery Store")
        self.createAccount("TRADER JOE'S GROCERY STORE","TRADER JOE'S #514  QPS","Food","Grocery Store")
        self.createAccount("UNION STATION FLYAWAY BUS LA","UNIONSTATIONFLYAWAY","Travel","Train/Bus/Taxi")
        self.createAccount("UNITED AIRLINES","UNITED      0162398120306","Travel","Airplane")
        self.createAccount("UNITED AIRLINES","UNITED      0162398120307","Travel","Airplane")
        self.createAccount("POST OFFICE","USPS 05631608335007426","Mail","Post Office")
        self.createAccount("POST OFFICE","USPS 07181206130302608","Mail","Post Office")
        self.createAccount("POST OFFICE","USPS 07981007830313597","Mail","Post Office")
        self.createAccount("POST OFFICE","USPS 24372306034107516","Mail","Post Office")
        self.createAccount("POST OFFICE","USPS 34014395518100933","Mail","Post Office")
        self.createAccount("Vehicle Registration","VEHICLE REGISTRATI","Car","Vehicle Registration")
        self.createAccount("WAL-MART DEPT STORE","WAL-MART #3805","Household","Department Store")
        self.createAccount("WAL-MART DEPT STORE","WAL-MART #3805","Household","Department Store")
        self.createAccount("WAL-MART DEPT STORE","WAL-MART #3805","Household","Department Store")
        self.createAccount("WAL-MART DEPT STORE","WAL-MART #3805","Household","Department Store")
        self.createAccount("WAL-MART DEPT STORE","WAL-MART #3805","Household","Department Store")
        self.createAccount("WAL-MART DEPT STORE","WAL-MART #3805","Household","Department Store")
        self.createAccount("WAL-MART DEPT STORE","WAL-MART #3805","Household","Department Store")
        self.createAccount("WALGREENS DRUG STORE","WALGREENS #10460","Household","Drug Store")
        self.createAccount("WALGREENS DRUG STORE","WALGREENS #12769","Household","Drug Store")
        self.createAccount("WHOLE FOODS GROCERY STORE","WHOLEFDS CCK 10095","Food","Grocery Store")
        self.createAccount("WHOLE FOODS GROCERY STORE","WHOLEFDS NCP 10435","Food","Grocery Store")
        self.createAccount("WHOLE FOODS GROCERY STORE","WHOLEFDS NCP 10435","Food","Grocery Store")
        self.createAccount("WHOLE FOODS GROCERY STORE","WHOLEFDS PPK 10146","Food","Grocery Store")
        self.createAccount("WILSONS LEATHER OUTLETS","WILSONS LEATHER OUTLETS","Clothing","Fur/Leather")
        self.createAccount("WILSONS LEATHER OUTLETS","WILSONS LEATHER OUTLETS","Clothing","Fur/Leather")
        self.createAccount("WAL-MART DEPT STORE","WM SUPERCENTER #3805","Household","Department Store")
        self.createAccount("WOLLEY TAXI CO CLEVELAND","WOLLEY TAXI CO","Travel","Train/Bus/Taxi")
        self.createAccount("WOLLEY TAXI CO CLEVELAND","WOLLEY TAXI CO","Travel","Train/Bus/Taxi")
        self.createAccount(" BIG O TIRES WOODLAND PARK","WOODLAND PARK BIG O TIRES","Car","Auto Parts")
        self.createAccount(" BIG O TIRES WOODLAND PARK","WOODLAND PARK BIG O TIRES","Car","Auto Parts")
        self.createAccount("WOODLAND PARK COMMUNITY CHURCH","WOODLAND PARK COMMUNITY C","Church/Mission","Marital Seminar")
        self.createAccount("WOODLAND PARK DENTAL GROUP","WOODLAND PARK DENTAL GROU","Medical/Dental","Dental Office")
        self.createAccount("WOODLAND PARK DENTAL GROUP","WOODLAND PARK DENTAL GROU","Medical/Dental","Dental Office")
        self.createAccount("WOODLAND PARK DENTAL GROUP","WOODLAND PARK DENTAL GROU","Medical/Dental","Dental Office")
        self.createAccount("WORLD OF DISNEY GIFT STORE","WORLD OF DISNEY - D","Gifts","Gift Shop")
        self.createAccount("WWW.MEDIADAZE.NET STREAMING VIDEO","WWW.MEDIADAZE.NET","Entertainment","Streaming")
        self.createAccount("WWW.MEDIADAZE.NET STREAMING VIDEO","WWW.MEDIADAZE.NET","Entertainment","Streaming")
        self.createAccount("WWW.MEDIADAZE.NET STREAMING VIDEO","WWW.MEDIADAZE.NET","Entertainment","Streaming")
        self.createAccount("WWW.NEWEGG.COM","WWW.NEWEGG.COM","Electronics","Cloud Computer")
        self.createAccount("WWW.OVERLAND.COM","WWW.OVERLAND.COM","Clothing","Cloud Clothing Store")

        self.createAccount("JOANIE'S BAKERY & DELI - Woodland Park","JOANIE'S BAKERY & DELI","Food","Eating Out")
        self.createAccount("WENDY'S","WENDYS","Food","Eating Out")
        self.createAccount("ASIAN FUSION - Woodland Park","ASIAN FUSION","Food","Eating Out")
        self.createAccount("SMITHS FOOD","SMITHS FOOD #4048","Food","Grocery Store")
        self.createAccount("BOMBAY HOUSE","BOMBAY HOUSE","Food","Eating Out")
        self.createAccount("HATCH FAMILY CHOCOLATES","HATCH FAMILY CHOCOLATES L","Food","Eating Out")
        self.createAccount("NEW GOLDEN DRAGON RESTAURANT","NEW GOLDEN DRAGON RESTAUR","Food","Eating Out")
        self.createAccount("APPLEBEES RESTAURANT","APPLEBEES GRAN48248249","Food","Eating Out")
        self.createAccount("AMICI RESTAURANT - Salt Lake City","AMICI RESTAURANT","Food","Eating Out")
        self.createAccount("RED BUTTE GARDENS - Salt Lake City","RED BUTTE GARDENS OFFICE","Entertainment","Site Seeing")
        self.createAccount("RED BUTTE GARDENS - Salt Lake City","RED BUTTE GARDEN AND ARB","Entertainment","Site Seeing")
        self.createAccount("MAVERIK - Salt Lake City", "MAVERIK #358","Car","Gas Station")
        self.createAccount("WWW.DRESSLINK.COM","WWW.DRESSLINK.COM","Clothing","Cloud Clothing Store")
        self.createAccount("JUDD'S GLASS & MIRROR - Woodland Park","JUDD'S GLASS & MIR","Car","Auto Repair")
               
        #for alias in self.map_alias_to_title.keys():
        #    account_title = self.map_alias_to_title[alias]
        #    print account_title

        return None
 
common = ConfigReportType()
'''
