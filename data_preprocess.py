import pandas as pd
import os

file_path = os.path.join("data", "reviews_reviews_package.com.example_202410.csv")
df = pd.read_csv(file_path, encoding='utf-16')

df[['Package Name', 'App Version Code', 'App Version Name',
       'Reviewer Language', 'Device', 'Review Submit Date and Time',
       'Review Submit Millis Since Epoch', 'Review Last Update Date and Time',
       'Review Last Update Millis Since Epoch', 'Review Title', 'Developer Reply Date and Time',
       'Developer Reply Millis Since Epoch', 'Developer Reply Text',
       'Review Link']] = 'Confidential'

df.to_csv('october_reviews_record.csv')