'''
    Records.Accumulate
    Records.Accumulate.Finance
    Records.Accumulate.Finance.BeyondBanking
    Records.Accumulate.Finance.PaypalFaraja
'''

import os, copy
from utils.CsvObject import *
from utils.ShellCommand import *
from utils.Container import *
from Database import Database


#===============================================================================
# Records.Accumulate
#===============================================================================
class Accumulate(Database):

    #===========================================================================
    # constructor
    #===========================================================================
    def __init__(self, normalized, website, camperid, day, dest, page, year, refresh):
        Database.__init__(self, website, camperid, day, dest, page, year, refresh)
        self.normalized = normalized
        csv_object_in = normalized.csv_object   
        self.folder_out = csv_object_in.foldername
        self.csv_accumulated = self.obtainAccumulatedRecords(csv_object_in)
        #self.csv_object = self.recordsSpecialFields(self.csv_accumulated)
        self.csv_object = self.csv_accumulated
        return None
    
    def title(self):
        return self.normalized.title()
    
    #===========================================================================
    # ordering, sectioning, subsectioning
    #===========================================================================
    def fieldsDeterminingSection(self):
        return self.sectionChange()
    
    def fieldsDeterminingSubsection(self):
        return self.sectionChange() + self.subsectionChange()

    def sortOrder(self):
        return self.selectOrdering().sortOrder()
 
    def sectionChange(self):
        return self.selectOrdering().sectionChange()

    def subsectionChange(self):
        return self.selectSections().subsectionChange()

    #===========================================================================
    # implementations
    #===========================================================================
    def obtainAccumulatedRecords(self, normalized):
        self.monitor_unique = MonitorField()
        self.monitor = MonitorField()
        self.running_totals = RunningTotals() # RunningTotals(14119.05)
        self.month_totals = RunningTotals()
        self.year_totals = RunningTotals()

        sorted      = self.recordsSorted(normalized)
        selected    = self.recordsSelected(sorted)
        accumulated = self.recordsAccumulated(selected)
        
        if False: print "Accumulated records are at", accumulated.filename
        return accumulated
    
    def pleaseSort(self, rows_in, sort_order, rows_out_fullpath, reversed=False):
        fieldnames = sort_order + rows_in.fieldnames        
        rows_extended = CsvObject('/tmp/Extended.csv', fieldnames)
        rows_in.copySomeFields(rows_extended)
        if reversed:
            ShellCommand( 'sort --reverse ' + rows_extended.filename 
                    ).redirect('/tmp/ExtendedSorted.csv')
        else:
            ShellCommand( 'sort ' + rows_extended.filename 
                    ).redirect('/tmp/ExtendedSorted.csv')
                    
        rows_extended_sorted = CsvObject(
            '/tmp/ExtendedSorted.csv', rows_extended.fieldnames)
        rows_sorted = CsvObject(
            rows_out_fullpath, rows_in.fieldnames)
        rows_extended_sorted.copySomeFields(rows_sorted)
        return rows_sorted
        
    def recordsSorted(self, rows_derived):
        rows_sorted = self.pleaseSort(
            rows_derived, self.sortOrder(), self.folder_out+'Sorted.csv')
        return rows_sorted    
    
    def recordsSelected(self, rows_sorted):
        fieldnames =  rows_sorted.fieldnames
        rows_in = rows_sorted
        rows_out = CsvObject(self.folder_out+'Selected.csv', fieldnames)
        
        rows_in.openRead(); rows_out.openWrite()
        for row in rows_in.reader:
            if self.isSelectedRow(row, rows_in):
                rows_out.writer.writerow([row[x] for x in rows_out.fieldnames])
        rows_in.closeRead(); rows_out.closeWrite()
                
        if False: print "The    selected .csv file is", rows_out.filename
        return rows_out

    def recordsAccumulated(self, rows_selected):
        
        def checkForChanges(row):
            self.monitor_unique.slideFieldValues(row)
            self.monitor.slideFieldValues(row)
            unique_has_changed = self.monitor_unique.fieldHasChanged(self.uniqueFields())
            field_list = self.sectionChange() + self.subsectionChange()
            field_has_changed  = self.monitor.fieldHasChanged(field_list)
            month_has_changed  = self.monitor.fieldHasChanged(['YearMonth'])
            year_has_changed   = self.monitor.fieldHasChanged(['Year'])
            # FIX THIS
            if 'Amount' in row.keys():
                self.running_totals.accumulate(row['Amount'], field_has_changed)
                self.month_totals.accumulate(row['Amount'], month_has_changed)
                self.year_totals.accumulate(row['Amount'], year_has_changed)
            return unique_has_changed

        accum_fieldnames = rows_selected.fieldnames + self.accumulatedFields()
        rows_accumulated = CsvObject(
            self.folder_out+'Accumulated.csv', accum_fieldnames)
        
        first_time = True; self.all_days = ''
        rows_selected.openRead(); rows_accumulated.openWrite()
        for future_row in rows_selected.reader:
            this_is_last_row_of_collapse = checkForChanges(future_row)
            if first_time:
                first_time = False
                row = future_row
                continue
     
            # FIX THIS FOR FINANCE       
            out = self.afterSortRestoreAndAccumulate('field', row, this_is_last_row_of_collapse)
            if len(self.uniqueFields()) == 0 or this_is_last_row_of_collapse:
                rows_accumulated.writer.writerow(
                    [String(out[x]).whiteSpaceToBlank() for x in rows_accumulated.fieldnames])

            
            
            #for x in rows_accumulated.fieldnames:
            #    out[x] = self.afterSortRestoreAndAccumulate(x, row)
            #    out[x] = String(out[x]).whiteSpaceToBlank()
            #if len(self.uniqueFields()) == 0 or this_is_last_row_of_collapse:
            #    out['all_days'] = 'Nary'
            #    fields_out = [out[x] for x in rows_accumulated.fieldnames]
            #    rows_accumulated.writer.writerow(fields_out)  
                          
            row = future_row
        rows_selected.closeRead(); rows_accumulated.closeWrite()
        
        return rows_accumulated
    
   
    
