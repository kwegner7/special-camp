'''
   namespace Aliases
      class src.finance.Aliases
'''

import re

###############################################################################
# allow access to these internal items
############################################################################### 
__all__ = \
[
    "Account",
    "Accounts",
    "EquivalenceClass",
    #"SubDivision",
]

###############################################################################
# Account
###############################################################################
class Account():

    # constructor              
    def __init__(self, title):
        self.title = title
        self.alias_begins_with = set()
        self.alias_ends_with = set()
        self.alias_contains = set()
        self.alias_matches_exactly = set()
        pass

    def beginsWith(self, set_of_patterns, item):
        for pattern in set_of_patterns:
            find_pattern = '^' +pattern+ '+'
            if re.match(find_pattern, item): return True
        return False

    def endsWith(self, set_of_patterns, item):
        for pattern in set_of_patterns:
            find_pattern = '.*' +pattern+ '$'
            if re.match(find_pattern, item): return True
        return False

    def matchesExactly(self, set_of_patterns, item):
        for pattern in set_of_patterns:
            find_pattern = '^' +pattern+ '$'
            if re.match(find_pattern, item): return True
        return False

    def matchesSomewhere(self, set_of_patterns, item):
        for pattern in set_of_patterns:
            find_pattern = '.*' +pattern+ '.*'
            if re.match(find_pattern, item): return True
        return False

    def matchesExactly(self, set_of_patterns, item):
        for pattern in set_of_patterns:
            find_pattern = pattern
            if re.match(find_pattern, item): return True
        return False
       
    # method              
    def isAlias(self, alias):
        if self.beginsWith(self.alias_begins_with, alias): return True
        if self.endsWith(self.alias_ends_with, alias): return True
        if self.matchesSomewhere(self.alias_contains, alias): return True
        if self.matchesExactly(self.alias_matches_exactly, alias): return True
        return False
       
    # method              
    def aliasBeginsWith(self, aliases):
        self.alias_begins_with = self.alias_begins_with.union(aliases)
        return None

    # method              
    def aliasEndsWith(self, aliases):
        self.alias_ends_with = self.alias_ends_with.union(aliases)
        return None

    # method              
    def aliasContains(self, aliases):
        self.alias_contains = self.alias_contains.union(aliases)
        return None

    # method              
    def aliasMatchesExactly(self, aliases):
        self.alias_matches_exactly = self.alias_matches_exactly.union(aliases)
        return None

    # method              
    def text(self):
        print "Account Title Is:", self.title
        if False:
            print "Aliases Are:"
            for alias in self.alias_begins_with:     print alias
            for alias in self.alias_ends_with:       print alias
            for alias in self.alias_contains:        print alias
            for alias in self.alias_matches_exactly: print alias
        return None

###############################################################################
# Aliases.Base
###############################################################################
class Base():

    def __init__(self):
        self.set_of_accounts = list()
        pass
    
    def insertAccountWithAliases(self, title, aliases):
        acnt = Account(title)
        acnt.aliasBeginsWith(aliases)
        self.add(acnt)
        return None
       
    def add(self, account):
        self.set_of_accounts.append(account)
        return None
       
    def getAccountName0(self, alias, mech1, mech2):

        for acnt in self.set_of_accounts:
            if acnt.isAlias(alias):
                return acnt.title

        if ( mech1 == 'VisaTransactions' and mech2 == 'Deferred' ):
            return 'Debit Card Beyond Banking'

        return 'ALIAS NOT FOUND'

    #===========================================================================
    # the account name is the key into the category tree
    #===========================================================================
    def getAccountName(self, alias, mech1, mech2):
        account_name = 'ALIAS NOT FOUND'
        for acnt in self.set_of_accounts:
            if acnt.isAlias(alias): account_name = acnt.title
        if mech1 in list(['Payment Review', 'Invoice Sent']):
            account_name += ''
        return account_name

       
    def text(self):
        print "Number of accounts is:", len(self.set_of_accounts)
        for acnt in self.set_of_accounts:
            acnt.text()
        return None

###############################################################################
# EquivalenceClass
###############################################################################
class EquivalenceClass():

    # constructor              
    def __init__(self, title):
        self.title = title
        self.subset_of_elements = set()
        pass

    # method              
    def whichAccounts(self, accounts):
        self.subset_of_elements = self.subset_of_elements.union(accounts)
        return None

    # method              
    def text(self):
        print "EquivalenceClass Title Is:", self.title
        for acnt in self.subset_of_elements:
            print acnt
        return None
'''
###############################################################################
# SubDivision
###############################################################################
class SubDivision():

    # constructor              
    def __init__(self):
        self.equiv_classes = set()
        pass
       
    # method              
    def add(self, equiv_class):
        self.equiv_classes.add(equiv_class)
        return None
       
    # method              
    def getEquivClassName(self, account):
        for clss in self.equiv_classes:
            if account in clss.subset_of_elements:
                return clss.title
        return ''

    def getAccountName(self, alias):
        for acnt in self.subset_of_elements:
            if acnt.isAlias(alias):
                return acnt.title
        return ''
       
    # method              
    def text(self):
        print "Number of equiv classes is:", len(self.equiv_classes)
        for clss in self.equiv_classes:
            clss.text()
        return None
'''

