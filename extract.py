def deploy_ext(user,_path):
    import os
    import sys
    file_dir = os.path.dirname(__file__)
    sys.path.append(file_dir)

    from helpful_scripts import add_skills_experience_qualifications
    import time
    t1 = time.time()

    import pandas as pd
    a =add_skills_experience_qualifications(user, f"{_path}/{user}")
    t2 = time.time()
    t = t2-t1
    print(t)
    df = pd.DataFrame.from_dict(a, orient='index')
    df = df.transpose()
    
    from pathlib import Path
    print("CWD: ", Path.cwd()) 
    print(_path)

    if user == 'employer':
        df.to_csv(f'market/{_path}/extracted_data_employer.csv')
    else:
        df.to_csv(f'{_path}/extracted_data.csv')
