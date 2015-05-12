'''
    namespace src.finance.kurt.ConfigCategories
'''

from utils import ConfigCategories

########################################################################
# Categories.HoldingsKurt
########################################################################
class HoldingsKurt(ConfigCategories.Base):

    def __init__(self, name_of_tree):
        ConfigCategories.Base.__init__(self, name_of_tree)

    def configureEquivalenceTree(self, maximal_subset):

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Banking', 'ATM' ],
        [
            'Cash',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Banking', 'Credit Card' ],
        [
            'Credit Card Bank of America',
            'Credit Card Barclay',
            'Credit Card Chase',
            'Debit Card Beyond Banking',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Car Expense', 'Auto Club' ],
        [
            'AAA'
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Car Expense', 'Auto Insurance' ],
        [
            '21st Century',
            'Arbella Mutual',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Car Expense', 'Auto Repair' ],
        [
            'DeMarc Auto Repair',
            'Independent Auto',
            'Jim Aloisio',
            'Sears Auto Center',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Banking', 'Merryl Lynch' ],
        [
            'ML Investment Account',
            'Paypal',
            'Kurt Wegner',
            'Account Receiving Wire',
            'ML Fee Administration',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'House Expense', 'Cable' ],
        [
            'AT&T Internet Service',
            'US Cable',
            'Baja Broadband',
            'Comcast',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Living Expense', 'Education' ],
        [
            'Univ Colorado',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'House Expense', 'Electricity' ],
        [
            'IREA',
            'NSTAR',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Living Expense', 'Entertainment' ],
        [
            'Pandora Music',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Charitable Donations', 'Churches' ],
        [
            'The Living Room',
            'Salvation Army',
            'SFVHC',
            'Vietnamese Evangelical Church',
            'West LA Holiness',
            'Woodland Park Community Church',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Charitable Donations', 'Missions' ],
        [
            'AIM', 
            'Bethany Christian Services', 
            'Campus Crusade',
            'Beate Reins',
            'Harvest Family Church',
            'JEMS',
            'The Lion of Judah Ministries, Inc.',
            'Friends of Faraja USA',
            'Faraja Orphans Rescue Ministry',
            'Mission to the World',
            'Hank and Cathy Pott',
            'Sheila Dilworth',
            'Special Camp',
            'World Gospel Mission',
            'World Vision',
            'Yekope Ministries',
            'ZOE International',
            'Other Beneficiary Account',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Other', 'Food' ],
        [
            'Food',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'House Expense', 'Natural Gas' ],
        [
            'National Grid',
            'Black Hills Energy',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Government Taxes', 'Federal' ],
        [
            'Federal Government',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Government Taxes', 'State' ],
        [
            'State of Colorado',
            'State of California',
            'Commonwealth of Massachusettes',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Government Taxes', 'Other' ],
        [
            'Other Tax Account',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'House Expense', 'House Insurance' ],
        [
            'Old Cape Cod Insurance',

            'Allstate',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'House Expense', 'House Maintenance' ],
        [
            'Andys Plumbing',
            'Doreen Kelley',
            'Forest Keepers',
            'Front Range Arbolists',
            'Green Lawn Treatment',
            'John Harnish',
            'John Viola',
            'Larry Bernard',
            'Post Office Box',
            'Viola Associates',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Living Expense', 'Immigration' ],
        [
            'Immigration',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Income', 'ITT Benefits' ],
        [
            'ITT Pension',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Living Expense', 'Medical and Dental' ],
        [
            'Heidi Chan DDS',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Banking', 'Mortgage' ],
        [
            'Fifth Third Bank',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'House Expense', 'Phone' ],
        [
            'Qwest',
            'Verizon',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Living Expense', 'Family and Friends' ],
        [
            'Danielle Perez',
            'Davida Wegner',
            'Karl Wegner',
            'Meredith Wegner',
            'Danny Perez',
            'James Amato',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Living Expense', 'Online Purchase' ],
        [
            'Amazon',
            'New Egg',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Living Expense', 'Other Purchase' ],
        [
            'Misc Account',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Other', 'ALIAS NOT FOUND' ],
        [
            'ALIAS NOT FOUND',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Income', 'Salary' ], 
        [
            'ITT Exelis',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'House Expense', 'Trash Collection' ], 
        [
            'Macombers Sanitary',
            'Waste Management',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'Living Expense', 'Transportation' ], 
        [
            'Transportation',
        ])

        self.insertElementsIntoMinimalSubset(
        [ 'SubdivisionA', 'House Expense', 'Water' ], 
        [
            'Hyannis Water',
            'Woodland Park Water and Sewer',
        ])


