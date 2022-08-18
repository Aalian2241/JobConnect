import joblib
import pandas as pd


test_file = pd.read_csv('extracted_data.csv')
xgb = joblib.load('svmmodel.pkl')
print(xgb)

tfidfvectorizer_r = joblib.load('tfidf_model.pkl')
print(tfidfvectorizer_r)

labencodermodel = joblib.load('label_encoder_model.pkl')
print(labencodermodel)

countvectorizer_r = joblib.load('countvectorizer_r.pkl')
print(countvectorizer_r)

# labencodermodel.inverse_transform([n])  to reverse the transformation

# convert to series
test = pd.Series(test_file['vectorized skills'][0])

# for testing


count_wm_X_test_tfidf = countvectorizer_r.transform(test.astype('U'))
tfidf_wm_X_test_tfidf = tfidfvectorizer_r.transform(test.astype('U'))
#print(tfidf_wm_r)
count_tokens_X_test_count = countvectorizer_r.get_feature_names()
tfidf_tokens_X_test_tfidf = tfidfvectorizer_r.get_feature_names()
print(tfidf_wm_X_test_tfidf.shape)
df_countvect_r = pd.DataFrame(data = count_wm_X_test_tfidf.toarray(),columns = count_tokens_X_test_count)
df_tfidfvect_r = pd.DataFrame(data = tfidf_wm_X_test_tfidf.toarray(),columns = tfidf_tokens_X_test_tfidf)#X_test_count = countvectorizer_r.fit(X_train)

print(df_tfidfvect_r)

pred_result = xgb.predict(df_tfidfvect_r)
print(pred_result)
import numpy as np
decoded= labencodermodel.inverse_transform([pred_result])
print(decoded[:][0])