
import re
from utils.Container import * 

###############################################################################
# allow access to these internal items
############################################################################### 
__all__ = \
[
    "EquivTransactionCategory",
    "EquivAccounts",
]

###############################################################################
# Mechanisms.Base
###############################################################################
class Base(EquivClasses):

    # constructor
    def __init__(self):
        EquivClasses.__init__(self)
        return None

    # virtual method
    def classNames(self): return set([
        'ATM Beyond Banking',
        'AAA',
        '21st Century',
        'Arbella Mutual',
        'DeMarc Auto Repair',
        'Independent Auto',
        'Jim Aloisio',
        'Sears Auto Center',
        'Beyond Banking',
        'Credit Card Bank of America',
        'Credit Card Barclay',
        'Credit Card Chase',
        'AT&T Internet Service',
        'US Cable',
        'Baja Broadband',
        'Comcast',
        'Univ Colorado',
        'IREA',
        'NSTAR',
        'Pandora Music',
        'Flowers',
        'Food',
        'National Grid',
        'Black Hills Energy',
        'Government Taxes',
        'Old Cape Cod Insurance',
        'Allstate',
        'House Maintenance',
        'Immigration',
        'ITT Pension',
        'Heidi Chan DDS',
        'Fifth Third Bank',
        'Qwest',
        'Verizon',
        'Other Purchase',
        'ITT Exelis',
        'Macombers Sanitary',
        'Waste Management',
        'Transportation',
        'Hyannis Water',
        'Woodland Park Water and Sewer',
    ])


    # virtual method
    def matchesCriteriaOfEquivClass(self, account, also_known_as, also_known_as2='', also_known_as3=''):

        if account == 'ATM Beyond Banking' and self.matchesLeadingText(set([
                'ATM',
            ]), also_known_as):
            return True;

        elif account == 'AAA' and self.matchesLeadingText(set([
            
                'AAA MEMBERSHIP'

            ]), also_known_as): return True;

        elif account == '21st Century' and self.matchesLeadingText(set([
            
                '21STCENTURY',

            ]), also_known_as): return True;

        elif account == 'Arbella Mutual' and self.matchesLeadingText(set([
            
                'ARBELLA INSURANC',
                'ARBELLA MUTUAL',

            ]), also_known_as): return True;

        elif account == 'DeMarc Auto Repair' and self.matchesLeadingText(set([
            
                'CK6497COSPRNGS10082808 COLORADO SPRI CO Service Stations',

            ]), also_known_as): return True;

        elif account == 'Independent Auto' and self.matchesLeadingText(set([
            
                'INDEPENDENT AUTO',

            ]), also_known_as): return True;

        elif account == 'Jim Aloisio' and self.matchesLeadingText(set([
            
                'JIM ALOISIO',

            ]), also_known_as): return True;

        elif account == 'Sears Auto Center' and self.matchesLeadingText(set([
            
                'SEARS AUTO CNTR',

            ]), also_known_as): return True;

        elif account == 'Beyond Banking' and self.matchesLeadingText(set([
            
                'BANK DEPOSIT',
                'CHECK DEPOSIT',
                'ML BANK DEPOSIT PROGRAM',
                'PAYPAL',
                'TRANSAMERICA ASSET ALLOCATION',
                'TRANSFR FEE',
                'WIRE TRF IN',
                'WIRE TRF OUT',
                'CASH',

            ]), also_known_as): return True;

        elif account == 'Credit Card Bank of America' and self.matchesLeadingText(set([
            
                'BANK OF AMERICA',

            ]), also_known_as): return True;

        elif account == 'Credit Card Barclay' and self.matchesLeadingText(set([
            
                'BARCLAYCARD US',

            ]), also_known_as): return True;

        elif account == 'Credit Card Chase' and self.matchesLeadingText(set([
            
                'CHASE',

            ]), also_known_as): return True;

        elif account == 'AT&T Internet Service' and self.matchesLeadingText(set([
            
                'AT&T INTERNET SVC',

            ]), also_known_as): return True;

        elif account == 'US Cable' and self.matchesLeadingText(set([
            
                'US CABLE 687',
                'US CABLE OF COLO',

            ]), also_known_as): return True;

        elif account == 'Baja Broadband' and self.matchesLeadingText(set([
            
                'BAJA BROADBAND',

            ]), also_known_as): return True;

        elif account == 'Comcast' and self.matchesLeadingText(set([
            
                'COMCAST',

            ]), also_known_as): return True;

        elif account == 'Univ Colorado' and self.matchesLeadingText(set([
            
                'CAMPUS WIDE EXTE',
                'UCCS VISITOR PARKING',

            ]), also_known_as): return True;

        elif account == 'IREA' and self.matchesLeadingText(set([
            
                'Intermountain Ru',
                'IREA',

            ]), also_known_as): return True;

        elif account == 'NSTAR' and self.matchesLeadingText(set([
            
                'NSTAR',

            ]), also_known_as): return True;

        elif account == 'Pandora Music' and self.matchesLeadingText(set([
            
                'PANDORA.COM',

            ]), also_known_as): return True;

        elif account == 'Flowers' and self.matchesLeadingText(set([
            
                'AFRICA INLAND MI',
                'AFRICA ISLAND MI',
                'BETHANY CHRISTIA',
                'CAMPUS CRUSADE',
                'EFCA',
                'HARVEST FAM',
                'JEMS',
                'LION OF JUDAH MI',
                'LIVING ROOM 673',
                'MISSION TO THE W',
                'OC INT',
                'SALVATION ARMY',
                'SFVHC',
                'SFVHC BLDG FUND',
                'SHEILA DILWORTH',
                'THE LION OF JUDA',
                'THE LIVING ROOM',
                'VAL SATOW',
                'VIETNAMESE EVANG',
                'WEST LA HOLINESS',
                'WORLD GOSPEL MISSION',
                'World Gospel Mis',
                'World Vision',
                'YEKOPE MINIST',
                'ZOE INTERNATIONA',
                'WOODLAND PARK CO',
                'VOICE 679',
                '84301767',
                'COLORADO PEACE O',
                'ERRC 747',
                'SANTANA'

            ]), also_known_as): return True;

        elif account == 'Food' and self.matchesLeadingText(set([
            
                "AAFES PABF CHARLEY'S",
                'AAFES PETERSON TACO BELL',
                'CAFFE EDOLCI',
                'ASIAN PACIFIC MARK COLORADO SPRI CO',
                'CK6497COSPRNGS10082808 COLORADO SPRI CO Service Stations',
                'DUTCH BROS COFFEE',
                'GOLD HILL JAVA',
                'HUNGRY BEAR RESTAURANT',
                'KING SOOPERS',
                'LA CASITA PATIO CAFE',
                'MARIKAS COFFEE HOUSE',
                'MOONSTAR II CHINESE',
                "PALMS FOOD INT'L",
                'PIKES PERK',
                'SAFEWAY STORE',
                'SUBWAY',

            ]), also_known_as): return True;

        elif account == 'National Grid' and self.matchesLeadingText(set([
            
                'NATIONAL GRID NE',

            ]), also_known_as): return True;

        elif account == 'Black Hills Energy' and self.matchesLeadingText(set([
            
                'BLACK HILLS'

            ]), also_known_as): return True;

        elif account == 'Government Taxes' and self.matchesLeadingText(set([
            
                'CO DEPT REVENUE',
                'colorado.gov',
                'COMM. OF MASS.',
                'DEPT OF MOTOR VE',
                'DMV',
                'FRANCHISE TAX BD',
                'ICI',
                'INVOICECLOUD-TAX',
                'IRS',
                'TAX PRODUCTS',
                'TELLER CO CLERK',
                'TOWN OF BARNSTAB',
                'CO DEPT OF REV',
                'COLORADO DEPT OF',
                'ICI*BARNSTABLE',

            ]), also_known_as): return True;

        elif account == 'Old Cape Cod Insurance' and self.matchesLeadingText(set([
            
                'MASS PROPERTY IN',

            ]), also_known_as): return True;

        elif account == 'Allstate' and self.matchesLeadingText(set([

                'ALLSTATE'

            ]), also_known_as): return True;

        elif account == 'House Maintenance' and self.matchesLeadingText(set([
            
                'ANDYS PLUMBING',
                'DOREEN KELLEY',
                'FOREST KEEPERS',
                'FRONT RANGE ARBO',
                'GREEN LAWN TREAT',
                'JOHN HARNISH',
                'JOHN VIOLA',
                'LARRY BERNARD',
                'USPS PO BOXES',
                'VIOLA ASSN INC',
                'VIOLA ASSOCIATES',
                'GREEN LANW TREAT',

            ]), also_known_as): return True;

        elif account == 'Immigration' and self.matchesLeadingText(set([
            
                'USCIS DALLAS',

            ]), also_known_as): return True;

        elif account == 'ITT Pension' and self.matchesLeadingText(set([
            
                'ACS HR SOLUTIONS',
                'BENEFIT PAYMENTS'

            ]), also_known_as): return True;

        elif account == 'Heidi Chan DDS' and self.matchesLeadingText(set([
            
                'HEIDI L CHAN DDS',

            ]), also_known_as): return True;

        elif account == 'Fifth Third Bank' and self.matchesLeadingText(set([
            
                '5/3 MORTGAGE LN',
                'FIFTH THIRD BANK',
                'ITT ISP CLEARING',
                'CKYY 09073-00092 JAMES AMATO',
                'REAL LIVING SELE',

            ]), also_known_as): return True;

        elif account == 'Qwest' and self.matchesLeadingText(set([
            
                'QWEST',

            ]), also_known_as): return True;

        elif account == 'Verizon' and self.matchesLeadingText(set([
            
                'VERIZON WIRELESS',

            ]), also_known_as): return True;

        elif account == 'Other Purchase' and self.matchesLeadingText(set([
            
                'AMAZON MARKETPLA',
                'CHECKMATE PIANO',
                'DANIELLE PEREZ',
                'DAVIDA WEGNER',
                'KARL WEGNER',
                'MEREDITH FLYNN',
                'NARITA AIRPORT TERMINAL',
                'SECURITY FIRST SELF STORA',
                'SPRINGS CPR TRAI',
                'WWW.NEWEGG.COM',

            ]), also_known_as): return True;

        elif account == 'ITT Exelis' and self.matchesLeadingText(set([
            
                'EXELIS SYSTEMS C',
                'ITT SYSTEMS CORP',
                'BENEFIT PAYMENTS',

            ]), also_known_as): return True;

        elif account == 'Macombers Sanitary' and self.matchesLeadingText(set([
            
                'MACOMBERS SANITA',

            ]), also_known_as): return True;

        elif account == 'Waste Management' and self.matchesLeadingText(set([
            
                'CURBSIDE RECYCLI',
                'Waste Management',

            ]), also_known_as): return True;

        elif account == 'Transportation' and self.matchesLeadingText(set([
            
                'PLYMOUTH & BROCKTON',
                'NNT BART-POWELL',

            ]), also_known_as): return True;

        elif account == 'Hyannis Water' and self.matchesLeadingText(set([
            
                'Hyannis Water MA',
                'HYANNIS WATER MA',
                'MCC eBill',
                'MCC EBILL',

            ]), also_known_as): return True;

        elif account == 'Woodland Park Water and Sewer' and self.matchesLeadingText(set([
            
                'CITY OF WOODLAND',
                'WOODLAND PARK',

            ]), also_known_as): return True;

        else:
            return False
 
