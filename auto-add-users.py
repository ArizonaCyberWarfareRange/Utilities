# -:*- coding: utf-8 -*-
import csv
import sys
import mechanize
import cookielib
import time

line_num = 0  # global to tell where u are in file
line_num_entered = []
line_num_dupe = []

# =================  Overview of this script=======
'''
1. main(): opens file from argument and creates a 2d list object and send to print_list()
     2. print_list(): iterates through the 2d list sends to enter_data
     3. enter_data(): pull the columns from csv, email, name, phone.
        check if column 'completed' is marked
        if passed, check if a duplicate exists in the row above the current row. send to check_dupe
        4. check_dupe(): takes in name, phone, email and check if they exists in csv above the current line num
            returns 1 if there is duplicate
            return 0 is there is not a duplicate
        if passed check_dupe(), then strip name and phone number of special characters
        5. uploadData(): attempts to add the user to the system, http://192.168.100.1/admin/useraccess.php?opt=add

		    5.1 checkUserDuplicate(): returns 1 if there is duplicate
                return 0 is there is not a duplicate

            uploadData returns 1 if entering user fails
                return 0 if entering user is successful

        6. sendEmail(): attempts to send a predefined email to the email after successfully entered

    7. mark_entered(): after marking the line numbers that have been entered and have been a duplicated
        this will open the file from argument and output argument.output.txt
        Must manually take this file and enter the 'completed' column in google docs

to install in mechanize

sudo apt-get install python-setuptools
sudo easy_install mechanize


'''


# =================  Overview of this script=======
def main():
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " <file.csv>")
        return 1
    print("WARNING. THE EMAIL IS CURRENT AS OF MAY 16th, 2016. CONTACT BRETT TO CHECK FOR UPDATED VERSION")
    print("Sleeping for 7 seconds")

    time.sleep(2)
    

    my_file = open(sys.argv[1])  # get data from argument
    csvReader = csv.reader(my_file)  # use csv package and create a reader
    exampleData = list(csvReader)  # take the reader ancd convert to list
    print_list(exampleData)

    mark_entered()

    print "Please read " +sys.argv[0]+".output.txt, and manually enter data in Google sheets"
    return 0


def strip_phone(phone):  # takes in a string phone, and strips the special characters. keep '+' for international
    name = ''
    international = False
    for e in phone:
        if e.isalnum():
            name = name + e
        elif e in '+':
            name = name + e
            international = True

    if international == False:
        name = name[-10:]
    return (name)


def print_list(list):
    header = list.pop(0)  # read first line, which is headers
    # print("" + header[1] + "\t\t" + header[2])
    global line_num  # global keyword to make writable
    line_num = line_num + 1

    for row in list:
        # printMe = strip_row_string(row)
        # print(printMe)
        enter_data(row)
        line_num = line_num + 1

def checkUserDuplicate(br,name,phone):
    userlist=br.open('http://192.168.100.1/admin/useraccess.php?opt=lu')
    #print userlist.read()
    print "Checking if user" + name + "exists in database"
    links=list(br.links())
    for link in links[24:]:
        strlink=str(link)
        if name in strlink:
            print strlink
            linktxt=br.follow_link(link)
            linktxtread=linktxt.read()
            #print linktxtread
            if phone in linktxtread:
                print 'duplicate'
                return 1
            else:
                print 'not duplicate'
    return 0

def uploadData(name, phone, last):
    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # user agent
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0')]
    # Browser Options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_redirect(mechanize.HTTPRedirectHandler)
    br.set_handle_refresh(mechanize.HTTPRefreshProcessor(), max_time=1)

    # Open website
    loginPage = br.open('http://192.168.100.1/admin/login.php')
    # show available forms
    # for form in br.forms():
    #   print "Form name:", form.name
    #   print form

    # enter data
    br.select_form(nr=0)  # only one form
    br.form['uname'] = 'rang'
    br.form['password'] = 'Rang525'

    responce = br.submit()
    responceText = responce.read()
    if "Beginner" in responceText:
        print "Login success!"
    else:
        print "Login failed!  Exiting"
        return 1


    if checkUserDuplicate(br,last,phone)==1:
        print 'User already exists.'
        return 1

    adduser = br.open('http://192.168.100.1/admin/useraccess.php?opt=add')
    # for form in br.forms():
    #   print "Form name:", form.name
    #   print form

    # enter data
    br.select_form(nr=0)  # only one form
    br.form['sName'] = name
    br.form['sPhone'] = phone
    print br.form

    br.submit() #uncomment this to enter into database
    return 0


