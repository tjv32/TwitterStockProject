import tweepy
import csv
import sys
import datetime
import pandas as pd
import numpy as np
import GetOldTweets3 as got3
consumer_key = "d6WTJg4JeWhJAtLWkW2yHEeJi"
consumer_secret = "pgkO3Cf5Z8ntKOcFnVtEwOio4P5WFeKjN4WwGR09CTwDexHjK9"

access_token = "1104541812126031873-05tEwqZA9GrGDkF3clsu3PNsRP0jpJ"
access_token_secret = "rDCjHiYZi18ETAYtDlXcevL70S1mo1VlrK5GEsiKXVJCf"

df = pd.read_csv('constituents_csv.csv')
print(len(df))

import tweepy
# assuming twitter_authentication.py contains each of the 4 oauth elements (1 per line)
#from twitter_authentication import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
api = tweepy.API(auth, wait_on_rate_limit=True)
def search(name, date, datetimes, num):
    i = num
    startDate = date
    endDate = date
    searchQuery = name  # this is what we're searching for
    maxTweets = 400000 # Some arbitrary large number
    tweetsPerQry = 125  # this is the max the API permits
    fName = 'tweets.txt' # We'll store the tweets in a text file.


# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
    sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = 0
    tweet_list = list()
    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))
    
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang = 'en')
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                             lang = 'en')
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1), lang = 'en')
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            lang = 'en')
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                tweet_list.append(tweet)
                #f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                        #'\n')
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break
    tweet_listdf = pd.DataFrame(tweet_list)
    tweet_listdf.to_csv("twitterlistpls")
    #print(type(tweet_list[0]))
    return tweet_list
    



def clean(list1, date, date1, i):
    tweets = []
    tmpTweets1 = list1
    current = date1[i]
    nextday = date1[i+1]
    #print(tmpTweets)
    #print(len(tmpTweets))
    #print(type(tmpTweets[0].created_at))
    #username = sys.argv[1]
    #for tweet in tmpTweets:
        #print(tweet.created_at)
    tmpTweets = list1
    for tweet in tmpTweets:
        if tweet.created_at < nextday and tweet.created_at > current:
            #print("here")
            tweets.append(tweet)

    ##while (tmpTweets[-1].created_at > datetimes[i]):
      #  tmpTweets = api.user_timeline(username, max_id = tmpTweets[-1].id)
       # for tweet in tmpTweets:
        #    if tweet.created_at < datetimes[i+1] and tweet.created_at > [i]:
         #       tweets.append(tweet)
    
    return tweets


query = ''
max_tweets = 1000
#searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]

import datetime
dates = ['2019-04-15','2019-04-16','2019-04-17','2019-04-18','2019-04-19', '2019-04-20']
a = datetime.datetime(2019, 4, 15, 0, 0, 0)
b = datetime.datetime(2019, 4, 16, 0, 0, 0)
c = datetime.datetime(2019, 4, 17, 0, 0, 0)
d = datetime.datetime(2019, 4, 18, 0, 0, 0)
e = datetime.datetime(2019, 4, 19, 0, 0, 0)
f = datetime.datetime(2019, 4, 20, 0, 0, 0)

dates1 = [a,b,c,d,e, f]

df1 = df[:100]
df2 = df[100:200]
df3 = df[200:300]
df4 = df[300:400]
df5 = df[400:]
#print(len(df['Name']))
data = []
for name in df1['Name']:
    list1 = search(name, dates, dates1, 0)

    list2 = clean(list1, dates, dates1, 0)
    for i in range(len(list2)):
    	list2[i] = list2[i].text
    data.append({'name':name,'date':dates[0], 'tweets': list2})
    list3 = clean(list1, dates, dates1, 1)
    for i in range(len(list3)):
    	list3[i] = list3[i].text
    data.append({'name':name,'date':dates[1], 'tweets': list3})
    list4 = clean(list1, dates, dates1, 2)
    for i in range(len(list4)):
    	list4[i] = list4[i].text
    data.append({'name':name,'date':dates[2], 'tweets': list4})
    list5 = clean(list1, dates, dates1, 3)
    for i in range(len(list5)):
    	list5[i] = list5[i].text
    data.append({'name':name,'date':dates[3], 'tweets': list5})
    list6 = clean(list1, dates, dates1, 4)
    for i in range(len(list6)):
    	list6[i] = list6[i].text
    data.append({'name':name,'date':dates[4], 'tweets': list6})
    print(name)
finaldf = pd.DataFrame(data)
print(finaldf.head())
finaldf.to_csv('finaldf1')

