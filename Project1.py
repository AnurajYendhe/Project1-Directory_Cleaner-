# Description :- File subsystems with job schedule - Accept directory name and time interval from user and delete all duplicate files from that directory after specified time interval and write the name of that duplicate files into log file and send log file to specified mail address.

######################################################################
# importing requried package
######################################################################
import os
import time
import smtplib
import hashlib
import schedule
from sys import *
import urllib.request
from email import encoders
from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

######################################################################
# Function name :- is_connected
# Description :- to check the internet connection
# Input :- Nothing
# Output :- return True(internet connection) / False(No internet connection)
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def is_connected():
    try:
        urllib.request.urlopen('http://www.gmail.com',timeout=1)
        return True
    except urllib.request.URLError as err:
        return False

######################################################################
# Function name :- MailSender
# Description :- to send mail to specified address
# Input :- attachment file path,current time,mail address
# Output :- send mail to specified address
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def MailSender(filename,startTime,num_of_file,counter,address):
    try:
        fromaddr = "abyendhe@gmail.com"
        toaddr = address

        msg = MIMEMultipart()

        msg['From'] = fromaddr

        msg['To'] = toaddr

        body = """ 
        Hello %s,
        Please find attached ducument which contains path of duplicate files.
        Starting time of scanning : %s
        Total number of files scanned : %s
        Total number of duplicate files found : %s

        This is auto gennerated mail.

        Thanks & Regards,
        Anuraj Yendhe
        """%(toaddr,startTime,num_of_file,counter)


        Subject = """
        Duplicate log generated at : %s
        """%(startTime)

        msg['Subject'] = Subject

        msg.attach(MIMEText(body,'plain'))

        attachment = open(filename,"rb")

        p = MIMEBase('application','octet-stream')

        p.set_payload((attachment).read())

        encoders.encode_base64(p)

        p.add_header('Content-Disposition',"attachment; filename= %s" % filename)

        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com',587)

        s.starttls()

        s.login(fromaddr,"ivyl yexa saze dpln")

        text = msg.as_string()

        s.sendmail(fromaddr,toaddr,text)

        s.quit()

        print("Log file successfully sent through Mail")
    
    except Exception as E:
        print("Unable to send mail",E)

######################################################################
# Function name :- checkAbs
# Description :- to check directory path is absolute path or not
# Input :- Path of file
# Output :- return True(path is absolute) / False(path is not absolute)
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def checkAbs(DirName):
    result = os.path.isabs(DirName)
    return result

######################################################################
# Function name :- createAbs
# Description :- to create absolute path of directory
# Input :- Path of file
# Output :- Absolute path of directory
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def createAbs(DirName):
    result = os.path.abspath(DirName)
    return result

######################################################################
# Function name :- checkDir
# Description :- to check directory exists or not
# Input :- Path of file
# Output :- return True( path is exists) / False(path is not exists)
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def checkDir(DirName):
    result = os.path.exists(DirName)
    return result

######################################################################
# Function name :- createDir
# Description :- to create directory
# Input :- Name of directory
# Output :- create directory of specified name
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def createDir(DirName):
    try:
        os.mkdir("Marvellous") 
    except:
        pass

######################################################################
# Function name :- calculateChecksum
# Description :- calculate checksum of file
# Input :- Path of file,blocksize(optional)
# Output :- checksum of file
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def calculateChecksum(path, blocksize = 1024):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

######################################################################
# Function name :- DeleteDups
# Description :- to delete duplicate files
# Input :- file path
# Output :- delete duplicate files
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def DeleteDups(results):
    for result in results:
        counter = 0
        for subresult in result:
            counter = counter + 1
            if(counter > 1):
                os.remove(subresult)

######################################################################
# Function name :- CheckDups
# Description :- to check file is duplicate or not
# Input :- file path
# Output :- path of duplicate files 
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def CheckDups(values):
    if(len(values) > 1):
        return values

