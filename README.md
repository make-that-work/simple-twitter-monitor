# Twitter Monitor Scripts

Twitter's API is really cool.

## Simple Script

### What is it?

`simple_twitter_monitor.py` is a simple script that gets tweet data and puts it in Airtable.

### How do I use it?

Just call `python simple_twitter_monitor.py`!

Don't forget to set your table name (`TABLE`) and fill out the list of user accounts you are interested in (`usernames`)

You will need to set three environment variables:

- TWITTER_BASE_ID: The Airtable Base where you want to put your Twitter data
- AIRTABLE_API_KEY: Your API key for the Airtable API (you will need an Airtable account [link](https://airtable.com/))
- TWITTER_KEY: Your API key for the Twitter API (you will need to sign up for a developer account [link](https://developer.twitter.com/en))
