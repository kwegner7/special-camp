'''
    class Html
'''

import sys, os, re, collections
from Container import *

########################################################################
# Style
########################################################################
class Style(Container):

    # constructor              
    def __init__(self, pairs):
        Container.__init__(self, pairs)
        return None
        
    def style(self):
        lines = VectorOfString()
        for next in self.assoc_array.keys():
            lines.append('   '+next+':'+self.get(next)+';')
        return lines

    def applyStyle(self, tag, tablename):
        text = VectorOfString()
        text.append('#'+tablename+' '+tag)
        text.append('{')
        text.concat(self.style())
        text.append('}')
        return text.write()


'''
    WEB-SAFE FONTS:

        font-family: Arial, Helvetica, sans-serif;
        font-family: 'Arial Black', Gadget, sans-serif;
        font-family: 'Bookman Old Style', serif;
        font-family: 'Comic Sans MS', cursive;
        font-family: Courier, monospace;
        font-family: 'Courier New', Courier, monospace;
        font-family: Garamond, serif;
        font-family: Georgia, serif;
        font-family: Impact, Charcoal, sans-serif;
        font-family: 'Lucida Console', Monaco, monospace;
        font-family: 'Lucida Sans Unicode', 'Lucida Grande', sans-serif;
        font-family: 'MS Sans Serif', Geneva, sans-serif;
        font-family: 'MS Serif', 'New York', sans-serif;
        font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, serif;
        font-family: Symbol, sans-serif;
        font-family: Tahoma, Geneva, sans-serif;
        font-family: 'Times New Roman', Times, serif;
        font-family: 'Trebuchet MS', Helvetica, sans-serif;
        font-family: Verdana, Geneva, sans-serif;
        font-family: Webdings, sans-serif;
        font-family: Wingdings, 'Zapf Dingbats', sans-serif;
'''
             
