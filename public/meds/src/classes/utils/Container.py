
import sys, csv, os, shutil, collections, re, datetime, string

###############################################################################
# allow access to these internal items
############################################################################### 
__all__ = \
[
    "EquivalenceTree", "EquivalenceTreePrint",
    "MapAccountToEquivalence1", "MapAccountToLevels",
    "Container",
    "Const", "State", "Virtual", "SHOW",
    "KeyedObject",
    "String",
    "List",
    "Map",
    "VectorOfString",
    "EquivClasses",
    "pureVirtual",
    "convertDateWithSlashes",
    "convertDateToYear",
    "convertDateToYearMonth",
    "Colors",
    "RunningTotals",
    "getNegativeAmounts",
    "getFloat", "getFloatNoCommas", "avePerMonth",
    "formatDollars",
    "MonitorField",
    "convertToStandardDate",
    "removeDayFromDate",
    "clearFolder",
    "touchFolder",
    "getPaypalAdjusted",
    "getAsPositive", "dirnameSlash","dirnameNoSlash",
]

Const = None
State = None
Virtual = None
SHOW = True
YEAR_OF_CAMP = '2020'

########################################################################
# clearFolder
########################################################################
class BaseFolder():
             
    # __file__ is the absolute location of this Container.py
    def __init__(self, abs_path_to_file):      
        self.location = (
            os.path.abspath(
                os.path.dirname(
                    os.path.dirname(abs_path_to_file))))
                
TheBaseFolder = None
    
def touchFolder(folder): 
    if not os.access(folder, os.F_OK):
        os.makedirs(folder)

def clearFolder(folder): 
    if os.access(folder, os.F_OK):
        shutil.rmtree(folder)
    touchFolder(folder)
        
def dirnameSlash(fullpath): 
    return os.path.dirname(fullpath)+'/'        
        
def dirnameNoSlash(fullpath): 
    return os.path.dirname(fullpath)     

###############################################################################
# SubsetPath
###############################################################################
class SubsetPath():
             
    def __init__(self):      
        self.subset_path = list()
        self.subset_indices = list()
        self.subset_indent = list()
             
    def push(self, subset_number, subset):      
        self.subset_path.append(subset)
        self.subset_indices.append(subset_number)
        self.subset_indent.append(self.textOfIndices()+' ')
             
    def pop(self):      
        self.subset_path.pop()
        self.subset_indices.pop()
        self.subset_indent.pop()

    def getIndentToIndices(self):
        accum = str()
        size = len(self.subset_indent)
        for i in range(size):
            if i < size-1:
                text = self.subset_indent[i]
                accum += text
        if len(accum) > 0:
            return ' '.ljust(len(accum))
        else:
            return ''

        return ' '.ljust(len(accum))

    def getIndentToElements(self):
        accum = str()
        for text in self.subset_indent:
            accum += text
        return ' '.ljust(len(accum))

    def textOfIndices(self):
        accum = str()
        for i in range(len(self.subset_indices)):
            index = self.subset_indices[i]
            if i < len(self.subset_indices)-1:
                accum += str(index) + '.'            or col['Account'] == 'Faraja Orphans Rescue Ministry'

            else:
                accum += str(index)
        return accum

    def wellOrderedPath(self):
        well_ordering = list()
        for i in range(len(self.subset_path)):
            subset_name = self.subset_path[i].getTitle()
            well_ordering.append(subset_name)
        return well_ordering

    def equals(self, other):
        this_path = self.wellOrderedPath()
        other_path = other.wellOrderedPath()
        return (this_path == other_path)
 
