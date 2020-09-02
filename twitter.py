import imghdr
import mimetypes
import os

import six

from tweepy import API, OAuthHandler
from tweepy.binder import bind_api
from tweepy.parsers import ModelParser, Parser
from tweepy.error import TweepError


class APIv2(object):
    def __init__(self,
                 auth_handler=None,
                 host='api.twitter.com',
                 search_host='search.twitter.com',
                 upload_host='upload.twitter.com',
                 cache=None,
                 api_root='/2',
                 search_root='',
                 upload_root='/2',
                 retry_count=0,
                 retry_delay=0,
                 retry_errors=None,
                 timeout=60,
                 parser=None,
                 compression=False,
                 wait_on_rate_limit=False,
                 wait_on_rate_limit_notify=False,
                 proxy=''):
        self.auth = auth_handler
        self.host = host
        self.search_host = search_host
        self.upload_host = upload_host
        self.api_root = api_root
        self.search_root = search_root
        self.upload_root = upload_root
        self.cache = cache
        self.compression = compression
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.timeout = timeout
        self.wait_on_rate_limit = wait_on_rate_limit
        self.wait_on_rate_limit_notify = wait_on_rate_limit_notify
        self.parser = parser or ModelParser()
        self.proxy = {}
        if proxy:
            self.proxy['https'] = proxy

        # Attempt to explain more clearly the parser argument requirements
        # https://github.com/tweepy/tweepy/issues/421

        parser_type = Parser
        if not isinstance(self.parser, parser_type):
            raise TypeError(
                '"parser" argument has to be an instance of "{required}".'
                ' It is currently a {actual}.'.format(
                    required=parser_type.__name__, actual=type(self.parser)))

    @property
    def request_metrics(self):
        """
        :refernce: https://developer.twitter.com/en/docs/twitter-api/metrics
        """
        return bind_api(api=self,
                        path='/tweets',
                        payload_type='status',
                        payload_list=True,
                        allowed_param=[
                            'ids', 'tweet.fields', 'expansions', 'media.fields'
                        ],
                        require_auth=True)

                 
# internal use only
    @staticmethod
    def _pack_image(filename, max_size, form_field='image', f=None, file_type=None):
        """Pack image from file into multipart-formdata post body"""
        # image must be less than 700kb in size
        if f is None:
            try:
                if os.path.getsize(filename) > (max_size * 1024):
                    raise TweepError('File is too big, must be less than %skb.'
                                     % max_size)
            except os.error as e:
                raise TweepError('Unable to access file: %s' % e.strerror)

            # build the mulitpart-formdata body
            fp = open(filename, 'rb')
        else:
            f.seek(0, 2)  # Seek to end of file
            if f.tell() > (max_size * 1024):
                raise TweepError('File is too big, must be less than %skb.'
                                 % max_size)
            f.seek(0)  # Reset to beginning of file
            fp = f

        # image must be gif, jpeg, png, webp
        if not file_type:
            file_type = imghdr.what(filename) or mimetypes.guess_type(filename)[0]
        if file_type is None:
            raise TweepError('Could not determine file type')
        if file_type in ['gif', 'jpeg', 'png', 'webp']:
            file_type = 'image/' + file_type
        elif file_type not in ['image/gif', 'image/jpeg', 'image/png']:
            raise TweepError('Invalid file type for image: %s' % file_type)

        if isinstance(filename, six.text_type):
            filename = filename.encode('utf-8')

        BOUNDARY = b'Tw3ePy'
        body = []
        body.append(b'--' + BOUNDARY)
        body.append('Content-Disposition: form-data; name="{0}";'
                    ' filename="{1}"'.format(form_field, filename)
                    .encode('utf-8'))
        body.append('Content-Type: {0}'.format(file_type).encode('utf-8'))
        body.append(b'')
        body.append(fp.read())
        body.append(b'--' + BOUNDARY + b'--')
        body.append(b'')
        fp.close()
        body = b'\r\n'.join(body)

        # build headers
        headers = {
            'Content-Type': 'multipart/form-data; boundary=Tw3ePy',
            'Content-Length': str(len(body))
        }

        return headers, body


class UserPosts:
    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def initialize_v1(self):
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = API(auth)
        return api

    def user_post(self, user, count):
        api = self.initialize_v1()
        user_timeline = api.user_timeline(screen_name=user, count=count)
        user_posts = [(post.created_at, post.id, post.text)
                      for post in user_timeline]
        return user_posts

    def initialize_v2(self):
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = API(auth)
        return api

    def request_metrics(self):
        api = self.initialize_v2()
        tweet_fields = 'tweet.fields'
        metric = api.request_metrics(
            ids='1300825750233321473',
            tweet_fields='non_public_metrics,public_metrics',
        )
        return metric