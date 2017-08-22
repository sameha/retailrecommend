import sqlite3
import pandas as pd
import gzip
import datetime

def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield eval(l)

def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')

df_electronic = getDF('Resources/Datasets/Amazon/reviews_Electronics_5.json.gz')
print('loaded Electronics DB')
df_metadata = getDF('Resources/Datasets/Amazon/metadata.json.gz')
print('loaded Metadata DB')

conn = sqlite3.connect('retailrecommend/db.sqlite3') #connected to database with out error
cur = conn.cursor()

print ('Starting to populate the data')
electronic_dict = {}
electronic_id_index = 1
for i in range(len(df_electronic)):
#for i in range(100000):
    if (i % 1000 == 0): print(i)
    review_id = i + 1
    pub_date = datetime.datetime.fromtimestamp(int(df_electronic.iloc[i]['unixReviewTime'])).strftime('%Y-%m-%d %H:%M:%S')
    user_id = df_electronic.iloc[i]['reviewerID']
    user_name = df_electronic.iloc[i]['reviewerName']
    # for now let's just take the summary of the comment
    comment = df_electronic.iloc[i]['summary']
    rating = int(df_electronic.iloc[i]['overall'])
    electronic_asin = df_electronic.iloc[i]['asin']

    if electronic_dict.has_key(electronic_asin):
        electronic_id = electronic_dict[electronic_asin]
    else:
        electronic_dict[electronic_asin] = electronic_id_index
        electronic_id = electronic_id_index
        electronic_name = df_metadata.loc[df_metadata['asin'] == electronic_asin]['title']
        electronic_imurl = df_metadata.loc[df_metadata['asin'] == electronic_asin]['imUrl']
        SQL = "insert into reviews_electronic values (?, ?, ?, ?)"  # Note: no quotes
        data = [electronic_id_index, electronic_name.to_string(), electronic_asin, electronic_imurl.to_string()]
        cur.execute(SQL, data)
        conn.commit()
        electronic_id_index += 1



    if type(user_name) is str:
        SQL = "insert into reviews_review values (?, ?, ?, ?, ?, ?, ?)"  # Note: no quotes
        data = [review_id, user_id, user_name, electronic_id, pub_date, comment, rating]
        cur.execute(SQL, data)
        conn.commit()

cur.close()
conn.close()

#cur.execute("select * from reviews_review;")
#results = cur.fetchall()
#print(results)

#cur.execute("SELECT * FROM reviews_review ORDER BY id DESC LIMIT 1;")
#results = cur.fetchall()
# Last ID
#print(results[0][0])

# (4, u'2017-08-09 05:28:23.570262', u'tvoer', u'nice tv, bad colors', 4, 2)
#cur.execute("insert into reviews_review values (7, '2017-11-21 12:28:23.570262', 'sameh', 'amazin bees', 5, 3)")
#conn.commit()
#print(cur.lastrowid)

#cur.execute("select * from reviews_review;")
# cur.execute("insert into reviews_review values (7, '2017-11-21 12:28:23.570262', 'sameh', 'amazin bees', 5, 3)")


#results = cur.fetchall()
#print(results)
# reviewerID, asin, reviewerName, helpful, unixReviewTime, reviewText, overall, reviewTime, summary
#print df_electronic.keys()

# Prints first row
#print df_electronic.iloc[0]

# 1689188 rows
#print len(df_electronic)

#print df_electronic[1]