###############################################################################
# EquivalenceTree
#   Elements are organized into multiple equivalence classes. There is exactly
#   one Subset at the top of the tree. Each Subset contains only Subsets
#   except the minimal Subset of each path consists of Elements only. The total
#   number of equivalence subdivisions of the Elements is equal to the height
#   of the tree.
###############################################################################
class EquivalenceTree():
             
    ########################### 
    # private state          
    ########################### 
    def __init__(self, top_level_set):
        self.initialize(top_level_set)

    def initialize(self, top_level_set):      
        self.top = top_level_set
        self.path = SubsetPath()
        self.height = 0
             
    ########################### 
    # private refactor methods
    ########################### 
    def doSomething(self, subset, elements):
        pass
             
    ########################### 
    # private local methods
    ########################### 
    def traverse(self, subset_number, subset):
        self.path.push(subset_number, subset)
        level = len(self.path.subset_indices)
        self.height = max(self.height, level)
        elements = list()

        for i in range(len(subset)):
            next_item_in_subset = subset[i]
            if isinstance(next_item_in_subset, Element):
                elements.append(next_item_in_subset)

        found, value = self.doSomething(subset, elements, level, self.path.subset_path)
        if found: self.value_to_return = value

        for i in range(len(subset)):
            next_item_in_subset = subset[i]
            if isinstance(next_item_in_subset, Subset):
                self.traverse(i+1, next_item_in_subset)

        self.path.pop()
        return self.value_to_return

    ########################### 
    # public local methods
    ########################### 
    def printTree(self):
        self.value_to_return = str('Not Found')
        i = 0
        for item in self.top:
            if isinstance(item, Subset):
                i += 1
                self.traverse(i, item)
                print_it = (
                    'The height of the tree "' + item.getTitle()
                     + '" is ' + str(self.height)
                )
                print print_it

    ########################### 
    # public local methods
    ########################### 
    def getCategory(self, element_name):
        self.value_to_find = element_name
        self.value_to_return = str('Not Found')
        self.traverse(1, self.top)
        return self.value_to_return

    ########################### 
    # public local methods
    ########################### 
    def getLevels(self, element_name):
        self.value_to_find = element_name
        self.value_to_return = ['','','','']
        self.traverse(1, self.top)
        return self.value_to_return

###############################################################################
# EquivalenceTreePrint
###############################################################################
class EquivalenceTreePrint(EquivalenceTree):
             
    ########################### 
    # private state          
    ########################### 
    def __init__(self, top_level_set):
        EquivalenceTree.__init__(self, top_level_set)
             
    ########################### 
    # private virtual methods
    ########################### 
    def doSomething(self, subset, elements, level, path):
        print (
            self.path.getIndentToIndices() +
            self.path.textOfIndices() + " " + 
            subset.getTitle()
        )
        for element in elements:
            print  (
                self.path.getIndentToElements() + 
                element.getTitle()
            )
        return False, str('None')


###############################################################################
# MapAccountToEquivalence1
###############################################################################
class MapAccountToEquivalence1(EquivalenceTree):
             
    ########################### 
    # private state          
    ########################### 
    def __init__(self, top_level_set):
        EquivalenceTree.__init__(self, top_level_set)
             
    ########################### 
    # private virtual methods
    ########################### 
    def doSomething(self, subset, elements, level, path):
        for element in elements:
            if element.getTitle() == self.value_to_find:
                broader = True
                if broader:
                    return True, path[2].getTitle()
                else:
                    return True, subset.getTitle()
        return False, str('Not Found')

###############################################################################
# MapAccountToLevels
###############################################################################
class MapAccountToLevels(EquivalenceTree):
             
    ########################### 
    # private state          
    ########################### 
    def __init__(self, top_level_set):
        EquivalenceTree.__init__(self, top_level_set)
             
    ########################### 
    # private virtual methods
    ########################### 
    def doSomething(self, subset, elements, level, path):
        for element in elements:
            if element.getTitle() == self.value_to_find:
                if len(path) == 4:
                    path_names = [ path[1].getTitle(), path[2].getTitle(), path[3].getTitle() ]
                else:
                    path_names = [ path[1].getTitle(), path[2].getTitle(), '' ]
                return True, path_names
        return False, str('Not Found')

###############################################################################
# pureVirtual
###############################################################################
def pureVirtual():
    print "ERROR: method not implemented"
    raise
def PublicFixed():
    print "ERROR: method not implemented"
    raise
def PublicVirtual():
    print "ERROR: method not implemented"
    raise
def PrivateVirtual():
    print "ERROR: method not implemented"
    raise

###############################################################################
# KeyedObject
###############################################################################
class KeyedObject():

    # state
    key = Const
    obj = Const

    # constructor              
    def __init__(self, key, obj):
        self.key = key
        self.obj = obj
        return None
       
    # method              
    def text(self):
        print "Key:",self.key,"Object:",self.obj
        return None

