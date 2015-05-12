'''
   namespace src.finance.faraja.Aliases
'''

from utils import ConfigAliases 

#===============================================================================
# ConfigAliases.FriendsOfFaraja
#===============================================================================
class FriendsOfFaraja(ConfigAliases.Base):
    
    def irrelevant(self):
        return ' (irrelevant)'
    
    #===========================================================================
    # the account name is the key into the category tree
    #===========================================================================
    def getAccountName(self, alias, mech1, mech2):
        account_name = 'ALIAS NOT FOUND'
        for acnt in self.set_of_accounts:
            if acnt.isAlias(alias): account_name = acnt.title
        if mech1 in list(['Payment Review', 'Invoice Sent']):
            account_name += self.irrelevant()
        return account_name

    #===========================================================================
    # map aliases to an account name
    #===========================================================================
    def __init__(self):
        ConfigAliases.Base.__init__(self)

        self.insertAccountWithAliases('Denny Roesel', set([
            'Denny Roesel',
        ]))

        self.insertAccountWithAliases('The Lion of Judah Ministries, Inc.', set([
            'The Lion of Judah Ministries, Inc.',
        ]))

        self.insertAccountWithAliases('Khadene Stone-Webley', set([
            'Khadene Stone-Webley',
        ]))

        self.insertAccountWithAliases('Adrian Weisensee', set([
            'Adrian Weisensee',
        ]))

        self.insertAccountWithAliases('Carrie Cooke', set([
            'Carrie Cooke',
        ]))

        self.insertAccountWithAliases('Paul Woodward', set([
            'Paul Woodward',
        ]))

        self.insertAccountWithAliases('Michael Kozlowski', set([
            'Michael Kozlowski',
        ]))

        self.insertAccountWithAliases('Michael Zobott', set([
            'Michael Zobott',
        ]))

        self.insertAccountWithAliases('Bank Account', set([
            'Bank Account',
        ]))

        self.insertAccountWithAliases('Kurt Wegner', set([
            'Kurt Wegner',
        ]))

        self.insertAccountWithAliases('John Cook', set([
            'John Cook',
        ]))
        pass
