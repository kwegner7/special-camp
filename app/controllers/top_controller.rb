class TopController < ApplicationController
  #http_basic_authenticate_with :name => "special", :password => "camp"
  #layout "top"

  def index
    puts "This is index method of TopController"
  end

  #-----------------------------------------------------------------------------
  # top#refresh
  #    Heruko or local server was bundled with a manually downloaded Meds database
  #    This method allows Heruko to update it from the Quickbase
  #    This method allows local server to copy again from a fixed PC location
  #    And this method clears all outputs except the TOC.html which
  #        user uses to re-generate html for each report type
  #-----------------------------------------------------------------------------
  def refresh0()
    require 'QuickBaseClient'
    puts "\ntop#refresh: INITIALIZE BY OBTAINING THE MEDS INPUT DATABASE"

    #---------------------------------------------------------------------------
    # Server is Heroku - so load from remote Quickbase
    #---------------------------------------------------------------------------
    if Rails.env.production?
        puts "\ntop#refresh: DOWNLOADING FROM REMOTE QUICKBASE"
        campers_dbid = "bgghbp7gs"
        meds_dbid = "bgghbp7gt"
        qb_apptoken = "rabajzbsx3v5nb3rki6udbnccbb"

        med_schedule_items_dbid = "bgghbp7g9"
        med_schedule_items_dbid_2013 = "bhqk2yzah"
        med_schedule_items_dbid_2014 = "bid3d67wn"

        #Camper table ID:  bid3d66xd
        #Meds table ID:  bid3d67wj
        #Med Schedule Items table ID 2014:  bid3d67wn

        puts "top#refresh: (1) "+`ls -l ./public/meds/in/*.csv`
        qbc = QuickBase::Client.new("kurt.wegner@gmail.com", "unicorn7")
        qbc.apptoken = "rabajzbsx3v5nb3rki6udbnccbb"
        qbc.makeSVFile("./public/meds/in/Med_Schedule_Items.csv", ",",
          med_schedule_items_dbid_2013,
          nil, nil, "List All for CSV Export")
        qbc.signOut

    #---------------------------------------------------------------------------
    # Server is local PC
    #---------------------------------------------------------------------------
    else
        puts "\ntop#refresh: COPY MEDS DATABASE FROM DEFAULT FOLDER"
        `cp ./public/meds/defaults/Med_Schedule_Items.csv ./public/meds/in/Med_Schedule_Items.csv`        
    end
    #unless $? == 0
    #    puts "\ntop#refresh: COULD NOT READ FROM REMOTE QUICKBASE"
    #   puts "\ntop#refresh: COPY MEDS DATABASE FROM DEFAULT FOLDER"
    #   `cp ./public/meds/defaults/Med_Schedule_Items.csv ./public/meds/in/Med_Schedule_Items.csv`        
    #end


    puts "top#refresh: (2) "+`ls -l ./public/meds/in/*.csv`

    #---------------------------------------------------------------------------
    # Clear the "out" folder and re-copy the top level TOC.html into it
    #---------------------------------------------------------------------------
    puts "\ntop#refresh: Clear the out folder and re-copy the top level TOC.html into it"
    if Dir.exists?("./public/meds/out")
      FileUtils.rm_r "./public/meds/out"
    end
    `mkdir --parents ./public/meds/out/2013`
    if File.exists?("./public/meds/defaults/TOC.html")
      `cp ./public/meds/defaults/TOC.html ./public/meds/out/2013/TOC.html`
    end

  end

  def refresh()
    refresh0()
    render "top/view.html.erb", layout: "application"
  end
  
  #-----------------------------------------------------------------------------
  # top#view
  #    create CSV files, HTML files, TOC files
  #-----------------------------------------------------------------------------
  def view

    if Rails.env.production?
        puts "PRODUCTION MODE"
    end

    if Rails.env.development?
        puts "DEVELOPMENT MODE"
    end

    if true
        puts "Application is running from "+Dir.pwd
        Dir.chdir("./public/meds")

        if Rails.env.production?
        then
           website = "HEROKU"
        else
           website = "RAILS"
        end
           
        puts "\nTopController: UPDATING ALL CSV FILES "
        results = %x(python ./src/MasterControl.py #{website} "Master-Schedule"); puts "VIEW: "+results
        results = %x(python ./src/MasterControl.py #{website} "Meds-Administered-By-HS"); puts "VIEW: "+results
        results = %x(python ./src/MasterControl.py #{website} "Meds-Administered-By-HS-Summarized"); puts "VIEW: "+results
        results = %x(python ./src/MasterControl.py #{website} "Meds-Administered-In-Cabin"); puts "VIEW: "+results
        results = %x(python ./src/MasterControl.py #{website} "Meds-Administered-During-LA-Bus-Trip"); puts "VIEW: "+results
        results = %x(python ./src/MasterControl.py #{website} "Guardian-Signature"); puts "VIEW: "+results
        results = %x(python ./src/MasterControl.py #{website} "Leftover-Meds"); puts "VIEW: "+results

        Dir.chdir("../..")
    end
  end

  #-----------------------------------------------------------------------------
  # top#htmltopdf
  #    for one report HTML --> PDF but do not download
  #-----------------------------------------------------------------------------
  def htmltopdf(which, html_files, pdf_file, prepend_toc, force)

      if not File.exists?( pdf_file ) or force
      then
        title_of_report = which.gsub( "-", " " )

        puts "\nTopController: (1) CONVERTING HTML TO PDF FOR #{which}"
        if Rails.env.production?
        then
          wkhtml = "/app/vendor/bundle/ruby/1.9.1/gems/wkhtmltopdf-heroku-1.0.0/bin/wkhtmltopdf-linux-amd64"
        else
          wkhtml = "/usr/bin/wkhtmltopdf11"
        end

        args = " --quiet --orientation Landscape --page-size Letter --margin-bottom 0mm"
        toc_text = " toc --enable-toc-back-links --toc-level-indentation 1em --toc-header-text '#{title_of_report}'"
        inputs = " #{html_files}"
        output = " #{pdf_file}"
        puts "\nTopController: (2) CONVERTING HTML TO PDF FOR #{which}"
        if prepend_toc
        then
            #puts "Rails Invocation is #{wkhtml} #{args} #{toc_text} #{inputs} #{output}"
            %x[#{wkhtml} #{args} #{toc_text} #{inputs} #{output}]
        else
            #puts "Rails Invocation is #{wkhtml} #{args} #{inputs} #{output}"
            %x[#{wkhtml} #{args} #{inputs} #{output}]
        end
        unless $? == 0
            puts "\nTopController: WKHTMLTOPDF ERROR HAS OCCURRED"
        else
            puts "\nTopController: PDF FILE HAS BEEN CREATED USING RAILS AT #{output}"
        end
      else
        puts "\nTopController: NO NEED TO REGENERATE PDF FOR #{which}"
      end
  end

  #-----------------------------------------------------------------------------
  # top#downloadAllPages
  #    print all pages of this report type
  #-----------------------------------------------------------------------------
  def downloadAllPages()
      which = params[:which]
      html_files = "./public/meds/out/2013/#{which}/html/*.html"
      pdf_file = "./public/meds/out/2013/#{which}/PRINTALL.pdf"
      pdf_file = "./public/meds/out/2013/printit.pdf"
      htmltopdf(which, html_files, pdf_file, true, true)
  end

  #-----------------------------------------------------------------------------
  # top#printLocalOnePage
  #    print this page to the local PC printer
  #-----------------------------------------------------------------------------
  def printLocalOnePage
      report_name = params[:report_name];
      html_filename = params[:html_filename];
      html_file_in = "./public/meds/out/2013/#{report_name}/html/#{html_filename}"
      pdf_file_out = "./public/meds/out/2013/printit.pdf"
      htmltopdf(report_name, html_file_in, pdf_file_out, false, true)
  end

  #-----------------------------------------------------------------------------
  # top#printRemoteOnePage
  #    print this page to the remote Special Camp printer
  #-----------------------------------------------------------------------------
  def printRemoteOnePage
      report_name = params[:report_name];
      html_filename = params[:html_filename];
      html_file_in = "./public/meds/out/2013/#{report_name}/html/#{html_filename}"
      pdf_file_out = "./public/meds/out/2013/printit.pdf"
      htmltopdf(report_name, html_file_in, pdf_file_out, false, true)

      if Rails.env.production?
      then
         website = "HEROKU"
      else
         website = "RAILS"
      end

      Dir.chdir("./public/meds")
      results = %x(python ./src/MasterControl.py #{website} "Remote-Print" "./out/2013/printit.pdf")
      puts "VIEW: "+results
      Dir.chdir("../..")
  end

  #-----------------------------------------------------------------------------
  # top#printRemote
  #    print this PDF file to the remote Special Camp printer
  #-----------------------------------------------------------------------------
  def printRemote
      if Rails.env.production?
      then
         website = "HEROKU"
      else
         website = "RAILS"
      end

      Dir.chdir("./public/meds")
      results = %x(python ./src/RemotePrint.py "./out/2013/printit.pdf")
      puts results
      Dir.chdir("../..")

      render "top/view.html.erb", layout: "application"
  end

  #-----------------------------------------------------------------------------
  # createHtmlPages
  #-----------------------------------------------------------------------------
  def createHtmlPages0(which, id)
      #which = params[:which]
      #id = params[:id]
      puts "which is #{which}, id is #{id}"
      report_folder = "./public/meds/out/2013/#{which}"
      if not Dir.exists?( report_folder )
      then
        puts "\nTopController: UPDATING CSV FILES FOR #{which}"
        Dir.chdir("./public/meds")

        if Rails.env.production?
        then
           website = "HEROKU"
        else
           website = "RAILS"
        end

        results = %x(python ./src/MasterControl.py #{website} "#{which}" "#{id}" "all" "kurt.wegner@gmail.com" "all" "2013" "true"); puts results
        Dir.chdir("../..")
      else
        puts "\nTopController: NO NEED TO UPDATE CSV FILES FOR #{which}"
      end
  end

  def createHtmlPages()
      which = params[:which]
      id = params[:id]
      createHtmlPages0(which,id)
      render inline: "#{which}", layout: "what_to_do"
  end

  #-----------------------------------------------------------------------------
  # createPdf
  #-----------------------------------------------------------------------------
  def createPdf()
      which = params[:which]
      id = params[:id]
      puts "which is #{which}, id is #{id}"
      refresh0()
      createHtmlPages0(which, id)
      #render inline: "#{which}", layout: "what_to_do"
  end

=begin

http://stark-retreat-1229.herokuapp.com/top/createPdf?which=Meds-Administered-By-HS;id=548

http://my.heroku.site.name/printform?formtype=med-schedule&camperid=1587
http://my.heroku.site.name/printform?formtype=hs-audit-sheet&camperid=1588
http://my.heroku.site.name/printform?formtype=hs-all-week-schedule
http://my.heroku.site.name/printform?formtype=bus-med-schedule
http://my.heroku.site.name/printform?formtype=all-forms&camperid=1585
=end

end # TopController








#-------------------------------------------------------------------------------
# OBSOLETE THINGS
#-------------------------------------------------------------------------------

=begin

  def getcsvMasterSchedule()                   which = params[:which]; getCsvAndHtml(which) end
  def getcsvMedsAdministeredByHS()            which = params[:which]; getCsvAndHtml(which) end
  def getcsvMedsAdministeredByHSSummarized()  which = params[:which]; getCsvAndHtml(which) end
  def getcsvMedsAdministeredInCabin()         which = params[:which]; getCsvAndHtml(which) end
  def getcsvMedsAdministeredDuringLABusTrip() which = params[:which]; getCsvAndHtml(which) end
  def getcsvGuardianSignature()               which = params[:which]; getCsvAndHtml(which) end
  def getcsvLeftoverMeds()                    which = params[:which]; getCsvAndHtml(which) end





    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Master-Schedule/TOC.html">View Individual Pages</a><br />
    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Master-Schedule/TOC1.html">Print Locally</a><br />
    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Master-Schedule/TOC2.html">Print Remotely</a><br />

    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Meds-Administered-By-HS/TOC.html">View Individual Pages</a><br />
    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Meds-Administered-By-HS/TOC1.html">Print Locally</a><br />
    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Meds-Administered-By-HS/TOC2.html">Print Remotely</a><br />

    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Meds-Administered-By-HS-Summarized/TOC.html">View Individual Pages</a><br />
    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Meds-Administered-By-HS-Summarized/TOC1.html">Print Locally</a><br />
    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Meds-Administered-By-HS-Summarized/TOC2.html">Print Remotely</a><br />

    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Meds-Administered-In-Cabin/TOC.html">View Individual Pages</a><br />
    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Meds-Administered-In-Cabin/TOC1.html">Print Locally</a><br />
    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Meds-Administered-In-Cabin/TOC2.html">Print Remotely</a><br />

    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Meds-Administered-During-LA-Bus-Trip/TOC.html">View Individual Pages</a><br />
    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Meds-Administered-During-LA-Bus-Trip/TOC1.html">Print Locally</a><br />
    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Meds-Administered-During-LA-Bus-Trip/TOC2.html">Print Remotely</a><br />

    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Guardian-Signature/TOC.html">View Individual Pages</a><br />
    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Guardian-Signature/TOC1.html">Print Locally</a><br />
    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Guardian-Signature/TOC2.html">Print Remotely</a><br />

    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Leftover-Meds/TOC.html">View Individual Pages</a><br />
    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Leftover-Meds/TOC1.html">Print Locally</a><br />
    <a style="font-size: 14px;" href="http://0.0.0.0:3000/meds/out/2013/Leftover-Meds/TOC2.html">Print Remotely</a><br />


  # This action uses query string parameters because it gets run
  # by an HTTP GET request, but this does not make any difference
  # to the way in which the parameters are accessed. The URL for
  # this action would look like this in order to list activated
  # clients: /clients?status=activated
  def indexx
    if params[:status] == "activated"
      @clients = Client.activated
    else
      @clients = Client.unactivated
    end
  end


  def practice
    puts "Top Controller - Method refresh"
    puts "Converting HTML to PDF"
    file = File.open("./public/index-meds.html", "rb")
    if true
      contents = file.read
    else
      contents = "<p>TESTING HEROKU</p>"
    end
    puts `find /app -name "*wkhtmltopdf*" -exec ls -l {} ';'`
    #result = `/app/bin/wkhtmltopdf-linux-amd64 --version`
    #puts result

    %x[/app/vendor/bundle/ruby/1.9.1/gems/wkhtmltopdf-heroku-1.0.0/bin/wkhtmltopdf-linux-amd64 --page-size Letter --orientation Landscape ./public/meds/out/2013/Master-Schedule/html/*.html ./public/meds/works.pdf]
    kit = PDFKit.new(contents)
    pdf = kit.to_file "./public/index-meds.pdf"
  end

#if false # this works 
#    qbc = QuickBase::Client.new( "kurt.wegner@gmail.com", "unicorn7", "https://www.quickbase.com/db/bhqk2yzah?a=q&qid=1" )
#    qbc.apptoken = $qb_apptoken
#    qbc.makeSVFile( "Med_Schedule_Items.csv", ",", $med_schedule_items_dbid )
#    qbc.signOut
#end

#qbc = QuickBase::Client.new($qb_user,$qb_pwd)
#qbc.apptoken = $qb_apptoken
#records = Hash.new
#records = qbc.getAllValuesForFields( $campers_dbid, ["Full Name","Full name(last name, first name)"] )
#qbc.signOut

#Notice that I had to make a call to the "apptoken" method and present the app token string, 
#    in order to gain access to the QuickBase application.

=end