###############################################################################
# EquivTransactionCategory
###############################################################################
class EquivTransactionCategory(EquivClasses):

    # constructor
    def __init__(self):
        EquivClasses.__init__(self)
        return None

    # virtual method
    def classNames(self): return set([
        'ATM',
        'Auto Club',
        'Auto Insurance',
        'Auto Repair',
        'Banking',
        'Credit Card',
        'Cable',
        'Education',
        'Electricity',
        'Entertainment',
        'Flowers',
        'Food',
        'Gas',
        'Government Taxes',
        'House Insurance',
        'House Maintenance',
        'Immigration',
        'ITT Benefits',
        'Medical and Dental',
        'Mortgage',
        'Phone',
        'Other Purchase',
        'Salary',
        'Trash Collection',
        'Transportation',
        'UNCLASSIFIED',
        'Water',
    ])

    # virtual method
    def matchesCriteriaOfEquivClass(self, classname, item, item2='', item3=''):

        if classname == 'ATM' and self.matchesLeadingText(set([
                'ATM',
            ]), item):
            return True;

        elif classname == 'Auto Club' and self.matchesLeadingText(set([
            
                'AAA MEMBERSHIP'

            ]), item): return True;

        elif classname == 'Auto Insurance' and self.matchesLeadingText(set([
            
                '21STCENTURY',
                'ARBELLA INSURANC',
                'ARBELLA MUTUAL',

            ]), item): return True;

        elif classname == 'Auto Repair' and self.matchesLeadingText(set([
            
                'CK6497COSPRNGS10082808 COLORADO SPRI CO Service Stations',
                'INDEPENDENT AUTO',
                'JIM ALOISIO',
                'SEARS AUTO CNTR',
                'INDEPENDENT AUTO'

            ]), item): return True;

        elif classname == 'Banking' and self.matchesLeadingText(set([
            
                'BANK DEPOSIT',
                'CHECK DEPOSIT',
                'ML BANK DEPOSIT PROGRAM',
                'PAYPAL',
                'TRANSAMERICA ASSET ALLOCATION',
                'TRANSFR FEE',
                'WIRE TRF IN',
                'WIRE TRF OUT',
                'CASH',

            ]), item): return True;

        elif classname == 'Credit Card' and self.matchesLeadingText(set([
            
                'BANK OF AMERICA',
                'BARCLAYCARD US',
                'CHASE',

            ]), item): return True;

        elif classname == 'Cable' and self.matchesLeadingText(set([
            
                'BAJA BROADBAND',
                'COMCAST',
                'US CABLE 687',
                'AT&T INTERNET SVC',
                'US CABLE OF COLO',

            ]), item): return True;

        elif classname == 'Education' and self.matchesLeadingText(set([
            
                'CAMPUS WIDE EXTE',
                'UCCS VISITOR PARKING',

            ]), item): return True;

        elif classname == 'Electricity' and self.matchesLeadingText(set([
            
                'Intermountain Ru',
                'IREA',
                'NSTAR',

            ]), item): return True;

        elif classname == 'Entertainment' and self.matchesLeadingText(set([
            
                'PANDORA.COM',

            ]), item): return True;

        elif classname == 'Flowers' and self.matchesLeadingText(set([
            
                'AFRICA INLAND MI',
                'AFRICA ISLAND MI',
                'BETHANY CHRISTIA',
                'CAMPUS CRUSADE',
                'EFCA',
                'HARVEST FAM',
                'JEMS',
                'LION OF JUDAH MI',
                'LIVING ROOM 673',
                'MISSION TO THE W',
                'OC INT',
                'SALVATION ARMY',
                'SFVHC',
                'SFVHC BLDG FUND',
                'SHEILA DILWORTH',
                'THE LION OF JUDA',
                'THE LIVING ROOM',
                'VAL SATOW',
                'VIETNAMESE EVANG',
                'WEST LA HOLINESS',
                'WORLD GOSPEL MISSION',
                'World Gospel Mis',
                'World Vision',
                'YEKOPE MINIST',
                'ZOE INTERNATIONA',
                'WOODLAND PARK CO',
                'VOICE 679',
                '84301767',
                'COLORADO PEACE O',
                'ERRC 747',
                'SANTANA'

            ]), item): return True;

        elif classname == 'Food' and self.matchesLeadingText(set([
            
                "AAFES PABF CHARLEY'S",
                'AAFES PETERSON TACO BELL',
                'CAFFE EDOLCI',
                'ASIAN PACIFIC MARK COLORADO SPRI CO',
                'CK6497COSPRNGS10082808 COLORADO SPRI CO Service Stations',
                'DUTCH BROS COFFEE',
                'GOLD HILL JAVA',
                'HUNGRY BEAR RESTAURANT',
                'KING SOOPERS',
                'LA CASITA PATIO CAFE',
                'MARIKAS COFFEE HOUSE',
                'MOONSTAR II CHINESE',
                "PALMS FOOD INT'L",
                'PIKES PERK',
                'SAFEWAY STORE',
                'SUBWAY',

            ]), item): return True;

        elif classname == 'Gas' and self.matchesLeadingText(set([
            
                'NATIONAL GRID NE',
                'BLACK HILLS'

            ]), item): return True;

        elif classname == 'Government Taxes' and self.matchesLeadingText(set([
            
                'CO DEPT REVENUE',
                'colorado.gov',
                'COMM. OF MASS.',
                'DEPT OF MOTOR VE',
                'DMV',
                'FRANCHISE TAX BD',
                'ICI',
                'INVOICECLOUD-TAX',
                'IRS',
                'TAX PRODUCTS',
                'TELLER CO CLERK',
                'TOWN OF BARNSTAB',
                'CO DEPT OF REV',
                'COLORADO DEPT OF',
                'ICI*BARNSTABLE',

            ]), item): return True;

        elif classname == 'House Insurance' and self.matchesLeadingText(set([
            
                'MASS PROPERTY IN',
                'ALLSTATE'

            ]), item): return True;

        elif classname == 'House Maintenance' and self.matchesLeadingText(set([
            
                'ANDYS PLUMBING',
                'DOREEN KELLEY',
                'FOREST KEEPERS',
                'FRONT RANGE ARBO',
                'GREEN LAWN TREAT',
                'JOHN HARNISH',
                'JOHN VIOLA',
                'LARRY BERNARD',
                'USPS PO BOXES',
                'VIOLA ASSN INC',
                'VIOLA ASSOCIATES',
                'GREEN LANW TREAT',

            ]), item): return True;

        elif classname == 'Immigration' and self.matchesLeadingText(set([
            
                'USCIS DALLAS',

            ]), item): return True;

        elif classname == 'ITT Benefits' and self.matchesLeadingText(set([
            
                'ACS HR SOLUTIONS',
                'BENEFIT PAYMENTS'

            ]), item): return True;

        elif classname == 'Medical and Dental' and self.matchesLeadingText(set([
            
                'HEIDI L CHAN DDS',
                'ACS HR SOLUTIONS',

            ]), item): return True;

        elif classname == 'Mortgage' and self.matchesLeadingText(set([
            
                '5/3 MORTGAGE LN',
                'FIFTH THIRD BANK',
                'ITT ISP CLEARING',
                'CKYY 09073-00092 JAMES AMATO',
                'REAL LIVING SELE',

            ]), item): return True;

        elif classname == 'Phone' and self.matchesLeadingText(set([
            
                'QWEST',
                'VERIZON WIRELESS',

            ]), item): return True;

        elif classname == 'Other Purchase' and self.matchesLeadingText(set([
            
                'AMAZON MARKETPLA',
                'CHECKMATE PIANO',
                'DANIELLE PEREZ',
                'DAVIDA WEGNER',
                'KARL WEGNER',
                'MEREDITH FLYNN',
                'NARITA AIRPORT TERMINAL',
                'SECURITY FIRST SELF STORA',
                'SPRINGS CPR TRAI',
                'WWW.NEWEGG.COM',

            ]), item): return True;

        elif classname == 'Salary' and self.matchesLeadingText(set([
            
                'EXELIS SYSTEMS C',
                'ITT SYSTEMS CORP',
                'BENEFIT PAYMENTS',

            ]), item): return True;

        elif classname == 'Trash Collection' and self.matchesLeadingText(set([
            
                'CURBSIDE RECYCLI',
                'MACOMBERS SANITA',
                'Waste Management',

            ]), item): return True;

        elif classname == 'Transportation' and self.matchesLeadingText(set([
            
                'PLYMOUTH & BROCKTON',
                'NNT BART-POWELL',

            ]), item): return True;

        elif classname == 'Water' and self.matchesLeadingText(set([
            
                'CITY OF WOODLAND',
                'Hyannis Water MA',
                'HYANNIS WATER MA',
                'WOODLAND PARK',
                'MCC eBill',
                'MCC EBILL',
            ]), item): return True;

        else:
            return False

