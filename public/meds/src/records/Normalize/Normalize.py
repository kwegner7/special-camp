'''
    Records.Normalize
    Records.Normalize.Finance.
    Records.Normalize.Finance.BeyondBanking
    Records.Normalize.Finance.PaypalFaraja
'''

import os, copy, re
from Database import Database
from utils.CsvObject import *
from utils import Container

#===============================================================================
# Records.Normalize
#===============================================================================
class Normalize(Database):

    #===========================================================================
    # implementations
    #===========================================================================
    def combineOriginals(self): pass
    def normalizeOriginals(self): pass
    def recordsDerived(self): pass

    #===========================================================================
    # constructor
    #===========================================================================
    def __init__(self, website, camperid, day, dest, page, year, refresh):
        Database.__init__(self, website, camperid, day, dest, page, year, refresh)
        csv_combined = self.combineOriginals(self.folderIn(), self.folderOut())
        self.csv_object = self.normalizeOriginals(csv_combined, self.folderOut())
        self.website = website
        return None
    
                 
    def doThis(self, row_in, rows_in, rows_out):
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

  
    #===========================================================================
    # combine original files with original format
    #===========================================================================
    def combineOriginals(self, folder_in, folder_out):
        Container.clearFolder(folder_out)
        file_out = folder_out+'OriginalsCombined.csv'
        csv_folder = CsvFolder( folder_in,
            self.originalFields(), 
            self.dialect(), 
            self.skipFirstRecord() )
        csv_objects = FolderOfCsvObjects(file_out, csv_folder)
        csv_originals = csv_objects.combineIntoOneCsvObject()
        return csv_originals

    #===========================================================================
    # original columns appended with derived columns
    #===========================================================================
    def normalizeOriginalsOld(self, csv_combined_originals, folder_out):
        normalized = self.recordsDerived(csv_combined_originals, folder_out)
        if False: print "\n    Normalized records are at", normalized.filename
        return normalized
    
    def normalizeOriginals(self, csv_combined_originals, folder_out):
        rows_in = csv_combined_originals
        fieldnames = self.usefulFields() + self.derivedFields()
        rows_out = CsvObject(folder_out+'Derived.csv', fieldnames)
        normalized = self.recordsDerived(rows_in, rows_out)
        #normalized = self.sql.forEachRow(rows_in, rows_out)
        if False: print "\n    Normalized records are at", normalized.filename
        return normalized
    
    #===========================================================================
    # recordsDerived
    #===========================================================================
    def recordsDerivedOld(self, rows_in, folder_out):
        fieldnames = self.usefulFields() + self.derivedFields()
        rows_out = CsvObject(folder_out+'Derived.csv', fieldnames)
        rows_in.openRead(); rows_out.openWrite()
        for row in rows_in.reader:
            derived = dict()
            for x in rows_out.fieldnames:
                derived[x] = self.determineDerivedFields(x, row, derived)
            rows_out.writer.writerow([derived[x] for x in rows_out.fieldnames])
        rows_in.closeRead(); rows_out.closeWrite()
        return rows_out

    def recordsDerived(self, rows_in, rows_out):
        rows_in.openRead(); rows_out.openWrite()
        for row in rows_in.reader:
            derived = self.determineDerivedFields(row, rows_in, rows_out)
            rows_out.writer.writerow([derived[x] for x in rows_out.fieldnames])
        rows_in.closeRead(); rows_out.closeWrite()
        return rows_out

    