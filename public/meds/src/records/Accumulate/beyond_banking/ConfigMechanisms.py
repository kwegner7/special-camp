'''
   namespace DerivedEquiv
      class DerivedEquiv.EquivBeyondBanking
'''

from utils import ConfigMechanisms

########################################################################
# Beyond Banking
########################################################################
class BeyondBanking(ConfigMechanisms.Base):

    # constructor
    def __init__(self):
        ConfigMechanisms.Base.__init__(self)
        return None

    # virtual method
    def classNames(self): return list([
        'BB ATM Cash Withdrawal' , # 0
        'BB ATM Fee Refund'      , # 1
        'Bank Check Payment'     , # 2
        'Bank Interest Credit'   , # 3
        'BB Debit Card Purchase' , # 4
        'Pre Auth Payment'       , # 5
        'Electronic Income'      , # 6
        'Fee Charged'            , # 7
        'Journal Entry'          , # 8
        'ML BillPay Paper Check' , # 9
        'Paper Check Income'     , # 10
        'Paper Check Payment'    , # 11
        'Wire Transfer'          , # 12
        'Dividends'              , # 13
        'UNKNOWN MECHANISM'
    ])

    # virtual method
    def matchesCriteriaOfEquivClass(self, classname, mech1, mech2, account_alias=''):
        name = self.classNames()
 
        if ( classname == name[0] # 'ATM Cash Withdrawal'
        and      mech1 == 'ATM'
        and      mech2 == 'Cash Machine'
        ): return True, classname

        if ( classname == name[1] # 'ATM Fee Credit'
        and      mech1 == 'ATMRefund'
        and      mech2 == 'ATM Refund'
        ): return True, classname
  
        if ( classname == name[2] # 'Bank Check Debit'
        and      mech1 == 'Other'
        and      mech2 == 'Withdrawal'
        ): return True, classname
  
        if ( classname == name[3] # 'Bank Interest Credit'
        and      mech1 == 'DividendAndInterest'
        and      mech2 == 'Bank Interest'
        ): return True, classname

        if ( classname == name[4] # 'Debit Card Transaction'
        and      mech1 == 'VisaTransactions'
        and      mech2 == 'Deferred'
        ): return True, classname
   
        if ( classname == name[5] # 'Pre Auth Payment'
        and      mech1 == 'Other'
        and      mech2 == 'Pre Authdebit'
        ): return True, classname
  
        if ( classname == name[6] # 'Electronic Refund'
        and      mech1 == 'FundReceipts'
        and      mech2 == 'DDS'
        ): return True, classname
  
        if ( classname == name[7] # 'Fee Charged'
        and      mech1 == 'Other'
        and      mech2 == 'Journal Entry'
        ): return True, classname
  
        if ( classname == name[8] # 'Journal Entry'
        and      mech1 == 'SecurityTransactions'
        and      mech2 == 'Journal Entry'
        ): return True, classname
  
        if ( classname == name[9] # 'ML BillPay'
        and      mech1 == 'BillPay'
        and      mech2 == 'Bill Payment'
        ): return True, classname
  
        if ( classname == name[10] # 'Paper Check Deposited'
        and      mech1 == 'FundReceipts'
        and      mech2 == 'Funds Received'
        ): return True, classname

        if ( classname == name[11] # 'Paper Check Paid'
        and      mech1 == 'Checking'
        ): return True, mech2
  
        if ( classname == name[12] # 'Wire Transfer'
        and      mech1 == 'FundTransfers'
        and      mech2 == 'Funds Transfer'
        ): return True, classname

        if ( classname == name[13] # 'Dividends'
        and      mech1 == 'Other'
        and      mech2 == 'Check'
        ): return True, classname

        if ( classname == name[13] # 'Dividends'
        and      mech1 == 'Other'
        and      mech2 == 'Total Mo Accum'
        ): return True, classname

        if ( classname == name[13] # 'Dividends'
        and      mech1 == 'Other'
        and      mech2 == 'Acum For Mo Ck'
        ): return True, classname

        if ( classname == name[13] # 'Dividends'
        and      mech1 == 'DividendAndInterest'
        and      mech2 == 'Dividend'
        ): return True, classname
 
        else:
            return False, 'NOT FOUND'

