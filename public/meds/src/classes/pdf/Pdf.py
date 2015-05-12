'''
    Pdf
'''

import os, sys
import time
from datetime import datetime, tzinfo

#===============================================================================
# Pdf
#===============================================================================
class Pdf():

    #===========================================================================
    # constructor
    #===========================================================================
    def __init__(self):
        return None
    
    def createPdfFile(self,
        folder_2014,
        report_type,
        orientationLandscape,
        tocHeading,
        isHeroku,
        camperid, day, page
        ):
            
        # create a footer
        if False:
            path_to_input_csv = (
                foldername + '../../../in/Med_Schedule_Items.csv')
            epochtime = os.path.getmtime(path_to_input_csv)
            struct_time = time.localtime(epochtime)
            
            datetime_of_database = datetime.fromtimestamp(epochtime)
            warning = (
                '"The instructions on this page are based upon the medication database dated ' +
                datetime_of_database.strftime("%A %B %d, %Y")+
                #str(struct_time.tm_mon) + '/' + str(struct_time.tm_mday) + '/' + str(struct_time.tm_year) + 
                '"')
            footer = (
                ' '+    
                '--footer-font-name Arial'  +' '+
                '--footer-font-size 10'     +' '+
                '--footer-center ' + warning  +' '+
                '--footer-line'             +' '+
                '--footer-spacing 0'        +' '+
                ''
            )

        # folder_2014   is "/meds/out/2014"
        # printall_file is "/meds/out/2014/printit.pdf"
        # report_type   is "Master-Schedule"
        #folder_2014 = os.path.dirname(os.path.dirname(foldername))
        printall_file = folder_2014 + '/printit.pdf'
        #report_type = os.path.basename(os.path.dirname(foldername))
        #report_type = '*'        
        
        if orientationLandscape: orientation = " --orientation Landscape "
        else:                    orientation = " --orientation Portrait "
        
        options = (
            orientation +
            '--page-size Letter --margin-bottom 0mm --quiet'+' '+
            ''
        )
        
        
        toc = (
            ' toc --enable-toc-back-links --toc-level-indentation 1em ' +
            '--toc-header-text "' + tocHeading + '" ' + 
            ''
        )
        toc1 = (
            ' toc --toc-l1-indentation 1 ' +
            '--toc-header-text "' + tocHeading + '" ' + 
            ''
        )
       
        if camperid=="all":
            include_camperid = ""
        else:
            include_camperid = "-" + camperid + "-*"
            
        if day=="all":
            include_day = ""
        else:
            include_day = "-" + day + "-*"

        if page=="all":
            include_page = ""
        else:
            include_page = "pg-" + page + "*"

        if camperid!="all" or day!="all" or page!="all":
            toc = ''
            
        files_to_include = "*" + include_camperid + include_day + include_page + ".html"

        # return how many html files will be included in the single PDF file
        import subprocess
        html_folder = folder_2014 + "/" + report_type + '/html'
        cmd = "find " + html_folder + ' -name "' + files_to_include + '" | wc --lines '   
        # find /working/rails/special-camp/public/meds/out/2014/Meds-Administered-By-HS/html -name "*-516-*-tue-*.html"     
        direct_output = subprocess.check_output(cmd, shell=True)
        remove_slash_n = direct_output[:-1]
        sys.stdout.write(remove_slash_n)
        
        if remove_slash_n == "0":
            return None

        if isHeroku:
            # use the heroku wkhtmltopdf
            wkhtmltopdf = "/app/vendor/bundle/ruby/1.9.1/gems/wkhtmltopdf-heroku-1.0.0/bin/wkhtmltopdf-linux-amd64"
        else:
            # use the local PC wkhtmltopdf
            wkhtmltopdf = "/usr/bin/wkhtmltopdf11.prev"
        command = wkhtmltopdf + options + toc + html_folder + '/' + files_to_include + " " + printall_file
        retvalue = os.system(command)

        return None                      

#/usr/bin/wkhtmltopdf11 --orientation Landscape --page-size Letter --margin-bottom 0mm --quiet 
#    /working/rails/special-camp/public/meds/out/2014/Meds-Administered-By-HS/html/*-516-*-wed-*.html 
#    /working/rails/special-camp/public/meds/out/2014/printit.pdf

#===============================================================================
# main
#===============================================================================
def Titles(report_type):
    titles = dict()
    titles["Master-Schedule" ] = 'Health Supervisor Master Schedule'
    titles["Meds-Administered-By-HS" ] = 'Meds Administered by Health Supervisor'
    titles["Meds-Administered-By-HS-Summarized" ] = 'Care Group Med Schedule for Health Supervisor Administered Meds'
    titles["Meds-Administered-During-LA-Bus-Trip" ] = 'Meds Administered During LA Bus Trip'
    titles["Meds-Administered-In-Cabin" ] = 'Meds Administered by Camper Care Group'
    titles["Guardian-Signature" ] = 'Guardian Signature'
    titles["Leftover-Meds" ] = 'Leftover Meds Receipt Acknowledgment'
    return titles[report_type]
    
if __name__ == '__main__':
    folder_2014 = "out/2015"
    report_type = sys.argv[2]
    
    if report_type == 'all':
        tocHeading = 'Camper Forms'
        report_type = '*'
    else:
        tocHeading = Titles(report_type)
        
    orientationLandscape = True
    if sys.argv[1] == "HEROKU":
        isHeroku = True
    else:
        isHeroku = False
    camperid = sys.argv[3]
    day = sys.argv[4]
    page = sys.argv[5]
        
    pdf = Pdf()    
    pdf.createPdfFile(
        folder_2014,
        report_type,
        orientationLandscape,
        tocHeading,
        isHeroku,
        camperid, day, page)

