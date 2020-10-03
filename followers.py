import requests
from requests_oauthlib import OAuth1Session
import json
import time
import pandas as pd
from secrets import consumer_key, consumer_secret, access_token, access_token_secret

class Followers:
    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret):
        self.authenticate = OAuth1Session(
            client_key=consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
            signature_type='auth_header')
        self.user_id = None

    def followers_ids(self):
        url = 'https://api.twitter.com/1.1/followers/ids.json'
        request = self.authenticate.get(url, params={'count':5000})
        # print(type(request.json().get('ids')))
        # print(request.json().get('ids'))
        return request.json().get('ids')

    def id_lookup(self, follower_id):
        url = f'https://api.twitter.com/2/users/{follower_id}'
        params = {
            'expansions': 'pinned_tweet_id',
            'user.fields': 'created_at,description,location,url,public_metrics',
            }
        request = self.authenticate.get(url, params=params)
        
            
        print(request.json().get('data'))
        # print(type(request.json().get('data')))
        return request.json().get('data')

    def followers_lookup(self):
        followers_data = []
        lookup_count = 0
        followers_ids = self.followers_ids()
        for follower_id in followers_ids: # remove [:10] when looking for all
            print(f'Follower ID: {follower_id}')
            lookup_count+=1
            if lookup_count %900 == 0: # if 300 requests sleep 15mins
                time.sleep(900)
            followers_data.append(self.id_lookup(follower_id))
        # print(len(followers_data))
        # print(followers_data[:10])
        return followers_data

    def followers_df(self):
        followers_lookup = self.followers_lookup()
        df = pd.DataFrame(followers_lookup)
        df.to_csv('./DataCSVs/Followers.csv')
        pass

f = Followers(consumer_key, consumer_secret, access_token, access_token_secret)
# f_id = f.followers_ids() # returns class list
# id_lookup = f.id_lookup('82270672') # returns class dict
# f_lookup = f.followers_lookup() # returns list of dicts
df = f.followers_df()

# Question?

# What kind of person is my follower