def mark_entered():  # check both entered and dupe arrays and marks them accordingly
    with open(sys.argv[1], 'r') as istr:
        with open(sys.argv[1] + '.output.txt', 'w') as ostr:
            for i, line in enumerate(istr):
                if i in line_num_entered:
                    # Get rid of the trailing newline (if any).
                    if '\r\n' in line:
                        line = line.rstrip('\r\n')
                        line += 'x'
                        line += '\r\n'
                    elif '\n' in line:
                        line = line.rstrip('\n')
                        line += 'x'
                        line += '\n'

                elif i in line_num_dupe:
                    # Get rid of the trailing newline (if any).
                    if '\r\n' in line:
                        line = line.rstrip('\r\n')
                        line += 'dupe'
                        line += '\r\n'
                    elif '\n' in line:
                        line = line.rstrip('\n')
                        line += 'dupe'
                        line += '\n'

                # print(line)
                ostr.write(line)
        ostr.close()
    istr.close()


def check_dupe(name, phone, email):
    print "Checking if " + name + "exists in csv file"
    global line_num_dupe
    result = 0
    with open(sys.argv[1], 'r') as istr:
        for i, line in enumerate(istr):
            if i == line_num:
                break  # dont check itself and future results

            if name in line:
                line_num_dupe.append(line_num)  # add a duplicate
                result = 1
            elif phone in line:
                line_num_dupe.append(line_num)  # add a duplicate
                result = 1
            elif email in line:
                line_num_dupe.append(line_num)  # add a duplicate
                result = 1

    istr.close()
    return result


