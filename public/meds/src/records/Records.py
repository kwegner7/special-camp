'''
    Records
'''


#===============================================================================
# Class derivation tree
#===============================================================================
from records.normalize.meds.special_camp.SpecialCamp import SpecialCamp
class Normalize():
       
    class Meds():
        
        class SpecialCamp(SpecialCamp):            
            def __init__(self, folder_in, folder_out):
                SpecialCamp.__init__(self, folder_in, folder_out)
                
from records.accumulate.meds.special_camp.SpecialCamp import SpecialCampp
class Accumulate():
       
    class Meds():
        
        class SpecialCamp(SpecialCampp):            
            def __init__(self, csv_object, folder_out):
                SpecialCampp.__init__(self, csv_object, folder_out)
                
from records.present.meds.special_camp.SpecialCamp import SpecialCamppp
class Present():
       
    class Meds():
        
        class SpecialCamp(SpecialCamppp):            
            def __init__(self, csv_object, folder_out, selections):
                SpecialCamppp.__init__(self, csv_object, folder_out, selections)
