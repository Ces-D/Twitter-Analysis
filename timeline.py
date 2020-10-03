import requests
from requests_oauthlib import OAuth1Session
import json
import time
import pandas as pd
import itertools
from secrets import consumer_key, consumer_secret, access_token, access_token_secret


class Timeline:
    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret):
        self.authenticate = OAuth1Session(
            client_key=consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
            signature_type='auth_header')

    def post_data(self, post_id):
        complex_params = {
            'expansions':
            'entities.mentions.username',
            'tweet.fields':
            'created_at,entities,non_public_metrics,organic_metrics,public_metrics,text'
        }
        request = self.authenticate.get(
            url=f'https://api.twitter.com/2/tweets/{post_id}',
            params=complex_params)
        if request.json().get('errors') is not None:
            simple_params = {
                'expansions': 'entities.mentions.username',
                'tweet.fields': 'created_at,text,public_metrics'
            }
            request = self.authenticate.get(
                url=f'https://api.twitter.com/2/tweets/{post_id}',
                params=simple_params)
            # print(f'Simple:{request.json().get("data")["id"]}')
            # print(f'Simple:{type(request.json().get("data"))}')
            return request.json().get("data")
        # print(f'Complex:{request.json().get("data")["id"]}')
        # print(f'Complex:{type(request.json().get("data"))}')
        return request.json().get("data")

    def user_timeline(self):
        loop=0
        user_timeline=[]
        params={
                'count':2, # change to 200 in prod
                'include_rts':1
            }
        i_request= self.authenticate.get(url='https://api.twitter.com/1.1/statuses/user_timeline.json', params=params)
        # print(f'Initial Request: {i_request.json()}')
        # print(f'Initial Request Type: {type(i_request.json())}')
        user_timeline.append(i_request.json())
        max_id = user_timeline[-1][-1].get('id') - 1
        for i in range(6): # change to larger for more rounds 
            loop+=1
            if loop%4.5==0: # if request count is 900 sleep 15mins
                time.sleep(900)
            params={
                'count':200, # change to 200 in prod
                'include_rts':1,
                'max_id': max_id,
            }
            request= self.authenticate.get(url='https://api.twitter.com/1.1/statuses/user_timeline.json', params=params)
            # print(f'Conseq Request: {request.json()}', '\n\n')
            user_timeline.append(request.json())
            max_id = user_timeline[-1][-1].get('id') - 1
        # print(f'User Timeline: {user_timeline}')
        # print(f'User Timeline Type: {type(user_timeline)}')
        # print(f'User Timeline Length: {len(user_timeline)}')
        return user_timeline

    def user_timeline_ids(self):
        user_timeline = self.user_timeline()
        f_user_timeline = list(itertools.chain.from_iterable(user_timeline)) #flatten list of lists
        timeline_post_ids = [post.get('id') for post in f_user_timeline]
        # print(f'Flat List Length: {len(f_user_timeline)}')
        # print(f'Flat List: {f_user_timeline}')
        # print(f'Timeline Post Ids: {timeline_post_ids}')
        return timeline_post_ids

    def timeline_post_data(self):
        user_timeline_ids = self.user_timeline_ids()
        timeline_post_data = []
        loop = 0
        for timeline_id in user_timeline_ids:
            loop+=1
            if loop%300==0: # if request count is 300 sleep 15mins
                time.sleep(900)
            timeline_post_data.append(self.post_data(timeline_id))
        # print(f'Timeline Post Data Len: {len(timeline_post_data)}')
        return timeline_post_data

    def timeline_post_df(self):
        timeline_post_data = self.timeline_post_data()
        df = pd.DataFrame(timeline_post_data)
        df.to_csv('./DataCSVs/TimelinePosts.csv')
        pass

t = Timeline(consumer_key, consumer_secret, access_token, access_token_secret)
# user_id = t.user_id() # returns class int
# post_d = t.post_data(1307016538227200004) # returns class dict
# u_timeline = t.user_timeline() # returns class list  aka list of lists of dicts
# u_timeline_ids = t.user_timeline_ids() # returns list
# t_post_data = t.timeline_post_data() # returns list of dicts
df = t.timeline_post_df()


