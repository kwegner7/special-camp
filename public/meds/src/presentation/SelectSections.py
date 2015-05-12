'''
    namespace src.finance.SelectSections
'''
    
########################################################################
# SelectSections.Continuous
########################################################################
class Continuous():
    
    def title(self): return 'Continuous'
            
    def subsectionChange(self):
        return list([ '' ])

########################################################################
# SelectSections.Month
########################################################################
class Year():

    def title(self): return 'Year'
                
    def subsectionChange(self): return list([
        'Year'
    ])

########################################################################
# SelectSections.Month
########################################################################
class Month():

    def title(self): return 'Month'
                
    def subsectionChange(self): return list([
        'YearMonth'
    ])
    
#===============================================================================
# Special Camp
#===============================================================================
class ByDay():

    def title(self): return 'SubsectionWeekdays'
                
    def subsectionChange(self):
        return ['day']

class SubsectionTime():

    def title(self): return 'SubsectionTime'
                
    def subsectionChange(self):
        return ['time']
    
class NoSubsection():

    def title(self): return 'NoSubsection'
                
    def subsectionChange(self):
        return ['']

