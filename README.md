# Twitter Monitor Scripts

Twitter's API is really cool. Here are some starter scripts for working with it!

## Simple Script

### What is it?

`simple_twitter_monitor.py` is a script that gets tweet data and puts it in Airtable.

The script ignores retweets and reply tweets that the account has made. This is switchable in the call to the Twitter API. 

### Airtable

The script sends the data it gets via the Twitter API to an Airtable table. You will need to set up a table in your account and create the necessary columns (or change the script to suit your own needs!)

![Image](/airtable_table.gif)

Columns:

- ID: a self-incrementing number to act as the unique identifier for the record (row)
- Timestamp: The date and time this data was retrieved
- Start Timestamp: The date and time of the last time data was retrieved for this user (the script goes back a maximum of 30 days if there is no data)
- Username: the account username
- Description: the account description
- NumFollowers: the number of followers the user has
- NumTweets: the number of tweets in this measurement period (max is 30 days)
- AvLikes: average number of likes on tweets in the measurement period
- AvRetweets: average number of retweets on tweets in the measurement period
- AvQuotes: average number of quotes on tweets in the measurement period
- AvReplies: average number of replies on tweets in the measurement period
- TenMostRecentTweets: an array of links to the account's ten most recent tweets
- TopTenRetweeted: an array of links to the account's ten most retweeted tweets
- TopTenReplied: an array of links to the account's ten most replied tweets
- TopTenQuoted: an array of links to the account's ten most quoted tweets
- TopTenLiked: an array of links to the account's ten most liked tweets

### How do I use it?

Just call `python simple_twitter_monitor.py`!

Don't forget to set your table name (`TABLE`) and fill out the list of user accounts you are interested in (`usernames`)

You will also need to set three environment variables:

- TWITTER_BASE_ID: The Airtable Base where you want to put your Twitter data
- AIRTABLE_API_KEY: Your API key for the Airtable API (you will need an Airtable account [link](https://airtable.com/))
- TWITTER_KEY: Your API key for the Twitter API (you will need to sign up for a developer account [link](https://developer.twitter.com/en))
