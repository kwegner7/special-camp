'''
    Database
'''

import os, copy, re

#===============================================================================
# Database
#===============================================================================
class Database():

    #===========================================================================
    # constructor
    #===========================================================================
    def __init__(self, website, camperid, day, dest, page, year, refresh):
        self.website = website
        self.id = id
        self.refresh = refresh

    #===========================================================================
    # methods
    #===========================================================================
    def isLocal(self):
        return self.website == 'LOCAL' # local csv to html and pdf conversion

    def isRails(self):
        return self.website == 'RAILS' # local server under rails

    def isHeroku(self):
        return self.website == 'HEROKU' # heroku server under rails