###############################################################################
# String
###############################################################################
class String():

    line = State
             
    def __init__(self, text=''):
        self.line = text
        return None
                  
    def append(self, other):
        self.line += other
        return None

    def show(self):
        print self.line
        return None

    def removeBlanks(self):
        return string.strip(re.sub('[ \t\n\r\f\v]+', '', self.line))

    def removeBlanksAndSlashes(self):
        return string.strip(re.sub('[/\\\ \t\n\r\f\v]+', '', self.line))

    def repeatCharacter(self, how_many):
        return self.line.rjust(how_many, self.line[0])

    def whiteSpaceToBlank(self):
        return string.strip(re.sub('[ \t\n\r\f\v]+', ' ', self.line))

    def whiteSpaceToBlankAndCapitalize(self):
        return string.strip(re.sub('[ \t\n\r\f\v]+', ' ', self.line)).upper()


    def removeBlanksAndNumbers(self):
        return string.strip(re.sub('[ \t\n\r\f\v0123456789]+', '', self.line))

###############################################################################
# List
###############################################################################
class List(list):
             
    def __init__(self, items=[]):      
        list.__init__(self, items)
        return None

###############################################################################
# Map
###############################################################################
class Map(dict):
             
    def __init__(self, pairs={}):      
        dict.__init__(self, pairs)
        return None

###############################################################################
# Relation
###############################################################################
class Relation(dict):
             
    def __init__(self, key_list={}):      
        dict.__init__(self, key_list)
        return None

    def inverse(self):
        return None

###############################################################################
# VectorOfStrings
###############################################################################
class VectorOfString():
             
    def __init__(self, first_item=None):
        self.vector = list()
        if first_item != None:
            self.append(first_item)
        return None
                  
    def append(self, line):
        self.vector.append(line)
        return None
                  
    def concat(self, other):
        self.vector.extend(other.vector)
        return None
                  
    def show(self):
        for line in self.vector: print line
        return None
                  
    def write(self):
        lines = String()
        for line in self.vector: lines.append(line+'\n')
        return lines.line

###############################################################################
# StoredVectorOfStrings
###############################################################################
class StoredVectorOfStrings():

    # state
    key = Const
    obj = Const

    # constructor              
    def __init__(self, key, obj):
        self.key = key
        self.obj = obj
        return None
       
    # method              
    def text(self):
        print "Key:",self.key,"Object:",self.obj
        return None

###############################################################################
# Container
###############################################################################
class Container():

    # state
    assoc_array = State

    # constructor              
    def __init__(self, pairs=None):
        if pairs == None: 
            self.assoc_array = dict()
        else:
            self.assoc_array = pairs
        return None

    # method              
    def add(self, key, obj=None):
       if isinstance(key, KeyedObject):
           self.assoc_array[key.key] = key.obj
       else:
           self.assoc_array[key] = obj
       return None
       
    # method              
    def get(self, key):
        if self.contains(key):
            return self.assoc_array[key]
        else:
            return self.assoc_array.values()[0]
       
    # method              
    def contains(self, key):
        return key in self.assoc_array
       
    # method              
    def text(self):
        if False: print self.assoc_array.items()
        for next in self.assoc_array:
            print 'NEXT',next
        return None

###############################################################################
# EquivClasses
###############################################################################
class EquivClassesFixedMethods( object ):
    def __init__(self) : object.__init__(self)

    def getAllMembersOf(self, classname) : pureVirtual()
    def getClassName(self, item)         : pureVirtual()

class EquivClassesVirtualMethods( EquivClassesFixedMethods ):
    def __init__(self) : EquivClassesFixedMethods.__init__(self) 
         
    def classNames(self) : pureVirtual()
    def matchesCriteriaOfEquivClass0(self, classname, item1, item2='', item3='') : pureVirtual()

