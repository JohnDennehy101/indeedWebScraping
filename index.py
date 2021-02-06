import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

#URL to scrape
jobUrl = "https://ie.indeed.com/jobs?q=junior+developer&l=Ireland&fromage=7"

#Making request to Indeed for developer roles in Ireland posted in the last 7 days
jobPage = requests.get(jobUrl)

#Specifying format for BeautifulSoup
soup = BeautifulSoup(jobPage.text, "html.parser")

#Function for getting job titles from BeautifulSoup 'soup' object
def obtainJobTitle(soup):
    jobsListed = []
    for div in soup.find_all(name="div", attrs={"class": "row"}):
        for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
            jobsListed.append(a["title"])
    print(jobsListed)


obtainJobTitle(soup)

