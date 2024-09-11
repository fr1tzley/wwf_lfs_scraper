import pandas as pd
date_key = "date"

def get_lon_lat(df):
    if (len(df) == 0):
        return []
    print(df.columns)
    ret = df[["latitude", "longitude", "link", "title"]]
    ret = ret.dropna(subset=["latitude","longitude"])

    return ret