def sendEmail(email):
    #print("before this email system can be completed, please make sure that accounts are created successfully. ")
    #print("Check when adding user, the html page from useraccess.php contains the username")
    #return
    html = """
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8" />
    </head>
    <body>
    Excellent!  Your account has been created.  Thank you for seeking to improve you cybersecurity skills at the Arizona Cyber Warfare Range.
    <br>
    To get started, below are instructions on accessing the range.
    <br><br>

    Help us to expand our mission to improve understanding of information security and cyberwarfare by forwarding this message to a friend who might be interested in being exposed to or practicing their skills at the AzCWR.
    <br><br>
     <ol>
      <li><b>Again, using your cell phone, send the following in a SMS text message to 480-525-9801:</b></li>
       <ol type="a">
          <li>Beginners Range:&nbsp;&nbsp;&nbsp;&nbsp;         <b>enroll beginner</b></li>
          <li>Intermediate Range:    <b>enroll intermediate</b></li>
          <li>Advanced Range:&nbsp;&nbsp;&nbsp;&nbsp;          <b>enroll advanced</b></li>
          <li>Real-World Range:&nbsp;&nbsp;<b>enroll jedi</b></li>
        </ol>
        This action will give you access to the indicated range.  You will receive a response similar to: "Thank you, you are now enrolled in the <level> range."
      <li><b>Refresh your computer's 24-hour access to the range.</b></li>
      This step allows us to maintain security to the range by allowing only humans to whom we have given access, and only for 24-hour blocks of time.
    <ol type="a">
          <li>Gather your IP address from this webpage: <a href="http://home.azcwr.org">http://home.azcwr.org</a></li>
    You appear to me as IP address: ##.##.##.##
          <li>Send the following in a SMS text message to 480-525-9801: access ##.##.##.##</li>
    Input your IP address in place of ##.##.##.##
    <br>
    For example, if <u>home.azcwr.org</u> indicates your IP address is 8.8.8.8 you'll send the following in an SMS message to 480-525-9801: 8.8.8.8

        </ol>
      <li><b>Revisit this page to start your time at the range: <a href="http://home.azcwr.org">http://home.azcwr.org</a></b></li>
    <ol type="a">
          <li>Copy one of the IP addresses you see listed on the page</li>
          <li>Open a new browser and paste the IP address you copied into the address bar</li>
          <li>Begin your hacking adventure by choosing a challenge</li>
        </ol>
    </ol>

    --
    <br>
    Happy hacking!
    <br>
    <br>

    - Every Wednesday and Friday from 1000 - 1500 hours the range will be open for you to take time and experiment with the equipment.  Please check the schedule on <a href="http://www.azcwr.org">www.azcwr.org</a> since it changes frequently, plus vacations are set up.
    <br>
    - If the lights are on when you view the range through the camera, and no one is scheduled on the calendar to be there, please don't come down unless it is on the calendar that someone will be there!
    <br>
    - Anytime the range is open (usually Saturdays too, prior to coming please check the calendar) there are a lot of people working together in teams doing amazing things.  Just jump in and learn.
    <br>
    Please join us on our Google Plus and LinkedIn community pages.
    <br>
    --
    <br>
    The Arizona Cyberwarfare Range
    <br>
    480.525.9801
    <br>
    <a href="http://www.azcwr.org">www.azcwr.org</a>
    <br>

    <a href="https://plus.google.com/communities/109709683526296474584">
    <img border="0" alt="azcwr Google+" src="https://cdn3.iconfinder.com/data/icons/free-social-icons/67/google_circle_color-128.png" width="50" height="50" >
    </a>
    <a href="https://www.linkedin.com/company/arizona-cyber-warfare-range">
    <img border="0" alt="azcwr LinkedIn" src="https://cdn3.iconfinder.com/data/icons/free-social-icons/67/linkedin_circle_color-128.png" width="50" height="50" >
    </a>
    </body>
    </html>
    """

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    sender = "azcwr1@gmail.com"
    receiver = email

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Your AzCWR Account"
    msg['From'] = sender
    msg['To'] = receiver

    # Record the MIME types of both parts - text/plain and text/html.
    mime_html = MIMEText(html, 'html')
    msg.attach(mime_html)

    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login('azcwr1', 'livesquare')
    mail.sendmail(sender, receiver, msg.as_string())
    mail.quit()
    print("\n=========email sucessfully sent to "+email)


def enter_data(row):  # takes a row from the csv and enters the data into the form
    global line_num_entered

    Timestamp = row[0]  # discard
    name = row[1]
    phone = row[2]
    email = row[3]  # discard
    ent = row[4]

    if ent == '':
        if check_dupe(name, phone, email) == 1:  # dupe returns 1 if there is a duplicate. 0 if none
            return 1

        arr = name.split()
        if len(arr) == 3:  # case one, first middle last
            last = arr.pop()
            middle = arr.pop()
            first = arr.pop()
            # print 'First: %r' % first
            # print 'Middle: %r' % middle
            # print 'Last: %r' % last
            newName = first[0] + last
        elif len(arr) == 2:  # case two, first last
            last = arr.pop()
            first = arr.pop()
            # print 'First: %r' % first
            # print 'Last: %r' % last
            newName = first[0] + last
        elif len(arr) == 1:  # case three, first
            last = arr.pop()
            # print 'First: %r' % last
            newName = last

        # strip special characters. http://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
        newName = ''.join(e for e in newName if e.isalnum())  # strip characters in newName
        last = ''.join(e for e in last if e.isalnum())  # strip characters in last name

        newPhone = strip_phone(phone)
        if uploadData(newName, newPhone,last) == 0: #uploadData returns 0 if successful
            line_num_entered.append(line_num)  # add the line number into entered array
            sendEmail(email)


if __name__ == '__main__':
    main()
