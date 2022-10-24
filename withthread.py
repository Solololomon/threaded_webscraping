import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import threading
import time
from nothread import nothreadtime

start_time = time.time()

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")
job_elements = results.find_all("div", class_="card-content")

URLs = []
loops = 1
jobs = {'job_id': [], 'title': [], 'company': [], 'location': [], 'description': [], 'url': []}
for job_element in job_elements:
    title_element = job_element.find("h2", class_="title")
    title_element = title_element.text.strip()
    company_element = job_element.find("h3", class_="company")
    company_element = company_element.text.strip()
    location_element = job_element.find("p", class_="location")
    location_element = location_element.text.strip()
    url_element = job_element.find(attrs={'href': re.compile("^https://")}, string='Apply')
    url_element = url_element.get('href')
    jobs['job_id'].append(loops)
    jobs['title'].append(title_element)
    jobs['company'].append(company_element)
    jobs['location'].append(location_element)
    jobs['url'].append(url_element)
    loops += 1

def find_description(start, end):
    for url in jobs['url'][start:end]:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="ResultsContainer")
        job_elements = results.find_all("div", class_="content")
        for job_element in job_elements:
            description = results.find('p', string='')
            description = description.text.strip()
            jobs['description'].append(description)

trd1 = threading.Thread(target=find_description, args=[0, 20])
trd2 = threading.Thread(target=find_description, args=[20, 40])
trd3 = threading.Thread(target=find_description, args=[40, 60])
trd4 = threading.Thread(target=find_description, args=[60, 80])
trd5 = threading.Thread(target=find_description, args=[80, 100])

trd1.start()
trd2.start()
trd3.start()
trd4.start()
trd5.start()


trd1.join()
trd2.join()
trd3.join()
trd4.join()
trd5.join()

df = pd.DataFrame(jobs, columns=['job_id', 'title', 'company', 'location', 'description', 'url'])
#print(df.to_string(index=False))

print("With threading, this took %s seconds" % (time.time() - start_time))
