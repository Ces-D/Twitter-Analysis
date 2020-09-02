from twitter import UserPosts
from secrets import *

twitter = UserPosts(consumer_key, consumer_secret, access_token, access_token_secret)

user_posts = twitter.user_post(account_name, 2000)
metrics = twitter.request_metrics()
print(metrics)