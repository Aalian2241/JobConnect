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

driver.get("https://www.linkedin.com/jobs/search/")
"""
driver.find_element(By.XPATH,'//*[@id="global-nav-typeahead"]/input').send_keys("data scientist")
driver.find_element(By.XPATH,'//*[@id="global-nav-typeahead"]/input').send_keys(Keys.RETURN)
driver.find_element(By.XPATH, '//*[@id="search-reusables__filters-bar"]/ul/li[1]/button').click()"""
time.sleep(2)
time.sleep(2)
#panel is the section which contains the search results
panel=driver.find_element(By.XPATH,'/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div')#.find_elements(By.TAG_NAME,"li")#.find_elements(By.CLASS_NAME,"jobs-search-results__list-item occludable-update p0 relative ember-view")
#attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', a)
driver.implicitly_wait(5)    

time.sleep(1)
#jobs is the list of all jobs inside panel

jobs=panel.find_elements(By.XPATH,"/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li")
#print(len(jobs))

time.sleep(1)
def get_pages():
    
    pages= driver.find_elements(By.XPATH,f"/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/div[7]/ul/li")
    return (pages)

pages= get_pages()
page_count = pages[-1].text
#print(page_count)



def deploy(_page_count):
    j,jobid=0,0
    jobs_desc = []
    jobs_link = []
    jobs_dates = []
    jobs_titles= []
    jobs_posted_by = []
    job_id=[]

    
    p_c= 40
    final_stage =2
    print(page_count)
    if p_c ==0:
        p_c=3
    for l in range(1,p_c-1):
        print("l ",l)
        try:
            time.sleep(2)
            panel=driver.find_element(By.XPATH,'/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div')
            jobs=panel.find_elements(By.XPATH,"/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li")
            print(len(jobs))
            k= l+1
            
            # k is the next page   /html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1] 

            if l>=9 and l<33:
                k=7
            elif l>=33:
                final_stage+=1
                k=final_stage
            print("k: ",k)
            

            # vars = jobs:list , panel

            # returning = jobs_desc, job_titles, jobs_link, jobs_posted_by

            for i in range(len(jobs)):
                j=i+1 # for string literal
                driver.execute_script("arguments[0].scrollIntoView(true);", jobs[i])

                #print THE FUCKING JOB WOOOOOOOOOOOOOOOOOOO
                #card = jobs[i].find_element(By.XPATH, f"/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{i}]")
                
                print("Job NUmber to be clickd:", i)
                
                card = jobs[i].find_element(By.XPATH, f"/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{j}]/div/div[1]/div[1]/div[2]/div[1]/a")
                print('Clicking Job Card!', card.text)
                card.click()
                time.sleep(1)

                print('Clicked!!! extracting data \n')
                job=jobs[i].find_element(By.XPATH, f"/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{j}]/div/div[1]/div[1]/div[2]/div[1]/a")
                jobs_titles.append(job.text)
                jobs_link.append(job.get_attribute('href'))
                time.sleep(1)
                try:
                    posted_by = jobs[i].find_element(By.XPATH, f"/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{j}]/div/div[1]/div[1]/div[2]/div[2]/a")
                    jobs_posted_by.append(posted_by.text)
                except NoSuchElementException as e:
                    posted_by = jobs[i].find_element(By.XPATH, f"/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{j}]/div/div[1]/div[1]/div[2]/div[2]/div")
                    jobs_posted_by.append(posted_by.text)
                driver.implicitly_wait(3)
                card_data =driver.find_element(By.XPATH,"/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[2]/div/div[2]/div[1]/div/div[2]/article/div/div[1]")
                jobs_desc.append(card_data.text)
                job_id.append(jobid)
                jobid+=1
            if _page_count !=0:

# moving to next page
  #page 2        /html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/div[6]/ul
  #page 3        /html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/div[6]/ul
  #page 4        /html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/div[6]/
                 

                pagenumber_div=7
                pages= driver.find_elements(By.XPATH,f"/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/div[{pagenumber_div}]/ul/li")    
                if len(pages) ==0:
                    pagenumber_div = 6
                    pages= driver.find_elements(By.XPATH,f"/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/div[{pagenumber_div}]/ul/li")    

                print("number of pages now: ", len(pages))
                driver.implicitly_wait(2) 
                if l<10:
                    driver.execute_script("arguments[0].scrollIntoView(true);", pages[l])
                    button = WebDriverWait(pages[l], 200).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/div[{pagenumber_div}]/ul/li[{k}]/button")))    

                elif 10<=l<33 :
                    driver.execute_script("arguments[0].scrollIntoView(true);", pages[7])
                    button = WebDriverWait(pages[7], 200).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/div[{pagenumber_div}]/ul/li[{k}]/button")))    
                elif l>=33:
                    driver.execute_script("arguments[0].scrollIntoView(true);", pages[k])
                    button = WebDriverWait(pages[k], 200).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/div[{pagenumber_div}]/ul/li[{k}]/button")))    

                    

                print("finding page number ...")
                 
                
                print("page number to be clicked is:",button.text, '\n')
                time.sleep(1)
                button.click()
        except NoSuchElementException as e:
            print(e)
            pass
    return {'JobId':job_id,'job_descriptions': jobs_desc, 'job links': jobs_link, "job titles":jobs_titles, "Posted By": jobs_posted_by}


job_to_csv_result = deploy(40)    
df = pd.DataFrame.from_dict(job_to_csv_result, orient='index')
df = df.transpose()
df.to_csv('COMPLETE_LINKEDIN.csv')
