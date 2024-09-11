import json
from math import floor
import googlemaps
import pandas as pd

from querying_classify import contact_classify_model
from querying_date import get_date
from messages import CLASSIFY_MSG, elephant_death_model, date_event_model, location_model, human_death_model, elephant_injury_model, human_injury_model, classify_model
from querying_death_injury import contact_death_injury_model
from querying_location import get_loc
import concurrent.futures
from dotenv import load_dotenv
import os

'''
Logic used to build CSVs for directly comparing accuracy of different modalities
'''

load_dotenv()

gmaps_api_key =  os.getenv("GMAPS_API_KEY")

gmaps = googlemaps.Client(key=gmaps_api_key)

def gmaps_request(res_dict):
    qstring = ""
    for v in res_dict.values():
        if v != "NG":
            qstring = qstring + v + ", "
    geocode_result = gmaps.geocode(qstring)

    if not geocode_result:
        return None

    address_components = geocode_result[0]['address_components']
    for component in address_components:
        if 'country' in component['types'] and "Country" not in res_dict.keys():
            res_dict["Country"] = component["long_name"]
        if 'administrative_area_level_1' in component['types'] and "State" not in res_dict.keys():
            res_dict["State"] = component["long_name"]
        if 'administrative_area_level_2'in component['types'] and "District" not in res_dict.keys():
            res_dict["State"] = component["long_name"]
        
    return res_dict


def death_wrapper(row, df, model, shots):
    return contact_death_injury_model(row, df, "elephant", "died", "Edeath", model, shots)

def elephant_injury_wrapper(row, df, model, shots):
    return contact_death_injury_model(row, df, "elephant", "were injured", "Einjured", model, shots)

def human_death_wrapper(row, df, model, shots):
    return contact_death_injury_model(row, df, "human", "died", "Deaths", model, shots)

def human_injury_wrapper(row, df, model, shots):
    return contact_death_injury_model(row, df, "human", "were injured", "Injuries", model, shots)

def classify_wrapper(row, df, model, shots):
    return contact_classify_model(row, df, CLASSIFY_MSG, model, shots)

def loc_wrapper(row, df, model, shots):
    resdict = get_loc(row, df, model, shots)
    geo_keys = ["Village/Place", "State", "District", "Country"]

    for key in geo_keys:
        try:
            row[key + "_Pred"] = str(resdict[key])
        except:
            row[key + "_Pred"] = "NG"
    return row

def compare_orig_ai(model, shots, name, func, df, pred_key, orig_key):
    test_df = df[floor(len(df)/2):]
    train_df = df[:floor(len(df)/2)]

    test_df = test_df.sample(n=100, replace=True, random_state=1)

    test_df[pred_key] = test_df.apply(lambda x:func(x, train_df, model, shots), axis=1)

    test_df = test_df[[orig_key, pred_key]]

    if model == "gpt-3.5-turbo":
        test_df.to_csv(f"final_results/{name}-{shots}shot.csv")
    else:
        test_df.to_csv(f"final_results/{name}-ft-{shots}shot.csv")


def compare_orig_ai_location(model, shots, name, func, df):
    test_df = df[floor(len(df)/2):]
    train_df = df[:floor(len(df)/2)]

    geo_keys = ["Village/Place", "State", "District", "Country"]
    pred_keys = ["Village/Place_Pred", "State_Pred", "District_Pred", "Country_Pred"]

    test_df = test_df.sample(n=100, replace=True, random_state=1)
    test_df = test_df.apply(lambda x: func(x, train_df, model, shots), axis=1)

    test_df = test_df[geo_keys + pred_keys]
    for key in geo_keys:
        test_df[key] = test_df[key].apply(lambda x: str(x))
    if model == "gpt-3.5-turbo":
        test_df.to_csv(f"final_results/{name}-{shots}shot.csv")
    else:
        test_df.to_csv(f"final_results/{name}-ft-{shots}shot.csv")

def find_loc(train_df, test_df, model, name, shots):
    row_list = []
    def loc_func(index, row):
        print(f"doing row {index}")
        new_row = {}
        geo_keys = ["Country", "State", "District", "Village/Place"]
        attempts = 0
        while attempts < 3:
            try:
                result = get_loc(row, train_df, model, shots)
                
                #if len(list(result.keys())) < 4:
                #    result = gmaps_request(result)
                for key in geo_keys:
                    new_row[key] = row[key]
                    if key in result.keys():
                        new_row[key + "_Pred"] = result[key]
                    else:
                        new_row[key + "_Pred"] = "NG"
                break
                
            except Exception as e:
                print("Error: " + str(e))
                new_row = {
                    "Country_Pred": "Error",
                    "District_Pred": "Error",
                    "State_Pred": "Error",
                    "Village/Place_Pred": "Error"
                }
                attempts += 1
        row_list.append(new_row)

    
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(executor.map(lambda args: loc_func(*args), test_df.iterrows()))

    test_df = pd.DataFrame(row_list)
    if model == "gpt-3.5-turbo":
        test_df.to_csv(f"final_results/{name}-{shots}shot-test.csv")
    else:
        test_df.to_csv(f"final_results/{name}-ft-{shots}shot-test.csv")



def make_all_comparisons(name, func, model, df, pred_key, orig_key):
    combos = [
        #(0, "gpt-3.5-turbo"),
        (0, model),
        #(1, "gpt-3.5-turbo"),
        #(1, model),
        #(5, "gpt-3.5-turbo"),
        #(5, model),
    ]
    
    for (shots, model) in combos:
        print(f"doing {shots}, {model}")
        compare_orig_ai(model, shots, name, func, df, pred_key, orig_key)
        print("done")

def make_all_comparisons_location(name, func, model, df):
    combos = [
        (0, "gpt-3.5-turbo"),
        (0, model),
        (1, "gpt-3.5-turbo"),
        (1, model),
        (5, "gpt-3.5-turbo"),
        (5, model),
    ]

    test_df = df[floor(len(df)/2):]
    train_df = df[:floor(len(df)/2)]

    test_df = test_df.sample(n=100, replace=True, random_state=1)


    for (shots, model) in combos:
        print(f"doing {shots}, {model}")
        find_loc(train_df, test_df, model, name, shots)
        print("done")




main_df = pd.read_csv("data\STE HEC - Master 10.0.2 - Elephant Death & Injury(1).csv")[:100]
main_df["Datefixed"] = pd.to_datetime(main_df["Datefixed"])
hdeath_df = pd.read_csv("data/human_deaths_injuries.csv")
date_df = pd.read_csv("manual_dates_with_candidates.csv")[100:400]
classify_df = pd.read_csv("data\classification dataset - Sheet1.csv")

#make_all_comparisons("death", death_wrapper, elephant_death_model, main_df, "Openai_Edeath", "Edeath")
#make_all_comparisons("date", get_date, date_event_model, date_df, "Openai_Date", "Datefixed")
#make_all_comparisons_location("loc", loc_wrapper, location_model, main_df)
#make_all_comparisons("human_death", human_death_wrapper, human_death_model, hdeath_df, "Openai_Hdeath", "Deaths")
#make_all_comparisons("human_injury", human_injury_wrapper, human_injury_model, hdeath_df, "Openai_Hinjury", "Injuries")
#make_all_comparisons("elephant_injury", elephant_injury_wrapper, elephant_injury_model, main_df, "Openai_Einjured", "Einjured")
make_all_comparisons("classify", classify_wrapper, classify_model, classify_df.sample(frac=1), "Openai_Verdict", "Verdict")

