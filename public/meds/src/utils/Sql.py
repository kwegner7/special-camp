'''
    Records.Normalize
    Records.Normalize.Finance.
    Records.Normalize.Finance.BeyondBanking
    Records.Normalize.Finance.PaypalFaraja
'''

import re
from utils.Container import *
from utils import CsvObject

#===============================================================================
# Sql
#===============================================================================
class Sql():

    #===========================================================================
    # implementations
    #===========================================================================
    def doThis(self): pass

    #===========================================================================
    # constructor
    #===========================================================================
    def __init__(self):
        return None
  
    #===========================================================================
    # do something to each row of a csv file
    #===========================================================================
    def forEachRow(self, rows_in, rows_out):
        rows_in.openRead(); rows_out.openWrite()
        for row in rows_in.reader:
            derived = self.doThis(row, rows_in, rows_out)
            rows_out.writer.writerow([derived[x] for x in rows_out.fieldnames])
        rows_in.closeRead(); rows_out.closeWrite()
        return rows_out

                 
    def doThisWas(self, row_in, rows_in, rows_out):
        row_out = dict()
        for field in rows_in.fieldnames:
            if field in rows_out.fieldnames:
                row_out[field] = row_in[field]
                        
        #row_out['ordered_day'] = self.getOrderedDay(row_in['day'])
        #row_out['ordered_time'] = self.getOrderedTime(row_in['time'])
        #row_out['date'] = self.getDate(row_in['day'], YEAR_OF_CAMP)
        row_out['ordered_day'] = 'day'
        row_out['ordered_time'] ='time'
        row_out['date'] = 'date'
        convert = re.sub('1','yes', row_in['HS-dispenses'])
        convert = re.sub('0','no', convert)
        row_out['HS-dispenses'] = convert
        convert = re.sub('1','yes', row_in['la-bus'])
        convert = re.sub('0','no', convert)
        row_out['la-bus'] = convert
        return row_out
