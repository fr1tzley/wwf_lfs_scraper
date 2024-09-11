from datetime import datetime
import json
import random
import time
import openai
import pandas as pd
from sutime import SUTime
import dateparser
from dateparser.search import search_dates
import spacy

from messages import CLASSIFY_MSG, classify_model


from dotenv import load_dotenv
import os

'''
This file contains logic allowing the webscraper to query for the classification of articles.

After scraping articles from google, the webscraper then feeds their titles through here and the AI model classifies them as either
relevant or irrelevant(Y or N) on the basis of the contents of the title.
'''

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_api_key)


'''
Used to conver a row into a message for querying the AI model. If example is set to true, the verdict(Y or N) will be included in an assistant message.
'''
def get_messages(row, example):
        
    m1 = {
        "role": "user",
        "content":  row["FullTitle"]
    }
    if example:
        m2 = {
            "role": "assistant",
            "content": row["Verdict"]
        }
        return [m1, m2]
    return [m1]

'''
Contact the model to classify a row as irrelevant or relevant. 

msg parameter is the instructions given to the model. shots determines how many examples will be given, and if they are needed,
they are drawn from df. row is the row containing the title that will be clasified.

Returns the result of the query(either "Y" or "N")
'''
def contact_classify_model(row, df, msg, model, shots):
    m1 = {
            "role": "system",
            "content": msg
        }
    
    messages = [m1]

    for i in range(0,shots):
        index = random.randint(0, len(df)-1)
        testrow = df.iloc[index]
        ex_messages = get_messages(testrow, True)
        messages += ex_messages

    pred_messages = get_messages(row, False)
    messages = messages + pred_messages

    attempts = 0
    retval = "error"
    while attempts < 3:
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=messages
            )
            
            response = completion.choices[0].message
            retval = response.content
            break
        except Exception as e:
            if hasattr(e, 'status') and e.status == 429:
                time.sleep(10)
            attempts += 1
    return retval

def get_classify(row, test_df, model, shots):
    deaths = contact_classify_model(row, test_df, CLASSIFY_MSG, model, shots)
    return deaths


test_df = pd.read_csv("data\STE HEC - Master 10.0.2 - Elephant Death & Injury(1).csv")

