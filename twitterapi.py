import requests
from requests_oauthlib import OAuth1Session
import csv
import os
import json


class API:
    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def authenticate(self):
        oath = OAuth1Session(client_key=self.consumer_key,
                             client_secret=self.consumer_secret,
                             resource_owner_key=self.access_token,
                             resource_owner_secret=self.access_token_secret,
                             signature_type='auth_header')
        return oath

    def stringify(self, id):
        if type(id) == 'str':
            return id
        else:
            return str(id)

    def user_id(self):
        protected_url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
        oauth = self.authenticate()
        r = oauth.get(protected_url)
        r_json = r.json()
        return r_json['id']

    def initial_timeline_request(self):
        """        
        :reference: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-user_timeline
        """
        
        protected_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        oauth = self.authenticate()
        user_id = self.user_id
        parameters = {
            'user_id': self.stringify(user_id),
            'count': 200,
            'include_rts': 1
        }
        r = oauth.get(protected_url, params=parameters)
        return r.json()

    def continual_timeline_request(self, max_id):
        """        
        :reference: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-user_timeline
        """

        protected_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        oauth = self.authenticate()
        user_id = self.user_id
        parameters = {
            'user_id': self.stringify(user_id),
            'count': 200,
            'include_rts': 1,
            'max_id': max_id
        }
        r = oauth.get(protected_url, params=parameters)
        return r.json()

    def all_timeline_posts(self):
        """        
        :reference: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-user_timeline
        :returns: file containing 3,200 posts
        """

        all_posts = []
        posts = self.initial_timeline_request()
        all_posts.extend(posts)  # save the initial request to list

        # save the id of the oldest tweet minus 1
        max_id = all_posts[-1].get('id') - 1

        # status 200 request returns response of len of max 200
        while len(posts) > 0:
            print(f'Getting posts before {max_id}')
            posts = self.continual_timeline_request(max_id)
            all_posts.extend(posts)
            max_id = all_posts[-1].get('id') - 1
            print(f'{len(all_posts)} posts downloaded so far')

        cleaned_all_posts = [[post.get('id'),
                              post.get('created_at')] for post in all_posts]

        with open('Account_PostsID.csv', 'w',
                  encoding='utf-8') as file:  # write the IDs to a CSV
            writer = csv.writer(file)
            writer.writerow(["PostID", "Created At"])
            writer.writerows(post for post in cleaned_all_posts)

        pass

    def all_post_ids(self):
        if os.path.exists('Account_PostsID.csv'):  # if files exists
            with open('Account_PostsID.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                all_post_ids = [row for row in reader]
                print(f'Your IDs file has {len(all_post_ids)} rows')
                return all_post_ids

        self.all_timeline_posts()  # else run script and write file
        self.all_post_ids()  # run again to check condition
        pass

    def simple_parameters(self):
        parameters = {
            'expansions': 'entities.mentions.username',
            'tweet.fields': 'created_at,text,public_metrics'
        }
        return parameters

    def detailed_parameters(self):
        parameters = {
            'expansions':
            'entities.mentions.username',
            'tweet.fields':
            'created_at,entities,non_public_metrics,organic_metrics,public_metrics,text'
        }
        return parameters

    def post_data(self, post_id):
        """
        "reference: https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets-id
        """
        str_id = self.stringify(post_id)
        protected_url = f'https://api.twitter.com/2/tweets/{str_id}'
        oauth = self.authenticate()

        parameters = self.detailed_parameters()
        r = oauth.get(protected_url, params=parameters)

        if r.json().get('errors') is not None:  #Yes Errors exist
            print('Post is Simple')
            parameters = self.simple_parameters()
            r = oauth.get(protected_url, params=parameters)
            print(f'Status for Retweet {str_id}: {r.status_code}')
            return r.json()

        print(f'Status for Post {str_id}: {r.status_code}')
        return r.json()

    def all_post_data(self, start_index=1, end_index=5):
        """
        :returns: either simple or detailed json data for account posts in index range
        """
        post_ids = self.all_post_ids()
        all_post_data = []

        # change this to iterate through partial list
        for post_id in post_ids[start_index:end_index]:

            if post_id == [] or None:
                continue

            print(f'Grabbing data for: {post_id[0]}')
            # self.all_post_ids returns a list of id and created_at
            post_data = self.post_data(post_id[0])
            all_post_data.append(post_data)

        print(f'Resulting list: {len(all_post_data)}')

        return all_post_data

    def data_file(self, start_index=1, end_index=5):
        """"
        :returns: json file containing either simple or detailed json data for account posts in index range
        """
        data = self.all_post_data(start_index, end_index)
        json_data = json.dumps(data, indent=4)
        with open('Post_Data.json', 'w') as f:
            f.write(json_data)
        pass