class EquivClasses(EquivClassesVirtualMethods):            
    def __init__(self):
        EquivClassesVirtualMethods.__init__(self)

        self.equiv_class_names = self.classNames()
        pass

    def addElementToClass(self, classname, item):
        self.equiv_classes[classname].add(item)
        return None

    def getAllMembersOf(self, classname):
        return self.equiv_classes[classname]

    def getClassNameOfWAS(self, item):
        for classname in self.equiv_class_names:
            if item in self.getAllMembersOf(classname):
                return classname
        return 'UNCLASSIFIED'

    def text(self):
        for classname in self.equiv_class_names:
            print "CLASS:", classname
            for item in self.getAllMembersOf(classname):
                print "    ", self.getClassName(item), item
        return NonegetAsPositive

    def classify(self, original_set):
        self.original_set = original_set
        self.equiv_classes = dict()

        for classname in self.equiv_class_names:
            self.equiv_classes[classname] = set()

        for item in self.original_set:
            found = False
            for classname in self.equiv_class_names:
                if self.matchesCriteriaOfEquivClass(classname, item):
                    self.addElementToClass(classname, item)
                    found = True
                    break
            if not found: self.addElementToClass('UNCLASSIFIED', item)
        return None

    def getClassName(self, item1, item2='', item3=''):
        for classname in self.equiv_class_names:
            found, title = self.matchesCriteriaOfEquivClass(classname, item1, item2, item3)
            if found: return title
        return 'UNKNOWN MECHANISM'

    def getMechanismName(self, item1, item2='', item3=''):
        classname = self.getClassName(item1, item2, item3)
        out = re.sub(' \(credit\)','', classname)
        out = re.sub(' \(debit\)','', out)
        return out

    def matchesLeadingText(self, set_of_patterns, item):
        for pattern in set_of_patterns:
            find_pattern = '^' +pattern+ '+'
            if re.match(find_pattern, item): return True
        return False

    def matchesExactly(self, set_of_patterns, item):
        for pattern in set_of_patterns:
            find_pattern = '^' +pattern+ '$'
            if re.match(find_pattern, item): return True
        return False

    def matchesSomewhere(self, set_of_patterns, item):
        for pattern in set_of_patterns:
            find_pattern = '.*' +pattern+ '.*'
            if re.match(find_pattern, item): return True
        return False

###############################################################################
# RunningTotals
###############################################################################
class RunningTotals():
             
    # public
    def __init__(self, beginning_balance = 0.0):
        self.count_transactions = 0
        self.count_section_transactions = 0
        self.running_total = beginning_balance     
        self.section_total = 0
        self.section_credit = 0
        self.section_debit = 0
        pass

    # public
    def accumulate(self, amount, field_has_changed):
        self.count_transactions += 1      
        self.accumulateRunning(amount)
        self.accumulateSection(amount, field_has_changed)
        self.accumulateCredit(amount, field_has_changed)
        self.accumulateDebit(amount, field_has_changed)
        return None

    # public
    def getNumberTransactions(self):
        if False:
            return str(self.count_section_transactions) # if section total
        else:
            return str(self.count_transactions)         # if grand total

    # public
    def getRunningTotal(self):
        return formatDollars(self.running_total) # if grand total
        return formatDollars(self.section_total) # if section total

    # public
    def getSection(self):
        return formatDollars(self.section_total)

    # publicgetAsPositive
    def getCredit(self):
        return formatDollars(self.section_credit)

    # public
    def getDebit(self):
        return formatDollars(self.section_debit)

    # private
    def accumulateRunning(self, amount):
        self.running_total += getFloatNoCommas(amount) 
        return None

    # private
    def accumulateSection(self, amount, field_has_changed):
        if field_has_changed:
            self.section_total = getFloatNoCommas(amount)
            self.count_section_transactions = 1
        else:
            self.section_total += getFloatNoCommas(amount) 
            self.count_section_transactions += 1      
        return None

    # private
    def accumulateCredit(self, amount, field_has_changed):
        money = getFloatNoCommas(amount)
        if field_has_changed:
            if money >= 0.0: self.section_credit = money
            else:            self.section_credit = 0.0
        else:
            if money >= 0.0: self.section_credit += money
        return None

    # private
    def accumulateDebit(self, amount, field_has_changed):
        money = getFloatNoCommas(amount)
        if field_has_changed:
            if money < 0.0: self.section_debit = money
            else:           self.section_debit = 0.0
        else:
            if money < 0.0: self.section_debit += money
        return None

###############################################################################
# MonitorField
###############################################################################
class MonitorField():

    def __init__(self):
        self.first_time = True
        self.prev_fields = dict()
        self.new_fields = dict()
        pass

    def slideFieldValues(self, row):
        if self.first_time:
            self.first_time = False
            self.prev_fields = self.new_fields = row
            return None
        else:
            self.prev_fields = self.new_fields
            self.new_fields = row
            return None
 
    def fieldHasChanged(self, list_of_fields):
        for field in list_of_fields:
            if field in self.prev_fields.keys():
                if (self.prev_fields[field] != self.new_fields[field]):
                    return True
        return False

###############################################################################
# Useful functions
###############################################################################

