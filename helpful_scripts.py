# Python program to convert
# text file to pdf file

from importlib.resources import path
import os

from matplotlib.pyplot import text
#Library 2
import job_classifier
# spacy.load('en_core_web_sm')

import pandas as pd




# save FPDF() class into
# a variable pdf
#pdf = FPDF()

# Add a page
#pdf.add_page()

# set style and size of font
# that you want in the pdf
#pdf.set_font("Arial", size = 15)

# open the text file in read mode
#f = open("recognized.txt",encoding='ISO-8859-1').read()

# insert the texts in pdf
#pdf.multi_cell(0,5,f)

# save the pdf with name .pdf
#pdf.output("mygfg.pdf")

def read_directory(user,path):   #path = market/Users/sessionid/uploadtype
    from pathlib import Path
    # print("CWD: ", Path.cwd())  # /home/skovorodkin/stack
    rootdir = path # PATH/EMPLOYER
   
    from pathlib import Path

    #print(Path.cwd())  # /home/skovorodkin/stack
    #files = os.listdir(rootdir)
    file_names = []
    user_names = []
    # print(path)

    # print(os.listdir(rootdir))
    for file in os.listdir(rootdir):
        name = file.split('.')[0]
        user_names.append(name)
        file_names.append(os.path.join(rootdir, file))
    return [file_names, user_names]
#print(dir_list)



def open_pdf_file(file_name):
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage
    from io import StringIO
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    pagenums = set()
    try:
        infile = open(file_name, 'rb')
    except:
        pass
    try:
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
    except:
        pass
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()

    result = []

    for line in text.split('\n'):
        line2 = line.strip()
        if line2 != '':
            result.append(line2)
    return result, text

def open_docx_file(file_name,file_names):
    import docx2txt
    temp = docx2txt.process(file_names[0])
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    text = [t for t in text if len(t) > 1]
    return (text)


def remove_punctuations(line):
    import regex as re
    return re.sub(r'(\.|\,)', '', line)

def preprocess_document(document):
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))

    for index, line in enumerate(document):
        line = line.lower()
        line = remove_punctuations(line)
        line = word_tokenize(line)
        
        while '' in line:
            line.remove('')
            
        #print('line: ', line)
        

        words = [word for word in line if word.isalpha()]
        #print("words: ", words)

        final_line = [j.lower() for j in words if not j in stop_words]
        #print('result: ', final_line, '\n')
        #result.append(final_line)
       # string = ' '.join([str(item) for item in test])
       # print("string: ", string)
       # result =''.join(string)
    
        document[index] = ' '+' '.join(final_line)
    return (document)



def extract_skills(nlp_text, noun_chunks):
    import os
    '''
    Helper function to extract skills from spacy nlp text
    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param noun_chunks: noun chunks extracted from nlp text
    :return: list of skills extracted
    '''
    tokens = [token.text for token in nlp_text if not token.is_stop]
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'skills.csv')) # count skills.csv
    skills = list(data.columns.values)
    skillset = []
    skillsinstring=""
    # check for one-grams
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
            skillsinstring= skillsinstring+' '+''.join(token)
    
    # check for bi-grams and tri-grams
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
            skillsinstring =skillsinstring+' '+''.join(token)
    return ([i.capitalize() for i in set([i.lower() for i in skillset])],skillsinstring)








def get_email(document):
    import regex as re
    #Further optimization to be done.
    emails = []
    pattern = re.compile(r'\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}')
    for line in document:
        matches = pattern.findall(line)
        for mat in matches:
            if len(mat) > 0:
                emails.append(mat)
    #print (emails)
    return (emails)


