import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
start = 0
end = 30

resultsList = []

columns = ["Job Title", "Description", "Location", "Company", "Salary", "Rating", "Job Link"]

customFrame = pd.DataFrame(columns=columns)



#Function for getting job titles from BeautifulSoup 'soup' object
def obtainJobTitle(count):
    
    
    #URL to scrape
    jobUrl = "https://ie.indeed.com/jobs?q=junior+developer&l=Ireland&fromage=7&start=" + str(count)
    #Making request to Indeed for developer roles in Ireland posted in the last 7 days
    jobPage = requests.get(jobUrl)
    time.sleep(1)

    #Specifying format for BeautifulSoup
    soup = BeautifulSoup(jobPage.text, "html.parser")
    for div in soup.find_all(name="div", attrs={"class": "row"}):
        jobsListed = []
        num = 1
        for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
            jobsListed.append(a["title"])
        jobSummary = div.find_all(name="div", attrs={"class": "summary"})
        jobDescription = ''
        if jobSummary:
            for li in jobSummary:
                jobDescription = jobDescription + " " + str(li.text.strip().replace("\n", ""))
        
        jobsListed.append(jobDescription)
        jobDescription = ''

        location = div.find_all(name="div", attrs={"class": "location"})
        if len(location) > 0:
            for jobLocation in location:
                jobsListed.append(jobLocation.text.strip())
        else:
            jobsListed.append("No Location Provided")
        company = div.find_all(name="span", attrs={"class": "company"})
        if company:
            for companyTitle in company:
                jobsListed.append(companyTitle.text.strip())
        salary = div.find_all(name="span", attrs={"class": "salaryText"})
        if salary:
            for jobSalary in salary:
                jobsListed.append(jobSalary.text.strip())
        else:
            jobsListed.append("Salary Not Provided")
        rating = div.find_all(name="span", attrs={"class": "ratingsContent"})
        if rating:
            for jobRating in rating:
                jobsListed.append(jobRating.text.strip())
        else:
            jobsListed.append("Rating not provided")
        
        jobId = div.attrs["data-jk"]
        jobsListed.append("https://ie.indeed.com/viewjob?jk=" + str(jobId))
       
        resultsList.append(jobsListed)
        
        jobsListed = []
        num = num + 1
        
   


for jobQueryNumber in range(start, end, 10):
    obtainJobTitle(jobQueryNumber)

#print(resultsList)
frameCount = 1
for jobResult in resultsList:
    customFrame.loc[frameCount] = jobResult
    frameCount = frameCount + 1

customFrame.to_csv("./test.csv", encoding="utf-8")




