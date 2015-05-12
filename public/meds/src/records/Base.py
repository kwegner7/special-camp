'''
    namespace: database/Records.py
        class: Records
     subclass: Base
'''

import os, copy
from database.utils.Container import *
from database.utils.CsvObject import *
from database.utils.ShellCommand import *



########################################################################
# Records
########################################################################
class Base():

    def __init__(self, folder_out, selections):
       
        self.csv_format = selections.csv_format
        self.aliases    = selections.aliases
        self.payment    = selections.payment
        self.categories = selections.categories
        
        self.ordering = selections.ordering
        self.sections = selections.sections
        
        self.rows    = selections.rows
        self.fields  = selections.fields
        self.columns = selections.columns
        
        self.folder_out = folder_out
        self.useful_fields = self.csv_format.originalFields()  
        #self.useful_fields = useful_fields  
       
        return None

    ####################################################################
    # defaults for most applications
    ####################################################################
    def uniqueFields(self):
        return list([])

    ####################################################################
    # these depend on the database provider
    ####################################################################
    def normalizeDateField(self, date_string):
        return self.csv_format.normalizeDateField(date_string)
    
    def normalizeAmountField(self, amount_string, row):
        return self.csv_format.normalizeAmountField(amount_string, row)
    
    def getMethodOfPayment(self, mechanism1, mechanism2):
        return self.payment.getMethodOfPayment(mechanism1, mechanism2)
    
    def getAccountTitle(self, alias, mechanism1, mechanism2):
        return self.aliases.getAccountTitle(alias, mechanism1, mechanism2)    
    ####################################################################

    
    # local method - imposes subclass implementations
    def recordsUseful(self, rows_in):
        fields_out = self.useful_fields
        rows_out = CsvObject(self.folder_out+'Useful.csv', fields_out)
        rows_in.copySomeFieldsMinimizeWhitespace(rows_out)
        if False: print "The      useful .csv file is", rows_out.filename
        return rows_out
    
    # local method - imposes subclass implementations
       
    # local method - imposes subclass implementations
    def recordsSorted(self, rows_derived):
        fieldnames = self.ordering.sortOrder() + self.useful_fields + self.derivedFields()
        
        rows_extended = CsvObject(
            self.folder_out+'Extended.csv', fieldnames)
        rows_derived.copySomeFields(rows_extended)
        
        ShellCommand( 'sort  ' + rows_extended.filename 
                ).redirect(self.folder_out+'ExtendedSorted.csv')

        rows_extended_sorted = CsvObject(
            self.folder_out+'ExtendedSorted.csv', rows_extended.fieldnames)
        rows_sorted = CsvObject(
            self.folder_out+'Sorted.csv', rows_derived.fieldnames)
        rows_extended_sorted.copySomeFields(rows_sorted)
                
        if False: print "The      sorted .csv file is", rows_sorted.filename
        return rows_sorted
    
    def recordsSelected(self, rows_sorted):
        fieldnames = self.useful_fields + self.derivedFields()
        rows_in = rows_sorted
        rows_out = CsvObject(self.folder_out+'Selected.csv', fieldnames)
        
        rows_in.openRead(); rows_out.openWrite()
        for row in rows_in.reader:
            if self.rows.isSelectedRow(row, rows_in):
                rows_out.writer.writerow([row[x] for x in rows_out.fieldnames])
        rows_in.closeRead(); rows_out.closeWrite()
                
        if False: print "The    selected .csv file is", rows_out.filename
        return rows_out

    # local method - imposes subclass implementations
    def recordsAccumulated(self, rows_selected):
        
        def checkForChanges(row):
            self.monitor_unique.slideFieldValues(row)
            self.monitor.slideFieldValues(row)
            unique_has_changed = self.monitor_unique.fieldHasChanged(self.uniqueFields())
            field_list = self.ordering.sectionChange() + self.sections.subsectionChange()
            field_has_changed  = self.monitor.fieldHasChanged(field_list)
            month_has_changed  = self.monitor.fieldHasChanged(['YearMonth'])
            year_has_changed   = self.monitor.fieldHasChanged(['Year'])
            self.running_totals.accumulate(row['Amount'], field_has_changed)
            self.month_totals.accumulate(row['Amount'], month_has_changed)
            self.year_totals.accumulate(row['Amount'], year_has_changed)
            return unique_has_changed

        fieldnames = self.useful_fields + self.derivedFields() + self.accumulatedFields()
        rows_accumulated = CsvObject(
            self.folder_out+'Accumulated.csv', fieldnames)
        
        rows_selected.openRead(); rows_accumulated.openWrite()
        for row in rows_selected.reader:
            unique_has_changed = checkForChanges(row)
            out = dict()
            for x in rows_accumulated.fieldnames:
                out[x] = self.afterSortRestoreAndAccumulate(x, row)
                out[x] = String(out[x]).whiteSpaceToBlank()
            if len(self.uniqueFields()) == 0 or unique_has_changed:
                fields_out = [out[x] for x in rows_accumulated.fieldnames]
                rows_accumulated.writer.writerow(fields_out)            
        rows_selected.closeRead(); rows_accumulated.closeWrite()
        
        if False: print "The accumulated .csv file is", rows_accumulated.filename
        return rows_accumulated

    def recordsSpecialFields(self, rows_accumulated):
        rows_in = rows_accumulated
        rows_out = CsvObject(self.folder_out+'SpecialFields.csv', rows_accumulated.fieldnames)
        
        rows_in.openRead(); rows_out.openWrite()
        for row in rows_in.reader:
            special = self.fields.determineSpecialFields(row)
            rows_out.writer.writerow([special[x] for x in rows_out.fieldnames])
        rows_in.closeRead(); rows_out.closeWrite()
                
        if False: print "Final CSV file ready for presentation", rows_out.filename
        return rows_out
    
        
    #===========================================================================
    # 3) sort and section and append the accumulated columns
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

    #===========================================================================
    # 4) select rows and modify fields for presentation
    #===========================================================================
    def selectRowsAndModifyFieldsForPresentation(self, accumulated):
        selected = self.recordsSpecialFields(accumulated)
        return selected
    
    

