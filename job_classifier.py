import json
import requests
import pandas as pd
import json



#a=pd.DataFrame(job_categories).to_json('data.json')
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer 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"}

f = open('data.json')
 
# returns JSON object as
# a dictionary
data = json.load(f)
#unique job categories
job_categories = ['Data Science', 'HR', 'Advocate', 'Arts', 'Web Designing', 'Mechanical Engineer', 'Sales', 'Health and fitness', 'Civil Engineer', 'Java Developer', 'Business Analyst', 'SAP Developer', 'Automation Testing', 'Electrical Engineering', 'Operations Manager', 'Python Developer', 'DevOps Engineer', 'Network Security Engineer', 'PMO', 'Database', 'Hadoop', 'ETL Developer', 'DotNet Developer', 'Blockchain', 'Testing']

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    while response.status_code ==503:
        response = requests.post(API_URL, headers=headers, json=payload)
        print(response)
    return response.json()

def job_classify(resume_text):
    try:
        _data = query(
            {
                "inputs": {
                    "source_sentence": resume_text,
                    "sentences": job_categories
                }
            })
    except:
        import time
        time.sleep(20)
        _data = query(
            {
                "inputs": {
                    "source_sentence": resume_text,
                    "sentences": job_categories
                }
            })
#print(_data)


    # index of the matching job title with resume    
    matching_title_index= _data.index(max(_data))


    # job of resume, the .json file has enumarated so we find through indexing :)
    search_this = data['0'][str(matching_title_index)]
    #print(search_this)
    return search_this

f.close()
