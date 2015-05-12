from __future__ import print_function

'''
   namespace TreeCreator
      class Element
      class Subset
      class InclusionPath
      class InclusionPaths
      class TreeCreator
      class TreeBeyondBanking


   The set theoretic tree consists of subsets and elements. A subset
   contains subsets and elements. Each subset has a title and each
   element has a title. The element is a non-trivial class object and
   is refactored.
'''

import os, re, collections
from utils.Container import *

__all__ = [ "TreeCreator",
]

########################################################################
# Element
########################################################################
class Element(object):
             
    def __init__(self, title):      
        object.__init__(self)
        self.title = title
        pass

    def getTitle(self):      
        return self.title

###############################################################################
# Subset - a Subset is a Python list of types Subset or Element
###############################################################################
class Subset():
             
    def __init__(self, title_of_subset):      
        self.title = title_of_subset
        self.subset = list()
             
    def __len__(self):
        return len(self.subset)     
             
    def __getitem__(self, index):
        return self.subset[index]     
            
    def append(self, item):      
        if (isinstance(item, Subset)
        or  isinstance(item, Element)):
            self.subset.append(item)
        else:
            raise str('Object must be a Subset or an Element')
             
    def getTitle(self):      
        return self.title

    def containsSubsetNamed(self, name):
        for item in self.subset:
            if (isinstance(item, Subset)):
                if item.getTitle() == name: return True, item
        return False, self.subset


###############################################################################
# InclusionPath
###############################################################################
class InclusionPath():
             
    def __init__(self, well_ordered_list=list()):
        self.well_ordered_list = well_ordered_list[:] # not shallow copy

    def pushback(self, subset):
        if (not isinstance(subset, Subset)):
            raise BaseException('Subset expected')
        self.well_ordered_list.append(subset)

    def pop(self):
        self.well_ordered_list.pop()

    def getListOfSubsets(self):
        return self.well_ordered_list

    def __eq__(self, other):

        show = False
        if (self.well_ordered_list == other.well_ordered_list):
            if show: print("Well Ordered Lists Match")
            return True
        else:
            if show: print("Well Ordered Lists Do Not Match")
            return False

    def __contains__(self, other):
        show = False
        size_other = len(other.well_ordered_list)
        if (other.well_ordered_list == self.well_ordered_list[0:size_other]):
            if show: print("Well Ordered List Is Subset")
            return True
        else:
            if show: print("Well Ordered List Is Not Subset")
            return False

###############################################################################
# InclusionPaths
###############################################################################
class InclusionPaths():
             
    def __init__(self):      
        self.paths = list()
        self.mapElementToPath = dict()

    def pushback(self, title_of_element, inclusion_path):
        if (not isinstance(inclusion_path, InclusionPath)):
            raise str('Object must be a Subset or an Element')

        self.paths.append(inclusion_path)
        self.mapElementToPath[title_of_element] = inclusion_path

    def front(self):
        return self.paths[0]

    def back(self):
        return self.paths[-1]

    def __getitem__(self, index):
        return self.paths[index]

    def __len__(self):
        return len(self.paths)

