import pandas as pd

post_data_json = pd.read_json('Post_Data.json')

data_frame = pd.read_json((post_data_json['data'].to_json()), orient='index')


class Post_Frame:
    def __init__(self, dataframe):
        self.df = dataframe
        self.flat_key_list = None

    def dict_keys(self, dictionary):
        dict_keys = list(dictionary.keys())
        return dict_keys

    def post_info(self, index):
        df_series = self.df.iloc[index]
        series_values = df_series.values
        return df_series, series_values

    def text(self):
        text = []
        for i in range(len(self.df)):
            df_series, df_values = self.post_info(i)
            text.append(df_series['text'])
        return text

    def created_at(self):
        created_at = []
        for i in range(len(self.df)):
            df_series, df_values = self.post_info(i)
            created_at.append(df_series['created_at'])
        return created_at

    def post_id(self):
        post_id = []
        for i in range(len(self.df)):
            df_series, df_values = self.post_info(i)
            post_id.append(df_series['id'])
        return post_id

    def inner_dict_keys(self, index):
        df_series, series_values = self.post_info(index)

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
        for i in range(len(self.df)):
            all_keys.append(self.inner_dict_keys(i))

        # creates a flat list of all the inner dict keys
        flat_all_keys = set([item for sublist in all_keys for item in sublist])
        # print(flat_all_keys)
        self.flat_key_list = list(flat_all_keys)
        pass

    def inner_dict_values(self, index):

        df_series, series_values = self.post_info(index)
        df_dict = pd.Series.to_dict(df_series)
        for key in :

        print(df_dict)
        pass

    def inner_values(self):
        all_keys = self.inner_keys()
        # print(all_keys)
        pass

    def inner_items(self, index):
        pass

    def flat_headers(self):
        if self.flat_key_list is None:
            inner_keys = self.inner_keys()
            self.flat_headers
        inner_keys = self.inner_keys()  
        return inner_keys + ['created_at', 'id', 'text']

    def write_dataframe(self):
        columns = self.flat_headers()
        posts = {
            'column_header': ['Column Values'],
            'column_header': ['Column Values']
        }

        df = pd.DataFrame(posts, columns=columns)

        return df

A = Post_Frame(data_frame)
# d = A.inner_keys()
# c = A.flat_headers()
# d = A.post_id()
# e = A.inner_dict_keys(1)
# f = A.post_info(2)
g = A.inner_dict_values(2)