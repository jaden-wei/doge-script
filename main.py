import tweepy
from keys import *

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authenticated")
except:
    print("Authentication Error")

api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

elon_tweets = api.user_timeline('elonmusk')

for tweet in elon_tweets:
    tweet = tweet.text.lower()
    if ('doge' in tweet or 'dog3' in tweet or 'dog' in tweet):
        print('Found the Doge..')
