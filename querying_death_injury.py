
import json
import random
import time
import openai
import pandas as pd

from messages import DEFAULT_INSTRUCTIONS_MSG, DEFAULT_TASK_MSG, elephant_death_model, elephant_injury_model, human_death_model, human_injury_model

from dotenv import load_dotenv
import os

load_dotenv()

'''
Combined querying for death and injury. Model is given a row, and returns the deaths or injuries that occurred in the incident mentioned in that row's
article.
'''


openai_api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_api_key)


'''
Convert a row into messages for querying. If it is an example, the key paramter is used to find what the assistant's response should be
'''
def get_messages(row, example, species, key):
        
    m1 = {
        "role": "user",
        "content":  row["Article"]
    }
    if example:
        m2 = {
            "role": "assistant",
            "content": str(row[key])
        }
        return [m1, m2]
    return [m1]


'''
Contact the model to find the deaths or injuries for the provided row. Unlike other tasks, different task and instruction messages can be input due to how
similar all four tasks(human death, elephant death, human injury, elephant injury) are.

Shots determines how many examples are used, if any. If examples are used, they are pulled from df. 
'''
def contact_death_injury_model(row, df, species, incident, key, model, shots):

    task_msg = DEFAULT_TASK_MSG.format(species=species, incident=incident)
    instr_msg = DEFAULT_INSTRUCTIONS_MSG.format(species=species, incident=incident)

    m1 = {
            "role": "system",
            "content": task_msg
        }
    m2 = {
        "role": "system",
        "content": instr_msg
    }
    
    messages = [m1, m2]

    for i in range(0,shots):
        index = random.randint(0, len(df)-1)
        testrow = df.iloc[index]
        ex_messages = get_messages(testrow, True, species, key)
        messages += ex_messages

    pred_messages = get_messages(row, False, species, key)
    messages = messages + pred_messages

    attempts = 0
    retval = "error"
    while attempts < 5:
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=messages
            )
            response = completion.choices[0].message.content
            retval = int(response)
            if retval < 100:
                break
        except Exception as e:
            if hasattr(e, 'status') and e.status == 429:
                time.sleep(10)
            attempts += 1
    return retval

'''
Wrappers for querying for different tasks.
'''
def get_death_elephant(row, test_df):
    deaths = contact_death_injury_model(row, test_df, "elephant", "died", "Edeath", elephant_death_model, 0)
    return deaths

def get_injury_elephant(row, test_df):
    deaths = contact_death_injury_model(row, test_df, "elephant", "was injured", "Einjured", elephant_injury_model, 3)
    return deaths

def get_death_human(row, test_df):
    deaths = contact_death_injury_model(row, test_df, "human", "was injured", "Deaths", human_death_model, 0)
    return deaths

def get_injury_human(row, test_df):
    deaths = contact_death_injury_model(row, test_df, "human", "was injured", "Injuries", human_injury_model, 0)
    return deaths