'''
    def pleaseWriteRecord(self, unique_has_changed, rows_accumulated, out, last_time):
        #return (
        #    len(self.uniqueFields()) == 0 or unique_has_changed,
        #    [out[x] for x in rows_accumulated.fieldnames] )

        if last_time:
            if len(self.uniqueFields()) == 0:
                return False, [out[x] for x in rows_accumulated.fieldnames]
            else:
                return True, [self.prev_out[x] for x in rows_accumulated.fieldnames]
            
        if len(self.uniqueFields()) == 0:
            return True, [out[x] for x in rows_accumulated.fieldnames]
        
        if unique_has_changed:
            print out['all_days']
            return True, [self.prev_out[x] for x in rows_accumulated.fieldnames]
        else:
            self.prev_out = out
            return False, [self.prev_out[x] for x in rows_accumulated.fieldnames]    



    def recordsAccumulated(self, rows_selected):
        
        def checkForChanges(row):
            self.monitor_unique.slideFieldValues(row)
            self.monitor.slideFieldValues(row)
            unique_has_changed = self.monitor_unique.fieldHasChanged(self.uniqueFields())
            field_list = self.sectionChange() + self.subsectionChange()
            field_has_changed  = self.monitor.fieldHasChanged(field_list)
            month_has_changed  = self.monitor.fieldHasChanged(['YearMonth'])
            year_has_changed   = self.monitor.fieldHasChanged(['Year'])
            # FIX THIS
            if 'Amount' in row.keys():
                self.running_totals.accumulate(row['Amount'], field_has_changed)
                self.month_totals.accumulate(row['Amount'], month_has_changed)
                self.year_totals.accumulate(row['Amount'], year_has_changed)
            return unique_has_changed

        accum_fieldnames = rows_selected.fieldnames + self.accumulatedFields()
        rows_accumulated = CsvObject(
            self.folder_out+'Accumulated.csv', accum_fieldnames)
        
        self.all_days = ''
        rows_selected.openRead(); rows_accumulated.openWrite()
        for row in rows_selected.reader:
            unique_has_changed = checkForChanges(row)
            out = dict()
            for x in rows_accumulated.fieldnames:
                out[x] = self.afterSortRestoreAndAccumulate(x, row)
                out[x] = String(out[x]).whiteSpaceToBlank()
            please_write, fields_out = self.pleaseWriteRecord(
                unique_has_changed, rows_accumulated, out, False)
            if please_write:
                rows_accumulated.writer.writerow([out[x] for x in rows_accumulated.fieldnames])
        #please_write, fields_out = self.pleaseWriteRecord(True,  rows_accumulated, out, True)
        #if please_write:
        #    rows_accumulated.writer.writerow(fields_out)
        rows_selected.closeRead(); rows_accumulated.closeWrite()
        
        return rows_accumulated
'''    
    
