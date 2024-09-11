
import json
import random
import time

import openai

from messages import LOCATION_INSTRUCTIONS_MSG, LOCATION_TASK_MSG


from dotenv import load_dotenv
import os

'''
Querying for location of incidents found in rows. Currently, we only worry about Country, District, State, and Village/Place. 
'''

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_api_key)

'''
Format a row
'''
def get_messages(row, example):
    geo_keys = ["Village/Place", "Country", "District", "State"]
    accum_row = {}
    
    m1 = {
        "role": "user",
        "content": "This is the article: " + str(row["Article"])
    }
    if example:
        for key in geo_keys:
            accum_row[key] = row[key]
        m2 = {
            "role": "assistant",
            "content": (json.dumps(accum_row))
        }
        return [m1, m2]
    return [m1]

def contact_location_model(row, df, model, shots):
    
    m1 = {
            "role": "system",
            "content": LOCATION_TASK_MSG
        }
    m2 = {
            "role": "system",
            "content": LOCATION_INSTRUCTIONS_MSG
        }
    
    messages = [m1, m2]

    for i in range(0,shots):
        index = random.randint(0, len(df)-1)
        testrow = df.iloc[index]
        ex_messages = get_messages(testrow, True)
        messages += ex_messages

    pred_messages = get_messages(row, False)
    messages = messages + pred_messages
    result = {
        "Country": "Error",
        "District": "Error",
        "State": "Error",
        "Village/Place": "Error"
    }
    attempts = 0
    while attempts < 5:
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=messages
            )
            
            response = completion.choices[0].message
            result = json.loads(response.content)
            break
        except Exception as e:
            try:
                if hasattr(e, 'status') and e.status == 429:
                    time.sleep(10)
                attempts += 1
            except:
                attempts += 1

    
    return result

'''
Wrapper for querying location. Used in case the contract for querying changes later.
'''
def get_loc(row, test_df, model, shots):
    return contact_location_model(row, test_df, model, shots)

