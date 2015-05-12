'''
    Database.TransformRow.Finance.ChaseCreditCard
'''

import re, copy
from classes.utils import Container, CsvObject
from classes.database.finance import Finance

super = Finance

#===============================================================================
# (1) HowToCombineOriginalFiles
#===============================================================================
class HowToCombineOriginalFiles(super.HowToCombineOriginalFiles):
    def __init__(self):
        super.HowToCombineOriginalFiles.__init__(self)

#===============================================================================
# (1) HowToCombineOriginalFiles
#===============================================================================
class HowToCombineOriginalFiles2(super.HowToCombineOriginalFiles2):
    def __init__(self, csv_in):
        super.HowToCombineOriginalFiles2.__init__(self, csv_in)

#===============================================================================
# (2) HowToValidateAndNormalizeTheFields
#===============================================================================
class HowToValidateAndNormalizeTheFields(super.HowToValidateAndNormalizeTheFields):
    def __init__(self, csv_in):
        super.HowToValidateAndNormalizeTheFields.__init__(self, csv_in)

#===============================================================================
# (3) HowToDeriveNewFields
#===============================================================================
class HowToDeriveNewFields(super.HowToDeriveNewFields):
    def __init__(self, csv_in):
        super.HowToDeriveNewFields.__init__(self, csv_in)

#===============================================================================
# (4) HowToSortTheRows
#===============================================================================
class HowToSortTheRows(super.HowToSortTheRows):
    def __init__(self, csv_in):
        print "got to ChaseCreditCard"
        super.HowToSortTheRows.__init__(self, csv_in)
                
#===============================================================================
# (5) HowToCollapseOnFields
#===============================================================================
class HowToCollapseOnFields(super.HowToCollapseOnFields):
    def __init__(self, csv_in):
        super.HowToCollapseOnFields.__init__(self, csv_in)
        
#===============================================================================
# (6) HowToSelectTheRows
#===============================================================================
class HowToSelectTheRows(super.HowToSelectTheRows):
    def __init__(self, csv_in):
        super.HowToSelectTheRows.__init__(self, csv_in)
        
#===============================================================================
# (7) HowToAccumulateNewColumns
#===============================================================================
class HowToAccumulateNewColumns(super.HowToAccumulateNewColumns):
    def __init__(self, csv_in):
        super.HowToAccumulateNewColumns.__init__(self, csv_in)
        
#===============================================================================
# (8) HowToFinallyModifyCertainFields
#===============================================================================
class HowToFinallyModifyCertainFields(super.HowToFinallyModifyCertainFields):
    def __init__(self, csv_in):
        super.HowToFinallyModifyCertainFields.__init__(self, csv_in)






#===============================================================================
# (1) HowToCombineOriginalFiles
#===============================================================================
class HowToCombineOriginalFiles(super.HowToCombineOriginalFiles):
    
    def __init__(self):
        super.HowToCombineOriginalFiles.__init__(self)

    def folderIn(self):
        return "/home/kurt/ubu/finances/Chase/download/" 
        
    def originalFields(self): return list([
        "Type",
        "Trans Date",
        "Post Date",
        "Description",
        "Amount",
    ])

    def dialect(self):
        return CsvObject.CsvStandardDialect()

    def skipFirstRecord(self):
        return True

