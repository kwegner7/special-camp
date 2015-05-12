'''
    Row
'''

#===============================================================================
# Row
#===============================================================================
class Row(dict):
    
    def __init__(self):        
        dict.__init__(self)

    def initializeRowOut(self, row_in):
        for field in row_in.keys():
            self[field] = row_in[field]
            
#===============================================================================
# Pass1
#===============================================================================
class Pass1(Row):
    
    def __init__(self, config):
        self.config = config        
        Row.__init__(self)
            
    def query(self, row_in):
        pleaseA, rowA = self.config.HowToCombineOriginalFiles(row_in)
        pleaseB, rowB = self.config.HowToValidateAndNormalizeTheFields(rowA)
        pleaseC, rowC = self.config.HowToDeriveNewFields(rowB)
        return pleaseA and pleaseB and pleaseC, rowC
        
#===============================================================================
# Pass2
#===============================================================================
class Pass2(Row):
    
    def __init__(self, config):
        self.config = config        
        Row.__init__(self)
            
    def query(self, row_in):
        pleaseA, rowA = self.config.HowToCollapseOnFields(row_in)
        pleaseB, rowB = self.config.HowToSelectTheRows(rowA)
        return pleaseA and pleaseB, rowB
        
#===============================================================================
# Pass4
#===============================================================================
class Pass4(Row):
    
    def __init__(self, config):
        self.config = config        
        Row.__init__(self)
            
    def query(self, row_in):
        pleaseA, rowA = self.config.HowToFinallyModifyCertainFields(row_in)
        return pleaseA, rowA

