import requests
from requests_oauthlib import OAuth1Session
import json
import time
import pandas as pd

class Timeline:
    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret):
        self.authenticate = OAuth1Session(
            client_key=consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
            signature_type='auth_header')
        self.user_id = None
        self.timeline_id = None

    def user_profile(self):
        request = self.authenticate.get(
            url='https://api.twitter.com/1.1/account/verify_credentials.json')
        request_json = request.json()
        self.user_id = str(request_json['id'])

    def simple_search_parameters(self):
        parameters = {
            'expansions': 'entities.mentions.username',
            'tweet.fields': 'created_at,text,public_metrics'
        }
        return parameters

    def detailed_search_parameters(self):
        parameters = {
            'expansions':
            'entities.mentions.username',
            'tweet.fields':
            'created_at,entities,non_public_metrics,organic_metrics,public_metrics,text'
        }
        return parameters

    def request_post(self, post_id):
        url = f'https://api.twitter.com/2/tweets/{post_id}'
        params = self.detailed_search_parameters()
        request = self.authenticate.get(url, params=params)
        if request.json().get('errors') is not None:  #Yes Errors exist
            params = self.simple_search_parameters()
            request = self.authenticate.get(url, params=params)
            print(f'Status for Retweet {post_id}: {request.status_code}')
            return request.json()
        print(f'Status for Post {post_id}: {request.status_code}')
        return request.json()

    def request_timeline(self, max_id=None):
        """        
        :reference: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-user_timeline
        """
        if self.user_id is None:
            self.user_profile()
            self.request_timeline()
        if max_id is None:
            params = {'user_id': self.user_id, 'count': 200, 'include_rts': 1}
        else:
            params = {
                'user_id': self.user_id,
                'count': 200,
                'include_rts': 1,
                'max_id': max_id
            }

        request = self.authenticate.get(
            url='https://api.twitter.com/1.1/statuses/user_timeline.json',
            params=params)
        return request.json()

    def timeline_ids(self):
        timeline = []
        max_id = 0
        for i in range(2):  # change value to get more inputs max is 32
            if i == 0:
                request = self.request_timeline()
                timeline.append(request)
                max_id = timeline[0][-1].get('id') - 1
                continue
            request = self.request_timeline(max_id=max_id)
            timeline.append(request)
            max_id = timeline[0][-1].get('id') - 1

        timeline_ids=[]
        for l in timeline:
            for d in l:
                timeline_ids.append(d.get('id'))
        self.timeline_id = timeline_ids

    def timeline_posts(self):
        posts = []
        request_count = 0
        if self.timeline_id is None:
            self.timeline_ids()
            self.timeline_posts()
        for post_id in self.timeline_id:
            request_count += 1
            if request_count % 300 == 0:
                time.sleep(900)
            request = self.request_post(post_id)
            posts.extend(request)
        return posts
        

    def normalizing(self):
        timeline = self.timeline_posts()
        normalizing = []
        for post in timeline:
            normalizing.append(pd.json_normalize(post['data']))
        return normalizing

    def timeline(self):
        timeline = pd.DataFrame()
        normalizing = self.normalizing()
        for df in normalizing:
            timeline.append(df, ignore_index=True)
        timeline.to_csv()