import pandas as pd
import datetime

from locate import locate
from dotenv import load_dotenv
import os

'''
Logic to use the OpenMeteo API to find weather data for an incident of human-wildlife conflict. 

Currently, all the data available is added.
'''

load_dotenv()

api_key =  os.getenv("GMAPS_API_KEY")

row_list = []

import openmeteo_requests

om = openmeteo_requests.Client()
url = "https://archive-api.open-meteo.com/v1/archive"

geo_keys = ["Geo_Village/Place", "Geo_District", "Geo_State", "Geo_Country", "Village/Place", "District", "State", "Country"]

start_date = '2024-01-01'
end_date = '2024-06-01'

df_list = []

'''
Query with a row to find the lon and lat of the incident. returns ["error", "error"] if corodinates are not found
'''
def get_lat_lon(row):
    try:
        keys_to_use = list(set(geo_keys) & set(list(row.keys())))
        res = locate(row[keys_to_use].values, False)
        if res == -1 or res == -2:
            return pd.Series(["error", "error"])
        return pd.Series([res[0], res[1]])
    except:
        return pd.Series(["error", "error"])
'''
Using the lon, lat and date found in a row, query OpenMeteo for weather data, add it onto that row, and return it.
'''
def get_temp_data(row):

    daily_keys = ["temperature_2m_max", 
                  "precipitation_sum", 
                  "rain_sum",  
                  "weather_code", 
                  "sunshine_duration",
                  "daylight_duration",
                  "wind_speed_10m_max",
                  "temperature_2m_max",
                  "temperature_2m_min",
                    "snowfall_sum",
                    "precipitation_hours"
                  ]

   

    try:
        date = pd.to_datetime(row["Date (Event)"])
        date_string = date.strftime("%Y-%m-%d")
            
        lat = row["lat"]
        lon = row["lon"]
        print(date_string)

        params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": date_string,
        "end_date": date_string,
        "hourly": ["temperature_2m", "relative_humidity_2m"],
        "daily": daily_keys
        }

        responses = om.weather_api(url, params=params)
        response = responses[0]
        print(response)

        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m

        hourly_dataframe = pd.DataFrame(data = hourly_data)
        avg_temperature = hourly_dataframe.loc[:, "temperature_2m"].mean()
        avg_humidity = hourly_dataframe.loc[:, "relative_humidity_2m"].mean()
        print("avg temperature is " + str(avg_temperature))
        print("avg humidity is " + str(avg_humidity))

        daily = response.Daily()
        i = 0
        data_dict = {}

        while i < len(daily_keys):
            key = daily_keys[i]
            try:
                val = daily.Variables(i).ValuesAsNumpy()[0]
            except:
                val = daily.Variables(i).ValuesAsNumpy()
            data_dict[key] = val
            i = i+1

        data_dict["average_temperature_2m"] = avg_temperature
        data_dict["average_relative_humidity_2m"] = avg_humidity
        return pd.concat([row, pd.Series(data_dict)])
    except:
        error_dict = {}
        for key in daily_keys:
            error_dict[key] = "error"
        error_dict["average_temperature_2m"] = "error"
        error_dict["average_relative_humidity_2m"] = "error"
        return pd.concat([row, pd.Series(error_dict)])
    

'''
Function for later use in adding weather data to data from a single date of web scraping
'''
def add_temperature(single_date):
    curr_df = pd.read_csv(f"data/{single_date:%b-%d-%Y}/openai_{single_date:%b-%d-%Y}.csv")

    curr_df[["lat", "lon"]] = curr_df.apply(get_lat_lon, axis=1)
    curr_df = curr_df.apply(get_temp_data, axis=1)
    return curr_df


'''
Add weather dat to master dataset
'''
def add_temp_to_big_df():
    curr_df = pd.read_csv("data\STE HEC - Master 10.0.2 - Elephant Death & Injury(1).csv")

    curr_df[["lat", "lon"]] = curr_df.apply(get_lat_lon, axis=1)
    curr_df = curr_df.apply(get_temp_data, axis=1)

    curr_df.to_csv("data/Master 10.0.2 w temp data.csv")