###############################################################################
# MapAccountToEquivalence2
###############################################################################
class MapAccountToEquivalence2(EquivClasses):

    # constructor
    def __init__(self):
        EquivClasses.__init__(self)
        return None

    # virtual method
    def classNames(self): return set([
        'Banking',
        'Credit Card',
        'House Expense',
        'Flowers',
        'Income',
        'Mortgage',
        'Government Taxes',
        'Other',
    ])

    # virtual method
    def matchesCriteriaOfEquivClass(self, classname, type1, type2, item3=''):
        item = type1

        if classname == 'House Expense' and self.matchesExactly(set([
            'Auto Club',
            'Auto Insurance',
            'Auto Repair',
            'Cable',
            'Electricity',
            'Gas',
            'House Insurance',
            'House Maintenance',
            'Phone',
            'Trash Collection',
            'Water',
        ]), item): return True;

        elif classname == 'Banking' and self.matchesExactly(set([
            'ATM',
            'Banking',
        ]), item): return True;

        elif classname == 'Credit Card' and self.matchesExactly(set([
            'Credit Card',
        ]), item): return True;

        elif classname == 'Flowers' and self.matchesExactly(set([
            'Flowers',
        ]), item): return True;

        elif classname == 'Mortgage' and self.matchesExactly(set([
            'Mortgage',
        ]), item): return True;
 
        elif classname == 'Government Taxes' and self.matchesExactly(set([
            'Government Taxes',
        ]), item): return True;
 
        elif classname == 'Other' and self.matchesExactly(set([
            'Education',
            'Entertainment',
            'Food',
            'Immigration',
            'Medical and Dental',
            'Other Purchase',
            'Transportation',
        ]), item): return True;
 
        elif classname == 'Income' and self.matchesExactly(set([
            'Salary',
            'ITT Benefits',
        ]), item): return True;
 
        else:
            return False

