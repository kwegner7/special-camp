'''
    Records.Normalize.Meds
    Records.Normalize.Meds.SpecialCamp
    
    
                              EACH PAGE              MEDS      
                              CONTAINS             GIVEN BY        PAGE HELD BY       
                           
    1) Cabin-Days-Together     1 camper/7 days        Cabin          Cabin Leader
    2) HS-Days-Separated       1 camper/1 day         HS             HS
    3) HS-Days-Collapsed       1 camper/collapsed     Cabin          Cabin Leader
    4) Master-Schedule         all campers/1 day      HS and Cabin   HS
    5) Cabin-And-HS-Collapsed  1 camper/collapsed     HS and Cabin   Parent
    6) LA-Bus-Schedule         all bus campers/1 day  HS and Cabin   Bus Captain
    7) Leftover-Meds           1 camper/meds only     HS and Cabin   Parent
    
    
    
'''

import re
from utils.Container import *
from utils import CsvObject
from Normalize import Normalize

#===============================================================================
# Normalize.Meds
#===============================================================================
class Meds(Normalize):
    
    #===========================================================================
    # constructor
    #===========================================================================
    def __init__(self, website, camperid, day, dest, page, year, refresh):
        Normalize.__init__(self, website, camperid, day, dest, page, year, refresh)
        return None
    
    #===========================================================================
    # implementations
    #===========================================================================
    def usefulFields(self):
        return self.originalFields() 
    
    def derivedFields(self):
        return list([
            'ordered_day',
            'ordered_time',
            'date'
        ])

    def getOrderedDay(self, day):
        out = day.replace('Sunday',    '1-sun'      )
        out = out.replace('Monday',    '2-mon'      )
        out = out.replace('Tuesday',   '3-tue'      )
        out = out.replace('Wednesday', '4-wed'      )
        out = out.replace('Thursday',  '5-thu'      )
        out = out.replace('Friday',    '6-fri'      )
        out = out.replace('Saturday',  '7-sat'      )
        out = out.replace('as needed', '8-asneeded' )
        return out
        
    def getDate(self, day, year):
        if year == '2012':
            dates = dict({
                "Sunday" : "July 1, 2012",
                "Monday" : "July 2, 2012",
               "Tuesday" : "July 3, 2012",
             "Wednesday" : "July 4, 2012",
              "Thursday" : "July 5, 2012",
                "Friday" : "July 6, 2012",
              "Saturday" : "July 7, 2012",
             "as needed" : "",
            })
            
        elif year == '2013':
            dates = dict({
                "Sunday" : "June 30, 2013",
                "Monday" : "July 1, 2013",
               "Tuesday" : "July 2, 2013",
             "Wednesday" : "July 3, 2013",
              "Thursday" : "July 4, 2013",
                "Friday" : "July 5, 2013",
              "Saturday" : "July 6, 2013",
             "as needed" : "",
            })
            
        elif year == '2014':
            dates = dict({
                "Sunday" : "June 29, 2014",
                "Monday" : "June 30, 2014",
               "Tuesday" : "July 1, 2014",
             "Wednesday" : "July 2, 2014",
              "Thursday" : "July 3, 2014",
                "Friday" : "July 4, 2014",
              "Saturday" : "July 5, 2014",
             "as needed" : "",
            })
            
        elif year == '2015':
            dates = dict({
                "Sunday" : "June 28, 2015",
                "Monday" : "June 29, 2015",
               "Tuesday" : "June 30, 2015",
             "Wednesday" :  "July 1, 2015",
              "Thursday" :  "July 2, 2015",
                "Friday" :  "July 3, 2015",
              "Saturday" :  "July 4, 2015",
             "as needed" :  "",
            })
            
        else:
            dates = dict({
                "Sunday" : "June 29, 2014",
                "Monday" : "June 30, 2014",
               "Tuesday" : "July 1, 2014",
             "Wednesday" : "July 2, 2014",
              "Thursday" : "July 3, 2014",
                "Friday" : "July 4, 2014",
              "Saturday" : "July 5, 2014",
             "as needed" : "",
            })
        return dates[day]
        
    def getOrderedTime(self, time):          
        if len(time)==7:
            out = time.replace( '1:00 am', '0100')
            out = out.replace(  '2:00 am', '0200')
            out = out.replace(  '3:00 am', '0300')
            out = out.replace(  '4:00 am', '0400')
            out = out.replace(  '5:00 am', '0500')
            out = out.replace(  '6:00 am', '0600')
            out = out.replace(  '7:00 am', '0700')
            out = out.replace(  '8:00 am', '0800')
            out = out.replace(  '9:00 am', '0900')
            out = out.replace(  '1:00 pm', '1300')
            out = out.replace(  '2:00 pm', '1400')
            out = out.replace(  '3:00 pm', '1500')
            out = out.replace(  '4:00 pm', '1600')
            out = out.replace(  '5:00 pm', '1700')
            out = out.replace(  '6:00 pm', '1800')
            out = out.replace(  '7:00 pm', '1900')
            out = out.replace(  '8:00 pm', '2000')
            out = out.replace(  '9:00 pm', '2100')
        elif len(time)==8:
            out = time.replace( '10:00 am', '1000')
            out =  out.replace( '11:00 am', '1100')
            out =  out.replace( '10:00 pm', '2200')
            out =  out.replace( '11:00 pm', '2300')
        elif len(time)==10:
            out = time.replace( '12:00 noon', '1200')
        else:
            out = time
        return out
                
    def determineDerivedFieldsOld(self, field, useful, derived):
        if (field == 'ordered_day'):
            return self.getOrderedDay(useful['day'])

        elif (field == 'ordered_time'):
            return self.getOrderedTime(useful['time'])

        elif (field == 'date'):
            return self.getDate(useful['day'], YEAR_OF_CAMP)
        
        elif (field == 'HS-dispenses'):
            convert = re.sub('1','yes', useful[field])
            convert = re.sub('0','no', convert)
            return convert

        elif (field == 'la-bus'):
            convert = re.sub('1','yes', useful[field])
            convert = re.sub('0','no', convert)
            return convert

        else:
            return useful[field]
                
    def determineDerivedFields(self, row_in, rows_in, rows_out):
        row_out = dict()
        for field in rows_in.fieldnames:
            if field in rows_out.fieldnames:
                row_out[field] = row_in[field]
                        
        row_out['ordered_day'] = self.getOrderedDay(row_in['day'])
        row_out['ordered_time'] = self.getOrderedTime(row_in['time'])
        row_out['date'] = self.getDate(row_in['day'], YEAR_OF_CAMP)
        convert = re.sub('1','yes', row_in['HS-dispenses'])
        convert = re.sub('0','no', convert)
        row_out['HS-dispenses'] = convert
        convert = re.sub('1','yes', row_in['la-bus'])
        convert = re.sub('0','no', convert)
        row_out['la-bus'] = convert
        return row_out

