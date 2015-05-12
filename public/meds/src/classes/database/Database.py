'''
    Database
'''

import re, copy
from classes.utils import Container
from classes.utils.CsvObject import CsvObject
from classes.utils.CsvObject import CsvBackquoteDialect

#===============================================================================
# Database
#===============================================================================
class Database(CsvObject):

    #===========================================================================
    # common implementations
    #===========================================================================
    def folderOut(self):
        return "/working/python/finance/out/"
    
    #===========================================================================
    # constructor
    #===========================================================================
    def __init__(self, csv_in, fieldnames, filename):
        
        CsvObject.__init__(self,
            self.folderOut() + filename, fieldnames, CsvBackquoteDialect(), False) 

        self.forEachRow(csv_in)
        return None
  
    #===========================================================================
    # do something to each row of a csv file
    #===========================================================================
    def forEachRow(self, csv_in):
        csv_in.openRead(); self.openWrite()
        for row_in in csv_in.reader:
            rows = self.transformRow(row_in, csv_in, self)
            for row_out in rows.vector:
                self.writer.writerow([row_out[x] for x in self.fieldnames])   
        csv_in.closeRead(); self.closeWrite()
        return None

    #===========================================================================
    # default implementations
    #===========================================================================
    def initializeRowOut(self, row_in, csv_in, csv_out):
        row_out = dict()
        for field in csv_out.fieldnames:
            if field in csv_in.fieldnames:
                row_out[field] = row_in[field]
            else:
                row_out[field] = 'null'
        return row_out

    #===========================================================================
    # default implementations
    #===========================================================================
    def transformRow(self, row_in, csv_in, csv_out):
        row_out = self.initializeRowOut(row_in, csv_in, csv_out)
        # modify row_out            
        rows = Container.VectorOfString()    
        rows.append(row_out)   
        return rows
    
    def copyMatchingFields(self, row_in, csv_in, csv_out):
        row_out = self.initializeRowOut(row_in, csv_in, csv_out)
        # modify row_out            
        rows = Container.VectorOfString()    
        rows.append(row_out)   
        return rows
  
    def returnNoRowsAtAll(self, row_in, csv_in, csv_out):
        rows = Container.VectorOfString()    
        return rows

 
