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
    
    def protected_url(self):
        protected_url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
        oauth = self.authenticate()
        r = oauth.get(protected_url)
        print(r.json())
    

