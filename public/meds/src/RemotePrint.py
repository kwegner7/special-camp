'''
    RemotePrint
'''

import smtplib, sys, glob
    
#===============================================================================
# RemotePrint
#===============================================================================
class RemotePrint():
    
    def __init__(self, pdf_file, destination):
        self.pdf_file = pdf_file
        self.destination = destination
        
    def remotePrint(self):

        if self.destination == 'download':
            print "DOWNLOADING THE PDF FILE"
            return None
                       
        fromaddr = 'kurt.wegner@gmail.com'
        if True: 
            toaddrs  = 'kurt.wegner@gmail.com'
        else:  
            toaddrs  = 'bvsatow@hpeprint.com'
            
        toaddrs = self.destination

        username = 'kurtwegner'  
        password = 'Sunari99'
        
        from email.mime.image import MIMEImage
        from email.mime.application import MIMEApplication
        from email.mime.multipart import MIMEMultipart
        
        COMMASPACE = ', '
        
        # Create the container (outer) email message.
        msg = MIMEMultipart()
        msg['Subject'] = 'Page To Be Printed'
        # me == the sender's email address
        family = list( [ toaddrs ] )
        msg['From'] = fromaddr
        msg['To'] = COMMASPACE.join(family)
        msg['Attachment'] = 'OnePage.pdf'
        msg.preamble = 'Page To Be Printed'
        
        # Assume we know that the image files are all in PNG format
        pngfiles = glob.glob('/home/kurt/ubu/fotowall/*.png')
        pngfiles = glob.glob('/home/kurt/ToBePrinted//*.pdf')
        pngfiles = list([self.pdf_file])
        print pngfiles
        for file in pngfiles:
            fp = open(file, 'rb')
            if False:
                img = MIMEImage(fp.read())
            else:
                img = MIMEApplication(fp.read())
                img.add_header('Content-Disposition', 'attachment; filename="OnePage.pdf"')
            fp.close()
            msg.attach(img)
 
        # Send the email via our own SMTP server.
        s = smtplib.SMTP('smtp.gmail.com:587')
        s.starttls()  
        s.login(username,password)
        s.sendmail(fromaddr, family, msg.as_string())
        s.quit()        

#===============================================================================
# main
#===============================================================================
if __name__ == '__main__':
    pdf_file = sys.argv[1]
    destination = sys.argv[2]
    remote = RemotePrint(pdf_file, destination)
    remote.remotePrint()


































#===============================================================================
# obsolete ideas
#===============================================================================
if __name__ == '__dont__':
    import smtplib  
      
    fromaddr = 'kurt.wegner@gmail.com'  
    toaddrs  = 'kurt.wegner@gmail.com'  
    msg = 'There was a terrible error that occured and I wanted you to know!'
    attach = ("/working/python7/db/helpers/notes.txt")  
      
      
    # Credentials (if needed)  
    username = 'kurtwegner'  
    password = 'Sunari99'
    
    print "GOT HERE"
    
    # The actual mail send  
    if False:
        server = smtplib.SMTP('smtp.gmail.com:587')  
        server.starttls()  
        server.login(username,password)  
        server.sendmail(fromaddr, toaddrs, msg)  
        server.quit()  
        
    
    if False:
        from email.MIMEMultipart import MIMEMultipart
        from email.mime.application import MIMEApplication
        from email.MIMEText import MIMEText
        from email.MIMEImage import MIMEImage
        msg = MIMEMultipart()
        msg.attach(MIMEApplication(file("/working/rails/meds/public/meds/out.works/2013/pdf/Master-Schedule.pdf").read()))
    
        import smtplib
        mailer = smtplib.SMTP('smtp.gmail.com:587')
        #mailer.connect()
        mailer.login(username,password)  
        mailer.sendmail(fromaddr, toaddrs, msg.as_string())
        #mailer.close()    
        mailer.quit()  
 

    if False:
        import smtplib
        
        # Here are the email package modules we'll need
        from email.mime.application import MIMEApplication
        from email.mime.multipart import MIMEMultipart
            
        # Create the container (outer) email message.
        msg = MIMEMultipart()
        msg['Subject'] = 'Printing Special Camp 2013 Meds Page ...'
        msg['From'] = 'kurt.wegner@gmail.com' 
        msg['To'] = [ 'kurt.wegner@gmail.com' ]
        msg.preamble = 'Printing ...'
        
        fp = open("/working/rails/meds/public/meds/out.works/2013/pdf/Master-Schedule.pdf", 'rb')
        #img = MIMEImage(fp.read())
        pdf = MIMEApplication(fp.read())
        fp.close()
        msg.attach(pdf)
        
        s = smtplib.SMTP('smtp.gmail.com:587')
        s.starttls()  
        s.login(username,password)  
        s.sendmail(fromaddr, toaddrs, msg)
        s.quit()
        
        



