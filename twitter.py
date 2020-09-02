from tweepy import API, OAuthHandler
import csv
import time


class UserPosts:
    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def initialize_v1(self):
        """
        Runs the Tweepy OathHandler
        """
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = API(auth)
        return api

    def user_post(self, user, max_id=None):
        """
        :reference: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
        :allowed_param: 'id', 'user_id', 'screen_name', 'since_id',
                            'max_id', 'count', 'include_rts', 'trim_user',
                            'exclude_replies'
        :return: list of 200 posts with id before max_id
        """

        api = self.initialize_v1()
        user_timeline = api.user_timeline(screen_name=user,
                                          count=200,
                                          max_id=max_id)
        user_posts = [(post.created_at, post.id, post.text)
                      for post in user_timeline]
        return user_posts

    def last_id(self, list):
        """
        :return: id of last item in list
        """
        last = list[-1]
        post_id = last[1]
        self.last_id = post_id

    def write_to_csv(self, file_name, data):
        with open(file_name, 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def get_timeline(self, user, file_name, iterations=10):
        user_posts = self.user_post(user)
        self.write_to_csv(file_name, user_posts)
        self.last_id(user_posts)
        time.sleep(900)
        for iteration in range(1, iterations):
            user_posts = self.user_post(user, max_id=self.last_id)
            self.last_id(user_posts)
            self.write_to_csv(file_name, user_posts)
            print(f'At {iteration} iteration...', '/n')
            time.sleep(900)
        
