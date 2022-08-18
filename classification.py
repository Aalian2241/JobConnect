# Program to measure the similarity between
# two sentences using cosine similarity.
import nltk
from pydantic import NonNegativeInt

nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import textdistance
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# X = input("Enter first string: ").lower()
# Y = input("Enter second string: ").lower()
X = pd.read_csv("JOBDATA.csv")
Y = pd.read_csv("extracted_data.csv")
Y["Job Title"] = None
print(X)
scores = pd.DataFrame({'Y': Y['resume']}, columns=['Job Title', 'X', 'Y', 'Similarity'])

# Temporary variable to store both the highest similarity score, and the 'SAPH' value the score was computed with
highest_score = {"score": 0, "description": ""}

# Iterate though SAP['Description']
print(len(Y['resume']))
for job in Y['resume']:
    
    highest_score = {"score": 0, "description": "", "category": ""}  # Reset highest_score at each iteration
    title=""
    for description, title in zip(X['job_descriptions'], X['job titles']):  # Iterate through SAPH['Description']
        text = [job, description]
        #print("job: ", job)
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text)

        #print("\nSimilarity Scores:")
        #print(cosine_similarity(count_matrix))

        matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
        matchPercentage = round(matchPercentage, 2)  # round to two decimal
        #print("Your resume matches about " + str(matchPercentage) + "% of the job description.")

        # print(highest_score['category'])
        #similarity_score = similar(job, description)  # Get their similarity
        # print(similarity_score, highest_score["score"])

        if matchPercentage > highest_score['score']:  # Check if the similarity is higher than the already saved similarity. If so, update highest_score with the new values

            #print(matchPercentage)
            highest_score['score'] = matchPercentage
            highest_score['description'] = description
            # print(X["Category"])
            highest_score['category'] = title
            #print("highest_score: ",highest_score['category'])

        if matchPercentage == 100:  # If it's a perfect match, don't bother continuing to search.
            break
    # Update the dataframe 'scores' with highest_score
    #print(highest_score)
    print(highest_score['category'])
    print( highest_score['score'])
    scores['X'][scores['Y'] == job] = highest_score['description']
    scores['Job Title'][scores['Y'] == job] = highest_score['category']
    scores['Similarity'][scores['Y'] == job] = highest_score['score']
    Y["Job Title"][scores['Y'] == job] = highest_score['category']

Y.to_csv("extracted_data.csv", index=False)
print(scores)
scores.to_csv('Scores.csv', index=False)