def convertDateWithSlashes(date):
    mon_day_year = date.split('/')
    split_date = map(int, mon_day_year)
    out = datetime.date(
        split_date[2], split_date[0], split_date[1])
    return str(out)

# date style is "11/25/2012"
def convertDateWithSlashes1(date):
    mon_day_year = date.split('/')
    split_date = map(int, mon_day_year)
    out = datetime.date(
        split_date[2], split_date[0], split_date[1])
    return str(out)

def convertDateToYear(date):
    mon_day_year = date.split('/')
    split_date = map(int, mon_day_year)
    year_mon_day = datetime.date(
        split_date[2], split_date[0], split_date[1])
    return year_mon_day.strftime("%Y")

def convertStandardDateToYear(date):
    year_mon_day = date.split('-')
    split_date = map(int, year_mon_day)
    out = datetime.date(
        split_date[0], split_date[1], split_date[2])
    return out.strftime("%Y")

def convertStandardDateToYearMonth(date):
    year_mon_day = date.split('-')
    split_date = map(int, year_mon_day)
    out = datetime.date(
        split_date[0], split_date[1], split_date[2])
    return out.strftime("%Y-%m")

def convertDateToYearMonth(date):
    mon_day_year = date.split('/')
    split_date = map(int, mon_day_year)
    year_mon_day = datetime.date(
        split_date[2], split_date[0], split_date[1])
    return year_mon_day.strftime("%Y-%m")

def removeDayFromDate(date):
    day_mon_yr = date.split(' ')
    split_date = map(str, day_mon_yr)
    return list([split_date[1], split_date[2]])

def convertToStandardDate(date):
    year_mon_day = date.split('-')
    split_date = map(int, year_mon_day)
    standard = datetime.date(
        split_date[0], split_date[1], split_date[2])
    return standard.strftime("%d %b %Y")

class Colors():
    def __init__(self):
        self.first_time_color = True
        
    def getCyclicColors(self):
        if self.first_time_color:
            self.first_time_color = False
            self.colors = list()
            self.colors.append('#FEF1B5') # yellow
            self.colors.append('#EED2EE') # purple
            self.colors.append('#DAF4F0') # bluish
            self.colors.append('#FFDAB9') # orange-brown
            self.colors.append('#E6E6FA') # purple-blue
            self.colors.append('#CCFFCC') # green
    
            self.colors.append('#FEF1B5') # yellow
            self.colors.append('#EED2EE') # purple
            self.colors.append('#DAF4F0') # bluish
            self.colors.append('#FFDAB9') # orange-brown
            self.colors.append('#E6E6FA') # purple-blue
            self.colors.append('#CCFFCC') # green
            self.colors.append('lightpink')
            self.which_color = len(self.colors)-1
        self.which_color += 1
        self.which_color %= len(self.colors)
        return self.colors[self.which_color]

def getNegativeAmounts(amount_text):
    out = re.sub('\)$','', amount_text)
    out = re.sub('^\(','-', out)
    return out

def getAsPositive(amount_text):
    #out = re.sub('\)$','', amount_text) # convert (amount_text) to amount_text
    #out = re.sub('^\(','', out)
    out = re.sub('[\(\)-]','', amount_text)
    return out

def getFloat(amount_text):
    out = re.sub('\)$','', amount_text)
    out = re.sub('^\(','-', out)
    out = re.sub(',','', out)
    return float(out)

def getFloatNoCommas(amount_text):
    if amount_text == '&nbsp;' or amount_text == '':
        return float(0.0)
    out = re.sub('\)$','', amount_text) # convert (amount_text) to -amount_text
    out = re.sub('^\(','-', out)
    out = re.sub(',','', out)           # remove commas
    return float(out)

def formatDollars(amount):
    return "{:,.2f}".format(amount)

def avePerMonth(amount_text):
    annual_total = getFloatNoCommas(amount_text)
    ave_per_month = annual_total/12.0
    return formatDollars(ave_per_month)

def getPaypalAdjusted(amount_text, is_usa_payment=True):
    if is_usa_payment:
        # 2.9% plus $0.30
        rate = 0.029
        offset = 0.3
    else:
        # 3.9% plus $0.30
        rate = 0.039
        offset = 0.3
    net = getFloatNoCommas(amount_text)
    orig = (net+offset)/(1-rate)
    return formatDollars(orig)


