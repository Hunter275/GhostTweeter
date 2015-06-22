import feedparser, datetime, tweepy, random, time
import datetime
from datetime import date
import tweepy
import random
import time

# Array containing list of post
posts = []

# Needed to cycle through individual posts
post = 0

# Get the time between tweets in hours
timeBetweenTweets = float(raw_input("Hours between tweets?: "))

# Filters tweets based off of age
minPostAge = float(raw_input("Minimum age of blog post (in days, 0 = all posts)?: "))

# Get the blog url
blog = raw_input("What is your blog url? (ex: http://www.adventuresintechland.com): ")


def getPosts():
    # Start page (.../rss/1)
    page = 1

    while 1:
        feed = feedparser.parse(blog + '/rss/' + str(page))
        post = 0
        for item in feed['entries']:
            title = feed['entries'][post]['title']
            url = feed['entries'][post]['links'][0]['href']
            published = feed['entries'][post]['published']

            text = str(title + ": " + url)

            try:
                for item in feed['entries'][post]['tags']:
                    text = text + " #" + str(item['term'])
            except KeyError:
                text = text

            year = feed['entries'][post]['published_parsed'][0]
            month = feed['entries'][post]['published_parsed'][1]
            day = feed['entries'][post]['published_parsed'][2]

            today = str(datetime.date.today()).split("-")

            dayssince = date(int(today[0]), int(today[1]), int(today[2])) - date(year, month, day)
            dayssince = str(dayssince).split(" ")
            dayssince = dayssince[0]

            if dayssince == "0:00:00":
                dayssince = 0

            info = [text, dayssince]

            posts.append(info)
            post = post + 1
        if len(posts) % 15 == 0:
            page = page + 1
        else:
            break

# Twitter Auth
CONSUMER_KEY = 'yourshere'
CONSUMER_SECRET = 'yourshere'
ACCESS_KEY = 'yourshere'
ACCESS_SECRET = 'yourshere'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# Gets the tweet ready and checks if it is older than the set age
def postTweet():
    randomint = random.randint(0, len(posts) - 1)
    selected_tweet = posts[randomint]
    if float(selected_tweet[1]) < minPostAge:
        postTweet()
    else:
        single_tweet = selected_tweet[0]
        print "Attempting to post: " + single_tweet
        api.update_status(status=single_tweet)

# Will run forever, checking for new blog post before every tweet is posted
while 1:
    getPosts()
    postTweet()
    posts = []
    time.sleep(1)
    time.sleep(timeBetweenTweets * 3600.0)
