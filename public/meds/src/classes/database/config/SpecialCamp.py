'''
    Config.SpecialCamp
'''

import re, os
from classes.utils.CsvObject import CsvObject, CsvFolder, CsvStandardDialect, FolderOfCsvObjects
from classes.utils import Container
from classes.database.config import Config

#===============================================================================
# common to a category of database
#===============================================================================
class ConfigDatabaseCatagory(Config.ConfigDatabase):  
    
    def usefulFields(self):
        return self.originalFields() 
     
    def derivedFields(self): return list([
    ])
    
    def accumulatedFields(self): return list([
    ])

    def afterSortRestoreAndAccumulate(self, field, row):
        return row[field]

    def HowToValidateAndNormalizeTheFields(self, row_in):
        row_out = dict(row_in)            
        return True, row_out

    def HowToDeriveNewFields(self, row_in):
        row_out = dict(row_in)            
        return True, row_out
            
#===============================================================================
# configure a particular institution within the category
#===============================================================================
class ConfigInstitution(ConfigDatabaseCatagory):  

    def setFolders(self, folder_in, folder_out):
        self.in_folder = folder_in
        self.out_folder = folder_out

    def folderIn(self):
        pwd = os.getcwd() + '/'
        return self.in_folder
        return pwd+"in/"
        return "/home/kurt/ubu/special-camp/download/" 
        return "/home/kurt/working/rails/special-camp/public/meds/in/"
        return "/app/public/meds/in/"

    
    def folderOut(self):
        return self.out_folder
        return Container.TheBaseFolder.location + "/outIndex/"


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
        return CsvStandardDialect()

    def skipFirstRecord(self):
        return True

    def HowToCombineOriginalFiles(self, row_in):
        row_out = dict(row_in)        
        return True, row_out
    
#===============================================================================
# specific to report types
#===============================================================================
class ConfigReportType(ConfigInstitution):  

    def sortOrder(self): return list([
        'camper',
    ])
    
    def sectionChange(self): return list([
    ])
               
    def subsectionChange(self): return list([
    ])

    def collapseOnFields(self): return list([
        'camper',
    ])

    def isSelectedRow(self, row):
        return (
            row['camper'] != '')
       
    def HowToFinallyModifyCertainFields(self, row_in):          
        row_out = dict(row_in)
        return True, row_out
     
config = ConfigReportType()