#===============================================================================
# Normalize.Meds.SpecialCamp
#===============================================================================
class SpecialCamp:
    
    #===========================================================================
    # Normalize.Meds.SpecialCamp.Common
    #===========================================================================
    class Common(Meds):
            
        def __init__(self, pwd, website, camperid, day, dest, page, year, refresh):
            self.PWD = pwd
            Meds.__init__(self, website, camperid, day, dest, page, year, refresh)
            return None
                                      
        def folderIn(self):
            return self.PWD+"in/"
            return "/home/kurt/ubu/special-camp/download/" 
        
        def folderOut(self):
            folder = self.PWD+"out/"+YEAR_OF_CAMP+"/"+self.title()+"/"
            #print "FOLDER IS", folder 
            return folder
    
        def originalFields(self): return list([
            '1',
            '2',
            'camper-ID',
            'camper',
            'medication',
            'dosage', 
            '7',
            'day',
            'time',
            'special-instructions',
            'frequency',
            'purpose' ,
            '13' ,
            '14' ,
            'HS-dispenses',
            'la-bus',
            '17',
            '18',
            '19',
            '20',
            '21',
            '22'
            ])
        
        def dialect(self):
            return CsvObject.CsvStandardDialect()
    
        def skipFirstRecord(self):
            return True

    #===========================================================================
    # 1) Normalize.Meds.SpecialCamp.CabinDaysTogether
    #===========================================================================
    class CabinDaysTogether(Common):
        
        def __init__(self, pwd, website, camperid, day, dest, page, year, refresh):
            SpecialCamp.Common.__init__(self, pwd, website, camperid, day, dest, page, year, refresh)
            return None
        
        def title(self):
            return "Meds-Administered-In-Cabin"

    #===========================================================================
    # 2) Normalize.Meds.SpecialCamp.HsDaysSeparated
    #===========================================================================
    class HsDaysSeparated(Common):
        
        def __init__(self, pwd, website, camperid, day, dest, page, year, refresh):
            SpecialCamp.Common.__init__(self, pwd, website, camperid, day, dest, page, year, refresh)
            return None
                
        def title(self):
            return "Meds-Administered-By-HS"
         
    #===========================================================================
    # 3) Normalize.Meds.SpecialCamp.HsDaysCollapsed
    #===========================================================================
    class HsDaysCollapsed(Common):
        
        def __init__(self, pwd, website, camperid, day, dest, page, year, refresh):
            SpecialCamp.Common.__init__(self, pwd, website, camperid, day, dest, page, year, refresh)
            return None
    
        def title(self):
            return "Meds-Administered-By-HS-Summarized"
         
    #===========================================================================
    # 4) Normalize.Meds.SpecialCamp.MasterSchedule
    #===========================================================================
    class MasterSchedule(Common):
        
        def __init__(self, pwd, website, camperid, day, dest, page, year, refresh):
            SpecialCamp.Common.__init__(self, pwd, website, camperid, day, dest, page, year, refresh)
            return None
    
        def title(self):
            return "Master-Schedule"
             
    #===========================================================================
    # 5) Normalize.Meds.SpecialCamp.CabinAndHsCollapsed
    #===========================================================================
    class CabinAndHsCollapsed(Common):
        
        def __init__(self, pwd, website, camperid, day, dest, page, year, refresh):
            SpecialCamp.Common.__init__(self, pwd, website, camperid, day, dest, page, year, refresh)
            return None
    
        def title(self):
            return "Guardian-Signature"
                 
    #===========================================================================
    # 6) Normalize.Meds.SpecialCamp.LaBusDaysSeparated
    #===========================================================================
    class LaBusDaysSeparated(Common):
        
        def __init__(self, pwd, website, camperid, day, dest, page, year, refresh):
            SpecialCamp.Common.__init__(self, pwd, website, camperid, day, dest, page, year, refresh)
            return None
                
        def title(self):
            return "Meds-Administered-During-LA-Bus-Trip"
         
    #===========================================================================
    # 7) Normalize.Meds.SpecialCamp.LeftoverMeds
    #===========================================================================
    class LeftoverMeds(Common):
        
        def __init__(self, pwd, website, camperid, day, dest, page, year, refresh):
            SpecialCamp.Common.__init__(self, pwd, website, camperid, day, dest, page, year, refresh)
            return None
    
        def title(self):
            return "Leftover-Meds"
         

