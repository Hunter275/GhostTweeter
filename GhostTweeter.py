import feedparser
import tweepy

post = 1 #post 0 is most recent, higher # = older

feed = feedparser.parse('http://adventuresintechland.com/rss')
title = feed['entries'][post]['title']
url = feed['entries'][post]['links'][0]['href']
published = feed['entries'][post]['published']

text = str(title + ": " + url)

for item in feed['entries'][0]['tags']:
    text = text + " #" + str(item['term'])


CONSUMER_KEY = 'yourshere'
CONSUMER_SECRET = 'yourshere'

ACCESS_KEY = 'yourshere'
ACCESS_SECRET = 'yourshere'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#This is the tweet
api.update_status(text)
