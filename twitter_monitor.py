'''

Uses the Twitter API to get tweet data and then puts the data into Airtable

'''

import datetime
import dateutil.relativedelta
import time
import requests
import re
import numpy as np
import math
from collections import Counter
from pyairtable import Table
from pyairtable.formulas import match
import json
import os

# vvv SET YOUR PARAMS HERE vvv
# ============================
usernames = [
  "MakeThatWorkEng",
  "Apple",
  "Google",
  "NASA",
  "Tesla",
  "TheManufacturer",
  "TheEngineerUK"
]

# AIRTABLE PARAMSs
TABLE = "Twitter Monitor"
BASE = os.environ["TWITTER_BASE_ID"]
API_KEY = os.environ["AIRTABLE_API_KEY"]

# Connect to Airtable
table = Table(API_KEY, BASE, TABLE)

# TWITTER PARAMS
auth_header = "Bearer " + os.environ["TWITTER_KEY"]
headers = {"Authorization": auth_header}
DESIRED_RESULTS = 1000
MAX_RESULTS = "100"
ROUNDS = math.ceil(int(DESIRED_RESULTS)/100) # how many rounds to go through to get to the max number of results 
base_url = "https://api.twitter.com/2/"

# ^^^ MAKE SURE YOUR PARAMS ARE SET ABOVE ^^^
# ===========================================

def find_hashtags_in_tweet(a_tweet):
    split_tweet = re.split("[\s:/,.:]", a_tweet)
    
    return [s for s in split_tweet if len(s)>1 and s[0]=="#"]

def find_mentions_in_tweet(a_tweet):
    split_tweet = re.split("[\s:/,.:]", a_tweet)

    return [s for s in split_tweet if len(s)>1 and s[0]=="@"]

def find_words_in_tweet(a_tweet):
    split_tweet = re.split("[\s:/,.:]", a_tweet)

    return split_tweet

