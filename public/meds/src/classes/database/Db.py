'''
    Db
'''

from classes.utils import Container
from classes.utils.CsvObject import CsvObject
from classes.database import Row

#===============================================================================
# Db
#===============================================================================
class Db(CsvObject):

    def __init__(self, csv_in, csv_out, row, config):
        CsvObject.__init__(self, csv_out.filename, csv_out.fieldnames)                    
        self.csv_in = csv_in
        self.csv_out = csv_out
        self.row = row
        self.forEachRow()
            
    def forEachRow(self):
        print "Db.py",self.csv_in.filename, self.csv_out.filename
        self.csv_in.openRead(); self.csv_out.openWrite()
        for row_in in self.csv_in.reader:
            transform = self.row
            please_write_row, row_out = transform.query(row_in)
            if please_write_row:
                self.csv_out.writer.writerow([row_out[x] for x in self.csv_out.fieldnames])   
        self.csv_in.closeRead(); self.csv_out.closeWrite()
        return self.csv_out

#===============================================================================
# Pass0
#===============================================================================
def Pass0(config):
    csv_originals = config.HowToCombineFromFolder() 
    return csv_originals        

#===============================================================================
# Pass1
#===============================================================================
class Pass1(Db):
    def __init__(self, csv_in, config):
        sort_order = config.sortOrder()
        setA = set(config.usefulFields()+config.derivedFields())
        setB = set(sort_order)
        setC = setA - setB
        fieldnames = config.sortOrder() + list(setC)

        # /home/kurt/working/rails/special-camp/public/meds/out/csv
        csv_out = CsvObject(
            #Container.TheBaseFolder.location + "/out/csv/Derived.csv",
            Container.TheBaseFolder.location + "/public/meds/outIndex/csv/Derived.csv",
            fieldnames)
        row = Row.Pass1(config)
        Db.__init__(self, csv_in, csv_out, row, config)

#===============================================================================
# Pass2
#===============================================================================
class Pass2(Db):
    def __init__(self, csv_in, config):
        csv_out = CsvObject(
            Container.TheBaseFolder.location + "/public/meds/outIndex/csv/Selected.csv",
            csv_in.fieldnames)
        row = Row.Pass2(config)
        Db.__init__(self, csv_in, csv_out, row, config)

#===============================================================================
# Pass3
#===============================================================================
def Pass3(config, csv_selected, csv_accumulated):
    csv_accumulated = config.HowToAccumulateNewColumns(csv_selected, csv_accumulated) 
    return csv_accumulated        

#===============================================================================
# Pass3
#===============================================================================
class Pass4(Db):
    def __init__(self, csv_in, config):
        csv_out = CsvObject(
            Container.TheBaseFolder.location + "/public/meds/outIndex/csv/SpecialFields.csv",
            csv_in.fieldnames)
        row = Row.Pass4(config)
        Db.__init__(self, csv_in, csv_out, row, config)
        