###############################################################################
# MapFieldsToMechanism
###############################################################################
class MapFieldsToMechanism(EquivClasses):

    # constructor
    def __init__(self):
        EquivClasses.__init__(self)
        return None

    # virtual method
    def classNames(self): return list([
        'ATM Cash (debit)'         , # 0
        'ATM Fee (credit)'         , # 1
        'Bank Check (debit)'       , # 2
        'Bank Interest (credit)'   , # 3
        'Credit Card (debit)'      , # 4
        'Electronic (debit)'       , # 5
        'Electronic (credit)'      , # 6
        'Fee Charged (debit)'      , # 7
        'Journal Entry'            , # 8
        'ML BillPay (debit)'       , # 9
        'Paper Check (credit)'     , # 10
        'Paper Check (debit)'      , # 11
        'Wire Transfer (debit)'    , # 12
        'UNCLASSIFIED'
    ])

    # virtual method
    def matchesCriteriaOfEquivClass(self, classname, type1, type2, item3=''):
        name = self.classNames()
 
        if ( classname == name[0] # 'ATM Cash'
        and      type1 == 'ATM'
        and      type2 == 'Cash Machine'
        ): return True

        if ( classname == name[1] # 'ATM Fee Credit'
        and      type1 == 'ATMRefund'
        and      type2 == 'ATM Refund'
        ): return True
  
 
        if ( classname == name[2] # 'Bank Check Debit'
        and      type1 == 'Other'
        and      type2 == 'Withdrawal'
        ): return True
  
        if ( classname == name[3] # 'Bank Interest'
        and      type1 == 'DividendAndInterest'
        and      type2 == 'Bank Interest'
        ): return True

        if ( classname == name[4] # 'Credit Card Debit'
        and      type1 == 'VisaTransactions'
        and      type2 == 'Deferred'
        ): return True
   
        if ( classname == name[5] # 'Electronic Debit'
        and      type1 == 'Other'
        and      type2 == 'Pre Authdebit'
        ): return True
  
        if ( classname == name[6] # 'Electronic Credit'
        and      type1 == 'FundReceipts'
        and      type2 == 'DDS'
        ): return True
  
        if ( classname == name[7] # 'Fee Charged'
        and      type1 == 'Other'
        and      type2 == 'Journal Entry'
        ): return True
  
        if ( classname == name[8] # 'Journal Entry'
        and      type1 == 'SecurityTransactions'
        and      type2 == 'Journal Entry'
        ): return True
  
        if ( classname == name[9] # 'ML BillPay'
        and      type1 == 'BillPay'
        and      type2 == 'Bill Payment'
        ): return True
  
        if ( classname == name[10] # 'Paper Check Credit'
        and      type1 == 'FundReceipts'
        and      type2 == 'Funds Received'
        ): return True

        if ( classname == name[11] # 'Paper Check Debit'
        and      type1 == 'Checking'
        ): return True
  
        if ( classname == name[12] # 'Wire Transfer'
        and      type1 == 'FundTransfers'
        and      type2 == 'Funds Transfer'
        ): return True
 
        else:
            return False

 

