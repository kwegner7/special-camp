'''
   namespace DerivedEquiv
      class DerivedEquiv.Faraja
'''

from utils import ConfigMechanisms

########################################################################
# ConfigMechanisms.Faraja
########################################################################
class FriendsOfFaraja(ConfigMechanisms.Base):

    # constructor
    def __init__(self):
        ConfigMechanisms.Base.__init__(self)
        pass
    
    # these are my choices for describing a transaction payment method
    def classNames(self): return list([
        'Funds Transferred using FORM Website'     , # 0
        'Funds Transferred from a Paypal Account'  , # 1
        'Money Withdrawn to a Bank Account'     , # 2
        'Invoice Sent to a Paypal Account'      , # 3
        'Money Sent to a Paypal Account'        , # 4
        'Payment Review'                        , # 5
        'UNKNOWN MECHANISM'
    ])

    # virtual method
    def matchesCriteriaOfEquivClass(self, classname, mech1, mech2, item3=''):
        name = self.classNames()
 
        if ( classname == name[0]
        and      mech1 == 'Donation Received'
        ): return True, classname
        
        if ( classname == name[1] 
        and      mech1 == 'Payment Received'
        ): return True, classname

        if ( classname == name[2]
        and      mech1 == 'Withdraw Funds to a Bank Account'
        ): return True, classname
  
        if ( classname == name[3]
        and      mech1 == 'Invoice Sent'
        ): return True, classname
  
        if ( classname == name[4]
        and      mech1 == 'Payment Sent'
        ): return True, classname

        if ( classname == name[5]
        and      mech1 == 'Payment Review'
        ): return True, classname
    
        else:
            return False, 'NOT FOUND'

