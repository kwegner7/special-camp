'''
    Records.Accumulate.Meds
    Records.Accumulate.Meds.SpecialCamp
'''

import re
from records.Accumulate.Accumulate import Accumulate
from presentation import SelectOrdering, SelectSections, SelectColumns

#===============================================================================
# Accumulate.Meds
#===============================================================================
class Meds(Accumulate):
        
    def __init__(self, normalize, website, camperid, day, dest, page, year, refresh):
        Accumulate.__init__(self, normalize, website, camperid, day, dest, page, year, refresh)
        return None

    def accumulatedFields(self):
        return list([])
    
    def afterSortRestoreAndAccumulate(self, field, row):
        return row[field]

    def uniqueFields(self):
        return list([])

#===============================================================================
# Accumulate.Meds.SpecialCamp
#===============================================================================
class SpecialCamp:
    
    #===========================================================================
    # Accumulate.Meds.SpecialCamp.Common
    #===========================================================================
    class Common(Meds):
          
        def __init__(self, normalize, website, camperid, day, dest, page, year, refresh):
            Meds.__init__(self, normalize, website, camperid, day, dest, page, year, refresh)
            return None

        def accumulatedFields(self):
            return list(['all_days'])
            
        def afterSortRestoreAndAccumulate(self, field, in_row, this_is_last_row_of_collapse):
            out_row = dict(in_row)
            day = str(in_row['day'])[0:2] 
            if day == 'as':
                self.all_days += "as needed "
            else:
                self.all_days += day + " "
            out_row['all_days'] = self.all_days
            #print self.all_days
            if this_is_last_row_of_collapse or not self.accumulateDays():
                 self.all_days = ''
            return out_row

        def accumulateDays(self):
            return False
        
    #===========================================================================
    # Accumulate.Meds.SpecialCamp.CabinDaysTogether
    # Cabin-Days-Together     1 camper/7 days        Cabin          Cabin Leader
    #===========================================================================
    class CabinDaysTogether(Common):
        
        def __init__(self, normalize, website, camperid, day, dest, page, year, refresh):
            SpecialCamp.Common.__init__(self, normalize, website, camperid, day, dest, page, year, refresh)
            return None
    
        def sortOrder(self):
            return ['camper', 'ordered_day', 'ordered_time', 'medication']
    
        def sectionChange(self):
            return ['camper']
        
        def subsectionChange(self):
            return ['ordered_day']
    
        def isSelectedRow(self, col, records_in):
            return ( col['HS-dispenses'] != 'yes' and col['camper'] != '' )

    #===========================================================================
    # Accumulate.Meds.SpecialCamp.HsDaysCollapsed
    # HS-Days-Collapsed       1 camper/collapsed     Cabin          Cabin Leader
    #===========================================================================
    class HsDaysCollapsed(Common):
        
        def __init__(self, normalize, website, camperid, day, dest, page, year, refresh):
            SpecialCamp.Common.__init__(self, normalize, website, camperid, day, dest, page, year, refresh)
            return None
    
        def sortOrder(self):
            return ['camper', 'ordered_time', 'medication', 'ordered_day']
     
        def sectionChange(self):
            return ['camper']
    
        def subsectionChange(self):
            return ['ordered_time']
        
        def isSelectedRow(self, col, records_in):
            return (
                col['HS-dispenses'] == 'yes' and col['camper'] != '' 
            )
            
        def uniqueFields(self):
            return ['camper', 'ordered_time', 'medication']

    #===========================================================================
    # Accumulate.Meds.SpecialCamp.HsDaysSeparated
    # HS-Days-Separated       1 camper/1 day         HS             HS
    #===========================================================================
    class HsDaysSeparated(Common):
        
        def __init__(self, normalize, website, camperid, day, dest, page, year, refresh):
            SpecialCamp.Common.__init__(self, normalize, website, camperid, day, dest, page, year, refresh)
            return None
    
        def sortOrder(self):
            return ['camper', 'ordered_day', 'ordered_time', 'medication']

        def sectionChange(self):
            return ['camper', 'ordered_day']
        
        def subsectionChange(self):
            return ['ordered_time']

        def isSelectedRow(self, col, records_in):
            return (
                col['HS-dispenses'] == 'yes' and col['camper'] != '' 
            )

    #===========================================================================
    # Accumulate.Meds.SpecialCamp.MasterSchedule
    # Master-Schedule         all campers/1 day      HS and Cabin   HS
    #===========================================================================
    class MasterSchedule(Common):
        
        def __init__(self, normalize, website, camperid, day, dest, page, year, refresh):
            SpecialCamp.Common.__init__(self, normalize, website, camperid, day, dest, page, year, refresh)
            return None
    
        def sortOrder(self):
            return ['ordered_day', 'ordered_time', 'camper', 'HS-dispenses', 'medication']
     
        def sectionChange(self):
            return ['ordered_day']
    
        def subsectionChange(self):
            return ['ordered_time']
        
        def isSelectedRow(self, col, records_in):
            return ( col['camper'] != ''  )
                
    #===========================================================================
    # Accumulate.Meds.SpecialCamp.LaBusDaysSeparated
    # LA-Bus-Schedule         all bus campers/1 day  HS and Cabin   Bus Captain
    #===========================================================================
    class LaBusDaysSeparated(Common):
        
        def __init__(self, normalize, website, camperid, day, dest, page, year, refresh):
            SpecialCamp.Common.__init__(self, normalize, website, camperid, day, dest, page, year, refresh)
            return None
    
        def sortOrder(self):
            return ['ordered_day', 'ordered_time', 'camper', 'medication']

        def sectionChange(self):
            return list([ 'ordered_day' ])
        
        def subsectionChange(self):
            return ['ordered_time']

        def isSelectedRow(self, col, records_in):
            #print "LA BUS FIELD", col['la-bus']
            is_la_bus = (
                ( col['camper'] == 'Yamada, Jason' ) or
                re.search( 'trip', col['la-bus'] ) != None or
                re.search( 'only', col['la-bus'] ) != None )
            return ( is_la_bus and col['camper'] != '' and 
                (( col['day'] == 'Sunday') or
                 ( col['day'] == 'Saturday' and col['ordered_time'] > '0900') or
                 ( col['day'] == 'as needed' )
                ))
    
    #===========================================================================
    # Accumulate.Meds.SpecialCamp.CabinAndHsCollapsed
    # Cabin-And-HS-Collapsed  1 camper/collapsed     HS and Cabin   Parent
    #===========================================================================
    class CabinAndHsCollapsed(Common):
        
        def __init__(self, normalize, website, camperid, day, dest, page, year, refresh):
            SpecialCamp.Common.__init__(self, normalize, website, camperid, day, dest, page, year, refresh)
            return None
    
        def sortOrder(self):
            return ['camper', 'ordered_time', 'medication', 'ordered_day']
     
        def sectionChange(self):
            return ['camper']
    
        def subsectionChange(self):
            return ['ordered_time']
        
        def isSelectedRow(self, col, records_in):
            return ( col['camper'] != ''  )
            
        def uniqueFields(self):
            return ['camper', 'ordered_time', 'medication']
           
        def accumulateDays(self):
			return True
           
        def accumulatedFieldss(self):
            return list(['all_days'])
    
        def afterSortRestoreAndAccumulatee(self, field, row):
            if field == 'all_days':
                day = str(row['day'])[0:2]
                if day == 'as': self.all_days += "as needed" + " "
                else: self.all_days += day + " "
                print "new row", row['camper'], row['day'], row['medication'], self.all_days
                return self.all_days
            return row[field]

    #===========================================================================
    # Accumulate.Meds.SpecialCamp.CabinAndHsCollapsed
    # Leftover-Meds           1 camper/meds only     HS and Cabin   Parent
    #===========================================================================
    class LeftoverMeds(Common):
        
        def __init__(self, normalize, website, camperid, day, dest, page, year, refresh):
            SpecialCamp.Common.__init__(self, normalize, website, camperid, day, dest, page, year, refresh)
            return None
    
        def sortOrder(self):
            return ['camper', 'medication', 'ordered_day', 'ordered_time']
     
        def sectionChange(self):
            return ['camper']
    
        def subsectionChange(self):
            return ['']
        
        def isSelectedRow(self, col, records_in):
            return ( col['camper'] != ''  )
            
        def uniqueFields(self):
            return ['medication']

