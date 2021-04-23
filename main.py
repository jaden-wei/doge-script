import tweepy
import cv2
import pytesseract as tess
from urllib.request import urlopen
import numpy as np
import robin_stocks.robinhood as r
import time

from secret import *

# authenticate tweepy
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
    print("Logged into Robinhood")

def robinhood_logout():
    r.logout()
    print("Logged out of Robinhood")

#get and return doge price
def get_doge_price():
    try:
        doge_price = float(r.crypto.get_crypto_quote('DOGE').get('ask_price'))
        return doge_price
    except Exception as e:
        print(e)

#return true if doge or similar words are found, return false if not
def scan_image_for_text(img_url):
    # convert url to image
    resp = urlopen(img_url)
    img = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    # convert image to improve tesseract
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #convert to threshold using multiple threshold values
    for value in range(10, 210, 50):
        threshold_img = cv2.threshold(gray_img, value, 255, cv2.THRESH_BINARY)[1]

        #check if converted image includes doge text
        text = tess.image_to_string(threshold_img, lang="eng")
        if 'doge' in text or 'dog3' in text or 'dog' in text or 'd0ge' in text or 'd0g3' in text:
            return True

    return False

# tweets - list of recent tweets by elon musk
# search for doge or any similar words in the tweets
# returns true if order was placed
def search_text_for_doge(tweets):
    for tweet in tweets:
        tweet = tweet.text.lower()
        if ('doge' in tweet or 'dog3' in tweet or 'dog' in tweet or 'd0ge' in tweet or 'd0g3' in tweet):
            print(r.orders.order_buy_crypto_by_quantity('DOGE', 500))
            print('THE GOD HAS SPOKEN')
            return True
    return False

def search_media_for_doge(tweets):
    for tweet in tweets:
        media = tweet.entities.get('media', [])
        if (len(media) > 0):
            for picture in media:
                if scan_image_for_text(picture['media_url']):
                    print(r.orders.order_buy_crypto_by_quantity('DOGE', 500))
                    print('THE GOD HAS SPOKEN')
                    return True
    return False

def main():
    #set up, auth, login
    api = tweepy_setup()
    robinhood_login()

    #make sure we don't continuously buy
    purchase_doge = False

    while not purchase_doge:
        # get elon's recent tweets
        elon_tweets = api.user_timeline('elonmusk')

        print(get_doge_price())

        purchase_doge = search_text_for_doge(elon_tweets)
        
        if not purchase_doge:
            purchase_doge = search_media_for_doge(elon_tweets)
        
        time.sleep(90)

    robinhood_logout()

if __name__ == '__main__':
    main()