# LOOP FOR EACH USERNAME
for u in usernames:
    USERNAME = u

    # AIRTABLE STUFF PART 1
    # if there is already a record we need to get the timestamp
    formula = match({"Username": USERNAME})

    my_rec = table.first(formula=formula)

    NOW = datetime.datetime.utcnow()
    time_now = NOW.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    all_records_for_accountname = table.all(formula=formula, sort=["Timestamp"])


    if len(all_records_for_accountname)>0:
        print("record exists")
        last_record = all_records_for_accountname[-1]
        time_from = last_record["fields"]["Timestamp"]
    else:
        print("no existing record found")
        time_from = (NOW + dateutil.relativedelta.relativedelta(months=-1)).strftime("%Y-%m-%dT%H:%M:%SZ")

    # TWITTER STUFF
    PAG_TOKEN = ""

    account_collection = {
        "username": "",
        "description": "",
        "followers": 0,
        "av_likes": 0,
        "av_replies": 0,
        "av_retweet": 0,
        "av_quotes": 0,
        "num_posts_last_30_days": 0,
        "top_ten_liked": [],
        "top_ten_replied_to": [],
        "top_ten_quoted": [],
        "top_ten_retweeted": [],
        "top_ten_hashtags_used": [],
        "top_ten_mentioned": [],
        "offer_tweets": [],
        "date_from": "2022-01-01T09:00:00Z",
        "date_to": "",
        "date_now": "",
        "ten_most_recent_tweets": []
    }

    account_collection["date_from"] = time_from
    account_collection["date_to"] = time_now
    account_collection["date_now"] = time_now
    
    user_lookup = "users/by/username/" + USERNAME

    r = requests.get(base_url + user_lookup, headers=headers)

    user_id = r.json()["data"]["id"]
    user_data_url = base_url + "users/" + user_id + "?user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
    user_data = requests.get(user_data_url, headers=headers)
    user_data = user_data.json()

    num_followers = user_data["data"]["public_metrics"]["followers_count"]
    description = user_data["data"]["description"]

    account_collection["followers"] = num_followers
    account_collection["description"] = description

    # LOOP FOR GETTING TWEET DATA
    tweet_data = []

    for i in range(0,ROUNDS):
        if i==0:
            tweet_timeline = "users/" + user_id + "/tweets?start_time=" + time_from + "&exclude=retweets,replies&max_results=" + MAX_RESULTS + "&expansions=attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id&tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld" #&pagination_token=7140dibdnow9c7btw421dwu5n9nhkozgotv8vo4uapx69"
        else:
            if PAG_TOKEN == "":
                print("no more tweets for " + USERNAME)
                break
            tweet_timeline = "users/" + user_id + "/tweets?start_time=" + time_from + "&exclude=retweets,replies&max_results=" + MAX_RESULTS + "&expansions=attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id&tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld&pagination_token=" + PAG_TOKEN

        rtweets = requests.get(base_url + tweet_timeline, headers=headers)

        if "data" in rtweets.json():
            tweet_data = tweet_data + rtweets.json()["data"]
        if "next_token" in rtweets.json()["meta"]:
            PAG_TOKEN = rtweets.json()["meta"]["next_token"]

    all_words = []
    tweets_of_interest = []

    if len(tweet_data)==0:
        continue

    for t in tweet_data:

        all_words.append(t["text"])

        likes = t["public_metrics"]["like_count"]
        retweet = t["public_metrics"]["retweet_count"]
        quotes = t["public_metrics"]["quote_count"]
        replies = t["public_metrics"]["reply_count"]
        created_time = t["created_at"]

        hashtags = find_hashtags_in_tweet(t["text"])


    account_collection["ten_most_recent_tweets"] = tweet_data[0:10]

    likes_arr = np.array([t["public_metrics"]["like_count"] for t in tweet_data])
    most_likes = likes_arr.max()
    average_likes = likes_arr.mean()

    retweets_arr = np.array([t["public_metrics"]["retweet_count"] for t in tweet_data])
    most_retweets = retweets_arr.max()
    average_retweets = retweets_arr.mean()

    quotes_arr = np.array([t["public_metrics"]["quote_count"] for t in tweet_data])
    most_quotes = quotes_arr.max()
    average_quotes = quotes_arr.mean()

    replies_arr = np.array([t["public_metrics"]["reply_count"] for t in tweet_data])
    most_replies = replies_arr.max()
    average_replies = replies_arr.mean()

    account_collection["av_likes"] = average_likes
    account_collection["av_quotes"] = average_quotes
    account_collection["av_replies"] = average_replies
    account_collection["av_retweets"] = average_retweets

    hashtags = [find_hashtags_in_tweet(t["text"]) for t in tweet_data]
    hashtags = [ht for sub_ht in hashtags for ht in sub_ht]
    ten_most_used_hashtags = Counter(hashtags).most_common(10)

    mentions = [find_mentions_in_tweet(t["text"]) for t in tweet_data]
    mentions = [m for sub_m in mentions for m in sub_m]
    ten_most_mentioned = Counter(mentions).most_common(10)

    account_collection["top_ten_hashtags_used"] = ten_most_used_hashtags
    account_collection["top_ten_mentioned"] = ten_most_mentioned

    # sort for top 10 likes, retweets, replies and quotes
    top_ten_liked = sorted(tweet_data, key=lambda d: d["public_metrics"]["like_count"])[-10:]
    top_ten_replied = sorted(tweet_data, key=lambda d: d["public_metrics"]["reply_count"])[-10:]
    top_ten_quoted = sorted(tweet_data, key=lambda d: d["public_metrics"]["quote_count"])[-10:]
    top_ten_retweeted = sorted(tweet_data, key=lambda d: d["public_metrics"]["retweet_count"])[-10:]

    account_collection["top_ten_liked"] = top_ten_liked
    account_collection["top_ten_replied"] = top_ten_replied
    account_collection["top_ten_quoted"] = top_ten_quoted
    account_collection["top_ten_retweeted"] = top_ten_retweeted

    account_collection["num_posts_last_30_days"] = len(tweet_data)

    account_collection["username"] = USERNAME

    # GET THE DATA INTO AIRTABLE
    table.create({"Timestamp": account_collection["date_now"], 
                    "Description": account_collection["description"],
                    "Start Timestamp": account_collection["date_from"],
                    "NumFollowers": account_collection["followers"],
                    "NumTweets": account_collection["num_posts_last_30_days"],
                    "Username": account_collection["username"],
                    "AvLikes": account_collection["av_likes"],
                    "AvQuotes": account_collection["av_quotes"],
                    "AvRetweets": account_collection["av_retweets"],
                    "AvReplies": account_collection["av_replies"],
                    "TopTenLiked": str(["https://twitter.com/"+USERNAME+"/status/"+ael["id"] for ael in account_collection["top_ten_liked"]]),
                    "TopTenReplied": str(["https://twitter.com/"+USERNAME+"/status/"+ael["id"] for ael in account_collection["top_ten_replied"]]),
                    "TopTenQuoted": str(["https://twitter.com/"+USERNAME+"/status/"+ael["id"] for ael in account_collection["top_ten_quoted"]]),
                    "TopTenRetweeted": str(["https://twitter.com/"+USERNAME+"/status/"+ael["id"] for ael in account_collection["top_ten_retweeted"]]),
                    "TenMostRecentTweets": str(["https://twitter.com/"+USERNAME+"/status/"+ael["id"] for ael in account_collection["ten_most_recent_tweets"]]),
                    "TopTenHashtags": str(account_collection["top_ten_hashtags_used"]),
                    "TopTenMentioned": str(account_collection["top_ten_mentioned"])
                    })

