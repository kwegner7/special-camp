'''
    Account
'''

import re, copy
from classes.utils import Container

#===============================================================================
# Account
#===============================================================================
class Account():

    #===========================================================================
    # constructor
    #===========================================================================
    def __init__(self, title, category, subcategory):
        self.title = Container.String(title).whiteSpaceToBlank()
        self.category = Container.String(category).whiteSpaceToBlank()
        self.subcategory = Container.String(subcategory).whiteSpaceToBlank()
        self.aliases = set()
        return None
  
    #===========================================================================
    # add to the set of aliases
    #===========================================================================
    def addAlias(self, alias):
        simplified = self.simplifyAlias(alias)
        self.aliases.add(simplified)
        return simplified
           
    #===========================================================================
    # simplify the alias by removing blanks and numbers
    #===========================================================================
    def simplifyAlias(self, alias):
        return Container.String(alias).removeBlanksAndNumbers()
           
    #===========================================================================
    # print this object
    #===========================================================================
    def text(self):
        #print "      Title:", self.title,
        #print "   Category:", self.category,
        #print "Subcategory:", self.subcategory
        print "Account", self.title, "has", len(self.aliases), "aliases"
        #if len(self.aliases) > 0:
        #    for alias in self.aliases:
        #        print "    Alias:", alias
        return None
   
