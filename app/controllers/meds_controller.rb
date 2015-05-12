#---------------------------------------------------------------------------
# CONTROL
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# MODEL
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# VIEW
#---------------------------------------------------------------------------

class MedsController < ApplicationController

=begin
    #---------------------------------------------------------------------------
    # Examples of HTTP authentication
    #---------------------------------------------------------------------------
    http_basic_authenticate_with :name => "special", :password => "camp"
    http_basic_authenticate_with :name => "special", :password => "camFile.file?('image.jpg')p", :except => [:printform, :printRemote, :checkPasswordEnteredByUser]

    #---------------------------------------------------------------------------
    # Suppose you want to render a view called 'edit'
    #---------------------------------------------------------------------------
      render :edit
      render :action => :edit
      render 'edit'
      render 'edit.html.erb'
      render :action => 'edit'
      render :action => 'edit.html.erb'
      render 'books/edit'
      render 'books/edit.html.erb'
      render :template => 'books/edit'
      render :template => 'books/edit.html.erb'
      render '/path/to/rails/app/views/books/edit'
      render '/path/to/rails/app/views/books/edit.html.erb'
      render :file => '/path/to/rails/app/views/books/edit'
      render :file => '/path/to/rails/app/views/books/edit.html.erb'
=end
        
################################################################################
#
# MODEL
#    specialCampTime - extract info from database, get latest time changed
#    databaseHasChanged - extract info from database, has database been modified?
#    databaseReloaded - extract info from database, if changed, then reload
#                       and rewrite the main menu html file
#    createHtmlPages - extract info from database, using printform parameters
#                      to produce a PDF
#
################################################################################

#-------------------------------------------------------------------------------
# specialCampTime
#-------------------------------------------------------------------------------
def specialCampTime(qbc)
  require 'QuickBaseClient'
  millisecs = qbc.lastModifiedTime
  secs = millisecs.to_i/1000
  time_of_modify = Time.at(secs)
  time_california = time_of_modify.getlocal("-08:00")
  return millisecs, time_california.strftime("%Y-%m-%d %I:%M %P PDT") 
end


#-----------------------------------------------------------------------------
# mainMenuExists
#-----------------------------------------------------------------------------
def mainMenuExists()
  if File.file?("./public/meds/outIndex/CamperList/index.html")
  then
    puts "THE FILE ./public/meds/outIndex/CamperList/index.html EXISTS"
    return true
  else
    puts "THE FILE ./public/meds/outIndex/CamperList/index.html DOES NOT EXIST"
    return false
  end
end


