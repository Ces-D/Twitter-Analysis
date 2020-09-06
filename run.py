from twitterapi import API
from secrets import *

# posts = UserPosts(consumer_key, consumer_secret, access_token, access_token_secret)

# user_posts = posts.user_post(account_name, 200)


# timeline = posts.get_timeline(user=account_name, file_name="Twitter_timeline.csv")

twitter = API(consumer_key, consumer_secret, access_token, access_token_secret)


# test = twitter.all_post_data(start_index=700, end_index=731)
# print(test)

#test_post_ids = twitter.all_post_ids()


#test_post_data = twitter.post_data(933341130338590721)
#print(test_post_data) # if post type is a retweet, the typical metrics cannot be matched


data = twitter.data_file(start_index=1, end_index=644)
