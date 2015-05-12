'''
    namespace src.finance.friends_of_faraja.ConfigCategories
'''

import re
from utils import ConfigCategories

########################################################################
# Categories.FriendsOfFaraja
########################################################################
class FriendsOfFaraja(ConfigCategories.Base):

    def __init__(self, name_of_tree):
        ConfigCategories.Base.__init__(self, name_of_tree)
        
    def irrelevant(self):
        return ' (irrelevant)'
        
    ######################################################
    # Category refers to category of transactions
    # NOTE: the account names must match ConfigAlias.py
    ######################################################
    def configureEquivalenceTree(self, maximal_subset):
                
        donors = list([
            'Denny Roesel',
            'Khadene Stone-Webley',
            'Adrian Weisensee',
            'Carrie Cooke',
            'Paul Woodward',
            'Michael Kozlowski',
            'Michael Zobott',
            'John Cook',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Donation Received' ],
            donors
        )

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Payment Review or Invoice Sent' ],
            list([(donor+self.irrelevant()) for donor in donors])
        )

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Paypal Transfer to Lion of Judah' ],
        [
            'The Lion of Judah Ministries, Inc.',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', "Kurt Wegner Personal" ],
        [
            'Kurt Wegner',
            'Bank Account',
        ])

        pass
