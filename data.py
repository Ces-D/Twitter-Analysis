import pandas as pd
import os

from twitterapi import API

class CleanPostFrame:
    def __init__(self, dataframe):
        self.dataframe = data_frame
        self.new_df = None

    def post_info(self, index):
        df_series = self.dataframe.iloc[index]
        return df_series

    def series_to_dict(self):
        all_dicts = []
        for i in range(2): # change to len(self.dataframe)
            post_info = self.post_info(i)
            series_to_dict = pd.Series.to_dict(post_info)
            # print(series_to_dict)
            all_dicts.append(series_to_dict)
        return all_dicts
    
    def inner_dict_keys(self, i):
        df_series = self.post_info(i)
        series_values = df_series.values

        # check if item is type(dict) and append to list
        all_dict_items = [
            item for item in series_values if isinstance(item, dict)
        ]

        # creates a flat list from list of lists
        flat_dict_keys = set(
            [item for sublist in all_dict_items for item in sublist])
        
        return flat_dict_keys

    def inner_keys(self):
        all_keys = []
        for i in range(len(self.dataframe)):
            all_keys.append(self.inner_dict_keys(i))

        # creates a flat list of all the inner dict keys
        flat_all_keys = set([item for sublist in all_keys for item in sublist])
        # print(flat_all_keys)
        inner_keys = list(flat_all_keys)
        return inner_keys

    def flat_headers(self):
        inner_keys = self.inner_keys()
        return inner_keys + ['created_at', 'id', 'text']

    def update_dict(self, _dict):
        check = {}
        flat_headers = self.flat_headers()
        for header in flat_headers:
            try:
                check[header] = _dict[header]
            except KeyError:
                check[header] = None
        return check

    def flat_dict(self, nested_dict):
        out_dict = {}
        for key, val in nested_dict.items():
            if type(val) == dict:
                out_dict[key] = len(nested_dict.keys())
                out_dict.update(val)
            else:
                out_dict[key] = val
        return out_dict

    def perform_update_dict(self):
        data = []
        for d in self.series_to_dict():
            flat_dict = self.flat_dict(d)
            update_dict = self.update_dict(flat_dict)
            data.append(update_dict)
        return data
        
    def create_df(self):
        columns = self.flat_headers()
        data = self.perform_update_dict()
        new_df = pd.DataFrame.from_dict(data)
        return new_df

    def df_to_csv(self):
        df = self.create_df()
        df.to_csv('Cleaned_data.csv')





if os.path.exists('Post_Data.json'):  # if files exists
    post_data_json = pd.read_json('Post_Data.json')
    data_frame = pd.read_json((post_data_json['data'].to_json()), orient='index')

t = CleanPostFrame(data_frame)
# a = t.create_df()
# b = t.series_to_dict()
# c = t.perform_update_dict()
d = t.df_to_csv()