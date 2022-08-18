from re import search
import os

import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common import exceptions
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


## Linkedin ID and PASSWORD
email = ""
password = ""


#csv file creation
job_info = {'Title':"", "Posted: ":"", "Location":"", "Description": ""}
FINAL_JOBCSV= pd.DataFrame(columns=['Title', 'Posted', 'Location', 'Description'], dtype=object)
## Write here the job position and local for searche"

##example below: 
position = "data   scientist"
local = "pakistan"

## formating to linkedin model
position = position.replace(' ', "%20")
#System.setProperty("webdriver.chrome.driver","/usr/bin/chromedriver");
driver = webdriver.Chrome(executable_path="chromedriver")

driver.set_window_size(1920, 1080)
driver.maximize_window()

## Opening linkedin website
## waiting load
time.sleep(2)

driver.get("https://www.linkedin.com/login")
time.sleep(4)

## Search for login and password inputs, send credentions 
driver.find_element(By.ID,'username').send_keys(email)

driver.find_element(By.ID,'password').send_keys(password)
driver.find_element(By.ID,'password').send_keys(Keys.RETURN)
driver.implicitly_wait(10)
time.sleep(20)
driver.get("https://www.linkedin.com/jobs/search/")
"""
driver.find_element(By.XPATH,'//*[@id="global-nav-typeahead"]/input').send_keys("data scientist")
driver.find_element(By.XPATH,'//*[@id="global-nav-typeahead"]/input').send_keys(Keys.RETURN)
driver.find_element(By.XPATH, '//*[@id="search-reusables__filters-bar"]/ul/li[1]/button').click()"""
time.sleep(2)

file_name = ["Arts", ""]
time.sleep(1)
search_div = driver.find_element(By.XPATH, "/html/body/div[5]/header/div/div/div/div[2]/div[1]/div/div/input[1]")
#search_bar = search_div.find_element(By.TAG_NAME, "input")
search_div.send_keys(file_name[0])
search_div.send_keys(Keys.SPACE)
search_div.send_keys(file_name[1])
driver.implicitly_wait(3)
search_button = driver.find_element(By.XPATH, "/html/body/div[5]/header/div/div/div/div[2]/button[1]")
search_button.click()
#time.sleep(10)
#driver.get(f"https://www.linkedin.com/jobs/search/?geoId=101022442&keywords=data%20science")

time.sleep(1)
#panel is the section which contains the search results


# panel_xpath =  '/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div'
panel=driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div')#.find_elements(By.TAG_NAME,"li")#.find_elements(By.CLASS_NAME,"jobs-search-results__list-item occludable-update p0 relative ember-view")

#attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', a)
driver.implicitly_wait(5)    

time.sleep(1)
#jobs is the list of all jobs inside panel


# jobs_xpath = '/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li'
jobs=panel.find_elements(By.XPATH,"/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li")
#print(len(jobs))

time.sleep(1)
def get_pages():

    # pages_xpath =   "/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/section/div/ul/li"
    pages= driver.find_elements(By.XPATH,f"/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div/div/section/div/ul/li")
    return (pages)

pages= get_pages()
page_count = len(pages)
#print(page_count)



def deploy(_page_count):
    j,jobid=0,0
    jobs_desc = []
    jobs_link = []
    jobs_dates = []
    jobs_titles= []
    job_position_status = []
    jobs_posted_by = []
    job_id=[]
    location = []
    posted_date = []
    
    p_c= page_count
    print(page_count)
    if p_c ==0:
        p_c=3
    for l in range(1,p_c-1):
        print("l ",l)
        try:
            time.sleep(2)

            # panel_xpath = '/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div'
            # jobs_xpath = '/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li'

            panel=driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div')
            jobs=panel.find_elements(By.XPATH,"/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li")
            print(len(jobs))
            k= l+1
            print("k: ",k)
            

            # vars = jobs:list , panel

            # returning = jobs_desc, job_titles, jobs_link, jobs_posted_by

            for i in range(len(jobs)):
                j=i+1 # for string literal
                driver.execute_script("arguments[0].scrollIntoView(true);", jobs[i])

                #print THE FUCKING JOB WOOOOOOOOOOOOOOOOOOO
                #card = jobs[i].find_element(By.XPATH, f"/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{i}]")
                
                print("Job NUmber to be clickd:", i)
                card = jobs[i].find_element(By.XPATH, f"/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{j}]")
                card.click()
                time.sleep(1)
                
                job=jobs[i].find_element(By.XPATH, f"/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{j}]/div/div[1]/div[1]/div[2]/div[1]/a")
                jobs_titles.append(job.text)
                jobs_link.append(job.get_attribute('href'))
                time.sleep(1)
                try:
                    posted_by = jobs[i].find_element(By.XPATH, f"/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{j}]/div/div[1]/div[1]/div[2]/div[2]/a")
                    jobs_posted_by.append(posted_by.text)
                except NoSuchElementException as e:
                    posted_by = jobs[i].find_element(By.XPATH, f"/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{j}]/div/div[1]/div[1]/div[2]/div[2]/div")
                    jobs_posted_by.append(posted_by.text)
                driver.implicitly_wait(3)
                
                card_data =driver.find_element(By.XPATH,"/html/body/div[5]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[2]/article/div/div[1]")
                jobs_desc.append(card_data.text)
                job_id.append(jobid)
                
                job_position_info= card_data.find_element(By.XPATH, '/html/body/div[5]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[1]/div/div[1]/div[1]/div[2]/ul/li[1]/span')
                job_position_status.append(job_position_info.text)
                jobid+=1

                posted_on = card_data.find_element(By.XPATH, '/html/body/div[5]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[1]/div/div[1]/div[1]/div[1]/span[2]/span[1]').text
                posted_date.append(posted_on)
                
                job_location_info = card_data.find_element(By.XPATH,'/html/body/div[5]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[1]/div/div[1]/div[1]/div[1]/span[1]/span[2]')
                location.append(job_location_info.text)
            if _page_count !=0:

# moving to next page
  #page 2        /html/body/div[6]/div[3]/div[5]/div/div/main/div/section[1]/div/div[6]/ul
  #page 3        /html/body/div[6]/div[3]/div[5]/div/div/main/div/section[1]/div/div[6]/ul
  #page 4        /html/body/div[6]/div[3]/div[5]/div/div/main/div/section[1]/div/div[6]/
                 

                #pagenumber_div=7/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/section/div/ul/li
                pages= driver.find_elements(By.XPATH,f"/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div/div/section/div/ul/li")    
                if len(pages) ==0:
                    pagenumber_div = 6
                    pages= driver.find_elements(By.XPATH,f"/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div/div/section/div/ul/li")    

                print("number of pages now: ", len(pages))
                driver.implicitly_wait(2) 
                driver.execute_script("arguments[0].scrollIntoView(true);", pages[l])
                print("finding page number ...")
                 
                button = WebDriverWait(pages[l], 200).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div/div/section/div/ul/li[{k}]/button")))    
                print("page number to be clicked is:",button.text, '\n')
                time.sleep(1)
                button.click()
        except StaleElementReferenceException as e:
            pass
    return {'JobId':job_id,'job_descriptions': jobs_desc, 'job links': jobs_link, "job titles":jobs_titles, "Posted By": jobs_posted_by, "Posted Time":posted_date, "Employement Status":job_position_status, "Location": location}


job_to_csv_result = deploy(page_count)    
df = pd.DataFrame.from_dict(job_to_csv_result, orient='index')
df = df.transpose()
df.to_csv(f'JOBS_DATA/{file_name[0]+file_name[1]}.csv')
