import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
import config


import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

start = 0
end = 30

resultsList = []
jobIds = []

columns = ["Job Title", "Location", "Company", "Salary", "Rating", "Job Link", "Description"]

customFrame = pd.DataFrame(columns=columns)
pd.set_option('max_colwidth', 40)



#Function for getting job titles from BeautifulSoup 'soup' object
def obtainJobTitle(count):
    
    
    #URL to scrape
    jobUrl = "https://ie.indeed.com/jobs?q=junior+developer&l=Ireland&fromage=1&start=" + str(count)
    #Making request to Indeed for junior developer roles in Ireland posted in the last 24 hours
    jobPage = requests.get(jobUrl)
    time.sleep(1)

    #Specifying format for BeautifulSoup
    soup = BeautifulSoup(jobPage.text, "html.parser")
    for div in soup.find_all(name="div", attrs={"class": "row"}):
        #Setting empty list for job information
        jobsListed = []
        num = 1

        #Scraping job title
        for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
            jobsListed.append(a["title"])
        
        #Scraping job location (if available)
        location = div.find_all(name="div", attrs={"class": "location"})
        if len(location) > 0:
            for jobLocation in location:
                jobsListed.append(jobLocation.text.strip())
        else:
            jobsListed.append("No Location Provided")
        company = div.find_all(name="span", attrs={"class": "company"})

        #Scraping company title
        if company:
            for companyTitle in company:
                jobsListed.append(companyTitle.text.strip())
        
        #Scraping job salary (if available)
        salary = div.find_all(name="span", attrs={"class": "salaryText"})
        if salary:
            for jobSalary in salary:
                jobsListed.append(jobSalary.text.strip())
        else:
            jobsListed.append("Salary Not Provided")
        
        #Scraping company rating (if available)
        rating = div.find_all(name="span", attrs={"class": "ratingsContent"})
        if rating:
            for jobRating in rating:
                jobsListed.append(jobRating.text.strip())
        else:
            jobsListed.append("Rating not provided")
        
        #Scraping job id and constructing url for viewing job
        jobId = div.attrs["data-jk"]
        jobsListed.append("https://ie.indeed.com/viewjob?jk=" + str(jobId))
        if jobId not in jobIds:
            jobIds.append(jobId)
            resultsList.append(jobsListed)
        #Scraping high level overview of position
        jobSummary = div.find_all(name="div", attrs={"class": "summary"})
        jobDescription = ''
        if jobSummary:
            for li in jobSummary:
                jobDescription = jobDescription + " " + str(li.text.strip().replace("\n", ""))
        
        jobsListed.append(jobDescription)
        jobDescription = ''
            
    
        
        jobsListed = []
        num = num + 1
        
   


for jobQueryNumber in range(start, end, 10):
    obtainJobTitle(jobQueryNumber)


frameCount = 1
for jobResult in resultsList:
    customFrame.loc[frameCount] = jobResult
    frameCount = frameCount + 1

customFrame.to_csv("./test.csv", encoding="utf-8")

def emailCsv(filePath, fromEmail, toEmail):
    fromaddr = fromEmail
    toaddr = toEmail
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 
    # storing the senders email address   
    msg['From'] = fromaddr 
    # storing the receivers email address  
    msg['To'] = toaddr 
    # storing the subject  
    msg['Subject'] = "Junior Developer Roles - Last 24 hours"
    # string to store the body of the mail 
    body = "Attached file contains junior developer roles posted on Indeed in the past 24 hours."
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
    # open the file to be sent  
    filename = "juniorDeveloperRoles.csv"
    #attachment = open("./test.csv", "rb") 
    attachment = open(filePath, "rb")
    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 
    # To change the payload into encoded form 
    p.set_payload((attachment).read()) 
    # encode into base64 
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    # attach the instance 'p' to instance 'msg' 
    msg.attach(p) 
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    # start TLS for security 
    s.starttls() 
    # Authentication 
    s.login(fromaddr, config.emailPassword)
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
    # terminating the session 
    s.quit() 

emailCsv("./test.csv", "indeedjuniordeveloperroles@gmail.com", "johndennehy101@gmail.com")








