'''
    Report.SpecialCamp
'''

from classes.report.Report import Report 
from classes.html import HtmlSpecialCamp
from classes.database import Db
from classes.database.config import SpecialCamp
    
#===============================================================================
# CamperList
#===============================================================================
class CamperList(Report):
    
    def __init__(self, in_folder, out_folder):
        self.in_folder = in_folder
        self.out_folder = out_folder
        Report.__init__(self)

    def whichConfigClass(self):
        SpecialCamp.config.setFolders(self.in_folder, self.out_folder)
        return SpecialCamp.config
    
    def htmlFolder(self):
        return 'CamperList/'
    
    def whichCsvModule(self):
        return Db
    
    def whichHtmlModule(self):
        return HtmlSpecialCamp.Details

 