#-----------------------------------------------------------------------------
# databaseHasChanged
#-----------------------------------------------------------------------------
def databaseHasChanged(qbc, input_folder, year)
  require 'QuickBaseClient'
  
  timestamp_file = input_folder + "timestamp.txt"

  # Camper table ID:  bid3d66xd
  # Meds table ID:  bid3d67wj
  # Med Schedule Items table ID 2014: bid3d67wn
  
  # determine the id of each database table
  qb_apptoken = "rabajzbsx3v5nb3rki6udbnccbb"
  if year == '2013'
  then
      camperTableId = "bgghbp7gs"
      medsTableId = "bgghbp7gt"
      medScheduleItemsTableId = "bhqk2yzah"
  end
  if year == '2014'
      camperTableId = "bid3d66xd"
      medsTableId = "bid3d67wj"
      medScheduleItemsTableId = "bid3d67wn"
  end
  # Camper table ID:  bi8b6igq7
  # Meds table ID:  bi8b6igw7
  # Med Schedule Items table ID:  bi8b6igxf
  if year == '2015'
      camperTableId = "bi8b6igq7"
      medsTableId = "bi8b6igw7"
      medScheduleItemsTableId = "bi8b6igxf"
  end

  # get current database timestamps
  qbc.apptoken = qb_apptoken
  timestamp = Hash.new
  
  qbc.getDBInfo(camperTableId)
  latest_timestamp1a, latest_timestamp1 = self.specialCampTime(qbc)
  timestamp[latest_timestamp1a] = latest_timestamp1

  qbc.getDBInfo(medsTableId)
  latest_timestamp2a, latest_timestamp2 = self.specialCampTime(qbc)
  timestamp[latest_timestamp2a] = latest_timestamp2

  qbc.getDBInfo(medScheduleItemsTableId)
  latest_timestamp3a, latest_timestamp3 = self.specialCampTime(qbc)
  timestamp[latest_timestamp3a] = latest_timestamp3
  
  puts "    2) CHECKING DATABASE TIMESTAMPS"
      
  puts "       #{latest_timestamp1a} CALIFORNIA #{latest_timestamp1} " 
  puts "       #{latest_timestamp2a} CALIFORNIA #{latest_timestamp2} "
  puts "       #{latest_timestamp3a} CALIFORNIA #{latest_timestamp3} "
  
  stamps = [ latest_timestamp1a, latest_timestamp2a, latest_timestamp3a ]
      
  latest_timestamp = stamps.sort[2]
  all_timestamps = "#{latest_timestamp1a} #{latest_timestamp2a} #{latest_timestamp3a}"
  prev_timestamp = %x(cat #{timestamp_file})
  if (prev_timestamp == all_timestamps)
  then
      return false, medScheduleItemsTableId, timestamp[latest_timestamp]
  else
      %x(echo -n #{all_timestamps} > #{timestamp_file})
      return true, medScheduleItemsTableId, timestamp[latest_timestamp]
  end
end

#-----------------------------------------------------------------------------
# databaseReloaded
#    maybe reload the database and rewrite the Special Camp top level menu
#-----------------------------------------------------------------------------
def databaseReloaded(qbc, input_folder, has_changed, db, timestamp, refresh, menu_exists)
  require 'QuickBaseClient'

  imported_csv = input_folder + "Med_Schedule_Items.csv"
  numberlines_file = input_folder + "numberlines.txt"
 
  #---------------------------------------------------------------------------
  # if user indicated to refresh the database
  # or if user indicated to check for changes and database has changed
  #---------------------------------------------------------------------------
  if (refresh == "true") or (refresh == "check" and has_changed) or (not menu_exists)
  then
      #-------------------------------------------------------------------------
      # import the csv file
      #-------------------------------------------------------------------------
      qbc.makeSVFile(imported_csv, ",", db, nil, nil, "List All for CSV Export")  
      numberlines_slash_n = %x(wc --lines #{imported_csv} | cut -f1 -d' ')
      numberlines = `echo -n #{numberlines_slash_n}`
      %x(echo #{numberlines} > #{numberlines_file})    
      puts "    3) DATABASE HAS BEEN RELOADED AND CONTAINS #{numberlines} LINES"
     
      #-----------------------------------------------------------------------
      # compute the html file that is the top level menu for Special Camp
      #-----------------------------------------------------------------------
      puts "    4) FROM NEW DATABASE DETERMINE CAMPER NAMES"
      if Rails.env.production?
      then
        show_debug = %x(python ./public/meds/src/GoSpecialCamp.py ./public/meds/in/ ./public/meds/outIndex/)
        puts "MAIN MENU HAS BEEN REGENERATED"
        #puts show_debug   
        #check = %x(cp --verbose ./public/meds/outIndex/CamperList/index.html ./app/views/meds/index.html.erb)
        # THIS CP DOES NOT WORK SO USE ./public/meds/outIndex/CamperList/index.html INSTEAD
        #check = %x(cp --verbose ./public/meds/outIndex/CamperList/index.html ./public/top_menu.html)
        #puts check
      else
        if false
        then
          show_debug = %x(python ./public/meds/src/GoSpecialCamp.py ./public/meds/in/ ./public/meds/outIndex/)
          #puts show_debug
        else   
          # THIS IS NOT CORRECT BECAUSE I HARD-CODED ./public/meds/outIndex/
          show_debug = %x(python ./public/meds/src/GoSpecialCamp.py ./public/meds/in/ ./public/meds/outIndex/)
          #puts show_debug 
          check = %x(cat ./public/meds/outIndex/CamperList/index.html | sed 's@stark-retreat-1229.herokuapp.com@0.0.0.0:3000@' > /tmp/special-camp.html)
          check = %x(cat /tmp/special-camp.html > ./public/meds/outIndex/CamperList/index.html)
          puts "MAIN MENU HAS BEEN REGENERATED"
          
        end  
        #check = %x(cat ./public/meds/outIndex/CamperList/index.html > ./app/views/meds/menu.html.erb)
        #check = %x(cat ./public/meds/outIndex/CamperList/index.html | sed 's@stark-retreat-1229.herokuapp.com@0.0.0.0:3000@' > ./app/views/meds/index.html.erb)
        #check = %x(cat ./public/meds/outIndex/CamperList/index.html | sed 's@stark-retreat-1229.herokuapp.com@0.0.0.0:3000@' > ./public/top_menu.html)
        #puts check
      end
      puts "    5) FROM NEW DATABASE CREATE TOP LEVEL HTML"
      return true, numberlines
  else
      numberlines_slash_n = %x(wc --lines #{imported_csv} | cut -f1 -d' ')
      numberlines = `echo -n #{numberlines_slash_n}`
      return false, numberlines
  end
end

          
#-------------------------------------------------------------------------------
# createHtmlPages
#-------------------------------------------------------------------------------
def createHtmlPages(formtype, camperid, day, dest, page, year, refresh, timestamp)

    report_folder = "./public/meds/out/#{year}/#{formtype}"
    #if not Dir.exists?( report_folder )
    if true
    then

      if Rails.env.production?
      then
         website = "HEROKU"
      else
         website = "RAILS"
      end

      Dir.chdir("./public/meds")

      if formtype == 'all'      
      then
          puts "    6) PRODUCE HTML FILES FOR #{formtype}"
          debug = %x(python ./src/MasterControl.py #{website} "Master-Schedule"                      "#{camperid}" "#{day}" "#{dest}" "#{page}" "#{year}" "#{timestamp}");# puts debug           
          debug = %x(python ./src/MasterControl.py #{website} "Meds-Administered-By-HS"              "#{camperid}" "#{day}" "#{dest}" "#{page}" "#{year}" "#{timestamp}");# puts debug 
          debug = %x(python ./src/MasterControl.py #{website} "Meds-Administered-By-HS-Summarized"   "#{camperid}" "#{day}" "#{dest}" "#{page}" "#{year}" "#{timestamp}");# puts debug 
          debug = %x(python ./src/MasterControl.py #{website} "Meds-Administered-During-LA-Bus-Trip" "#{camperid}" "#{day}" "#{dest}" "#{page}" "#{year}" "#{timestamp}");# puts debug 
          debug = %x(python ./src/MasterControl.py #{website} "Meds-Administered-In-Cabin"           "#{camperid}" "#{day}" "#{dest}" "#{page}" "#{year}" "#{timestamp}");# puts debug 
          debug = %x(python ./src/MasterControl.py #{website} "Guardian-Signature"                   "#{camperid}" "#{day}" "#{dest}" "#{page}" "#{year}" "#{timestamp}");# puts debug 
          debug = %x(python ./src/MasterControl.py #{website} "Leftover-Meds"                        "#{camperid}" "#{day}" "#{dest}" "#{page}" "#{year}" "#{timestamp}");# puts debug 
          puts "    7) PRODUCE A SINGLE PDF FILE FROM FILTERED HTML FILES"
          number_pages = %x(python ./src/classes/pdf/Pdf.py #{website} "#{formtype}" "#{camperid}" "#{day}" "#{page}")
      else
          puts "    6) PRODUCE HTML FILES FOR #{formtype}"
          debug = %x(python ./src/MasterControl.py #{website} "#{formtype}" "#{camperid}" "#{day}" "#{dest}" "#{page}" "#{year}" "#{timestamp}");        
          puts "    7) PRODUCE A SINGLE PDF FILE FROM FILTERED HTML FILES"
          number_pages = %x(python ./src/classes/pdf/Pdf.py  #{website} "#{formtype}" "#{camperid}" "#{day}" "#{page}")
      end
      Dir.chdir("../..")
      
    else
      puts "\nTopController: NO NEED TO UPDATE CSV FILES FOR #{formtype}"
    end
    return number_pages
end
  
################################################################################
#
# VIEW
#    renderPrintform - prompt the user to print local, remote or go to main menu
#    howToRenderAfterPdfProduced - prompt the user after PDF file has been produced
#    howToRenderMainMenu - prompt the user to print local, remote or go to main menu
#                      
################################################################################
def renderPrintform()
    numbers = [@@timestamp, @@numberlines, @@number_pages]
    render \
        :inline => \
            "<span class=databasetext>(The most recent change to Med Schedule Items occurred #{@@timestamp})</span><br><br><br>" \
            "PDF FILE CONSISTS OF #{@@number_pages} PAGES", \
        :layout => "printform"
end
  
#-------------------------------------------------------------------------------
# howToRenderAfterPdfProduced
#-------------------------------------------------------------------------------
def howToRenderAfterPdfProduced(number_pages, timestamp)
    if number_pages == '0'
      render :inline => "THERE WERE NO PAGES PRODUCED", :layout => "finished", :formats => [:html]
    else
      render :inline => \
          "<span class=databasetext>(The most recent change to Med Schedule Items occurred #{timestamp})</span><br><br><br>" \
          "PDF FILE CONSISTS OF #{number_pages} PAGES", \
      :layout => "printform", :formats => [:html]
    end
end

#-------------------------------------------------------------------------------
# howToRenderMainMenu
#-------------------------------------------------------------------------------
def howToRenderMainMenu()
    menu_exists = self.mainMenuExists()
    if menu_exists
    then
      puts "SO RENDERING ./public/meds/outIndex/CamperList/index"
      file = File.open("./public/meds/outIndex/CamperList/index.html", "r")
      contents = file.read
      render :inline => contents, :layout => "yield_body", :formats => [:html]
    else
      puts "ERROR OCCURRED, SO REGENERATING ./public/meds/outIndex/CamperList/index"
      qbc, timestamp, menu_exists, reloaded, numlines =
          self.checkMenuAndDatabase("2015", "true")
    end

  # this works for local but not for cloud
  #render :file => "./public/meds/outIndex/CamperList/index", :layout => "yield_body", :formats => [:html]
      
  # this works for local but not for cloud
  #render :action => :menu, :layout => "yield_body", :handlers => [:erb]
      
  #puts self.hardCodedMenu() 
end
  
        
################################################################################
#
# CONTROL
#    index - open the main menu
#    printRemote - action responding to user, send email to remote printer
#    masterControl - control the printform request and produce PDF
#    setdefault - helper to change the remote print destination
#    checkInlinePassword - helper to check that usr and pwd is correct
#    checkPasswordEnteredByUser - what to do if password correct or not
#                                 for printform
#    checkPasswordEnteredByUserMainMenu - what to do if password correct or not
#                                         for main menu
#    printform - entry point, receive parameters from user and produce PDF
#    openMainMenu - entry point, open the main menu
#
################################################################################
      
#-------------------------------------------------------------------------------
# index
#-------------------------------------------------------------------------------
def index
    self.openMainMenu()
end

#-------------------------------------------------------------------------------
# printRemote
#-------------------------------------------------------------------------------
def printRemote0(dest, year)
  Dir.chdir("./public/meds")
  puts "    9) SENDING THE PDF FILE TO THE SPECIFIED DESTINATION: #{dest}"
  results = %x(python ./src/RemotePrint.py "./out/#{year}/printit.pdf" "#{dest}")
  Dir.chdir("../..")
end

def printRemote()
    printRemote0(@@dest, @@year)
    render :inline => "#{@@number_pages} PAGES HAVE BEEN SENT TO #{@@dest}", :layout => "finished"
end

#-------------------------------------------------------------------------------
# downloadPDF
#-------------------------------------------------------------------------------
def downloadPDF()
  puts "DOWNLOADING /meds/out/2015/printit.pdf"
  send_file "./public/meds/out/2015/printit.pdf", :filename => "special-camp-meds.pdf"
  #render :nothing => true
end

#-----------------------------------------------------------------------------
# checkDatabase
#-----------------------------------------------------------------------------
def checkDatabase(year)  
  qbc = QuickBase::Client.new("kurt.wegner@gmail.com", "unicorn7")
  input_folder= "./public/meds/in/"

  has_changed, db, timestamp = 
      self.databaseHasChanged(qbc, input_folder, year)
      
  if has_changed
      then puts "       TIMESTAMP HAS CHANGED"
      else puts "       TIMESTAMP HAS NOT CHANGED"
  end

  return input_folder, qbc, has_changed, db, timestamp
end



#-----------------------------------------------------------------------------
# checkMenuAndDatabase
#-----------------------------------------------------------------------------
def checkMenuAndDatabase(year, refresh)

  input_folder, qbc, has_changed, db, timestamp = 
      self.checkDatabase(year)
          
  menu_exists = self.mainMenuExists()
  
  reloaded, numlines =
      self.databaseReloaded(qbc, input_folder, has_changed, db, timestamp, refresh, menu_exists)
     
  if not reloaded
      then puts "    3) DATABASE HAS NOT BEEN RELOADED, IT CONTAINS #{numlines} LINES"
  end
      
  return qbc, timestamp, menu_exists, reloaded, numlines
end

#-----------------------------------------------------------------------------
# masterControl
#-----------------------------------------------------------------------------
def masterControl(year, refresh, formtype, camperid, day, page, dest, user, pw) 
            
  qbc, timestamp, menu_exists, reloaded, numlines =
      self.checkMenuAndDatabase(year, refresh)
 
  qbc.signOut  
    
  @@number_pages = 
      self.createHtmlPages(
          formtype, camperid, day, dest, page, year, refresh, timestamp)
            
  self.howToRenderAfterPdfProduced(@@number_pages, timestamp)
    
end
 
#-----------------------------------------------------------------------------
# setdefault
#-----------------------------------------------------------------------------
def setdefault() 
 
    dest = params[:dest]
    input_folder= "./public/meds/in/"
    default_dest_file = input_folder + "defaultdest.txt"
    %x(echo -n #{dest} > #{default_dest_file})
    render :inline => "THE DEFAULT DESTINATION IS NOW<br>#{dest}", :layout => "finished", :formats => [:html]
    
end
    
#-----------------------------------------------------------------------------
# checkInlinePassword
#-----------------------------------------------------------------------------
def checkInlinePassword(user, pw)
  if user == "special" and pw == "camp"
  then
      puts "    1) CHECKING PASSWORD INLINE - OK"
      return true
  else
      puts "    1) CHECKING PASSWORD INLINE - NOT OK, PROMPT USER"
      return false
  end    
end

#-----------------------------------------------------------------------------
# checkPasswordEnteredByUser
#-----------------------------------------------------------------------------
def checkPasswordEnteredByUser()  
    user = params[:usr]
    pw = params[:pwd]
    if user == "special" and pw == "camp"
    then
        self.masterControl(@@year, @@refresh, @@formtype, @@camperid, @@day, @@page, @@dest, @@user, @@pw)
    else
        render :inline => "PASSWORD IS INCORRECT", :layout => "finished", :formats => [:html]
    end
end

#-----------------------------------------------------------------------------
# checkPasswordEnteredByUserMainMenu
#-----------------------------------------------------------------------------
def checkPasswordEnteredByUserMainMenu()  
    user = params[:usr]
    pw = params[:pwd]
    if user == "special" and pw == "camp"
    then
        self.howToRenderMainMenu()
    else
        render :inline => "PASSWORD IS INCORRECT", :layout => "finished", :formats => [:html]
        #html_body = "<div><br /><h1>THIS IS THE BODY</h1><br /></div>"
        #render :inline => html_body, :layout => "yield_body"
        #render :action => :checkPasswordEnteredByUserMainMenu, :handlers => [:erb], :layout => "yield_body"
        #render :file => "public/meds/outIndex/CamperList/index", :handlers => [:erb], :layout => "yield_body"
    end
end
    
#-----------------------------------------------------------------------------
# printform
#-----------------------------------------------------------------------------
def printform() 

    @@user     = params[:usr]
    @@pw       = params[:pwd]
    @@year     = params[:year]
    @@refresh  = params[:refresh]
    @@formtype = params[:formtype]
    @@camperid = params[:camperid]
    @@day      = params[:day]
    @@page     = params[:page]
    @@dest     = params[:dest]

    if @@user == nil     then @@user     = "none"                 end
    if @@pw == nil       then @@pw       = "none"                 end
    if @@formtype == nil then @@formtype = "all"                  end
    if @@camperid == nil then @@camperid = "all"                  end
    if @@day == nil      then @@day      = "all"                  end
    if @@page == nil     then @@page     = "all"                  end
    if @@refresh == nil  then @@refresh  = "check"                end
    if @@year == nil     then @@year     = "2015"                 end
    
    if (@@dest == nil) or (@@dest == "default")
    then
        input_folder = "./public/meds/in/"
        default_dest_file = input_folder + "defaultdest.txt"
        @@dest = %x(cat #{default_dest_file})
    end
        
    if @@formtype == "hs-master-schedule"         then @@formtype = "Master-Schedule" end
    if @@formtype == "hs-med-audit-sheets"        then @@formtype = "Meds-Administered-By-HS" end
    if @@formtype == "caregroup-hs-med-schedule"  then @@formtype = "Meds-Administered-By-HS-Summarized" end
    if @@formtype == "bus-med-audit-sheet"        then @@formtype = "Meds-Administered-During-LA-Bus-Trip" end
    if @@formtype == "caregroup-med-audit-sheets" then @@formtype = "Meds-Administered-In-Cabin" end
    if @@formtype == "guardian-signature-sheet"   then @@formtype = "Guardian-Signature" end
    if @@formtype == "leftover-meds-receipt"      then @@formtype = "Leftover-Meds" end

    puts "\nParameters passed in service request:"
    puts   "        year: "+@@year
    puts   "     refresh: "+@@refresh
    puts   "    formtype: "+@@formtype
    puts   "    camperid: "+@@camperid
    puts   "         day: "+@@day
    puts   "        page: "+@@page
    puts   "        dest: "+@@dest
    puts   "        user: "+@@user
    puts   "          pw: "+@@pw

    puts "\n    0) BEGIN printform"
    
    inline_password_is_ok =
        checkInlinePassword(@@user, @@pw)
        
    if inline_password_is_ok
    then
      self.masterControl(@@year, @@refresh, @@formtype, @@camperid, @@day, @@page, @@dest, @@user, @@pw)
    else
      render :action => :printform, :layout => "check_password", :handlers => [:erb]
    end

    puts   "    8) END printform"
end
    
#-----------------------------------------------------------------------------
# openMainMenu
#-----------------------------------------------------------------------------
def openMainMenu() 

    @@user     = params[:usr]
    @@pw       = params[:pwd]

    if @@user == nil     then @@user     = "none"                 end
    if @@pw == nil       then @@pw       = "none"                 end

    puts "\nParameters passed in service request:"
    puts   "        user: "+@@user
    puts   "          pw: "+@@pw

    puts "\n    0) BEGIN openMainMenu"
    
    inline_password_is_ok =
        checkInlinePassword(@@user, @@pw)

    qbc, timestamp, menu_exists, reloaded, numlines =
      self.checkMenuAndDatabase("2015", "check")
          
    if inline_password_is_ok
    then
      self.howToRenderMainMenu()
    else
      render :action => :openMainMenu, :layout => "check_password_main_menu", :handlers => [:erb]
    end
    
    puts   "    8) END openMainMenu"
end









def hardCodedMenu() 
return <<-eos
<base href="http://0.0.0.0:3000/meds/" target="_blank">
  <title>Special Camp</title>

<style>

    .main
    {
        font-family:Verdana, Geneva, sans-serif;
        font-size:20px;
        font-weight:bold;
        color:green;
        text-align:left;
        margin-left:150px;
        text-decoration:none;
        line-height:150%
    }

    .heading
    {
         font-family:Verdana, Geneva, sans-serif;
         font-size:18px;
         font-weight:bold;
         color:black;
         text-align:left;
         margin-left:0px;
         text-decoration:none;
         line-height:150%;
    }

    .goto
    {
         font-family:Verdana, Geneva, sans-serif;
         font-size:18px;
         font-weight:bold;
         color:blue;
         text-align:left;
         margin-left:0px;
         text-decoration:underline;
         line-height:150%;
         padding-left:20pt;
    }
    
    .tbl
    {
         font-family:Verdana, Geneva, sans-serif;
         font-size:16px;
         font-weight:bold;
         color:black;
         text-align:left;
         margin-left:20px;
         text-decoration:underline;
         line-height:150%;
         padding-left:20pt;
    }
    
    td
    {
        width:170px;
        white-space:nowrap;
    }
   
    td.week
    {
        width:60px;
        white-space:nowrap;
    }
   
    td.camper
    {
        width:200px;
        white-space:nowrap;
    }
   
    a
    {
        color:black;
    }
    
    a.camper
    {
        color:blue;
    }
    
    .text
    {
         font-family:Verdana, Geneva, sans-serif;
         font-size:12px;
         font-weight:bold;
         black;
         text-align:left;
         margin-left:0px;
         text-decoration:normal;
         line-height:150%;
         padding-left:20pt;
    }

</style>

</head>

<body>

<script type="text/javascript">
function pop(url) {
    popupWindow = window.open(
        url,'popUpWindow','height=300,width=900,left=10,top=10,resizable=yes,scrollbars=no,toolbar=no,menubar=no,location=no,directories=no,status=yes')
}
</script>

<!-- ------------------------------------------------------------------ -->
<div><hr><span class=main>FORMS FOR HEALTH SUPERVISOR</span><hr><br>

<a class=goto target="_blank" href="printform?formtype=hs-master-schedule&year=2015&usr=special&pwd=camp"
>Health Supervisor Master Schedule</a><br>


<table class=tbl>
  <tr>
    <td class=week><a target="_blank" href="printform?formtype=hs-master-schedule&day=sun&year=2015&usr=special&pwd=camp">Sun</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-master-schedule&day=mon&year=2015&usr=special&pwd=camp">Mon</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-master-schedule&day=tue&year=2015&usr=special&pwd=camp">Tue</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-master-schedule&day=wed&year=2015&usr=special&pwd=camp">Wed</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-master-schedule&day=thu&year=2015&usr=special&pwd=camp">Thu</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-master-schedule&day=fri&year=2015&usr=special&pwd=camp">Fri</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-master-schedule&day=sat&year=2015&usr=special&pwd=camp">Sat</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-master-schedule&day=asneeded&year=2015&usr=special&pwd=camp">As&nbsp;Needed</a></td>
  </tr>
</table><br>

<a class=goto target="_blank" href="printform?formtype=hs-med-audit-sheets&year=2015&usr=special&pwd=camp"
>Meds Administered by Health Supervisor</a><br>
    
<table class=tbl>
  <tr>
    <td class=camper><a class=camper target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=553&year=2015&usr=special&pwd=camp">Chua,Hannah</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=553&year=2015&usr=special&pwd=camp&day=sun">Sun</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=553&year=2015&usr=special&pwd=camp&day=mon">Mon</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=553&year=2015&usr=special&pwd=camp&day=tue">Tue</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=553&year=2015&usr=special&pwd=camp&day=wed">Wed</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=553&year=2015&usr=special&pwd=camp&day=thu">Thu</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=553&year=2015&usr=special&pwd=camp&day=fri">Fri</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=553&year=2015&usr=special&pwd=camp&day=sat">Sat</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=553&year=2015&usr=special&pwd=camp&day=asneeded">As&nbsp;Needed</a></td>
  </tr>
  <tr>
    <td class=camper><a class=camper target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=519&year=2015&usr=special&pwd=camp">Conville,Mariko</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=519&year=2015&usr=special&pwd=camp&day=sun">Sun</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=519&year=2015&usr=special&pwd=camp&day=mon">Mon</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=519&year=2015&usr=special&pwd=camp&day=tue">Tue</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=519&year=2015&usr=special&pwd=camp&day=wed">Wed</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=519&year=2015&usr=special&pwd=camp&day=thu">Thu</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=519&year=2015&usr=special&pwd=camp&day=fri">Fri</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=519&year=2015&usr=special&pwd=camp&day=sat">Sat</a></td>
    <td class=week><a target="_blank" href="printform?formtype=hs-med-audit-sheets&camperid=519&year=2015&usr=special&pwd=camp&day=asneeded">As&nbsp;Needed</a></td>
  </tr>

</table><br>

</div>
<!---------------------------------------------------------------------->
<div><hr><span class=main>FORMS FOR CABIN CARE GROUP</span><hr><br>

<a class=goto target="_blank" href="printform?formtype=caregroup-med-audit-sheets&year=2015&usr=special&pwd=camp"
>Meds Administered by Camper Care Group</a><br>
<table class=tbl>

  <tr>
    <td><a target="_blank" href="printform?formtype=caregroup-med-audit-sheets&camperid=553&year=2015&usr=special&pwd=camp">Chua,Hannah</a></td>
    <td><a target="_blank" href="printform?formtype=caregroup-med-audit-sheets&camperid=519&year=2015&usr=special&pwd=camp">Conville,Mariko</a></td>
  </tr>

</table><br>

<a class=goto target="_blank" href="printform?formtype=caregroup-hs-med-schedule&year=2015&usr=special&pwd=camp"
>Care Group Med Schedule for Health Supervisor Administered Meds</a><br>
<table class=tbl>
  <tr>
    <td><a target="_blank" href="printform?formtype=caregroup-hs-med-schedule&camperid=553&year=2015&usr=special&pwd=camp">Chua,Hannah</a></td>
    <td><a target="_blank" href="printform?formtype=caregroup-hs-med-schedule&camperid=519&year=2015&usr=special&pwd=camp">Conville,Mariko</a></td>
  </tr>

</table><br>

</div
<!---------------------------------------------------------------------->
<div><hr><span class=main>FORMS FOR GUARDIAN</span><hr><br>

<a class=goto target="_blank" href="printform?formtype=guardian-signature-sheet&year=2015&usr=special&pwd=camp"
>Guardian Signature</a><br>
<table class=tbl>
  <tr>
    <td><a target="_blank" href="printform?formtype=guardian-signature-sheet&camperid=553&year=2015&usr=special&pwd=camp">Chua,Hannah</a></td>
    <td><a target="_blank" href="printform?formtype=guardian-signature-sheet&camperid=519&year=2015&usr=special&pwd=camp">Conville,Mariko</a></td>
  </tr>

</table><br>

<a class=goto target="_blank" href="printform?formtype=leftover-meds-receipt&year=2015&usr=special&pwd=camp"
>Leftover Meds Receipt Acknowledgment</a><br>
<table class=tbl>
  <tr>
    <td><a target="_blank" href="printform?formtype=leftover-meds-receipt&camperid=553&year=2015&usr=special&pwd=camp">Chua,Hannah</a></td>
    <td><a target="_blank" href="printform?formtype=leftover-meds-receipt&camperid=519&year=2015&usr=special&pwd=camp">Conville,Mariko</a></td>
  </tr>

</table><br>

</div>
<!---------------------------------------------------------------------->
<div><hr><span class=main>FORMS FOR LA BUS CAPTAIN</span><hr><br>

<a class=goto target="_blank" href="printform?formtype=bus-med-audit-sheet&year=2015&usr=special&pwd=camp"
>Meds Administered During LA Bus Trip</a><br>
<table class=tbl>
  <tr>
    <td class=week><a target="_blank" href="printform?formtype=bus-med-audit-sheet&day=sun&year=2015&usr=special&pwd=camp">Sun</a></td>
    <td class=week><a target="_blank" href="printform?formtype=bus-med-audit-sheet&day=sat&year=2015&usr=special&pwd=camp">Sat</a></td>
    <td class=week><a target="_blank" href="printform?formtype=bus-med-audit-sheet&day=asneeded&year=2015&usr=special&pwd=camp">As&nbsp;Needed</a></td>
  </tr>
</table><br>  

</div>
<!---------------------------------------------------------------------->
<hr>

</body>
</html>
eos
end



















 
end # MedsController
