import requests
from requests_oauthlib import OAuth1Session
import csv
import os


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
        """

        all_posts = []
        posts = self.initial_timeline_request()
        all_posts.extend(posts)  # save the initial request to list
        max_id = all_posts[-1].get('id') - 1  # save the id of the oldest tweet minus 1

        while len(posts) > 0:  # while still requesting, status 200 request length is 200
            print(f'Getting posts before {max_id}')
            posts = self.continual_timeline_request(max_id)
            all_posts.extend(posts)
            max_id = all_posts[-1].get('id') - 1
            print(f'{len(all_posts)} posts downloaded so far')

        cleaned_all_posts = [[post.get('id'), post.get('created_at')] for post in all_posts]

        with open('Account_PostsID.csv',
                  'w', encoding='utf-8') as file:  # write the IDs to a CSV
            writer = csv.writer(file)
            writer.writerow(["PostID","Created At"])
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


    def post_data(self, post_id):
        """
        "reference: https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets-id
        """
        str_id = self.stringify(post_id)
        protected_url = f'https://api.twitter.com/2/tweets/{str_id}'
        oauth = self.authenticate()
        parameters = {
            'expansions':
            'entities.mentions.username',
            'tweet.fields':
            'created_at,entities,non_public_metrics,organic_metrics,public_metrics,text'
        }
        r = oauth.get(protected_url, params=parameters)
        print(f'Status for {str_id} is:{r}')
        return r.json()


    def test_post_data(self):
        post_ids = self.all_post_ids()
        all_post_data = []
        post_id = post_ids[2]   
        post_data = self.post_data(post_id)  # self.all_post_ids returns a list of id and created_at
        all_post_data.append(post_data)

        print(f'Resulting list: {all_post_data}')
        pass

