import os
import pandas as pd

from twitterapi import API
from data import CleanPostFrame
from secrets import *


if os.path.exists('Post_Data.json'): 
        post_data_json = pd.read_json('Post_Data.json')
        data_frame = pd.read_json((post_data_json['data'].to_json()), orient='index')

        t = CleanPostFrame(data_frame)
        d = t.df_to_csv()

else:
    twitter = API(consumer_key, consumer_secret, access_token, access_token_secret)
    data_file = twitter.data_file(start_index=1, end_index=899)