'''
    GoChase
'''

import os
import sys
from classes.utils import Container
from classes.report import SpecialCamp
 
#===============================================================================
# GoSpecialCamp
#===============================================================================
class GoSpecialCamp():
        
    def run(self, in_folder, out_folder):
        
        #=======================================================================
        # determine the base folder and clear all outputs
        #=======================================================================
        #Container.TheBaseFolder = Container.BaseFolder(__file__)
        Container.TheBaseFolder = Container.BaseFolder("./public/meds")
        #out_folder = Container.TheBaseFolder.location + "/outIndex"
        print "The out folder is", out_folder
        Container.clearFolder(out_folder)
        
        #=======================================================================
        # select a database and a report type
        #=======================================================================        
        report = SpecialCamp.CamperList(in_folder, out_folder)  
         
#===============================================================================
# entry
#===============================================================================
in_folder = sys.argv[1]
out_folder = sys.argv[2]
print "GoSpecialCamp",in_folder, out_folder
mc = GoSpecialCamp()
mc.run(in_folder, out_folder)
print "DONE"
exit()

