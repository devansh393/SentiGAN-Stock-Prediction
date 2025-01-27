# Install required libraries
import tweepy
import pandas as pd
import nltk
import re
from datetime import datetime, timedelta

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Twitter API credentials
consumer_key = "##CONSUMER_KEY##"
consumer_secret = "##CONSUMER_SECRET##"
access_token = "##ACCESS_TOKEN##"
access_token_secret = "##ACCESS_TOKEN_SECRET##"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Set search parameters
keyword = "AMZN"
start_date = datetime(2021, 9, 30)
end_date = datetime(2022, 9, 30)

# Function to clean tweets
def clean_tweet(tweet):
    # Remove URLs
    tweet = re.sub(r'http\S+|www\S+|https\S+', '', tweet, flags=re.MULTILINE)
    # Remove user mentions
    tweet = re.sub(r'@\w+', '', tweet)
    return tweet

# Fetch tweets
tweets = []
for tweet in tweepy.Cursor(api.search_tweets, q=keyword, lang="en", tweet_mode="extended").items():
    if start_date <= tweet.created_at <= end_date:
        tweets.append({
            'Date': tweet.created_at,
            'Tweet': tweet.full_text,
            'Stock Name': keyword,
            'Company Name': 'Amazon.com, Inc.'
        })

# Create DataFrame
df = pd.DataFrame(tweets)

# Clean tweets
df['Cleaned Tweet'] = df['Tweet'].apply(clean_tweet)

# Save to CSV
df.to_csv('amzn_tweets.csv', index=False)