#===============================================================================
# (3) HowToDeriveNewFields
#===============================================================================
class HowToDeriveNewFields(super.HowToDeriveNewFields):
    
    def __init__(self, csv_in):

        self.map_title_to_account = dict()
        self.map_alias_to_title = dict()

        self.createAccount("ADVANCE AUTO PARTS","ADVANCE AUTO PARTS #8830","Car","Auto Parts")
        self.createAccount("AGODA TRAVEL WEBSITE","AGODA.COM","Travel","Hotel")
        self.createAccount("AGODA TRAVEL WEBSITE","AGODA.COM","Travel","Hotel")        
        self.createAccount("ALBERTO'S RESTAURANT - HYANNIS", "ALBERTO'S RISTORANTE","Food","Eating Out")
        self.createAccount("ALBERTSONS GROCERY STORE","ALBERTSONS #0967","Food","Grocery Store")
        self.createAccount("ALBERTSONS GROCERY STORE","ALBERTSONS #0967","Food","Grocery Store")
        self.createAccount("AMAZON ONLINE SHOPPING","AMAZON MKTPLACE PMTS","Clothing","Cloud Store")
        self.createAccount("AMTRAK TRAIN","AMTRAK      0209646558533","Travel","Train/Bus/Taxi")
        self.createAccount("FEDEX","ANDERSEN PACK N SHIP","Mail","Fedex")
        self.createAccount("APPLEBEES","APPLEBEES GARD48248272","Food","Eating Out")
        self.createAccount("ASIAN PACIFIC MARKET","ASIAN PACIFIC MARK","Food","Grocery Store")
        self.createAccount("ASIAN PACIFIC MARKET","ASIAN PACIFIC MARK","Food","Grocery Store")
        self.createAccount("ASIAN PACIFIC MARKET","ASIAN PACIFIC MARK","Food","Grocery Store")
        self.createAccount("ASIAN PACIFIC MARKET","ASIAN PACIFIC MARK","Food","Grocery Store")
        self.createAccount("BEYOND BANKING TRANSFER","AUTOMATIC PAYMENT - THANK","Credit Card","Pay Credit Card")
        self.createAccount("BEYOND BANKING TRANSFER","AUTOMATIC PAYMENT - THANK","Credit Card","Pay Credit Card")
        self.createAccount("BEYOND BANKING TRANSFER","AUTOMATIC PAYMENT - THANK","Credit Card","Pay Credit Card")
        self.createAccount("BARNES & NOBLE","BARNES & NOBLE #2092","Gifts","Book Store")
        self.createAccount("BASKIN ROBBINS ICE CREAM","BASKIN #360035     Q35","Food","Eating Out")
        self.createAccount("BASS SHOE OUTLET","BASS SHOE OUTLET 361","Clothing","Shoe Store")
        self.createAccount("BED BATH & BEYOND","BED BATH & BEYOND #338","Household","Department Store")
        self.createAccount("BEST BUY","BEST BUY      00017822","Electronics","Computer Store")
        self.createAccount("BEST BUY","BEST BUY MHT  00005686","Electronics","Computer Store")
        self.createAccount("BEST BUY","BEST BUY MHT  00005686","Electronics","Computer Store")
        self.createAccount("BLUEMOUNTAIN GREETING CARDS","BLUEMOUNTAIN*0101-0131","Gifts","Cloud Greeting Card")
        self.createAccount("BLUEMOUNTAIN GREETING CARDS","BLUEMOUNTAIN*0131-0302","Gifts","Cloud Greeting Card")
        self.createAccount("BLUEMOUNTAIN GREETING CARDS","BLUEMOUNTAIN*0302-0401","Gifts","Cloud Greeting Card")
        self.createAccount("BLUEMOUNTAIN GREETING CARDS","BLUEMOUNTAIN*0401-0501","Gifts","Cloud Greeting Card")
        self.createAccount("BRUEGGER'S BAGLES","BRUEGGER'S BAGLES","Food","Eating Out")
        self.createAccount("BURGER KING","BURGER KING #17712","Food","Eating Out")
        self.createAccount("BURGER KING","BURGER KING #5778","Food","Eating Out")
        self.createAccount("CALPHALON KITCHEN OUTLET","CALPHALON KITCHEN OUTL","Household","Kitchen Store")
        self.createAccount("CANOPY AIRPORT PARKING","CANOPY AIRPORT PARKING","Travel","Parking")
        self.createAccount("CANOPY AIRPORT PARKING","CANOPY AIRPORT PARKING","Travel","Parking")
        self.createAccount("CAPE COD POTATO CHIPS","CAPE COD POTATO CHIPS","Food","Eating Out")
        self.createAccount("CAPE TIRE SERVICE INC","CAPE TIRE SERVICE INC","Car","Auto Parts")
        self.createAccount("CHEVRON GAS STATION","CHEVRON 00075703","Car","Gas Station")
        self.createAccount("CHEVRON GAS STATION","CHEVRON 00090172","Car","Gas Station")
        self.createAccount("CHEVRON GAS STATION","CHEVRON 00090172","Car","Gas Station")
        self.createAccount("CHEVRON GAS STATION","CHEVRON 00096368","Car","Gas Station")
        self.createAccount("CHICO HATS","CHICO HATS","Clothing","Cloud Hat Store")
        self.createAccount("CHINA TOWN RESTAURANT","CHINA TOWN","Food","Eating Out")
        self.createAccount("DISNEYLAND CHURRO STAND","CHURRO - TOMORROWLA","Food","Eating Out")
        self.createAccount("CITY OF SANTA MONICA PARKING","CITY OF SM PARKING","Car","Parking")
        self.createAccount("CITY MARKET","CITY-MARKET #0431","Food","Grocery Store")
        self.createAccount("CITY MARKET","CITY-MARKET #0431","Food","Grocery Store")
        self.createAccount("COCO'S RESTAURANT","COCO'S - 503","Food","Eating Out")
        self.createAccount("CHINA BUFFET SF VALLEY","CP CHINA BUFFET","Food","Eating Out")
        self.createAccount("CA SCIENCE MUSEUM STORE","CSCF EXPLORASTORE","Entertainment","Museum")
        self.createAccount("CVS PHARMACY","CVS PHARMACY #0050 Q03","Household","Drug Store")
        self.createAccount("DARRELLS AUTOMOTIVE","DARRELLS AUTOMOTIVE","Car","Auto Repair")
        self.createAccount("DAYS INN CLEVELAND","DAYS INN CLEVELAND AIRPO","Travel","Hotel")
        self.createAccount("DELL SALES & SERVICE","DELL SALES & SERVICE","Electronics","Cloud Computer")
        self.createAccount("DENNY'S","DENNY'S #8097","Food","Eating Out")
        self.createAccount("DISNEYLAND GIFT STORE","DISNEY SHOWCASE - D","Gifts","Gift Shop")
        self.createAccount("DISNEYLAND TICKETS","DISNEYLAND TICKETS","Entertainment","Amusement Park")
        self.createAccount("DUNKIN DONUTS","DUNKIN DONUTS MAIN MT270","Food","Eating Out")
        self.createAccount("E-470 EXPRESS TOLLS","E 470 EXPRESS TOLLS","Car","Toll Road")
        self.createAccount("EINSTEIN BAGELS","EINSTEIN BAGELS","Food","Eating Out")
        self.createAccount("EINSTEIN BAGELS","EINSTEIN BROS BAGELS1599","Food","Eating Out")
        self.createAccount("PHARMACY IN SO CALIF","ESI PHARM COLUMBUS","Household","Drug Store")
        self.createAccount("FEDEX","FEDEXOFFICE   00004762","Mail","Fedex")
        self.createAccount("FOX RENT A CAR","FOX RENT A CAR LAX","Travel","Rental Car")
        self.createAccount("FOX RENT A CAR","FOX RENT A CAR LAX","Travel","Rental Car")
        self.createAccount("FOX RENT A CAR","FOX RENT A CAR LAX","Travel","Rental Car")
        self.createAccount("FRONTIER AIRLINES","FRONTIER AI 4222178188503","Travel","Airplane")
        self.createAccount("FRONTIER AIRLINES","FRONTIER AI 4222178188504","Travel","Airplane")
        self.createAccount("FRYS GAS STATION","FRYS #7104","Car","Gas Station")
        self.createAccount("FURHATWORLD.COM","FURHATWORLD.COM","Clothing","Cloud Hat Store")
        self.createAccount("Foxworth-Galbraith Lumber","FXWTH GALB LMBR CO 90","Household","Hardware Store")
        self.createAccount("GALLERIA MARKET SO CALIF","GALLERIA MARKET","Food","Grocery Store")
        self.createAccount("GIANT GROCERY STORE","GIANT 6037","Food","Grocery Store")
        self.createAccount("GOLD HILL JAVA","GOLD HILL JAVA","Food","Eating Out")
        self.createAccount("GOLD HILL JAVA","GOLD HILL JAVA","Food","Eating Out")
        self.createAccount("GOLDEN FOUNTAIN RESTAURANT","GOLDEN FOUNTAIN RESTAURAN","Food","Eating Out")
        self.createAccount("GRAND CANYON TICKET","GRAND CYN NP-SOUTH ES","Entertainment","Site Seeing")
        self.createAccount("GREYHOUND BUS","GREYHOUND KIOSK 0550","Travel","Train/Bus/Taxi")
        self.createAccount("GRAND CANYON STORE","GRNDCYNASSN-YAVAPAI","Gifts","Gift Shop")
        self.createAccount("HANNOUSH JEWELERS CAPE COD MALL","HANNOUSH JEWELERS #260","Clothing","Jewelry Store")
        self.createAccount("HARRY & DAVID OUTLET STORE","HARRY & DAVID #529","Clothing","Fur/Leather")
        self.createAccount("HOPI HOUSE GIFT SHOP","HOPI HOUSE GIFT SHOP","Gifts","Gift ShoFinance.Financep")
        self.createAccount("HOUDINI'S MAGIC SHOP DISNEYLAND","HOUDINI'S MAGIC SHO","Gifts","Magic Shop")
        self.createAccount("HUNTINGTON GARDENS","HUNTINGTON ADMISSIONS 2","Entertainment","Park/Gardens")
        self.createAccount("HUNTINGTON BOOKSTORE","HUNTINGTON BOOKSTORE","Gifts","Gift Shop")
        self.createAccount("HUNTINGTON BOOKSTORE","HUNTINGTON BOOKSTORE","Gifts","Gift Shop")
        self.createAccount("TURBOTAX","INTUIT *TURBOTAX","Government","Taxes")
        self.createAccount("ITOPIT YOGURT","ITOPIT","Food","Eating Out")
        self.createAccount("ITOPIT YOGURT","ITOPIT","Food","Eating Out")
        self.createAccount("ITOPIT YOGURT","ITOPIT","Food","Eating Out")
        self.createAccount("JAPANESE FUSION RESTAURANT","JAPANESE FUSION","Food","Eating Out")
        self.createAccount("JAPANESE FUSION RESTAURANT","JAPANESE FUSION","Food","Eating Out")
        self.createAccount("JOLLY HOLIDAY BAKERY DISNEYLAND","JOLLY HOLIDAY BAKER","Food","Eating Out")
        self.createAccount("KITCHEN COLLECTION OUTLET STORE","KITCHEN COLLECTION #82","Household","Kitchen Store")
        self.createAccount("KMART","KMART 3040","Household","Department Store")
        self.createAccount("KMART","KMART 3040","Household","Department Store")
        self.createAccount("KNOTT'S BERRY FARM","KNOTT'S BERRY FARM","Food","Eating Out")
        self.createAccount("KNOTT'S BERRY FARM","KNOTT'S BERRY FARM","Food","Eating Out")
        self.createAccount("KNOTT'S BERRY FARM","KNOTT'S BERRY FARM","Food","Eating Out")
        self.createAccount("LOAF N JUG GAS STATION","LOAF N JUG #0099   Q81","Car","Gas Station")
        self.createAccount("LOVE SUSHI RESTAURANT","LOVE SUSHI","Food","Eating Out")
        self.createAccount("LOWES HARDWARE STORE","LOWES #01099*","Household","Hardware Store")
        self.createAccount("LOWES HARDWARE STORE","LOWES #02578*","Household","Hardware Store")
        self.createAccount("LOWES HARDWARE STORE","LOWES #02578*","Household","Hardware Store")
        self.createAccount("MACY'S DEPT STORE","MACY'S EAST #523","Clothing","Department Store")
        self.createAccount("MARSHALLS DEPT STORE","MARSHALLS #0004","Clothing","Department Store")
        self.createAccount("MAYFLOWER CHINESE RESTAURANT","MAYFLOWER CHINESE REST","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S F10576","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S F10576","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S F1212","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S F1212","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S F13573","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S F32477","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S F32477","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S F6231","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S M2368 OF CA","Food","Eating Out")
        self.createAccount("MCDONALD'S","MCDONALD'S M2368 OF CA","Food","Eating Out")
        self.createAccount("MONARCH MOUNTAIN SKI","MONARCH MOUNTAIN RENTAL","Entertainment","Skiing")
        self.createAccount("MONARCH MOUNTAIN SKI","MONARCH ON MOUNTAIN TICKE","Entertainment","Skiing")
        self.createAccount("MORRISON MOTOR WORKS HYANNIS","MORRISON MOTOR WORKS","Car","Auto Repair")
        self.createAccount("MOUNTAIN HARDWEAR SKI","MOUNTAIN HARDWEAR 418","Entertainment","Skiing")
        self.createAccount("NAVAJO HOPI INDIAN ART","NAVAJO HOPI INDIAN ART","Gifts","Gift Shop")
        self.createAccount("NETFLIX.COM","NETFLIX.COM","Entertainment","Streaming")
        self.createAccount("NETFLIX.COM","NETFLIX.COM","Entertainment","Streaming")
        self.createAccount("NETFLIX.COM","NETFLIX.COM","Entertainment","Streaming")
        self.createAccount("NETFLIX.COM","NETFLIX.COM","Entertainment","Streaming")
        self.createAccount("NOMORERACK ONLINE STORE","NOMORERACK 18005389798","Clothing","Cloud Clothing Store")
        self.createAccount("NOMORERACK ONLINE STORE","NOMORERACK 18005389798","Clothing","Cloud Clothing Store")
        self.createAccount("NOMORERACK ONLINE STORE","NOMORERACK 18005389798","Clothing","Cloud Clothing Store")
        self.createAccount("NORDSTROM RACK DEPT STORE","NORDSTROM-RACK #0347","Clothing","Department Store")
        self.createAccount("OFFICE MAX","OFFICE MAX","Electronics","Computer Store")
        self.createAccount("OLD NAVY STORE","OLD NAVY STORE 6706","Clothing","Clothing Store")
        self.createAccount("OTG MANAGEMENT TAXI","OTG MANAGEMENT BOS, LLC","Travel","Train/Bus/Taxi")
        self.createAccount("PANDA EXPRESS","PANDA EXPRESS #1141","Food","Eating Out")
        self.createAccount("PANDA EXPRESS","PANDA EXPRESS #1491","Food","Eating Out")
        self.createAccount("PANDA EXPRESS","PANDA EXPRESS 700","Food","Eating Out")
        self.createAccount("PANDA EXPRESS","PANDA EXPRESS 700","Food","Eating Out")
        self.createAccount("PANDA EXPRESS","PANDA EXPRESS 700","Food","Eating Out")
        self.createAccount("PANDA EXPRESS","PANDA EXPRESS 700","Food","Eating Out")
        self.createAccount("PATRIOT HEALTH INSTITUTE","PATRIOTHEALTHINSTITUTE","Medical/Dental","Cloud Pharmacy")
        self.createAccount("PEARL RESTAURANT","PEARL RESTAURANT","Food","Eating Out")
        self.createAccount("PRICELINE HOTELS","PLN*PRICELINE HOTELS","Travel","Hotel")
        self.createAccount("PRICELINE HOTELS","PLN*PRICELINE HOTELS","Travel","Hotel")
        self.createAccount("PRICELINE HOTELS","PLN*PRICELINE.COM HTL","Travel","Hotel")
        self.createAccount("PRICELINE HOTELS","PLN*PRICELINE.COM HTL","Travel","Hotel")
        self.createAccount("PRICELINE HOTELS","PLN*PRICELINE.COM HTL","Travel","Hotel")
        self.createAccount("PLYMOUTH AND BROCKTON BUS","PLYMOUTH AND BROCK","Travel","Train/Bus/Taxi")
        self.createAccount("DISNEYLAND?","PP*0934CODE","Entertainment","Amusement Park")
        self.createAccount("Pikes Peak Regional Hospital","PPRH MEDICAL CARE","Medical/Dental","Medical Office")
        self.createAccount("Parking Meter","PUBLIC WORKS-PRKG METR","Car","Parking")
        self.createAccount("Rock and Roll Museum Cleveland","R AND R HOF BOX OFFICE","Entertainment","Site Seeing")
        self.createAccount("RALPHS GROCERY STORE","RALPHS #0060","Food","GrocFinanceery Store")
        self.createAccount("RALPHS GROCERY STORE","RALPHS #0235","Food","Grocery Store")
        self.createAccount("RALPHS GROCERY STORE","RALPHS #0712","Food","Grocery Store")
        self.createAccount("RALPHS GROCERY STORE","RALPHS #0717","Food","Grocery Store")
        self.createAccount("RALPHS GROCERY STORE","RALPHS #0717","Food","Grocery Store")
        self.createAccount("RALPHS GROCERY STORE","RALPHS #0717","Food","Grocery Store")
        self.createAccount("RALPHS GROCERY STORE","RALPHS #0717","Food","Grocery Store")
        self.createAccount("RALPHS GROCERY STORE","RALPHS #0717","Food","Grocery Store")
        self.createAccount("RALPHS GAS STATION","RALPHS FUEL #1717","Car","Gas Station")
        self.createAccount("RAPID LUBE OF WOODLAND PARK","RAPID LUBE OF WOOD","Car","Auto Repair")
        self.createAccount("Chase Credit Card","REDEMPTION CREDIT","Credit Card","Reward Money Back")
        self.createAccount("Rendezvous Cafe Hyannis","Rendezvous Cafe & Creperi","Food","Eating Out")
        self.createAccount("RHAPSODY","RI *RHAPSODY","Entertainment","Streaming")
        self.createAccount("RHAPSODY","RI *RHAPSODY","Entertainment","Streaming")
        self.createAccount("RHAPSODY","RI *RHAPSODY","Entertainment","Streaming")
        self.createAccount("RHAPSODY","RI *RHAPSODY","Entertainment","Streaming")
        self.createAccount("RITE AID STORE","RITE AID STORE #10189","Household","Drug Store")
        self.createAccount("RITE AID STORE","RITE AID STORE #10190","Household","Drug Store")
        self.createAccount("RITE AID STORE","RITE AID STORE #10190","Household","Drug Store")
        self.createAccount("RITE AID STORE","RITE AID STORE 5661","Household","Drug Store")
        self.createAccount("RITE AID STORE","RITE AID STORE 5661","Household","Drug Store")
        self.createAccount("S & Z PETROLEUM INC GAS STATION","S & Z PETROLEUM INC","Car","Gas Station")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE00015784","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE10046134","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE10046134","Food","Grocery Store")
        self.createAccount("SAFEWAY  GROCERY STORE","SAFEWAY  STORE10046134","Food","Grocery Store")
        self.createAccount("SARKU JAPAN RESTAURANT SANTA MONICA","SARKU JAPAN 263","Food","Eating Out")
        self.createAccount("SARKU JAPAN RESTAURANT SANTA MONICA","SARKU JAPAN 263","Food","Eating Out")
        self.createAccount("SHANGHAI CHINESE REST","SHANGHAI CHINESE REST","Food","Eating Out")
        self.createAccount("SHELL OIL GAS STATION","SHELL OIL 57442462909","Car","Gas Station")
        self.createAccount("SHELL OIL GAS STATION","SHELL OIL 57442462909","Car","Gas Station")
        self.createAccount("SHELL OIL GAS STATION","SHELL OIL 57442718805","Car","Gas Station")
        self.createAccount("SHELL OIL GAS STATION","SHELL OIL 57443811500","Car","Gas Station")
        self.createAccount("SHELL OIL GAS STATION","SHELL OIL 57443812102","Car","Gas Station")
        self.createAccount("SHELL OIL GAS STATION","SHELL OIL 57444230007","Car","Gas Station")
        self.createAccount("SHELL OIL GAS STATION","SHELL OIL 57445118805","Car","Gas Station")
        self.createAccount("SHELL OIL GAS STATION","SHELL OIL 57445118805","Car","Gas Station")
        self.createAccount("SMARTE CARTE LOCKER SKI","SMARTE CARTE","Entertainment","Skiing")
        self.createAccount("SMILE WORKS DENTAL CS","SMILE WORKS DENTAL","Medical/Dental","Dental Office")
        self.createAccount("SOHO ARTS COMPANY HYANNIS","SOHO ARTS COMPANY","Gifts","Gift Shop")
        self.createAccount("GRAND CANYON STORE","SOUTH RIM GENERAL STOR","Gifts","Gift Shop")
        self.createAccount("SPEEDWAY GAS & OIL CAPE COD","SPEEDWAY GAS & OIL","Car","Gas Station")
        self.createAccount("SPIRIT AIRLINES","SPIRIT AIRL 4870097262339","Travel","Airplane")
        self.createAccount("SPIRIT AIRLINES","SPIRIT AIRL 4870097551484","Travel","Airplane")
        self.createAccount("STAPLES STATIONARY STORE","STAPLES       00101543","Household","Stationary Store")
        self.createAccount("STAPLES STATIONARY STORE","STAPLES       00113480","Household","Stationary Store")
        self.createAccount("STAPLES STATIONARY STORE","STAPLES       00113480","Household","Stationary Store")
        self.createAccount("STAR MARKET CAPE COD","STAR MARKET #7595","Food","Grocery Store")
        self.createAccount("STAR MARKET CAPE COD","STAR MARKET #7595","Food","Grocery Store")
        self.createAccount("STAR MARKET CAPE COD","STAR MARKET #7595","Food","Grocery Store")
        self.createAccount("SUBWAY SANDWICHES","SUBWAY        00478453","Food","Eating Out")
        self.createAccount("SUNBIRD RESTAURANT COLORADO SPRINGS","SUNBIRD","Food","Eating Out")
        self.createAccount("SIRIUS XM","SXM*SIRIUSXM.COM/ACCT","Entertainment","Streaming")
        self.createAccount("SIRIUS XM","SXM*SIRIUSXM.COM/ACCT","Entertainment","Streaming")
        self.createAccount("THAI MINI CAFE","THAI MINI CAFE","Food","Eating Out")
        self.createAccount("THE CAFE","THE CAFE","Food","Eating Out")
        self.createAccount("THE HOME DEPOT HARDWARE STORE","THE HOME DEPOT 2612","Household","Hardware Store")
        self.createAccount("THE HOT CHOCOLATE SPARROW","THE HOT CHOCOLATE SPAR","Food","Eating Out")
        self.createAccount("THE LEGO STORE","THE LEGO STORE","Gifts","Toy Store")
        self.createAccount("THELADDERS.COM","THELADDERS.COM","Job","Cloud Job Search")
        self.createAccount("DISNEYLAND TIKI JUICE BAR","TIKI JUICE BAR - DL","Food","Eating Out")
        self.createAccount("TJMAXX DEPT STORE","TJMAXX #0241","Clothing","Clothing Store")
        self.createAccount("TJMAXX DEPT STORE","TJMAXX #0241","Clothing","Clothing Store")
        self.createAccount("TJMAXX DEPT STORE","TJMAXX #0241","Clothing","Clothing Store")
        self.createAccount("TJMAXX DEPT STORE","TJMAXX #0241","Clothing","Clothing Store")
        self.createAccount("TOBY KEITH'S RESTAURANT LA","TOBY KEITH'S I LOVE TH","Food","Eating Out")
        self.createAccount("DISNEYLAND PARKING","TOLLS WEST - PARKIN","Entertainment","Amusement Park")
        self.createAccount("DISNEYLAND RESTAURANT","TOMORROWLAND TERRAC","Food","Eating Out")
        self.createAccount("DISNEYLAND TOONTOWN RESTAURANT","TOONTOWN - DL","Food","Eating Out")
        self.createAccount("DISNEYLAND TOONTOWN RESTAURANT","TOONTOWN - DL","Food","Eating Out")
        self.createAccount("TRADER JOE'S GROCERY STORE","TRADER JOE'S #217  QPS","Food","Grocery Store")
        self.createAccount("TRADER JOE'S GROCERY STORE","TRADER JOE'S #217  QPS","Food","Grocery Store")
        self.createAccount("TRADER JOE'S GROCERY STORE","TRADER JOE'S #514  QPS","Food","Grocery Store")
        self.createAccount("TRADER JOE'S GROCERY STORE","TRADER JOE'S #514  QPS","Food","Grocery Store")
        self.createAccount("TRADER JOE'S GROCERY STORE","TRADER JOE'S #514  QPS","Food","Grocery Store")
        self.createAccount("TRADER JOE'S GROCERY STORE","TRADER JOE'S #514  QPS","Food","Grocery Store")
        self.createAccount("UNION STATION FLYAWAY BUS LA","UNIONSTATIONFLYAWAY","Travel","Train/Bus/Taxi")
        self.createAccount("UNITED AIRLINES","UNITED      0162398120306","Travel","Airplane")
        self.createAccount("UNITED AIRLINES","UNITED      0162398120307","Travel","Airplane")
        self.createAccount("POST OFFICE","USPS 05631608335007426","Mail","Post Office")
        self.createAccount("POST OFFICE","USPS 07181206130302608","Mail","Post Office")
        self.createAccount("POST OFFICE","USPS 07981007830313597","Mail","Post Office")
        self.createAccount("POST OFFICE","USPS 24372306034107516","Mail","Post Office")
        self.createAccount("POST OFFICE","USPS 34014395518100933","Mail","Post Office")
        self.createAccount("Vehicle Registration","VEHICLE REGISTRATI","Car","Vehicle Registration")
        self.createAccount("WAL-MART DEPT STORE","WAL-MART #3805","Household","Department Store")
        self.createAccount("WAL-MART DEPT STORE","WAL-MART #3805","Household","Department Store")
        self.createAccount("WAL-MART DEPT STORE","WAL-MART #3805","Household","Department Store")
        self.createAccount("WAL-MART DEPT STORE","WAL-MART #3805","Household","Department Store")
        self.createAccount("WAL-MART DEPT STORE","WAL-MART #3805","Household","Department Store")
        self.createAccount("WAL-MART DEPT STORE","WAL-MART #3805","Household","Department Store")
        self.createAccount("WAL-MART DEPT STORE","WAL-MART #3805","Household","Department Store")
        self.createAccount("WALGREENS DRUG STORE","WALGREENS #10460","Household","Drug Store")
        self.createAccount("WALGREENS DRUG STORE","WALGREENS #12769","Household","Drug Store")
        self.createAccount("WHOLE FOODS GROCERY STORE","WHOLEFDS CCK 10095","Food","Grocery Store")
        self.createAccount("WHOLE FOODS GROCERY STORE","WHOLEFDS NCP 10435","Food","Grocery Store")
        self.createAccount("WHOLE FOODS GROCERY STORE","WHOLEFDS NCP 10435","Food","Grocery Store")
        self.createAccount("WHOLE FOODS GROCERY STORE","WHOLEFDS PPK 10146","Food","Grocery Store")
        self.createAccount("WILSONS LEATHER OUTLETS","WILSONS LEATHER OUTLETS","Clothing","Fur/Leather")
        self.createAccount("WILSONS LEATHER OUTLETS","WILSONS LEATHER OUTLETS","Clothing","Fur/Leather")
        self.createAccount("WAL-MART DEPT STORE","WM SUPERCENTER #3805","Household","Department Store")
        self.createAccount("WOLLEY TAXI CO CLEVELAND","WOLLEY TAXI CO","Travel","Train/Bus/Taxi")
        self.createAccount("WOLLEY TAXI CO CLEVELAND","WOLLEY TAXI CO","Travel","Train/Bus/Taxi")
        self.createAccount(" BIG O TIRES WOODLAND PARK","WOODLAND PARK BIG O TIRES","Car","Auto Parts")
        self.createAccount(" BIG O TIRES WOODLAND PARK","WOODLAND PARK BIG O TIRES","Car","Auto Parts")
        self.createAccount("WOODLAND PARK COMMUNITY CHURCH","WOODLAND PARK COMMUNITY C","Church/Mission","Marital Seminar")
        self.createAccount("WOODLAND PARK DENTAL GROUP","WOODLAND PARK DENTAL GROU","Medical/Dental","Dental Office")
        self.createAccount("WOODLAND PARK DENTAL GROUP","WOODLAND PARK DENTAL GROU","Medical/Dental","Dental Office")
        self.createAccount("WOODLAND PARK DENTAL GROUP","WOODLAND PARK DENTAL GROU","Medical/Dental","Dental Office")
        self.createAccount("WORLD OF DISNEY GIFT STORE","WORLD OF DISNEY - D","Gifts","Gift Shop")
        self.createAccount("WWW.MEDIADAZE.NET STREAMING VIDEO","WWW.MEDIADAZE.NET","Entertainment","Streaming")
        self.createAccount("WWW.MEDIADAZE.NET STREAMING VIDEO","WWW.MEDIADAZE.NET","Entertainment","Streaming")
        self.createAccount("WWW.MEDIADAZE.NET STREAMING VIDEO","WWW.MEDIADAZE.NET","Entertainment","Streaming")
        self.createAccount("WWW.NEWEGG.COM","WWW.NEWEGG.COM","Electronics","Cloud Computer")
        self.createAccount("WWW.OVERLAND.COM","WWW.OVERLAND.COM","Clothing","Cloud Clothing Store")
        
        
        self.createAccount("JOANIE'S BAKERY & DELI - Woodland Park","JOANIE'S BAKERY & DELI","Food","Eating Out")
        self.createAccount("WENDY'S","WENDYS","Food","Eating Out")
        self.createAccount("ASIAN FUSION - Woodland Park","ASIAN FUSION","Food","Eating Out")
        self.createAccount("SMITHS FOOD","SMITHS FOOD #4048","Food","Grocery Store")
        self.createAccount("BOMBAY HOUSE","BOMBAY HOUSE","Food","Eating Out")
        self.createAccount("HATCH FAMILY CHOCOLATES","HATCH FAMILY CHOCOLATES L","Food","Eating Out")
        self.createAccount("NEW GOLDEN DRAGON RESTAURANT","NEW GOLDEN DRAGON RESTAUR","Food","Eating Out")
        self.createAccount("APPLEBEES RESTAURANT","APPLEBEES GRAN48248249","Food","Eating Out")
        self.createAccount("AMICI RESTAURANT - Salt Lake City","AMICI RESTAURANT","Food","Eating Out")
        self.createAccount("RED BUTTE GARDENS - Salt Lake City","RED BUTTE GARDENS OFFICE","Entertainment","Site Seeing")
        self.createAccount("RED BUTTE GARDENS - Salt Lake City","RED BUTTE GARDEN AND ARB","Entertainment","Site Seeing")
        self.createAccount("MAVERIK - Salt Lake City", "MAVERIK #358","Car","Gas Station")
        self.createAccount("WWW.DRESSLINK.COM","WWW.DRESSLINK.COM","Clothing","Cloud Clothing Store")
        self.createAccount("JUDD'S GLASS & MIRROR - Woodland Park","JUDD'S GLASS & MIR","Car","Auto Repair")
               
        for alias in self.map_alias_to_title.keys():
            account_title = self.map_alias_to_title[alias]
            
        super.HowToDeriveNewFields.__init__(self, csv_in)
        return None