def add_skills_experience_qualifications(user,_path):
    import model
    import spacy
    nlp = spacy.load('en_core_web_sm')
    from pyresparser import ResumeParser 
    all_experience = []
    skills = []
    email_ids = []
    names=[]
    qualifications =[]
    resume = []
    job_title=[]
    vect_skills = []
    if user == 'employer':
        _path = f"market/{_path}/files"
    # print('path for employer: ', f"{_path}")
    name_func = read_directory(user,_path) 
    file_names = name_func[0]
    print("Reading files to be read ...")
    name_count =0
    for file_name in file_names:
        names.append(name_func[1][name_count])
        name_count+=1
        current = ""    
        append_this=[]
        if file_name.endswith('.pdf'):
            document,textonly = open_pdf_file(file_name)
            
        elif file_name.endswith('.docx'):

            document = open_docx_file(file_name,file_names)
        print("\nFile Read! Proceeding to parse!!! ")
        #RUN SCRIPTS TO GET COLUMN VALUES


        #print("extracting emails...")
        email = get_email(document)
        if len(email)>0:
            email = email[0]
        email_ids.append(email)
        
        print(len(email), type(email))
        
        document = preprocess_document(document)

        #print("extracting experiences...")
        experience = get_experience(document)
        all_experience.append(get_experience(document))

        #print("extracting qualifications")
        qual= get_qualifications(document)
        #print('-------------------------------------------')
        #print(qual)
        qualifications.append(qual)
        #print("All Information Extracted! ")
        
        
        
        #IF EMAIL EXISTS, APPEND IT
        #if len(email) > 0:
         #   email_ids.append(email[0])
        #else:
         #   email_ids.append('')
        
        #EXTRACT SKILLS FROM DOCUMENT

        __nlp         = nlp(textonly)
        noun_chunks = list(__nlp.noun_chunks)
        skills     = extract_skills(__nlp, noun_chunks)


        #print('------------------------------------------------------------------------------------------------------------------------------------')
        #exp=preprocess_document(data['experience'])        
        #all_experience.append(data['experience'])
        
        # print("setting up database")
        vect_skills.append(skills[1])
        current += f"SKILLS: \n {skills[1]}"
        # print(data['skills'], len(data['skills']))
        
        

        current += "\n \n Experience: \n \n "
        # EXPERIENCE
        for i in experience:
            
            current = current + "".join(i)
            #print('experience: ', current)
        
        
        # QUALIFICATIONS
        current += "\n \n Qualifications: \n "
        for k in qual:
            
            for l in k:
                #tokens = word_tokenize(l)
                #print('tokens: \n', tokens)


                #words = [word for word in tokens if word.isalpha()]
                #print("words: \n", words)

                #test = [j for j in words if not j in stop_words]
                #print('result: \n', test)
                
                #string = ' '.join([str(item) for item in test])
                #current += " "+l
                current = current + "".join(l)



        #current.append(get_qualifications(document))


        #print("current array in loop:",current)
        #print (current)
        append_this.append(current)
        resume.append(append_this)
       
        job_title.append(model.deploy_model(skills[1]))   
          


    return {"emails":email_ids,"names":names,"resume":resume,"job title": job_title,"skills":[skills], "all experiences": all_experience, "education/qualifications":qualifications, "vectorized skills":vect_skills}

# exp and qual clash fix needed
def get_experience(document):
    import regex as re
    pattern1 = re.compile(r'(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)(\s|\S)(\d{2,4}).*(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)(\s|\S)(\d{2,4})')
    pattern2 = re.compile(r'(\d{2}(.|..)\d{4}).{1,4}(\d{2}(.|..)\d{4})')
    pattern3 = re.compile(r'(\d{2}(.|..)\d{4}).{1,4}(present)')
    pattern5 = re.compile(r'(\d{2}(.|..)\d{4}).{1,4}(exp.....ce)')
    pattern6 = re.compile(r'(pr....ts)')
    pattern4 = re.compile(r'(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)(\s|\S)(\d{2,4}).*(present)')
    patterns = [pattern1, pattern2, pattern3, pattern4,pattern5,pattern6]
    experience = []
    
    for index, line in enumerate(document):
        for pattern in patterns:
            exp = pattern.findall(line)
            if len(exp) > 0:
                experience.append(document[index:index+4])
    

    return (experience)

def get_qualifications(document):
    

    import regex as re
    pattern1 = re.compile(r'(\d{2}(.|..)\d{4}).{1,4}(present)')
    pattern2 = re.compile(r'(cer........on)')
    pattern3 = re.compile(r'(ed.....on)')
    patterns = [pattern1, pattern2, pattern3]
    qualifications = []
    for index, line in enumerate(document):
        for pattern in patterns:
            exp = pattern.findall(line)
            if len(exp) > 0:
                qualifications.append(document[index:index+4])
    

    return (qualifications)