###############################
# Categories.Base  
###############################
class Base():

    ########################### 
    # public constructor          
    ###########################
    def __init__(self, name_of_tree):
        self.initialize(name_of_tree)

    ########################### 
    # private state          
    ###########################
    def initialize(self, name_of_tree):

        # simple data
        self.where_base = 'ftp://kmwegner:unicorn7@upload.comcast.net/finance/'
        self.where_base = './'

        # the maximal subset is the base node of the tree
        # establish nesting of Subsets and Elements
        self.maximal_subset = Subset(name_of_tree)
        self.configureEquivalenceTree(self.maximal_subset)

        # traverse the tree to create conveniences
        self.equiv_class_names = list()
        self.equiv_class_names.append(list()) # level 0 subsets
        self.equiv_class_names.append(list()) # level 1 subsets
        self.equiv_class_names.append(list()) # level 2 subsets
        for subset in self.maximal_subset:
            if isinstance(subset, Subset):

                # element_paths is a map indexed by account title
                # it maps an account to an InclusionPath
                # an InclusionPath is a list of Subsets leading to Elements
                self.element_paths = InclusionPaths()

                # equiv_class_names[i] is a list of Subset titles at level i
                self.equiv_class_names[0].append(subset.getTitle())

                self.current_path = InclusionPath()
                self.traverse(0, subset)

    ########################### 
    # private local methods
    ########################### 
    def getAllPaths(self, element_paths):
        all_paths = list() # of titles

        for key in element_paths.mapElementToPath.keys():

            temp1 = element_paths.mapElementToPath[key].getListOfSubsets()
            fullpath1 = [subset.getTitle() for subset in temp1[:]]
            if len(fullpath1) == 3:
                if fullpath1[0:2] not in all_paths: all_paths.append(fullpath1[0:2])
            if fullpath1 not in all_paths: all_paths.append(fullpath1)
            temp2 = element_paths.mapElementToPath[key].getListOfSubsets()
            fullpath2 = [subset.getTitle() for subset in temp2[:]]
            fullpath2.append(key)
            fullpath2.append('ELEMENT')
            if fullpath2 not in all_paths: all_paths.append(fullpath2)

        all_paths.sort()
        return all_paths


    def determinePathsOfLength(self, element_paths):
        all_paths = list([
            path.getList() for path in element_paths.mapElementToPath.values() ])
        
        paths_of_length_2 = list()
        paths_of_length_3 = list()

        for key in element_paths.mapElementToPath.keys():
            copy_of_path = InclusionPath(element_paths.mapElementToPath[key].getList())
            path = list(copy_of_path.getList())
            path.append(key)
            truncate = path[0:2+1]
            if len(path) >= 2+1 and truncate not in paths_of_length_2:
                paths_of_length_2.append(truncate)
            if len(path) == 3+1 and path not in paths_of_length_3:
                paths_of_length_3.append(path)

        paths_of_length_2.sort()
        paths_of_length_3.sort()
        return paths_of_length_2, paths_of_length_3
                            
    def traverse(self, level, current_subset):
        # extend the current path
        self.current_path.pushback(current_subset)
        if False:
            blanks = String(' ').repeatCharacter(3*level)
            print(blanks, current_subset.getTitle())

        # determine the subsets and the elements in current subset
        subsets = list()
        elements = list()
        for subset_or_element in current_subset:
            if isinstance(subset_or_element, Element):
                elements.append(subset_or_element) # simple list of all elements
            if isinstance(subset_or_element, Subset):
                subsets.append(subset_or_element) # simple list of all subsets

        ##########################################################
        # The purpose of "traverse" is to create the set of paths
        # from max subset to leaf subset including each element
        ##########################################################
        for element in elements:
            copy_of_path = InclusionPath(self.current_path.getListOfSubsets())

            # change this to push an element object that can have useful
            # methods
            self.element_paths.pushback(element.getTitle(), copy_of_path)
            if False:
                blanks = String(' ').repeatCharacter((3*level)+3)
                print(blanks, element.getTitle())

        for subset in subsets:
            self.equiv_class_names[level+1].append(subset.getTitle())
            self.traverse(level+1, subset)

        self.current_path.pop()
        return None

    ########################### 
    # private local methods
    ########################### 
    def htmlContentsBegin(self):
        return (
'''
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">

<!---------------->
<!--   Styles   -->
<!---------------->
<html>
<head>
   <title>Cash Flow</title>
   <style type="text/css">
    
   p {
   font-family:Verdana, Geneva, sans-serif;
   color:black;
   font-size:1.0em;
   text-align:left;
   margin-left:0px;
   line-height:130%;
   font-weight:bold;
   } 

   a {
   white-space:pre;
   text-decoration:none;
   }

   a.MainAccount
   {
   color:brown;
   }

   a.category
   {
   color:blue;
   }

   a.subcategory
   {

   color:red;
   }

   a.element
   {
   color:green;
   }

   a.account
   {
   color:green;
   }

    </style>
</head>

<!----------------->
<!-- Top of Page -->
<!----------------->
<body style="font-size:14px; line-height:14px;">
<br/>
<hr>
<br/>

<!---------------->
<!-- Discussion -->
<!---------------->
<p style="line-height:50%;">
   <font style="color:black;font-size:1.1em;text-decoration:underline;">
      Cash Flow Report:
   </font>
</p>
<p style="margin-left:50px;">
   <font style="color:brown;">
      Brown indicates a monthly report of all transactions<br/>
   </font>
   <font style="color:blue;">
      Blue indicates a monthly report of those transactions related to the selected category<br/>
   </font>
   <font style="color:red;">
      Red indicates a monthly report of those transactions related to the selected sub-category<br/>
   </font>
   <font style="color:green;">
      Green indicates a yearly report of those transactions related to a particular account<br/>
   </font>
</p>


<br/>

<!---------------->
<!--   Links    -->
<!---------------->
<p style="line-height:50%;">
   <font style="color:black;font-size:1.1em; text-align:left; text-decoration:underline;">
      Merrill Lynch Beyond Banking:
   </font>
</p>
<p>
'''
    #+ '<a class=MainAccount href="'+self.where_base+'All-Monthly.html">          Beyond Banking</a><br/>')
    + '<a class=MainAccount href="'
    #+ '/working/python/db/out/beyond_banking/ordering_sections/Date_'+self.cont_year_month+'/presentation/Standard/Presentation.html">          Beyond Banking</a><br/>')
    + 'Date-'+self.top_year_month+'.html">          Beyond Banking</a><br/>')

    def getHref(self, a_class, dirname, basename, title):
        a_tag = (
            '   <a class=' + a_class +
            
                ' href="file://' + dirname + '/' + basename +
                ' href=./' + basename +
                ' href=' + basename +
                ' href="' + self.where_base + basename +
                '.html">'+title+'</a><br/>'
        )
        a_tag = (
            '   <a class=' + a_class +     
                ' href=' + basename +
                '">'+title+'</a><br/>'
        )
        return a_tag

    def filenameToUbuntuOne(self):
        translate = dict({
            'Account-Continuous' : 'UBUNTU',
                 'Account-Month' : 'UBUNTU',
                  'Account-Year' : 'UBUNTU',
           'Category-Continuous' : 'UBUNTU',
                'Category-Month' : 'UBUNTU',
                 'Category-Year' : 'UBUNTU',
            'CONTENTS-Continuous' : 'UBUNTU',
                 'CONTENTS-Month' : 'UBUNTU',
                  'CONTENTS-Year' : 'UBUNTU',
               'Date-Continuous' : 'UBUNTU',
                    'Date-Month' : 'UBUNTU',
                     'Date-Year' : 'UBUNTU',
        'Subcategory-Continuous' : 'UBUNTU',
             'Subcategory-Month' : 'UBUNTU',
              'Subcategory-Year' : 'UBUNTU'
        })

    def filenameToUbuntuOne(self, html_filename):
        translate = dict({
            'Account-Continuous' : 'http://ubuntuone.com/5oYPMVwOHuIjkRwjplYV2F',
                 'Account-Month' : 'http://ubuntuone.com/0ufEPCIAUmONbGnwcXcuW8',
                  'Account-Year' : 'http://ubuntuone.com/6dQPL27Cr0kqIeuGUj57pR',
           'Category-Continuous' : 'http://ubuntuone.com/2zzB9TjflXZiFArELsZeeX',
                'Category-Month' : 'http://ubuntuone.com/6wnVya83FhcaaFfXMC46fG',
                 'Category-Year' : 'http://ubuntuone.com/1PRkXtOuoQWxR7seCM3ARK',
            'CONTENTS-Continuous' : 'http://ubuntuone.com/2GCEBCF9UIg4DkFuymzvUK',
                 'CONTENTS-Month' : 'http://ubuntuone.com/1QXe90HHTnHG752gptnnuz',
                  'CONTENTS-Year' : 'http://ubuntuone.com/7RhWcZA9sS2mrGHXq32bHU',
               'Date-Continuous' : 'http://ubuntuone.com/4IICdNOcfXjPOrcvXkqKcz',
                    'Date-Month' : 'http://ubuntuone.com/71zD8cMLwIXhMlDzq5Y4gU',
                     'Date-Year' : 'http://ubuntuone.com/0bVdVIqhr5MnSSIpEsIoOd',
        'Subcategory-Continuous' : 'http://ubuntuone.com/1dWICJHbTZcalkxtCRofIw',
             'Subcategory-Month' : 'http://ubuntuone.com/027EwFkaDLwr5nPhOgsDxM',
              'Subcategory-Year' : 'http://ubuntuone.com/0MNj2rOAmRHsid54bQxLCP'
        }) 
        return translate[os.path.splitext(html_filename)[0]]   
        
    def htmlContentsMiddle(self):
        dirname = '/working/python7/records/out/html/Finance'
        dirname = '/working/python7/db/out/beyond_banking/html'
        hrefs = list()
        structure = self.getAllPaths(self.element_paths)
        initial_indent = 15
        subsequent_indent = 6

        for path in structure:
            is_element = (path[-1] == 'ELEMENT')
            is_subset  = (path[-1] != 'ELEMENT')
            is_subcategory = (is_subset and len(path) > 2)
            is_category = (is_subset and not is_subcategory)

            if is_element:
                number_indents = len(path)-2
                number_indents = 2
            elif is_category:
                number_indents = 0
            elif is_subcategory:
                number_indents = 1

            number_blanks = initial_indent + (number_indents*subsequent_indent)
            blanks = String(' ').repeatCharacter(number_blanks)

            if is_subcategory:
                #basename = String(path[1]+'-'+path[2]).removeBlanksAndSlashes()
                #basename = 'Subcategory-Monthly-'+String(path[1]+'-'+path[2]).removeBlanksAndSlashes()
                #basename = 'Subcategory-'+self.cont_year_month+'-'+String(path[1]+'-'+path[2]).removeBlanksAndSlashes()
                
                flname = 'Subcategory-'+self.subcategory_year_month
                if False: flname = self.filenameToUbuntuOne(flname)
                if not self.split_into_separate_files:
                    basename = flname+'.html'+'#'+String(path[1]+'-'+path[2]).removeBlanksAndSlashes()
                else:
                    basename = flname+'-'+String(path[1]+'-'+path[2]).removeBlanksAndSlashes()+'.html'
                
                title = blanks+path[2]
                href = self.getHref('subcategory', dirname, basename, title)
                hrefs.append(href)
                
            elif is_category:
                #basename = String(path[1]).removeBlanksAndSlashes()
                #basename = 'Category-Monthly-'+String(path[1]).removeBlanksAndSlashes()
                #basename = 'Category-'+self.cont_year_month+'-'+String(path[1]).removeBlanksAndSlashes()
                
                flname = 'Category-'+self.category_year_month
                if False: flname = self.filenameToUbuntuOne(flname)
                if not self.split_into_separate_files:
                    basename = flname+'.html'+'#'+String(path[1]).removeBlanksAndSlashes()
                else:
                    basename = flname+'-'+String(path[1]).removeBlanksAndSlashes()+'.html'
                
                title = blanks+path[1]
                href = self.getHref('category', dirname, basename, title)
                hrefs.append(href)
                
            elif is_element:
                #basename = 'Account-'+String(path[-2]).removeBlanksAndSlashes()
                #basename = 'Account-Yearly-'+String(path[-2]).removeBlanksAndSlashes()
                #basename = 'Account-'+self.cont_year_month+'-'+String(path[-2]).removeBlanksAndSlashes()
                
                flname = 'Account-'+self.account_year_month
                if False: flname = self.filenameToUbuntuOne(flname)
                if not self.split_into_separate_files:
                    basename = flname+'.html'+'#'+String(path[-2]).removeBlanksAndSlashes()
                else:
                    basename = flname+'-'+String(path[-2]).removeBlanksAndSlashes()+'.html'
                
                title = blanks+path[-2]
                href = self.getHref('element', dirname, basename, title)
                hrefs.append(href)
                
            else:
                print("ERROR IN htmlContentsMiddle")
        return hrefs
        return (
'''
   <a href="HouseExpense.html">HouseExpense</a><br/>
   <a href="file:///working/python7/records/out/html/Finance/HouseExpense.html">HouseExpense</a><br/>
   <a href="file:///working/python7/records/out/html/Finance/Income.html">Income</a><br/>
   <a href="file:///working/python7/records/out/html/Finance/Income.html">Income</a><br/>
'''
        )

    def htmlContentsEnd(self):
        return (
'''
</p>

<!-------------------->
<!-- Bottom of Page -->
<!-------------------->
<br/>
<hr>
<br/>
</body>
</html>
''')

    ######################################################### 
    # private final method introduced here
    # all successor classes should not re-implement
    ######################################################### 
    def insertElementsIntoMinimalSubset(self,
            path_to_minimal_subset, elements_to_insert):

        prev_subset = self.maximal_subset
        for subset_name in path_to_minimal_subset:
            found, existing_subset = prev_subset.containsSubsetNamed(subset_name)
            if found:
                prev_subset = existing_subset
            else:
                new_subset = Subset(subset_name)
                prev_subset.append(new_subset)
                prev_subset = new_subset
        for element_name in elements_to_insert:
            prev_subset.append(Element(element_name))

    ######################################################### 
    # private refactor method introduced here
    # immediate successor classes should implement (or propogate)
    ######################################################### 
    def configureEquivalenceTree(self, maximal_subset):
        raise BaseException('configureEquivalenceTree is pure virtual here')

    ################################################ 
    # public final protected methods introduced here
    ################################################ 
    def getNameOfTree(self):
        return self.maximal_subset.getTitle()

    def getMaximalSubsetsAtLevel0(self):
        return self.equiv_class_names[0]

    def mapAccountToInclusionPath(self, account_title):
        titles = [subset.getTitle() for subset in 
            self.element_paths.mapElementToPath[account_title].getListOfSubsets()]
        return titles

    def mapAccountToCategory(self, account_title):
        if not account_title in self.element_paths.mapElementToPath.keys():
            return "CATEGORY NOT FOUND"
        titles = [subset.getTitle() for subset in 
            self.element_paths.mapElementToPath[account_title].getListOfSubsets()]
        return titles[1]

    def mapAccountToSubcategory(self, account_title):
        if not account_title in self.element_paths.mapElementToPath.keys():
            return "SUBCATEGORY NOT FOUND"
        titles = [subset.getTitle() for subset in 
            self.element_paths.mapElementToPath[account_title].getListOfSubsets()]
        if len(titles) > 2: return titles[2]
        else: return ''

    def equivClassTitlesAtLevel(self, level):
        return self.equiv_class_names[level]

    def pathsOfLength(self, size):
        if size == 2: return self.paths_of_length_2
        if size == 3: return self.paths_of_length_3

    def getStructure(self):
        structure = self.pathsOfLength(2)
        structure.extend(self.pathsOfLength(3))
        structure.sort()
        return structure

    def createTableContents(self, 
        folder_html,
        top_year_month, 
        category_year_month, 
        subcategory_year_month, 
        account_year_month, 
        split_into_separate_files):
        
        self.folder_html = folder_html
        self.top_year_month = top_year_month
        self.category_year_month = category_year_month
        self.subcategory_year_month = subcategory_year_month
        self.account_year_month = account_year_month
        self.split_into_separate_files = split_into_separate_files
        
        touchFolder(folder_html)
        fullpath = folder_html + '/CONTENTS-'+self.top_year_month+'.html'
        print(self.htmlContentsBegin(),  file=open(fullpath, 'wb'))
        for href in self.htmlContentsMiddle():
            print(href, file=open(fullpath, 'ab'))
        print(self.htmlContentsEnd(),    file=open(fullpath, 'ab'))

    def getAllElementTitles(self):
        all_element_titles = list([ 
            element_title for element_title in self.element_paths.mapElementToPath.keys() 
        ])
        all_element_titles.sort()
        return all_element_titles



