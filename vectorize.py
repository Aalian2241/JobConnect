
## For employer
## X = jobs["job_descriptions"]
## Y = resumes["resume"][[0]]

from pathlib import Path

from matplotlib.pyplot import text

# print("CWD: ", Path.cwd()) 
from helpful_scripts import open_pdf_file, open_docx_file, read_directory

def deploy(user,_path, empupload):
        
    from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
    import pandas as pd

    import numpy as np

    
    #print(resumes)
    

    ################################################################
    tfidfvectorizer_r = TfidfVectorizer(analyzer='word',stop_words= 'english')
    countvectorizer_r = CountVectorizer(analyzer= 'word', stop_words='english')
    if user == 'employer':
    # for seeker
    # X = resumes["resume"][[0]]
    # y = jobs["job_descriptions"]
    # for employer
        name_func = read_directory(user,f"{_path}/employer/desc") 
        file_names = name_func[0]
        if file_names[0].endswith('.pdf'):
            document,textonly = open_pdf_file(file_names[0])
        X = textonly
        X=[X]   
        resumes = pd.read_csv(f'{_path}/extracted_data_employer.csv')
        y = resumes["resume"]   
    else:
        resumes = pd.read_csv(f"{_path}/extracted_data.csv")
        file_to_read = resumes['job title'][0]
        jobs=pd.read_csv(f"JOBS_DATA/{file_to_read}.csv")
    
        X = resumes["resume"][[0]]
       #  print(jobs.head())
        y = jobs["job_descriptions"]          
        print(y)

    # vector=pd.DataFrame({'job': jobs['job_descriptions']}, columns=['vector'],dtype=object)

    #in this section, poooooooooooore csv ka ek single file hai
    count_wm_r = countvectorizer_r.fit_transform(X)
    tfidf_wm_r = tfidfvectorizer_r.fit_transform(X)

    count_tokens_r = countvectorizer_r.get_feature_names()
    tfidf_tokens_r = tfidfvectorizer_r.get_feature_names()

    df_countvect_r = pd.DataFrame(data = count_wm_r.toarray(),columns = count_tokens_r)
    df_tfidfvect_r = pd.DataFrame(data = tfidf_wm_r.toarray(),columns = tfidf_tokens_r)
    #print(df_tfidfvect_r.shape)
    #print("Count Vectorizer\n")
    #print(df_countvect_r)
    #print("\nTD-IDF Vectorizer\n")
    #print(df_tfidfvect_r)
    ##############################################################3



    tfidfvectorizer = TfidfVectorizer(analyzer='word',stop_words= 'english')
    countvectorizer = CountVectorizer(analyzer= 'word', stop_words='english')


    # vector=pd.DataFrame({'job': jobs['job_descriptions']}, columns=['vector'],dtype=object)

    #in this section, poooooooooooore csv ka ek single file hai

    try:
        count_wm = countvectorizer.fit_transform(y)
        tfidf_wm = tfidfvectorizer.fit_transform(y)
    except:
        pass
    count_tokens = countvectorizer.get_feature_names()
    tfidf_tokens = tfidfvectorizer.get_feature_names()

    df_countvect = pd.DataFrame(data = count_wm.toarray(),columns = count_tokens)
    df_tfidfvect = pd.DataFrame(data = tfidf_wm.toarray(),columns = tfidf_tokens)
    #print(df_tfidfvect.shape)
    #print("Count Vectorizer\n")
    #print(df_countvect)
    #print("\nTD-IDF Vectorizer\n")
    #print(df_tfidfvect)

    ################################################33
    """

    #for each job description
    for description in jobs["job_descriptions"]:
        #a=description.splitlines()
        #print(len(a))
        count_wm = countvectorizer.fit_transform([description])
        tfidf_wm = tfidfvectorizer.fit_transform([description])

        count_tokens = countvectorizer.get_feature_names()
        tfidf_tokens = tfidfvectorizer.get_feature_names()

        df_countvect = pd.DataFrame(data = count_wm.toarray(),columns = count_tokens)
        df_tfidfvect = pd.DataFrame(data = tfidf_wm.toarray(),columns = tfidf_tokens)
        print("Count Vectorizer\n")
        print(df_countvect)
        print("\nTD-IDF Vectorizer\n")
        print(df_tfidfvect)
    """
    from sklearn.metrics.pairwise import linear_kernel
    # print(type(df_tfidfvect[0:1]))
    # print(df_tfidfvect[0:1].shape)


    # columns in jobs file to be resized 
    job_cl= df_tfidfvect.shape[1]
    arr= np.resize(df_countvect_r,(1,job_cl) )
    # print(arr.shape)
    cosine_similarities = linear_kernel(arr,df_tfidfvect).flatten()
    #print(cosine_similarities)
    if user != 'employer':
        related_docs_indices = cosine_similarities.argsort()[:-20:-1]
    else:
        related_docs_indices = cosine_similarities.argsort()[::]

    #print("related ",related_docs_indices)
    #print(cosine_similarities[related_docs_indices])
    #print(a[111], '\n ------------------------------------', resumes["resume"][0])
    
    ranks = dict(zip(cosine_similarities[related_docs_indices], related_docs_indices))
    #print(ranks)


    if user == 'employer':
        _jobs = {
            'Email': [],
            'Resume Id' : [],
            'Job Title' : [],
            'Resume Rank' : [],
            "Job Connect's Score":[]
            #'Job Id: ': []

            }
        count =0
        for i in related_docs_indices:
            _jobs['Job Title'].append(resumes['job title'][count])
            _jobs['Email'].append(resumes['emails'][count])
            _jobs['Resume Rank'].append(len(related_docs_indices)-count)
            _jobs['Resume Id'].append(count)
            _jobs["Job Connect's Score"].append(cosine_similarities[i])
            count+=1
            #_jobs['Posted By: '].append(jobs["Posted By"][i])
            #_jobs['Apply Here: '].append(jobs["job links"][i])
            #_jobs['Job Id: '].append(jobs["JobID"][i])
        
    else:
        _jobs = {
            "Job_Category":file_to_read,
            'Posted By: ' : [],
            'Job Title: ' : [],
            'Salary: ' : [],
            'Apply Here: ': [],
            'Location: ': [],
            'Experience: ':[],
            'Posted Time: ':[]
            
            #'Job Id: ': []

        }
        for i in related_docs_indices:
            _jobs['Apply Here: '].append(jobs["job links"][i])
            _jobs['Job Title: '].append(jobs["job titles"][i])
           # print(jobs["job titles"][i])
            _jobs['Posted By: '].append(jobs["Posted By"][i])
            _jobs['Posted Time: '].append(jobs['Posted Time'][i])
            _jobs['Location: '].append(jobs['Location'][i])
            _jobs['Experience: '].append(jobs['Employement Status'][i])

            #_jobs['Desc'].append(jobs['job_descriptions'][i])
            #_jobs['Apply Here: '].append(jobs["job links"][i])
            #_jobs['Job Id: '].append(jobs["JobID"][i])
    #print(_jobs)
    df = pd.DataFrame.from_dict(_jobs, orient='index')
    df = df.transpose()

    df.to_excel('market/outputs/result.xlsx')
    return _jobs

