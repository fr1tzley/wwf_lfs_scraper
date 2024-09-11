import pandas as pd
import datetime
from graph_utils import define_proper_dates, filter_by_date

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

##from querying.querying import filter_by_many_single_var
date_key = "event_date"

def get_histogram_data(df, bins, step):
    if (step == "D"):
        strftime_bins = bins.strftime('%d')
        count = df[date_key].groupby(df[date_key].dt.strftime('%d')).count()
    elif (step == "M"):
        strftime_bins = bins.strftime('%B')
        count = df[date_key].groupby(df[date_key].dt.strftime('%B')).count()
    else:
        strftime_bins = bins.strftime('%Y')
        count = df[date_key].groupby(df[date_key].dt.strftime('%Y')).count()
    count = count.reindex(strftime_bins, fill_value=0)
    return count

def get_stacked_bar_data(df, bins, step, column_keys):
    data = df[column_keys + [date_key]]
    if (step == "D"):
        strftime_bins = bins.strftime('%d')
        data = data.groupby(data[date_key].dt.strftime('%d'))[column_keys].sum()
    elif(step == "M"):
        strftime_bins = bins.strftime('%B')
        data = data.groupby(data[date_key].dt.strftime('%B'))[column_keys].sum()
    else:
        strftime_bins = bins.strftime('%Y')
        data = data.groupby(data[date_key].dt.strftime('%Y'))[column_keys].sum()
    
    data = data.reindex(strftime_bins, fill_value=0)
    return data

def bin_by_year(df, date_key):
    start_date = df[date_key].min().replace(day=1)
    end_date = df[date_key].max().replace(day=1) + pd.offsets.YearEnd(1)
    bins = pd.date_range(start=start_date, end=end_date, freq='Y')
    return bins

def bin_by_month(df, date_key):
    start_date = df[date_key].min().replace(day=1)
    end_date = df[date_key].max().replace(day=1) + pd.offsets.MonthEnd(1)
    bins = pd.date_range(start=start_date, end=end_date, freq='M')
    return bins

def bin_by_day(df, date_key):
    start_date = df[date_key].min()
    end_date = df[date_key].max() + pd.offsets.Day()
    bins = pd.date_range(start=start_date, end=end_date, freq='D')
    return bins

big_df = pd.read_csv("data\STE HEC - Master 10.0.2 - Elephant Death & Injury(1).csv")

class GRAPH_TYPE:
    STACKED_BAR = "STACKED_BAR"
    HISTOGRAM_TIME = "HISTOGRAM_TIME"
    HISTOGRAM_KEY = "HISTOGRAM_KEY"

def draw_graph(df, start_date, end_date, graph_type, keys, step):
    df = df.copy()
    df[date_key] = pd.to_datetime(df[date_key], format='mixed')

    if graph_type == GRAPH_TYPE.HISTOGRAM_TIME:
        return draw_graph_histogram_time(df,start_date,end_date,step)
    if graph_type == GRAPH_TYPE.HISTOGRAM_KEY:
        return draw_graph_histogram_key(df,keys[0])
    if graph_type == GRAPH_TYPE.STACKED_BAR:
        return draw_graph_stacked_bar(df,keys,start_date,end_date,step)
    
def get_xlab(freq):
    xlab = ""
    if (freq == "M"):
        xlab = "Month"
    elif (freq == "D"):
        xlab = "Day"
    else:
      xlab = "Year"
    return xlab

def get_xticks(freq):
    if (freq == "D"):
        xlab = "%D"
    elif (freq == "W" or freq == "M"):
        xlab = "%b %Y"
    else:
      xlab = "%Y"
    return xlab
    
def get_bins(ydf,date_key,freq):
    ret = []
    if (freq == "M"):
        ret = bin_by_month(ydf, date_key)
    elif (freq == "D"):
        ret = bin_by_day(ydf,date_key)
    else:
        ret = bin_by_year(ydf, date_key)
    return ret

def draw_graph_histogram_time(df, start_date, end_date, step):
    xlab = get_xlab(step)
    bins = get_bins(df,date_key,step)

    count = get_histogram_data(df,bins,step)
   
    count.plot(kind='bar', figsize=(10, 6), color='skyblue', edgecolor='black')

    plt.title(f'Data Distribution From {start_date} to {end_date}')
    plt.xlabel(xlab)
    plt.ylabel('Count')

    step_size = max(len(bins) // 20, 1)
    xtick_positions = range(0, len(bins), step_size)

    plt.xticks(xtick_positions, bins[xtick_positions].strftime(get_xticks(step)), rotation=45)
    plt.show()

    fig = plt.gcf()
    return fig

def toint(val):
    try:
        return int(val)
    except:
        return 0


def draw_graph_histogram_key(df, key):

    histogram_data = df.groupby(key).size()
    histogram_data.plot(kind='bar', figsize=(10, 6), color='skyblue', edgecolor='black')

    plt.title(f'Data Distribution Grouped by {key}')
    plt.xlabel(key)
    plt.ylabel('Count')
    return plt.gcf()


def draw_graph_stacked_bar(df,column_keys,start_date,end_date,step):
    fig, ax = plt.subplots()
    bins = get_bins(df,date_key,step)

    for key in column_keys:
        df[key] = pd.to_numeric(df[key], errors='coerce')
    
    data = get_stacked_bar_data(df,bins,step,column_keys)
    
    ax = data.plot(kind='bar', stacked=True, figsize=(10, 6))

    ax.set_xlabel(get_xlab(step))
    ax.set_ylabel('Value')
    ax.set_title('Bar Chart Plotting ' + str(column_keys))

    step_size = max(len(bins) // 20, 1)
    xtick_positions = range(0, len(bins), step_size)

    plt.xticks(xtick_positions, bins[xtick_positions].strftime(get_xticks(step)), rotation=45)
    plt.show()
    return plt.gcf()
##draw_graph(big_df,datetime.datetime(2000,1,1), datetime.datetime(2001,12,31),"HISTOGRAM_KEY",["Country"],[],"M")
##draw_graph(big_df,datetime.datetime(2010,1,1), datetime.datetime(2015,12,31),"STACKED_BAR",["Edeath"],[],"M")
#draw_graph(big_df, datetime.datetime(2009,1,1), datetime.datetime(2009,2,28), "HISTOGRAM_TIME", [], [], "D")