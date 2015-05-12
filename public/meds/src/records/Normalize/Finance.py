'''
    Records.Normalize.Finance
    Records.Normalize.Finance.BeyondBanking
    Records.Normalize.Finance.PaypalFaraja
'''

import re
from utils import Container
from utils import CsvObject
from Normalize import Normalize

#===============================================================================
# Records.Normalize.Finance
#===============================================================================
class Finance(Normalize):
    
    #===========================================================================
    # implementations
    #===========================================================================
    def usefulFields(self): pass
    def derivedFields(self): pass
    def determineDerivedFields(self): pass
    def determineAmount(self): pass
    
    #===========================================================================
    # constructor
    #===========================================================================
    def __init__(self):
        Normalize.__init__(self)
        return None
    
    #===========================================================================
    # Any database
    #===========================================================================
    def usefulFields(self):
        useful = list([
            'Date',
            'Amount',
            'TransferMech1',
            'TransferMech2',
            'AccountAlias'
        ])
        return self.originalFields() 
    
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
                
    def determineDerivedFields(self, field, useful, derived):

        is_amount, amount = self.determineAmount(field, useful, derived)
        if is_amount:
            return amount
        
        elif (field == 'Date'):
            return self.normalizeDateField(useful[field])

        elif (field == 'Credit'):
            amount = Container.getNegativeAmounts(useful['Amount'])
            no_commas = re.sub(',','', amount)
            if float(no_commas) >= 0.0:
                return amount
            else:
                return ''

        elif (field == 'Debit'):
            amount = Container.getNegativeAmounts(useful['Amount'])
            no_commas = re.sub(',','', amount)
            if float(no_commas) < 0.0:
                return amount
            else:
                return ''

        elif (field == 'Year'):
            return Container.convertDateToYear(useful['Date'])

        elif (field == 'YearMonth'):
            return Container.convertDateToYearMonth(useful['Date'])

        elif (field == 'Mechanism'):
            mech = self.getMethodOfPayment(
                useful['TransferMech1'], useful['TransferMech2'] )
            if useful['TransferMech1'] == "Checking":
                show_check_number = re.sub(
                    'Check','Paper Check ',useful['TransferMech2'])
                return show_check_number
            if useful['TransferMech2'] == "Bill Payment":
                show_check_number = re.sub(
                    'THE LION OF JUDA00','ML BillPay Check ',useful['AccountAlias'])
                return show_check_number
            return mech

        elif (field == 'SimplifiedAlias'):
            self.simplified_alias = re.sub('[0123456789]+', '', useful['AccountAlias'])
            self.simplified_alias = Container.String(self.simplified_alias).removeBlanks()
            return self.simplified_alias

        elif (field == 'Account'):
            self.account_name = self.getAccountTitle(
                useful['AccountAlias'],
                useful['TransferMech1'],
                useful['TransferMech2'],
            )
            return self.account_name

        elif (field == 'Institution'):
            return self.institutionName()

        elif (field == 'CenterAccount'):
            return self.centerAccount()

        elif (field == 'OrbitAccount'):
            return derived['Account']

        elif (field == 'FromAccount'):
            if Container.getFloatNoCommas(self.normalizeAmountField(useful['Amount'], useful)) < 0.0:
                return self.centerAccount()
            else:
                return derived['Account']

        elif (field == 'ToAccount'):
            if Container.getFloatNoCommas(self.normalizeAmountField(useful['Amount'], useful)) < 0.0:
                return derived['Account']
            else:
                return self.centerAccount()
        
        elif (field == 'Subcategory'):
            return self.getSubcategory(self.account_name)

        elif (field == 'Category'):
            return self.getCategory(self.account_name)

        else:
            return useful[field]
    
    #===========================================================================
    # Finance database
    #===========================================================================
    def determineAmount(self, field, row, out):
        if ((field == 'Amount')
        or  (field == 'AmountPositive')
        or  (field == 'Adjusted')):
            amount = self.normalizeAmountField(row['Amount'], row)
            #amount = getAsPositive(row['Amount'])
            return True, amount      
        return False, '0.0'