###############################################################################
# Also Known As
###############################################################################
def alsoKnownAs():
    setA = set([
    '21STCENTURY',
    '5/3 MORTGAGE LN',
    '84301767',
    'AAA MEMBERSHIP RENEWAL-A 800-222-8794 CA Other/Unclassified PROCESSED',
    "AAFES PABF CHARLEY'S STE PETERSON AFB CO Other/Unclassified PROCESSED",
    'AAFES PETERSON TACO BELL PETERSON AFB CO Other/Unclassified PROCESSED',
    'ACS HR SOLUTIONS00880326',
    'AFRICA INLAND MI',
    'AFRICA ISLAND MI 672',
    'AFRICA ISLAND MI 681',
    'ALLSTATE 767',
    'AMAZON MARKETPLA',
    'ANDYS PLUMBING 757',
    'ARBELLA INSURANC',
    'ARBELLA MUTUAL',
    'ASIAN PACIFIC MARK COLORADO SPRI CO Merchandise PROCESSED',
    'ATM 0008210 REFUND AURORA CO 09/06',
    'ATM 008210 AURORA CO 09/06',
    'ATM 0141124 REFUND COLORADO SPGS CO 03/15',
    'ATM 0550458 REFUND BLYTHE CA 02/20',
    'ATM 0573891 REFUND COLORADO SPRI CO 02/22',
    'ATM 0587880 REFUND SANTA MONICA CA 06/21',
    'ATM 141124 COLORADO SPGS CO 03/15',
    'ATM 338514 AMBON 12/30 2,000,000.00 IDR Or $219.43 + $4.39 Int.Trn.Fee',
    'ATM 338522 AMBON 12/30 2,000,000.00 IDR Or $219.43 + $4.39 Int.Trn.Fee',
    'ATM 338533 AMBON 12/30 1,000,000.00 IDR Or $109.71 + $2.19 Int.Trn.Fee',
    'ATM 357774 DENPASAR 12/31 1,500,000.00 IDR Or $166.24 + $3.32 Int.Trn.Fee',
    'ATM 387763 RENON 01/03 1,500,000.00 IDR Or $166.24 + $3.32 Int.Trn.Fee',
    'ATM 452012 SURABAYA 08/03 1,000,000.00 IDR Or $106.02 + $2.12 Int.Trn.Fee',
    'ATM 521209 MAKASSAR 04/11 2,000,000.00 IDR Or $219.31 + $4.39 Int.Trn.Fee',
    'ATM 550458 BLYTHE CA 02/20',
    'ATM 573891 COLORADO SPRI CO 02/22',
    'ATM 587880 SANTA MONICA CA 06/21',
    'ATM 649977 BOGOR 12/22 1,000,000.00 IDR Or $110.38 + $2.21 Int.Trn.Fee',
    'ATM 774436 JAKARTA 12/16 1,000,000.00 IDR Or $110.02 + $2.20 Int.Trn.Fee',
    'ATM 911041 JAKARTA 09/08 2,500,000.00 IDR Or $293.05 + $5.86 Int.Trn.Fee',
    'ATM LOS ANGELES CA 04/03',
    'ATM ROTENBURG1 05/10 200.00 EUR Or $287.68 + $5.75 Int.Trn.Fee',
    'AT&T INTERNET SVC 877-SBCDSL5 TX Other/Unclassified PROCESSED',
    'BAJA BROADBAND',
    'BANK DEPOSIT INT 04/15',
    'BANK DEPOSIT INTEREST FROM 01/01 THRU 01/30',
    'BANK DEPOSIT INTEREST FROM 01/31 THRU 02/27',
    'BANK DEPOSIT INTEREST FROM 01/31 THRU 02/28',
    'BANK DEPOSIT INTEREST FROM 02/28 THRU 03/30',
    'BANK DEPOSIT INTEREST FROM 02/29 THRU 03/29',
    'BANK DEPOSIT INTEREST FROM 03/30 THRU 04/29',
    'BANK DEPOSIT INTEREST FROM 03/31 THRU 04/28',
    'BANK DEPOSIT INTEREST FROM 04/29 THRU 05/30',
    'BANK DEPOSIT INTEREST FROM 04/30 THRU 05/30',
    'BANK DEPOSIT INTEREST FROM 05/31 THRU 06/28',
    'BANK DEPOSIT INTEREST FROM 05/31 THRU 06/29',
    'BANK DEPOSIT INTEREST FROM 06/29 THRU 07/30',
    'BANK DEPOSIT INTEREST FROM 06/30 THRU 07/28',
    'BANK DEPOSIT INTEREST FROM 07/29 THRU 08/30',
    'BANK DEPOSIT INTEREST FROM 07/31 THRU 08/30',
    'BANK DEPOSIT INTEREST FROM 08/31 THRU 09/29',
    'BANK DEPOSIT INTEREST FROM 09/30 THRU 10/28',
    'BANK DEPOSIT INTEREST FROM 09/30 THRU 10/30',
    'BANK DEPOSIT INTEREST FROM 10/29 THRU 11/29',
    'BANK DEPOSIT INTEREST FROM 10/31 THRU 11/29',
    'BANK DEPOSIT INTEREST FROM 11/30 THRU 12/30',
    'BANK DEPOSIT INTEREST FROM 11/30 THRU 12/31',
    'BANK DEPOSIT INTEREST FROM 12/31 THRU 01/30',
    'BANK OF AMERICA',
    'BARCLAYCARD US',
    'BENEFIT PAYMENTS',
    'BETHANY CHRISTIA00880151',
    'BETHANY CHRISTIA00880155',
    'BETHANY CHRISTIA00880292',
    'BETHANY CHRISTIA 697',
    'BETHANY CHRISTIA 750',
    'BLACK HILLS UTLH',
    'CAFFE EDOLCI 667',
    'CAMPUS CRUSADE F',
    'CAMPUS WIDE EXTE 754',
    'CASH 769',
    'CHASE',
    'CHECK DEPOSIT01/03*',
    'CHECK DEPOSIT07/22*',
    'CHECK DEPOSIT',
    'CHECKMATE PIANO 700',
    'CITY OF WOODLAND 691',
    'CITY OF WOODLAND',
    'CK6497COSPRNGS10082808 COLORADO SPRI CO Service Stations PROCESSED',
    'CKYY 09073-00092 JAMES AMATO OFFICIAL CHECK # 00092',
    'CO DEPT OF REV 731',
    'CO DEPT REVENUE',
    'COLORADO DEPT OF 748',
    'colorado.gov',
    'COLORADO PEACE O 694',
    'COMCAST',
    'COMM. OF MASS.',
    'CURBSIDE RECYCLI 695',
    'DANIELLE PEREZ 744',
    'DANIELLE PEREZ 749',
    'DAVIDA WEGNER 759',
    'DAVIDA WEGNER 761',
    'DEPT OF MOTOR VE 662',
    'DMV 669',
    'DOREEN KELLEY 00880168',
    'DOREEN KELLEY 00880261',
    'DOREEN KELLEY 739',
    'DUTCH BROS COFFEE - PL COLORADO SPRI CO Other/Unclassified PROCESSED',
    'EFCA 00880114',
    'EFCA 00880115',
    'EFCA 00880123',
    'EFCA 00880133',
    'EFCA 00880140',
    'EFCA 00880147',
    'EFCA 00880164',
    'EFCA 00880178',
    'EFCA 00880189',
    'EFCA 00880201',
    'EFCA 00880221',
    'EFCA 00880234',
    'EFCA 00880248',
    'EFCA 00880276',
    'EFCA 00880293',
    'EFCA 00880306',
    'EFCA ATTN DONOR 00880211',
    'EFCA ATTN DONOR 00880260',
    'ERRC 747',
    'EXELIS SYSTEMS C',
    'FIFTH THIRD BANK 688',
    'FOREST KEEPERS T00880225',
    'FRANCHISE TAX BD',
    'FRONT RANGE ARBO00880277',
    'FRONT RANGE ARBO 751',
    'GOLD HILL JAVA WOODLAND PARK CO Other/Unclassified PROCESSED',
    'GREEN LANW TREAT 735',
    'GREEN LAWN TREAT00880179',
    'GREEN LAWN TREAT00880236',
    'GREEN LAWN TREAT 698',
    'HARVEST FAM CH 00880268',
    'HARVEST FAMILY C00880105',
    'HARVEST FAMILY C00880106',
    'HARVEST FAMILY C00880113',
    'HARVEST FAMILY C00880122',
    'HARVEST FAMILY C00880132',
    'HARVEST FAMILY C00880137',
    'HARVEST FAMILY C00880146',
    'HARVEST FAMILY C00880163',
    'HARVEST FAMILY C00880187',
    'HARVEST FAMILY C00880197',
    'HARVEST FAMILY C00880209',
    'HARVEST FAMILY C00880220',
    'HARVEST FAMILY C00880232',
    'HARVEST FAMILY C00880246',
    'HARVEST FAMILY C00880258',
    'HARVEST FAMILY C00880289',
    'HARVEST FAMILY C00880305',
    'HEIDI L CHAN DDS 766',
    'HUNGRY BEAR RESTAURANT WOODLAND PARK CO Restaurants PROCESSED',
    'Hyannis Water MA',
    'HYANNIS WATER MA',
    'ICI*BARNSTABLE',
    'INDEPENDENT AUTO 752',
    'Intermountain Ru',
    'INVOICECLOUD-TAX',
    'IREA',
    'IRS',
    'ITT ISP CLEARING',
    'ITT SYSTEMS CORP',
    'JEMS 728',
    'JEMS 765',
    'JIM ALOISIO 671',
    'JOHN HARNISH 00880294',
    'JOHN HARNISH 753',
    'JOHN VIOLA 00880149',
    'JOHN VIOLA 00880167',
    'JOHN VIOLA 00880180',
    'JOHN VIOLA 00880190',
    'JOHN VIOLA 00880202',
    'JOHN VIOLA 00880262',
    'JOHN VIOLA 00880264',
    'JOHN VIOLA 00880280',
    'JOHN VIOLA 00880296',
    'JOHN VIOLA 00880322',
    'JOHN VIOLA 00880324',
    'JOHN VIOLA 678',
    'JOHN VIOLA 729',
    'JOHN VIOLA 737',
    'JOHN VIOLA 741',
    'JOHN VIOLA 746',
    'KARL WEGNER 00880152',
    'KING SOOPERS DENVER Merchandise PROCESSED',
    'LA CASITA PATIO CAFE COLORADO SPRI CO Other/Unclassified PROCESSED',
    'LARRY BERNARD 762',
    'LARRY BERNARD 764',
    'LION OF JUDAH MI 676',
    'LION OF JUDAH MI 683',
    'LION OF JUDAH MI 684',
    'LION OF JUDAH MI 685',
    'LIVING ROOM 673',
    'MACOMBERS SANITA00880279',
    'MACOMBERS SANITARY REFUSE MARSTON MILLS MA Merchandise PROCESSED',
    'MARIKAS COFFEE HOUSE MANITOU SPRIN CO Restaurants PROCESSED',
    'MASS PROPERTY IN',
    'MCC eBill',
    'MCC EBILL',
    'MEREDITH FLYNN 732',
    'MISSION TO THE W00880108',
    'MISSION TO THE W00880109',
    'MISSION TO THE W00880121',
    'MISSION TO THE W00880127',
    'MISSION TO THE W00880139',
    'MISSION TO THE W00880144',
    'MISSION TO THE W00880161',
    'MISSION TO THE W00880174',
    'MISSION TO THE W00880185',
    'MISSION TO THE W00880194',
    'MISSION TO THE W00880206',
    'MISSION TO THE W00880217',
    'MISSION TO THE W00880229',
    'MISSION TO THE W00880241',
    'MISSION TO THE W00880253',
    'MISSION TO THE W00880270',
    'MISSION TO THE W00880284',
    'MISSION TO THE W00880300',
    ])
    setB = set([
    'ML BANK DEPOSIT PROGRAM',
    'MOONSTAR II CHINESE COLORADO SPRI CO Restaurants PROCESSED',
    'NARITA AIRPORT TERMINAL CHIBA Merchandise PROCESSED',
    'NATIONAL GRID NE',
    'NNT BART-POWELL 360962 SAN FRANCISCO Other/Unclassified PROCESSED',
    'NSTAR',
    'OC INTERNATIONAL00880230',
    'OC INTERNATIONAL00880242',
    'OC INTERNATIONAL00880254',
    'OC INTERNATIONAL00880272',
    'OC INTERNATIONAL00880285',
    'OC INTERNATIONAL00880301',
    'OC INTL 00880156',
    'OC INTL 00880162',
    'OC INTL 00880175',
    'OC INTL 00880186',
    'OC INTL 00880195',
    'OC INTL 00880207',
    'OC INTL 00880218',
    "PALMS FOOD INT'L P/L SINGAPORE Restaurants PROCESSED",
    'PANDORA.COM 510-842-6998 CA Other/Unclassified PROCESSED',
    'PAYPAL',
    'PIKES PERK #1 COLORADO SPRI CO Restaurants PROCESSED',
    'PLYMOUTH & BROCKTON PLYMOUTH MA Other/Unclassified PROCESSED',
    'QWEST 686',
    'QWEST 8004238994',
    'REAL LIVING SELE 674',
    'SAFEWAY STORE00012864 COLORADO SPGS CO Merchandise PROCESSED',
    'SALVATION ARMY 00880107',
    'SALVATION ARMY 00880110',
    'SALVATION ARMY 00880120',
    'SALVATION ARMY 00880126',
    'SALVATION ARMY 00880138',
    'SALVATION ARMY 00880143',
    'SALVATION ARMY 00880160',
    'SALVATION ARMY 00880173',
    'SALVATION ARMY 00880184',
    'SALVATION ARMY 00880193',
    'SALVATION ARMY 00880205',
    'SALVATION ARMY 00880216',
    'SALVATION ARMY 00880228',
    'SALVATION ARMY 00880240',
    'SALVATION ARMY 00880252',
    'SALVATION ARMY 00880269',
    'SALVATION ARMY 00880283',
    'SALVATION ARMY 00880299',
    'SALVATION ARMY 668',
    'SANTANA 699',
    'SEARS AUTO CNTR 6293 HYANNIS MA Merchandise PROCESSED',
    'SECURITY FIRST SELF STORA CHULA VISTA CA Other/Unclassified PROCESSED',
    'SFVHC 727',
    'SFVHC 743',
    'SFVHC 786',
    'SFVHC BLDG FUND 00880130',
    'SFVHC BLDG FUND 00880131',
    'SFVHC BLDG FUND 00880134',
    'SFVHC BLDG FUND 00880145',
    'SFVHC BLDG FUND 00880165',
    'SFVHC BLDG FUND 00880177',
    'SFVHC BLDG FUND 00880188',
    'SFVHC BLDG FUND 00880198',
    'SFVHC BLDG FUND 00880210',
    'SFVHC BLDG FUND 00880222',
    'SFVHC BLDG FUND 00880233',
    'SFVHC BLDG FUND 00880247',
    'SFVHC BLDG FUND 00880259',
    'SFVHC BLDG FUND 00880271',
    'SFVHC BLDG FUND 00880290',
    'SFVHC BLDG FUND 00880307',
    'SHEILA DILWORTH 00880200',
    'SHEILA DILWORTH 00880309',
    'SHEILA DILWORTH 670',
    'SHEILA DILWORTH 692',
    'SHEILA DILWORTH 730',
    'SHEILA DILWORTH 740',
    'SPRINGS CPR TRAI 742',
    'SUBWAY 23025 COLORADO SPRI CO Other/Unclassified PROCESSED',
    'TAX PRODUCTS PE2',
    'TELLER CO CLERK 726',
    'THE LION OF JUDA00880101',
    'THE LION OF JUDA00880102',
    'THE LION OF JUDA00880103',
    'THE LION OF JUDA00880104',
    'THE LION OF JUDA00880111',
    'THE LION OF JUDA00880112',
    'THE LION OF JUDA00880116',
    'THE LION OF JUDA00880117',
    'THE LION OF JUDA00880118',
    'THE LION OF JUDA00880119',
    'THE LION OF JUDA00880124',
    'THE LION OF JUDA00880125',
    'THE LION OF JUDA00880128',
    'THE LION OF JUDA00880135',
    'THE LION OF JUDA00880136',
    'THE LION OF JUDA00880141',
    'THE LION OF JUDA00880142',
    'THE LION OF JUDA00880153',
    'THE LION OF JUDA00880154',
    'THE LION OF JUDA00880157',
    'THE LION OF JUDA00880158',
    'THE LION OF JUDA00880159',
    'THE LION OF JUDA00880166',
    'THE LION OF JUDA00880171',
    'THE LION OF JUDA00880172',
    'THE LION OF JUDA00880182',
    'THE LION OF JUDA00880183',
    'THE LION OF JUDA00880191',
    'THE LION OF JUDA00880192',
    'THE LION OF JUDA00880203',
    'THE LION OF JUDA00880204',
    'THE LION OF JUDA00880212',
    'THE LION OF JUDA00880214',
    'THE LION OF JUDA00880215',
    'THE LION OF JUDA00880224',
    'THE LION OF JUDA00880226',
    'THE LION OF JUDA00880227',
    'THE LION OF JUDA00880238',
    'THE LION OF JUDA00880239',
    'THE LION OF JUDA00880249',
    'THE LION OF JUDA00880250',
    'THE LION OF JUDA00880251',
    'THE LION OF JUDA00880265',
    'THE LION OF JUDA00880266',
    'THE LION OF JUDA00880267',
    'THE LION OF JUDA00880278',
    'THE LION OF JUDA00880281',
    'THE LION OF JUDA00880282',
    'THE LION OF JUDA00880295',
    'THE LION OF JUDA00880297',
    'THE LION OF JUDA00880298',
    'THE LION OF JUDA00880310',
    'THE LION OF JUDA00880325',
    'THE LIVING ROOM 00880169',
    'THE LIVING ROOM 00880170',
    'THE LIVING ROOM 00880181',
    'THE LIVING ROOM 00880196',
    'THE LIVING ROOM 00880208',
    'THE LIVING ROOM 00880219',
    'THE LIVING ROOM 00880231',
    'THE LIVING ROOM 00880243',
    'THE LIVING ROOM 00880255',
    'THE LIVING ROOM 00880273',
    'THE LIVING ROOM 00880286',
    'TOWN OF BARNSTAB 677',
    'TOWN OF BARNSTAB 680',
    'TOWN OF BARNSTAB 734',
    'TOWN OF BARNSTAB 768',
    'TRANSAMERICA ASSET ALLOCATION GROWTH PTF A DEPOSIT TRF FROM 22D81993',
    'TRANSFR FEE P31130809402',
    'UCCS VISITOR PARKING COLORADO SPRI CO Education PROCESSED',
    'US CABLE 687',
    'US CABLE OF COLO',
    'USCIS DALLAS',
    'USPS PO BOXES 66101510 800-3447779 DC Merchandise PROCESSED',
    'VAL SATOW 745',
    'VERIZON WIRELESS',
    'VIETNAMESE EVANG00880237',
    'VIETNAMESE EVANG00880245',
    'VIETNAMESE EVANG00880257',
    'VIETNAMESE EVANG00880275',
    'VIETNAMESE EVANG00880288',
    'VIETNAMESE EVANG00880304',
    'VIETNAMESE EVANG 755',
    'VIETNAMESE EVANG 760',
    'VIOLA ASSN INC 00880150',
    'VIOLA ASSN INC 00880263',
    'VIOLA ASSN INC 00880323',
    'VIOLA ASSN INC 736',
    'VIOLA ASSN INC 738',
    'VIOLA ASSOCIATES00880148',
    'VOICE 679',
    'Waste Management',
    'WEST LA HOLINESS 758',
    'WIRE TRF IN D31035707167',
    'WIRE TRF OUTP31034309377',
    'WIRE TRF OUTP31035509379',
    'WIRE TRF OUTP31106010808',
    'WIRE TRF OUTP31126411313',
    'WIRE TRF OUTP31128507774',
    'WIRE TRF OUTP31130809243',
    'WIRE TRF OUTP31130809402',
    'WIRE TRF OUTP31204409345',
    'WIRE TRF OUTP31211110312',
    'WOODLAND PARK CO',
    'WOODLAND PARK',
    'WORLD GOSPEL MISSION 765-6647331 IN Other/Unclassified PROCESSED',
    'World Gospel Mis',
    'World Vision',
    'WWW.NEWEGG.COM 800-390-1119 CA Merchandise PROCESSED',
    'YEKOPE MINIST IN00880235',
    'YEKOPE MINIST IN00880244',
    'YEKOPE MINIST IN00880256',
    'YEKOPE MINIST IN00880274',
    'YEKOPE MINISTRIE00880287',
    'YEKOPE MINISTRIE00880303',
    'ZOE INTERNATIONA',
    ])
    return setA.union(setB)

