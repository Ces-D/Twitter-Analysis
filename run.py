from twitter import UserPosts
from twitterapi import API
from secrets import *

posts = UserPosts(consumer_key, consumer_secret, access_token, access_token_secret)

user_posts = posts.user_post(account_name, 200)


timeline = posts.get_timeline(user=account_name, file_name="Twitter_timeline.csv")

#twitter = API(consumer_key, consumer_secret, access_token, access_token_secret)

# test = twitter.protected_url()