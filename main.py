import tweepy
import robin_stocks.robinhood as r
import time

from secret import *

# set up and authenticate tweepy
def tweepy_setup():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Tweepy Authenticated")
    except:
        print("Tweepy Authentication Error")
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    return api

def robinhood_login():
    r.login(username=ROBINHOOD_USERNAME, password=ROBINHOOD_PASSWORD, expiresIn=86400, by_sms=True)

def robinhood_logout():
    r.logout()

def main():
    #set up, auth, login
    api = tweepy_setup()
    robinhood_login()
    print("Logged into Robinhood")

    #make sure we don't continuously buy
    purchase_doge = False

    while not purchase_doge:

        # get elon's recent tweets
        elon_tweets = api.user_timeline('elonmusk')

        #print doge price
        doge_price = float(r.crypto.get_crypto_quote('DOGE').get('ask_price'))
        print(doge_price)

        # search for doge/similar words in recent tweets
        for tweet in elon_tweets:
            tweet = tweet.text.lower()
            if ('doge' in tweet or 'dog3' in tweet or 'dog' in tweet or 'd0ge' in tweet or 'd0g3' in tweet):
                print(r.orders.order_buy_crypto_by_quantity('DOGE', 1000))
                purchase_doge = True
                
        time.sleep(30)

    robinhood_logout()
    print("Logged out of Robinhood")

if __name__ == '__main__':
    main()