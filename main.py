import requests
from bs4 import BeautifulSoup, SoupStrainer
from time import sleep
import pandas as pd

positions = []
companies = []
locations = []
dates = []

def scrape_data():
    """Scrape the company name, position, location, and date of each entry level job posting on indeed.
    Store each piece of data in a list. Scrape the first 7 pages. 
    """
    #scrape the first 7 pages of indeed. Numbers represent where page starts. Each page change increases start by 10
    pages = [0,10,20,30,40,50,60,70] 
    for page in pages:
        URL = f'https://www.indeed.com/jobs?q=software+engineer&l=United+States&explvl=entry_level&start={page}'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content,'html.parser')
        job_results = soup.find(id='resultsCol')

        job_listings = job_results.find_all('div',class_="jobsearch-SerpJobCard unifiedRow row result")

        for job in job_listings:
            company = job.find('span',class_='company').text.strip()
            companies.append(company)
            
            position = job.find('h2',class_='title').text.strip()
            positions.append(position)
            
            location = getattr(job.find('span',class_="location accessible-contrast-color-location"),'text',None)
            locations.append(location)
            
            date = job.find('span',class_='date').text.strip()
            dates.append(date)
            
            if None in (position,company,location,date):
                continue
        
        sleep(5) #5 second delay between requests to avoid any issues with indeed

def create_dataFrame():
    """Store scraped data in a dictionary then create dataframe from scraped data

    Returns:
        [type]: dataframe with scraped job data
    """
    data_dict = {'Companies':companies, "Positions":positions, "Locations":locations, "Date Posted": dates}
    df = pd.DataFrame(data_dict)
    return df   

def df_to_excel():
    """Convert dataframe to excel file"""
    df = create_dataFrame()
    df.to_excel("/Users/hsmahal/Documents/JobTracker/indeedJobs.xlsx", sheet_name="Sheet_name_1")

def main():
    """Scrape data from Indeed and convert dataframe to excel"""
    scrape_data()
    df_to_excel()

if __name__ == '__main__':
    main()


