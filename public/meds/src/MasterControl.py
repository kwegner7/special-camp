'''
    namespace database.MasterControl

    Derived class is at class definition is passed a well ordered path
    of behaviors from a class tree. And is passed any refactored methods
    along the path. This defines the "ISA" components of the class 
    object.
    
    At instantiation, the class is passed state objects. This defines
    the "HASA" components of the class object.
    
    http://0.0.0.0:3000/meds/printform?formtype=med-schedule&campercamperid=548&day=thu&dest=bvsatow@hpeprint.com

'''


PLEASE_SPLIT = True
DONT_SPLIT = False

import sys, os, shutil, glob
from utils import Container

    
#===============================================================================
# goMasterControl
#===============================================================================
def goMasterControl(self, website, formtype, camperid, day, dest, page, year, refresh):
    

    pwd = os.getcwd() + '/'
    #out_folder = pwd + 'out/' + year
    
    sys.path.insert(0, pwd + 'src/records')
       
    import Accumulate.Meds, Normalize.Meds, HtmlTable.Meds
    
    #Container.YEAR_OF_CAMP = year
    
    if formtype == 'All':  
      norm  =  Normalize.Meds.SpecialCamp.MasterSchedule(pwd, website, camperid, day, dest, page, year, refresh)
      accum = Accumulate.Meds.SpecialCamp.MasterSchedule(norm, website, camperid, day, dest, page, year, refresh) 
      norm  =  Normalize.Meds.SpecialCamp.HsDaysSeparated(pwd, website, camperid, day, dest, page, year, refresh)
      accum = Accumulate.Meds.SpecialCamp.HsDaysSeparated(norm, website, camperid, day, dest, page, year, refresh) 
      norm  =  Normalize.Meds.SpecialCamp.HsDaysCollapsed(pwd, website, camperid, day, dest, page, year, refresh)
      accum = Accumulate.Meds.SpecialCamp.HsDaysCollapsed(norm, website, camperid, day, dest, page, year, refresh) 
      norm  =  Normalize.Meds.SpecialCamp.CabinDaysTogether(pwd, website, camperid, day, dest, page, year, refresh)
      accum = Accumulate.Meds.SpecialCamp.CabinDaysTogether(norm, website, camperid, day, dest, page, year, refresh) 
      norm  =  Normalize.Meds.SpecialCamp.LaBusDaysSeparated(pwd, website, camperid, day, dest, page, year, refresh)
      accum = Accumulate.Meds.SpecialCamp.LaBusDaysSeparated(norm, website, camperid, day, dest, page, year, refresh) 
      norm  =  Normalize.Meds.SpecialCamp.CabinAndHsCollapsed(pwd, website, camperid, day, dest, page, year, refresh)
      accum = Accumulate.Meds.SpecialCamp.CabinAndHsCollapsed(norm, website, camperid, day, dest, page, year, refresh) 
      norm  =  Normalize.Meds.SpecialCamp.LeftoverMeds(pwd, website, camperid, day, dest, page, year, refresh)
      accum = Accumulate.Meds.SpecialCamp.LeftoverMeds(norm, website, camperid, day, dest, page, year, refresh) 
         
    if formtype == 'Master-Schedule':   
      norm  =  Normalize.Meds.SpecialCamp.MasterSchedule(pwd, website, camperid, day, dest, page, year, refresh)
      accum = Accumulate.Meds.SpecialCamp.MasterSchedule(norm, website, camperid, day, dest, page, year, refresh) 
      table =  HtmlTable.Meds.SpecialCamp.MasterSchedule(accum, False, website, camperid, day, dest, page, year, refresh)

    if formtype == 'Meds-Administered-By-HS':  
      norm  =  Normalize.Meds.SpecialCamp.HsDaysSeparated(pwd, website, camperid, day, dest, page, year, refresh)
      accum = Accumulate.Meds.SpecialCamp.HsDaysSeparated(norm, website, camperid, day, dest, page, year, refresh) 
      table =  HtmlTable.Meds.SpecialCamp.HsDaysSeparated(accum, False, website, camperid, day, dest, page, year, refresh)

    if formtype == 'Meds-Administered-By-HS-Summarized':   
      norm  =  Normalize.Meds.SpecialCamp.HsDaysCollapsed(pwd, website, camperid, day, dest, page, year, refresh)
      accum = Accumulate.Meds.SpecialCamp.HsDaysCollapsed(norm, website, camperid, day, dest, page, year, refresh) 
      table =  HtmlTable.Meds.SpecialCamp.HsDaysCollapsed(accum, False, website, camperid, day, dest, page, year, refresh)

    if formtype == 'Meds-Administered-In-Cabin':   
      norm  =  Normalize.Meds.SpecialCamp.CabinDaysTogether(pwd, website, camperid, day, dest, page, year, refresh)
      accum = Accumulate.Meds.SpecialCamp.CabinDaysTogether(norm, website, camperid, day, dest, page, year, refresh) 
      table =  HtmlTable.Meds.SpecialCamp.CabinDaysTogether(accum, False, website, camperid, day, dest, page, year, refresh)
   
    if formtype == 'Meds-Administered-During-LA-Bus-Trip':   
      norm  =  Normalize.Meds.SpecialCamp.LaBusDaysSeparated(pwd, website, camperid, day, dest, page, year, refresh)
      accum = Accumulate.Meds.SpecialCamp.LaBusDaysSeparated(norm, website, camperid, day, dest, page, year, refresh) 
      table =  HtmlTable.Meds.SpecialCamp.LaBusDaysSeparated(accum, False, website, camperid, day, dest, page, year, refresh)

    if formtype == 'Guardian-Signature':   
      norm  =  Normalize.Meds.SpecialCamp.CabinAndHsCollapsed(pwd, website, camperid, day, dest, page, year, refresh)
      accum = Accumulate.Meds.SpecialCamp.CabinAndHsCollapsed(norm, website, camperid, day, dest, page, year, refresh) 
      table =  HtmlTable.Meds.SpecialCamp.CabinAndHsCollapsed(accum, False, website, camperid, day, dest, page, year, refresh)

    if formtype == 'Leftover-Meds':   
      norm  =  Normalize.Meds.SpecialCamp.LeftoverMeds(pwd, website, camperid, day, dest, page, year, refresh)
      accum = Accumulate.Meds.SpecialCamp.LeftoverMeds(norm, website, camperid, day, dest, page, year, refresh) 
      table =  HtmlTable.Meds.SpecialCamp.LeftoverMeds(accum, True, website, camperid, day, dest, page, year, refresh)
      

#===============================================================================
# MasterControl
#===============================================================================
class MasterControl():
    
    def __init__(self):
        self.current_directory = os.getcwd()
    
    def PWD(self):
        return self.current_directory
    
    def go(self, website, formtype, camperid, day, dest, page, year, refresh):
        goMasterControl(self, website, formtype, camperid, day, dest, page, year, refresh)

#===============================================================================
# main
#===============================================================================
if __name__ == '__main__':
    website = sys.argv[1]
    formtype = sys.argv[2]
    camperid = sys.argv[3]
    day = sys.argv[4]
    dest = sys.argv[5]
    page = sys.argv[6]
    year = sys.argv[7]
    refresh = sys.argv[8]
    masterControl = MasterControl()
    masterControl.go(website, formtype, camperid, day, dest, page, year, refresh)