data = []
for name in df2['Name']:
    list1 = search(name, dates, dates1, 0)

    list2 = clean(list1, dates, dates1, 0)
    for i in range(len(list2)):
    	list2[i] = list2[i].text
    data.append({'name':name,'date':dates[0], 'tweets': list2})
    list3 = clean(list1, dates, dates1, 1)
    for i in range(len(list3)):
    	list3[i] = list3[i].text
    data.append({'name':name,'date':dates[1], 'tweets': list3})
    list4 = clean(list1, dates, dates1, 2)
    for i in range(len(list4)):
    	list4[i] = list4[i].text
    data.append({'name':name,'date':dates[2], 'tweets': list4})
    list5 = clean(list1, dates, dates1, 3)
    for i in range(len(list5)):
    	list5[i] = list5[i].text
    data.append({'name':name,'date':dates[3], 'tweets': list5})
    list6 = clean(list1, dates, dates1, 4)
    for i in range(len(list6)):
    	list6[i] = list6[i].text
    data.append({'name':name,'date':dates[4], 'tweets': list6})
    print(name)
finaldf = pd.DataFrame(data)
print(finaldf.head())
finaldf.to_csv('finaldf2')


data = []
for name in df3['Name']:
    list1 = search(name, dates, dates1, 0)

    list2 = clean(list1, dates, dates1, 0)
    for i in range(len(list2)):
    	list2[i] = list2[i].text
    data.append({'name':name,'date':dates[0], 'tweets': list2})
    list3 = clean(list1, dates, dates1, 1)
    for i in range(len(list3)):
    	list3[i] = list3[i].text
    data.append({'name':name,'date':dates[1], 'tweets': list3})
    list4 = clean(list1, dates, dates1, 2)
    for i in range(len(list4)):
    	list4[i] = list4[i].text
    data.append({'name':name,'date':dates[2], 'tweets': list4})
    list5 = clean(list1, dates, dates1, 3)
    for i in range(len(list5)):
    	list5[i] = list5[i].text
    data.append({'name':name,'date':dates[3], 'tweets': list5})
    list6 = clean(list1, dates, dates1, 4)
    for i in range(len(list6)):
    	list6[i] = list6[i].text
    data.append({'name':name,'date':dates[4], 'tweets': list6})
    print(name)
finaldf = pd.DataFrame(data)
print(finaldf.head())
finaldf.to_csv('finaldf3')


data = []
for name in df4['Name']:
    list1 = search(name, dates, dates1, 0)

    list2 = clean(list1, dates, dates1, 0)
    for i in range(len(list2)):
    	list2[i] = list2[i].text
    data.append({'name':name,'date':dates[0], 'tweets': list2})
    list3 = clean(list1, dates, dates1, 1)
    for i in range(len(list3)):
    	list3[i] = list3[i].text
    data.append({'name':name,'date':dates[1], 'tweets': list3})
    list4 = clean(list1, dates, dates1, 2)
    for i in range(len(list4)):
    	list4[i] = list4[i].text
    data.append({'name':name,'date':dates[2], 'tweets': list4})
    list5 = clean(list1, dates, dates1, 3)
    for i in range(len(list5)):
    	list5[i] = list5[i].text
    data.append({'name':name,'date':dates[3], 'tweets': list5})
    list6 = clean(list1, dates, dates1, 4)
    for i in range(len(list6)):
    	list6[i] = list6[i].text
    data.append({'name':name,'date':dates[4], 'tweets': list6})
    print(name)
finaldf = pd.DataFrame(data)
print(finaldf.head())
finaldf.to_csv('finaldf4')


data = []
for name in df5['Name']:
    list1 = search(name, dates, dates1, 0)

    list2 = clean(list1, dates, dates1, 0)
    for i in range(len(list2)):
    	list2[i] = list2[i].text
    data.append({'name':name,'date':dates[0], 'tweets': list2})
    list3 = clean(list1, dates, dates1, 1)
    for i in range(len(list3)):
    	list3[i] = list3[i].text
    data.append({'name':name,'date':dates[1], 'tweets': list3})
    list4 = clean(list1, dates, dates1, 2)
    for i in range(len(list4)):
    	list4[i] = list4[i].text
    data.append({'name':name,'date':dates[2], 'tweets': list4})
    list5 = clean(list1, dates, dates1, 3)
    for i in range(len(list5)):
    	list5[i] = list5[i].text
    data.append({'name':name,'date':dates[3], 'tweets': list5})
    list6 = clean(list1, dates, dates1, 4)
    for i in range(len(list6)):
    	list6[i] = list6[i].text
    data.append({'name':name,'date':dates[4], 'tweets': list6})
    print(name)
finaldf = pd.DataFrame(data)
print(finaldf.head())
finaldf.to_csv('finaldf5')

