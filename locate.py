import datetime
import json
from geopy.geocoders import Nominatim
import pandas as pd
import requests

date_today = datetime.datetime.now()
locator = Nominatim(user_agent="scraper_geocoder")
geo_keys = ["Geo_Village/Place", "Geo_Sub-District", "Geo_District", "Geo_State", "Geo_Country"]

'''
Functions for geolocating incidents based on associated geokeys. Uses google maps API.
'''


from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GMAPS_API_KEY")


'''
Takes a pandas dataframe, then fills in the lat and lon associated with the geokeys found in every row 
'''
def get_coords(df):
    present_keys = list(set(geo_keys) & set(df.keys()))
    for index, row in df.iterrows():
        result = locate(row[present_keys], True)
        if result != -1 and result != -2:
            latitude = result[0]
            longitude = result[1]
            print(f"coodinates for incident found at {latitude}, {longitude}")
            df.at[index, "lat"] = latitude
            df.at[index, "lon"] = longitude
        elif result == -1:
            print("Location string empty")
        else:
            print(f"Coordinates not found for " + str(row[present_keys]))

    return df

'''
Takes a list of geokeys as an input(i.e. ["Vancouver", "British Columbia", "Canada"]). Then quries google maps with those keys and returns the 
latitude and longitude that are found.
'''
def locate(list, out):
    geolocation_string = ""
    for s in list:
        if isinstance(s,str) and len(s) > 0 and s != "NG":
            if geolocation_string == "":
                geolocation_string = s
            else:
                geolocation_string = geolocation_string + ", " + s
    if geolocation_string == "":
        return -1

    geolocation_string = geolocation_string.replace(", ", "+")
    req_string = f"https://maps.googleapis.com/maps/api/geocode/json?address={geolocation_string}&key={api_key}"
    location = json.loads(requests.get(req_string).text)
    if location["status"] != "OK":
        return -2
    else:
        location = location["results"][0]["geometry"]["location"]
        retval = (location["lat"], location["lng"])
        copystr = str(location["lat"]) + ", " + str(location["lng"])
        return retval