######################################################################
# Function name :- printResult
# Description :- generate record of duplicate files
# Input :- file path and its checksum
# Output :- if duplicate file found generate log file to mantain the record of that files
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def printResult(Arr,startTime,num_of_file):
    
    results = list(filter(CheckDups,Arr.values())) # filter out duplicates files

    if(len(results) > 0):
        print("Duplicate files found")
        if not os.path.exists("Marvellous"):
            createDir("Marvellous")

        separator = "-" * 100
        log_path = os.path.join("Marvellous","Marvellous"+str(datetime.now().strftime("%Y-%m-%d -%H-%M-%S"))+".log")
        f = open(log_path,'w')
        f.write(separator + "\n")
        f.write("Duplicate files found at : "+time.ctime()+"\n")
        f.write(separator + "\n")
        f.write("\n")

        counter = 0
        for result in results:
            f.write(separator + "\n")
            for subresult in result:
                f.write("%s\n"%subresult)
                counter = counter + 1
        f.write("\n") 
        f.write(separator + "\n")
        f.write("Total numbers of duplicate files found %s"%counter + "\n")
        f.write(separator + "\n")
        f.close()

        print("Log file successfully generated at location %s" %(log_path)) 
        print("That contain absolute path duplicate files.")
        DeleteDups(results)
        connected = is_connected() # check internet connection
        if (connected == True):
            startTime = time.time()
            MailSender(log_path,startTime,num_of_file,counter,argv[3])
            endTime = time.time()

            print('Took %s seconds to send mail' %(endTime - startTime))
        else:
            print("There is no internet connection")


    else:
        print("No duplicate files found")
######################################################################
# Function name :- DirectoryTrevel
# Description :- To trevel specified directory
# Input : - path of directory
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def DirectoryTrevel():
    DirName = argv[1]
    flag = checkAbs(DirName)
    if(flag == False):
        DirName = createAbs(DirName)
    
    exist = checkDir(DirName)

    if(exist == True):
        startTime = time.ctime()
        Arr = dict()
        counter = 0
        for folderName, subfolderName, fileName in os.walk(DirName):
            print("Current folder name is : ",folderName)
            for fname in fileName:
                filepath = os.path.join(folderName,fname)
                checksum = calculateChecksum(filepath)
                counter = counter + 1
                if checksum in Arr:
                    Arr[checksum].append(filepath)
                else:
                    Arr[checksum] = [filepath]

        printResult(Arr,startTime,counter)

    else:
        print("Error : Invalid inputs")
        exit()

######################################################################
# Function name :- main
# Description :- Main function from where execution starts
# Author :- Yendhe Anuraj Balasaheb
# Date :- 07/09/2024
######################################################################
def main():
    print("-------------Automation using Python------------")
    print("--------File Subsystems with Job Schedule--------")
    print("Name of script : ",argv[0])
    print("    ")

    if(len(argv) == 2): # validation
        if((argv[1] == "-H") or (argv[1] == "-h")): # flag for help
            print("Help : This automation script is use to delete duplicate file from directory after specified time interval and write name of deleted files into log files.Send that file to specified mail address")
            exit()

        elif((argv[1] == "-U") or (argv[1] == "-u")): # flag for usage
            print('Usage : Name_of_script.py Path_of_directory Time_interval Mail_address')
            print('Example : schedule_with_duplicate_files.py "Anuraj" 50 abyendh@gmail.com')
            exit()

        else:
            print("Error : invalid arguments.")

    elif(len(argv) == 4):
        try:
            schedule.every(int(argv[2])).minutes.do(DirectoryTrevel)
            while True:
                schedule.run_pending()
                time.sleep(1)

        except ValueError:
            print("invalid inputs")

        except Exception as Err:
            print("invalid inputs ",Err)

    else:
        print("Error : invalid numbers of arguments")
        exit()

######################################################################
# Application stater
######################################################################
if __name__ == "__main__":
    main()
