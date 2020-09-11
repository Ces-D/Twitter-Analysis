import pandas as pd

class CleanPostFrame:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def post_info(self, index):
        """
        returns pd.Series type object containing a df rows info
        """
        df_series = self.dataframe.iloc[index]
        return df_series

    def series_to_dict(self):
        """
        Converts all the rows to pd.Series to Dicts
        """
        all_dicts = []
        for i in range(len(self.dataframe)):
            post_info = self.post_info(i)
            series_to_dict = pd.Series.to_dict(post_info)
            # print(series_to_dict)
            all_dicts.append(series_to_dict)
        return all_dicts
    
    def inner_dict_keys(self, i):
        """
        json data contained nested dicts of two levels
        grabbing the keys for the innermost dict for a single row
        """
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
        """
        returning the inner keys for the entire dataframe
        """
        all_keys = []
        for i in range(len(self.dataframe)):
            all_keys.append(self.inner_dict_keys(i))

        # creates a flat list of all the inner dict keys
        flat_all_keys = set([item for sublist in all_keys for item in sublist])
        # print(flat_all_keys)
        inner_keys = list(flat_all_keys)
        return inner_keys

    def flat_headers(self):
        """
        creating df headers using the unique inner keys and the non-dict outer keys
        """
        inner_keys = self.inner_keys()
        return inner_keys + ['created_at', 'id', 'text']

    def update_dict(self, _dict):
        """
        checking if the inner_keys exist in the dict else create them filling them with None
        """
        check = {}
        flat_headers = self.flat_headers()
        for header in flat_headers:
            try:
                check[header] = _dict[header]
            except KeyError:
                check[header] = None
        return check

    def flat_dict(self, nested_dict):
        """
        flattening a dict
        """
        out_dict = {}
        for key, val in nested_dict.items():
            if type(val) == dict:
                out_dict[key] = len(nested_dict.keys())
                out_dict.update(val)
            else:
                out_dict[key] = val
        return out_dict

    def perform_update_dict(self):
        """
        first grabs all the pd.Series converting to dicts
        then flattens each dict
        then checks if the key exists else created empty value
        """
        data = []
        for d in self.series_to_dict():
            flat_dict = self.flat_dict(d)
            update_dict = self.update_dict(flat_dict)
            data.append(update_dict)
        return data
        
    def create_df(self):
        """
        creates df from the unique headers and the returned data 
        """
        columns = self.flat_headers()
        data = self.perform_update_dict()
        new_df = pd.DataFrame.from_dict(data)
        return new_df

    def df_to_csv(self):
        """
        converts df to csv
        """
        df = self.create_df()
        df.to_csv('Cleaned_data.csv')

