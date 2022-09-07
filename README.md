# Twitter Monitor Scripts

Twitter's API is really cool. Here are some starter scripts for working with it!

## Simple Script

### What is it?

`simple_twitter_monitor.py` is a script that gets tweet data and puts it in Airtable.

### Airtable

The script sends the data it gets via the Twitter API to an Airtable table. You will need to set up a table in your account and create the necessary columns (or change the script to suit your own needs!)

![Image](airtable_table.gif)

Columns:

-

### How do I use it?

Just call `python simple_twitter_monitor.py`!

Don't forget to set your table name (`TABLE`) and fill out the list of user accounts you are interested in (`usernames`)

You will also need to set three environment variables:

- TWITTER_BASE_ID: The Airtable Base where you want to put your Twitter data
- AIRTABLE_API_KEY: Your API key for the Airtable API (you will need an Airtable account [link](https://airtable.com/))
- TWITTER_KEY: Your API key for the Twitter API (you will need to sign up for a developer account [link](https://developer.twitter.com/en))
