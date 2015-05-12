'''
   namespace src.finance.beyond_banking.ConfigAliases
'''

from utils import ConfigAliases 

########################################################################
# Aliases.Faraja
########################################################################
class BeyondBanking(ConfigAliases.Base):

    # constructor
    def __init__(self):
        ConfigAliases.Base.__init__(self)

        self.insertAccountWithAliases('Cash', set([
            'ATM',
        ]))

        self.insertAccountWithAliases('AAA', set([
            'AAA MEMBERSHIP'
        ]))

        self.insertAccountWithAliases('21st Century', set([
            '21STCENTURY',
        ]))

        self.insertAccountWithAliases('Arbella Mutual', set([
            'ARBELLA INSURANC',
            'ARBELLA MUTUAL',
        ]))

        self.insertAccountWithAliases('DeMarc Auto Repair', set([
            'CK6497COSPRNGS10082808 COLORADO SPRI CO Service Stations',
        ]))

        self.insertAccountWithAliases('Independent Auto', set([
            'INDEPENDENT AUTO',
        ]))

        self.insertAccountWithAliases('Jim Aloisio', set([
            'JIM ALOISIO',
        ]))

        self.insertAccountWithAliases('Sears Auto Center', set([
            'SEARS AUTO CNTR',
        ]))

        self.insertAccountWithAliases('ML Investment Account', set([
            'TRANSAMERICA ASSET ALLOCATION',
            'MONTHLY AMT ISSUED',
            'TOTAL DIV/INT PAYMENTS',
            'TRANS ASSET ALL GRW',
        ]))

        self.insertAccountWithAliases('Account Receiving Wire', set([
            'WIRE TRF IN',
            'WIRE TRF OUT',
        ]))

        self.insertAccountWithAliases('Paypal', set([
            'PAYPAL',
        ]))

        self.insertAccountWithAliases('ML Fee Administration', set([
            'EXTEND OVERDRAFT LOAN',
            'REPAY OVERDRAFT LOAN',
            'TRANSFR FEE',
            'TR FROM ML',
        ]))

        self.insertAccountWithAliases('Kurt Wegner', set([
            'BANK DEPOSIT',
            'CHECK DEPOSIT',
            'ML BANK DEPOSIT PROGRAM',
            'CASH',
            'MOBILE CHECK DEPOSIT',
            'VOID DIVD CHECK',
        ]))

        self.insertAccountWithAliases('Credit Card Bank of America', set([
            'BANK OF AMERICA',
            'BK OF AM CRD'
        ]))

        self.insertAccountWithAliases('Credit Card Barclay', set([         
            'BARCLAYCARD US',
        ]))

        self.insertAccountWithAliases('Credit Card Chase', set([
            'CHASE',
        ]))

        self.insertAccountWithAliases('AT&T Internet Service', set([
            'AT&T INTERNET SVC',
        ]))

        self.insertAccountWithAliases('US Cable', set([
            'US CABLE 687',
            'US CABLE OF COLO',
        ]))

        self.insertAccountWithAliases('Baja Broadband', set([
            'BAJA BROADBAND',
        ]))

        self.insertAccountWithAliases('Comcast', set([
            'COMCAST',
        ]))

        self.insertAccountWithAliases('Univ Colorado', set([
            'CAMPUS WIDE EXTE',
            'UCCS VISITOR PARKING',
        ]))

        self.insertAccountWithAliases('IREA', set([
            'Intermountain Ru',
            'IREA',
        ]))

        self.insertAccountWithAliases('NSTAR', set([
            'NSTAR',
        ]))

        self.insertAccountWithAliases('Pandora Music', set([
            'PANDORA.COM',
            'PANDORA',
        ]))

        self.insertAccountWithAliases('AIM', set([
            'AFRICA INLAND MI',
            'AFRICA ISLAND MI',
        ]))

        self.insertAccountWithAliases('Bethany Christian Services', set([
            'BETHANY CHRISTIA',
        ]))

        self.insertAccountWithAliases('Campus Crusade', set([
            'CAMPUS CRUSADE',
        ]))

        self.insertAccountWithAliases('Beate Reins', set([
            'EFCA',
        ]))

        self.insertAccountWithAliases('Harvest Family Church', set([
            'HARVEST FAM',
        ]))

        self.insertAccountWithAliases('JEMS', set([
            'JEMS',
        ]))
        
        lion_of_judah_monthly = set([
            'THE LION OF JUDA00880' + '101',
            'THE LION OF JUDA00880' + '103',
            'THE LION OF JUDA00880' + '111',
            'THE LION OF JUDA00880' + '118',
            'THE LION OF JUDA00880' + '124',
            'THE LION OF JUDA00880' + '135',
            'THE LION OF JUDA00880' + '141',
            'THE LION OF JUDA00880' + '158',
            'THE LION OF JUDA00880' + '171',
            'THE LION OF JUDA00880' + '182',
            'THE LION OF JUDA00880' + '191',
            'THE LION OF JUDA00880' + '203',
            'THE LION OF JUDA00880' + '214',
            'THE LION OF JUDA00880' + '226',
            'THE LION OF JUDA00880' + '238',
            'THE LION OF JUDA00880' + '250',
            'THE LION OF JUDA00880' + '266',
            'THE LION OF JUDA00880' + '281',
            'THE LION OF JUDA00' + '880297',
            'THE LION OF JUDA00' + '880311',
            'THE LION OF JUDA00' + '880328',
            'THE LION OF JUDA00' + '880346',
            'THE LION OF JUDA00' + '880364'])
        
        faraja_orphans_monthly = set([        
            'THE LION OF JUDA00880' + '102',
            'THE LION OF JUDA00880' + '104',
            'THE LION OF JUDA00880' + '112',
            'THE LION OF JUDA00880' + '119',
            'THE LION OF JUDA00880' + '125',
            'THE LION OF JUDA00880' + '136',
            'THE LION OF JUDA00880' + '142',
            'THE LION OF JUDA00880' + '159',
            'THE LION OF JUDA00880' + '172',
            'THE LION OF JUDA00880' + '183',
            'THE LION OF JUDA00880' + '192',
            'THE LION OF JUDA00880' + '204',
            'THE LION OF JUDA00880' + '215',
            'THE LION OF JUDA00880' + '227',
            'THE LION OF JUDA00880' + '239',
            'THE LION OF JUDA00880' + '251',
            'THE LION OF JUDA00880' + '267',
            'THE LION OF JUDA00880' + '282',
            'THE LION OF JUDA00' + '880298',
            'THE LION OF JUDA00' + '880312',
            'THE LION OF JUDA00' + '880329',
            'THE LION OF JUDA00' + '880347',
            'THE LION OF JUDA00' + '880365'])
        

        self.insertAccountWithAliases('The Lion of Judah Ministries, Inc.', lion_of_judah_monthly)
        self.insertAccountWithAliases('Friends of Faraja USA', faraja_orphans_monthly)
        self.insertAccountWithAliases('Faraja Orphans Rescue Ministry', set([
            'LION OF JUDAH MI',
            'THE LION OF JUDA',
        ]))
        

        self.insertAccountWithAliases('The Living Room', set([
            'LIVING ROOM 673',
            'THE LIVING ROOM',
        ]))

        self.insertAccountWithAliases('Mission to the World', set([
            'MISSION TO THE W',
        ]))

        self.insertAccountWithAliases('Hank and Cathy Pott', set([
            'OC INT',
        ]))

        self.insertAccountWithAliases('Salvation Army', set([
            'SALVATION ARMY',
        ]))

        self.insertAccountWithAliases('SFVHC', set([
            'SFVHC',
            'SFVHC BLDG FUND',
        ]))

        self.insertAccountWithAliases('Sheila Dilworth', set([
            'SHEILA DILWORTH',
        ]))

        self.insertAccountWithAliases('Special Camp', set([
            'VAL SATOW',
        ]))

        self.insertAccountWithAliases('Vietnamese Evangelical Church', set([
            'VIETNAMESE EVANG',
        ]))

        self.insertAccountWithAliases('West LA Holiness', set([
            'WEST LA HOLINESS',
        ]))

        self.insertAccountWithAliases('World Gospel Mission', set([
            'WORLD GOSPEL MISSION',
            'World Gospel Mis',
        ]))

        self.insertAccountWithAliases('World Vision', set([
            'World Vision',
        ]))

        self.insertAccountWithAliases('Yekope Ministries', set([
            'YEKOPE MINIST',
        ]))

        self.insertAccountWithAliases('ZOE International', set([
            'ZOE INTERNATIONA',
        ]))

        self.insertAccountWithAliases('Woodland Park Community Church', set([
            'WOODLAND PARK CO',
        ]))

        self.insertAccountWithAliases('Other Beneficiary Account', set([
            'VOICE 679',
            '84301767',
            'COLORADO PEACE O',
            'ERRC 747',
            'SANTANA',
            'PAYEE UNRECORDE',
        ]))

        if False: self.insertAccountWithAliases('Food', set([
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
        ]))

        self.insertAccountWithAliases('National Grid', set([
            'NATIONAL GRID NE',
        ]))

        self.insertAccountWithAliases('Black Hills Energy', set([
            'BLACK HILLS'
        ]))

        self.insertAccountWithAliases('Federal Government', set([
            'IRS',
            'TAX PRODUCTS',
        ]))

        self.insertAccountWithAliases('State of Colorado', set([
            'CO DEPT REVENUE',
            'colorado.gov',
            'TELLER CO CLERK',
            'CO DEPT OF REV',
            'COLORADO DEPT OF',
        ]))

        self.insertAccountWithAliases('State of California', set([
            'DMV',
            'FRANCHISE TAX BD',
        ]))

        self.insertAccountWithAliases('Commonwealth of Massachusettes', set([
            'COMM. OF MASS.',
            'DEPT OF MOTOR VE',
            'TOWN OF BARNSTAB',
            'ICI*BARNSTABLE',
            'MASSDOT-RMV',
            'ICI',
        ]))

        self.insertAccountWithAliases('Other Tax Account', set([
            'INVOICECLOUD-TAX',
        ]))

        self.insertAccountWithAliases('Old Cape Cod Insurance', set([
            'MASS PROPERTY IN',
        ]))

        self.insertAccountWithAliases('Allstate', set([
            'ALLSTATE'
        ]))

        self.insertAccountWithAliases('Andys Plumbing', set([
            'ANDYS PLUMBING',
        ]))

        self.insertAccountWithAliases('Doreen Kelley', set([
            'DOREEN KELLEY',
        ]))

        self.insertAccountWithAliases('Forest Keepers', set([
            'FOREST KEEPERS',
        ]))

        self.insertAccountWithAliases('Front Range Arbolists', set([
            'FRONT RANGE ARBO',
        ]))

        self.insertAccountWithAliases('Green Lawn Treatment', set([
            'GREEN LAWN TREAT',
            'GREEN LANW TREAT',
        ]))

        self.insertAccountWithAliases('John Harnish', set([
            'JOHN HARNISH',
        ]))

        self.insertAccountWithAliases('John Viola', set([
            'JOHN VIOLA',
        ]))

        self.insertAccountWithAliases('Larry Bernard', set([
            'LARRY BERNARD',
        ]))

        self.insertAccountWithAliases('Post Office Box', set([
            'USPS PO BOXES',
        ]))

        self.insertAccountWithAliases('Viola Associates', set([
            'VIOLA ASSN INC',
            'VIOLA ASSOCIATES',
        ]))

        self.insertAccountWithAliases('Immigration', set([
            'USCIS DALLAS',
        ]))

        self.insertAccountWithAliases('ITT Pension', set([
            'ACS HR SOLUTIONS',
            'BENEFIT PAYMENTS'
        ]))

        self.insertAccountWithAliases('Heidi Chan DDS', set([
            'HEIDI L CHAN DDS',
        ]))

        self.insertAccountWithAliases('Fifth Third Bank', set([
            '5/3 MORTGAGE LN',
            'FIFTH THIRD BANK',
            'REAL LIVING SELE',
        ]))

        self.insertAccountWithAliases('Qwest', set([
            'QWEST',
        ]))

        self.insertAccountWithAliases('Verizon', set([
            'VERIZON WIRELESS',
        ]))

        self.insertAccountWithAliases('Danielle Perez', set([
            'DANIELLE PEREZ',
        ]))

        self.insertAccountWithAliases('Davida Wegner', set([
            'DAVIDA WEGNER',
        ]))

        self.insertAccountWithAliases('Karl Wegner', set([
            'KARL WEGNER',
        ]))

        self.insertAccountWithAliases('Meredith Wegner', set([
            'MEREDITH FLYNN',
        ]))

        self.insertAccountWithAliases('Danny Perez', set([
            'DANNY PEREZ',
        ]))

        self.insertAccountWithAliases('James Amato', set([
            'JAMES AMATO',
            'CKYY 09073-00092 JAMES AMATO',
        ]))

        self.insertAccountWithAliases('Amazon', set([
            'AMAZON MARKETPLA',
        ]))

        self.insertAccountWithAliases('New Egg', set([
            'WWW.NEWEGG.COM',
        ]))

        self.insertAccountWithAliases('Misc Account', set([
            'CHECKMATE PIANO',
            'NARITA AIRPORT TERMINAL',
            'SECURITY FIRST SELF STORA',
            'SPRINGS CPR TRAI',
            'CAFFE EDOLCI',
        ]))

        self.insertAccountWithAliases('ITT Exelis', set([
            'EXELIS SYSTEMS C',
            'ITT SYSTEMS CORP',
            'ITT ISP CLEARING',

        ]))

        self.insertAccountWithAliases('Macombers Sanitary', set([
            'MACOMBERS SANITA',
        ]))

        self.insertAccountWithAliases('Waste Management', set([
            'CURBSIDE RECYCLI',
            'Waste Management',
        ]))

        self.insertAccountWithAliases('Transportation', set([
            'PLYMOUTH & BROCKTON',
            'NNT BART-POWELL',
        ]))

        self.insertAccountWithAliases('Hyannis Water', set([
            'Hyannis Water MA',
            'HYANNIS WATER MA',
            'MCC eBill',
            'MCC EBILL',
        ]))

        self.insertAccountWithAliases('Woodland Park Water and Sewer', set([
            'CITY OF WOODLAND',
            'WOODLAND PARK',
        ]))
        pass


