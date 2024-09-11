import pandas as pd

def find_step(start_date,end_date):
    days_between = end_date - start_date
    if (days_between < 14):
        return "D"
    elif (days_between < 120):
        return "W"
    elif(days_between < 730):
        return "M"
    else:
        return "Y"

def define_proper_dates(df,date_key):
    df[date_key] = pd.to_datetime(df[date_key], format='mixed')

def filter_by_date(df,start_date,end_date,date_key):
    df = df[df[date_key] >= start_date]
    df = df[df[date_key] <= end_date]
    return df

def bin_by_year(df, date_key):
    bins = pd.date_range(start=df[date_key].min(), end=df[date_key].max() + pd.DateOffset(years=1), freq="Y")

    df['bin'] = pd.cut(df[date_key], bins=bins, labels=False, right=False)
    
    data = df.groupby('bin')
    return bins

def bin_by_month(df, date_key):
    bins = pd.date_range(start=df[date_key].min(), end=df[date_key].max() + pd.DateOffset(months=1), freq="M")

    df['bin'] = pd.cut(df[date_key], bins=bins, labels=False, right=False)
    
    return bins
    
def bin_by_week(df, date_key):
    bins = pd.date_range(start=df[date_key].min(), end=df[date_key].max() + pd.DateOffset(weeks=1), freq="W")

    df['bin'] = pd.cut(df[date_key], bins=bins, labels=False, right=False)
    
    return bins

def bin_by_day(df, date_key):
    bins = pd.date_range(start=df[date_key].min(), end=df[date_key].max() + pd.DateOffset(days=1), freq="D")

    df['bin'] = pd.cut(df[date_key], bins=bins, labels=False, right=False)
    
    return bins