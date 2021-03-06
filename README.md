# Twitter-Analysis

This project uses endpoints from Twitter API v2. As such you need to first obtain both a developer account and create a project through the [Twitter Developer Portal](https://developer.twitter.com/content/developer-twitter/en/portal/dashboard).

When initializing the API class, enter your credentials to authenticate your requests.
````
def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
````

The goal of the project was to create one single file containing all the data for the various Twitter posts of the authenticated account. `API.data_file()` creates this file by first grabbing the first 3,200 post ids and then running a search for each post id. You are returned a json file containing all the data. `API.all_post_ids()` creates a csv file with these post ids and `API.post_data()` requests the data from Twitter API v2. 

The goal of the project was very specific and as such the number of methods for the various Twitter endpoints is very limited. However, if you are interested in pulling information from other endpoints, copy the structure from `API.user_ids()` replacing the url with your desired url. 