#===============================================================================
# Records.Normalize.Finance.BeyondBanking
#===============================================================================
class BeyondBanking(Finance):
    
    #===========================================================================
    # implementations
    #===========================================================================
    def originalFieldNames(self): pass
    def originalFields(self): pass
    def dialect(self): pass
    def skipFirstRecord(self): pass
    def getCategory(self): pass
    def getSubcategory(self): pass
    def institutionName(self): pass
    def centerAccount(self): pass
    def normalizeDateField(self): pass
    def normalizeAmountField(self): pass
    def getMethodOfPayment(self): pass
    def getAccountTitle(self): pass
    
    #===========================================================================
    # constructor
    #===========================================================================
    def __init__(self):
        Finance.__init__(self)
        return None
                      
    #===========================================================================
    # implementations
    #===========================================================================
    def folderIn(self):
        return "/home/kurt/ubu/finances/MerrilLynch/download/" 
    
    def title(self):
        return "Beyond-Banking"
     
    def folderOut(self):
        return "/working/python7/db/out/beyond_banking/"+self.title()+"/" 
    
    def originalFieldNames(self): return list([
        "Trade Date",
        "Settlement Date",      # renamed useful field
        "Pending/Settled",
        "Account Nickname",
        "Account Registration",
        "Account #",
        "Type",                 # renamed useful field
        "Description 1",        # renamed useful field
        "Description 2",        # renamed useful field
        "Symbol/CUSIP #",
        "Quantity",
        "Price ($)",
        "Amount ($)"            # renamed useful field
    ])

    def originalFields(self):
        useful = dict({
            "Settlement Date" : "Date",
            "Type"            : "TransferMech1",       
            "Description 1"   : "TransferMech2",
            "Description 2"   : "AccountAlias",    
            "Amount ($)"      : "Amount"
        })
        names = list()
        for fieldname in self.originalFieldNames():
            if fieldname in useful.keys():
                names.append(useful[fieldname])
            else:                
                names.append(fieldname)
        return names
        
        return list([
            useful.get(useful[fieldname], fieldname)
            for fieldname in self.originalFieldNames()
        ])

    def dialect(self):
        return CsvObject.CsvStandardDialect()

    def skipFirstRecord(self):
        return True
    
    def getCategory(self, account):
        from Accumulate.beyond_banking import ConfigCategories
        cat = ConfigCategories.HoldingsKurt('Kurt Holdings')
        return cat.mapAccountToCategory(account)
    
    def getSubcategory(self, account):
        from Accumulate.beyond_banking import ConfigCategories
        sub = ConfigCategories.HoldingsKurt('Kurt Holdings')
        return sub.mapAccountToSubcategory(account)

    #===========================================================================
    # Referenced by determineDerivedFields
    #===========================================================================
    def institutionName(self):
        return 'Beyond Banking (Kurt)'
        
    def centerAccount(self):
        return 'Kurt Wegner'

    def normalizeDateField(self, date_text):
        return Container.convertDateWithSlashes(date_text)
    
    def normalizeAmountField(self, amount_text, row):
        return Container.getNegativeAmounts(amount_text)

    def getMethodOfPayment(self, mechanism1, mechanism2):
        from Accumulate.beyond_banking import ConfigMechanisms
        return ConfigMechanisms.BeyondBanking().getMechanismName(mechanism1, mechanism2)
    
    def getAccountTitle(self, alias, mechanism1, mechanism2):
        from Accumulate.beyond_banking import ConfigAliases
        return ConfigAliases.BeyondBanking().getAccountName(alias, mechanism1, mechanism2)     


#===============================================================================
# Records.Normalize.Finance.PaypalFaraja
#===============================================================================
class PaypalFaraja(Finance):
    
    #===========================================================================
    # implementations
    #===========================================================================
    def originalFieldNames(self): pass
    def originalFields(self): pass
    def dialect(self): pass
    def skipFirstRecord(self): pass
    def getCategory(self): pass
    def getSubcategory(self): pass
    def institutionName(self): pass
    def centerAccount(self): pass
    def normalizeDateField(self): pass
    def normalizeAmountField(self): pass
    def getMethodOfPayment(self): pass
    def getAccountTitle(self): pass
    
    #===========================================================================
    # __init__
    #===========================================================================
    def __init__(self):
        Finance.__init__(self)
        return None
                      
    #===========================================================================
    # implementations
    #===========================================================================
    def folderIn(self):
        return "/home/kurt/ubu/finances/FarajaOrphans/download/" 
    
    def title(self):
        return "Paypal-Faraja"
     
    def folderOut(self):
        return "/working/python7/db/out/paypal_faraja/"+self.title()+"/" 

    def originalFieldNames(self): return list([
        "Date",       # renamed useful field
        "Time",
        "Time Zone",
        "Name",       # renamed useful field
        "Type",       # renamed useful field
        "Status",
        "Amount",     # renamed useful field
        "Receipt ID", # renamed useful field
        "Balance", 
        "Dummy", 
    ])
            
    def originalFields(self):
        useful = dict({
            "Date"       : "Date",
            "Type"       : "TransferMech1",       
            "Receipt ID" : "TransferMech2",
            "Name"       : "AccountAlias",    
            "Amount"     : "Amount"
        })
        names = list()
        for fieldname in self.originalFieldNames():
            if fieldname in useful.keys():
                names.append(useful[fieldname])
            else:                
                names.append(fieldname)
        return names

    def dialect(self):
        return CsvObject.CsvStandardDialect()

    def skipFirstRecord(self):
        return True
    
    def getCategory(self, account):
        from Accumulate.paypal_faraja import ConfigCategories
        cat = ConfigCategories.FriendsOfFaraja('Friends of Faraja')
        return cat.mapAccountToCategory(account)
    
    def getSubcategory(self, account):
        from Accumulate.paypal_faraja import ConfigCategories
        sub = ConfigCategories.FriendsOfFaraja('Friends of Faraja')
        return sub.mapAccountToSubcategory(account)

    #===========================================================================
    # Referenced by determineDerivedFields
    #===========================================================================
    def institutionName(self):
        return 'Paypal (Friends of Faraja)'
    
    def centerAccount(self):
        return 'Friends of Faraja USA'
    
    def normalizeDateField(self, date_string):
        return Container.convertDateWithSlashes(date_string)
        
    def normalizeAmountField(self, amount_text, row):
        is_usa_donation = not (row['AccountAlias'] == 'Adrian Weisensee')
        if row['TransferMech1'] == 'Donation Received':
            amount = Container.getPaypalAdjusted(row['Amount'], is_usa_donation)
        else:
            amount = row['Amount']
        return amount
    
    def getMethodOfPayment(self, mechanism1, mechanism2):
        from Accumulate.paypal_faraja import ConfigMechanisms
        return ConfigMechanisms.FriendsOfFaraja().getMechanismName(mechanism1, mechanism2)
    
    def getAccountTitle(self, alias, mechanism1, mechanism2):
        from Accumulate.paypal_faraja import ConfigAliases
        return ConfigAliases.FriendsOfFaraja().getAccountName(alias, mechanism1, mechanism2)  
       
