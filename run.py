from twitterapi import API
from secrets import *

# posts = UserPosts(consumer_key, consumer_secret, access_token, access_token_secret)

# user_posts = posts.user_post(account_name, 200)


# timeline = posts.get_timeline(user=account_name, file_name="Twitter_timeline.csv")

twitter = API(consumer_key, consumer_secret, access_token, access_token_secret)


#test = twitter.test_post_data()

test_post_id = twitter.post_data(1301539994008518656)
print(test_post_id) # if post type is a retweet, the typical metrics cannot be matched
# should create checker for retweets