'''
    Report
'''

from classes.utils.ShellCommand import ShellCommand
from classes.utils import CsvObject

#===============================================================================
# Report
#===============================================================================
class Report():

    #===========================================================================
    # required implementations
    #===========================================================================
    def whichConfigClass(self): raise Exception("Method not implemented")
    def whichCsvModule(self):   raise Exception("Method not implemented")
    def whichHtmlModule(self):  raise Exception("Method not implemented")

    #===========================================================================
    # constructor generates the HTML from the CSV originals
    #===========================================================================
    def __init__(self):

        config = self.whichConfigClass()   
        csv    = self.whichCsvModule()   
        html   = self.whichHtmlModule()   
        
        csv_originals      = csv.Pass0(config)
        print  "csv_originals",csv_originals.filename 
        csv_derived        = csv.Pass1(csv_originals, config)
        csv_sorted         = CsvObject.CsvObject(config.sortedFilename(), csv_derived.fieldnames); self.sort(csv_derived,csv_sorted)
        csv_selected       = csv.Pass2(csv_sorted, config)
        csv_accumulated    = CsvObject.CsvObject(config.accumulatedFilename(), csv_selected.fieldnames+config.accumulatedFields())
        csv_accumulated    = csv.Pass3(config, csv_selected, csv_accumulated) 
        csv_special_fields = csv.Pass4(csv_accumulated, config)

        table = html(
            csv_special_fields,
            config.sectionChange(),
            config.subsectionChange(),
            config.folderOut() + self.htmlFolder())
 
        return None
    
    def sort(self, csv_derived, csv_sorted):
        ShellCommand('sort  ' + csv_derived.filename).redirect(csv_sorted.filename)                       
 
