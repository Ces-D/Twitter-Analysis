import requests
from requests_oauthlib import OAuth1Session


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
    
    def stringify(self,id):
        if type(id) =='str':
            return id
        else:
            return str(id)

    def user_id(self):
        protected_url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
        oauth = self.authenticate()
        r = oauth.get(protected_url)
        r_json = r.json()
        return r_json['id']
    
    def post_date(self,id):
        str_id = self.stringify(id)
        protected_url = f'https://api.twitter.com/2/tweets/{str_id}'
        oauth = self.authenticate()
        parameters = {
            'expansions': 'entities.mentions.username',
            'tweet.fields': 'created_at,entities,non_public_metrics,public_metrics,text'
        }
        r = oauth.get(protected_url, params=parameters)
        return r.json()
