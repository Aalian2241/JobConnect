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

FINAL_JOBCSV= pd.DataFrame(columns=['Title', 'Posted', 'Location', 'Description'])
## Write here the job position and local for searche"

##example below: 
position = ""
local = ""

## formating to linkedin model
position = position.replace(' ', "%20")
#System.setProperty("webdriver.chrome.driver","/usr/bin/chromedriver");
driver = webdriver.Chrome(executable_path="chromedriver")

driver.set_window_size(1920, 1080)
driver.maximize_window()

driver.get('https://pk.indeed.com/jobs?q=Data%20Scientist&vjk=15fb5da94ca8b32c')
time.sleep(30)
page_elements = driver.find_elements(By.XPATH, '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/nav/div/ul/li')
Next_button = driver.find_element(By.XPATH, "//*[@id='resultsCol']/nav/div/ul/li//a[@aria-label='Next']")

time.sleep(1)
j=0
jobs_desc = []
jobs_location=[]
jobs_link = []
jobs_dates = []
jobs_titles= []
jobs_posted_by = []

# popover button
# /html/body/div[5]/div[1]/button

# get total number of jobs to search through from. 
jobs_on_page= driver.find_elements(By.XPATH, "/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[5]/div/a")
# "/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[5]/div/a"

# iterate through each of the job clicking on it and fetch data
i=0
pages=driver.find_elements(By.XPATH, f"/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/nav/div/ul/li")
j=-1111
while j<-1:
    
    # FIND OUT TOTAL NUMBER OF PAGES
    pages=driver.find_elements(By.XPATH, f"/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/nav/div/ul/li")
    print("number of page buttons on screen : ", len(pages))
    time.sleep(4)
    jobs_on_page= driver.find_elements(By.XPATH, "/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[5]/div/a")
    if len(jobs_on_page)==0:
        jobs_on_page= driver.find_elements(By.XPATH, "/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[4]/div/a")
        change_iframe = True
    else:
        change_iframe = False
    ###  looping through jobs on the pages
    print("number of pages on the job are: ", len(jobs_on_page))
    print("clicking on jobs...")
    index=1
    for k in range(len(jobs_on_page)):
        index = k+1
        print("Clicking.")
        # 1.a click on the job
        jobs_on_page[k].click()
        print("Fetching job information... \n")
        time.sleep(2)

        # 1.a.a get job details:
        try:
            job_title = driver.find_element(By.XPATH,f"/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[5]/div/a[{index}]/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[1]/h2/span")
        except:
            job_title = driver.find_element(By.XPATH,f"/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[4]/div/a[{index}]/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[1]/h2/span")
        jobs_titles.append(job_title)

        job_link =  jobs_on_page[k].get_attribute('href')
        jobs_link.append(job_link) 

        job_posted_by = jobs_on_page[k].find_element(By.CLASS_NAME,'companyName')
        job_location = jobs_on_page[k].find_element(By.CLASS_NAME,"companyLocation")
        jobs_location.append(job_location.text)
        jobs_posted_by.append(job_posted_by.text)

        # 1.b Switch to the iframe
        if not(change_iframe):
            frame = driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[5]/div/section/iframe")
        else:
            frame = driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[4]/div/section/iframe")
        driver.switch_to.frame(frame)
        # 1.c fetch job description and append it
        card = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div/div/div/div[1]')
        jobs_desc.append(card.text)

        # 1.d switch back to ddefault screen at end of loop
        driver.switch_to.default_content()
 
    print('moving to next page!')
    j=i-len(pages)+1
    try: # 2 iterate over to the next page 

        
        print("j: ", j)
        time.sleep(1)
        
        # 2.a identify the button
        last_button = pages[j].find_element(By.TAG_NAME, "a" )
        texts=last_button.find_element(By.TAG_NAME,'span').text

        # 2.a.a if the button is the next icon store that
        if len(texts)==0:  
            last_button = pages[-j-1].find_element(By.TAG_NAME, "a" )
            texts=last_button.find_element(By.TAG_NAME,'span').text
        
        print('next page number: ', texts)
        last_button.click()

    except:
        
        print("j: ", j)
        # 2.b if the tagname is b, click that
        if i>=len(pages):
            break
        j+=1
        last_button = pages[j].find_element(By.TAG_NAME, "a" )
        texts=last_button.text
        if len(texts)==0:  
            print('i came in 2nd loop')
            try:
                last_button = pages[-j-1].find_element(By.TAG_NAME, "a")
            except:
                last_button = pages[-j-1].find_element(By.TAG_NAME, "b")
            texts=last_button.text
        
        print('next page numberrr: ', texts)
        last_button.click()

        pass
    i+=1

print ("jobs_links:" ,jobs_link, '\n')
print ("posted_by: ", jobs_posted_by, '\n')
print("jobs_desc: ", jobs_desc)


"""
j=0
for i in jobs_on_page:
    i.click()
    time.sleep(2)

    frame = driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[5]/div/section/iframe")
    driver.switch_to.frame(frame)
    card = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div/div/div/div[1]')
    print(card.text)
    driver.switch_to.default_content()
i=0
pages=driver.find_elements(By.XPATH, f"/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/nav/div/ul/li")

print(len(pages))
time.sleep(1)
last_button = pages[0].find_element(By.TAG_NAME, "b" )
texts = last_button.text
print("text",texts, "  len", len(texts))


while i<len(pages):
        pages=driver.find_elements(By.XPATH, f"/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/nav/div/ul/li")
        print("len of pages : ", len(pages))
        try:
            j=i-len(pages)
            print("j: ", j)
            time.sleep(1)
            last_button = pages[j].find_element(By.TAG_NAME, "a" )
            texts=last_button.find_element(By.TAG_NAME,'span').text
            print("text: ",texts)
            if len(texts)==0:  
                last_button = pages[-j-1].find_element(By.TAG_NAME, "a" )
                texts=last_button.find_element(By.TAG_NAME,'span').text
                print("text: ",texts)
            

            last_button.click()

        except:
            print("i: ",i)
            if i>=len(pages):
                break
            last_button = pages[i].find_element(By.TAG_NAME, "b" ).text
            print(last_button)
            pass
        i+=1



time.sleep(10)


driver.switch_to.frame("vjs-container-iframe")
a= driver.find_element(By.XPATH, "/html/body/div[1]/div")
driver.switch_to.default_content()

"""

#job=f"/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[5]/div/a[{i}]"


